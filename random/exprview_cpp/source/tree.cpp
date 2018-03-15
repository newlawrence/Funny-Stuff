#include <stack>
#include <vector>

#include "tree.hpp"


TreeHandler::TreeHandler(QObject* parent) :
        QObject{parent},
        _parser{nullptr}
{
    auto lexer = calculate::make_lexer<double>({
        calculate::default_real,
        calculate::default_name,
        R"_(^[^A-Za-z\d.(),_\s]$)_"
    });
    _parser = std::make_unique<calculate::Parser>(lexer);
}

void TreeHandler::renderTree(const QString& expression) {
    try {
        using Expression = calculate::Parser::Expression;
        Expression tree = _parser->from_infix(expression.toStdString());

        using NodeIterator = decltype(tree.begin());
        emit infixChanged(QString::fromStdString(tree.infix()));
        emit postfixChanged(QString::fromStdString(tree.postfix()));
        emit resultChanged(QString::fromStdString(
            "<font color='red'><b>" +
            _parser->lexer()->to_string(tree) +
            "</font></b>"
        ));

        std::vector<Expression> init{std::move(tree)};
        std::stack<std::pair<NodeIterator, NodeIterator>> nodes;
        QString body{};

        nodes.push({init.begin(), init.end()});
        body += "<ul>";
        while (!nodes.empty()) {
            auto node = nodes.top().first, end = nodes.top().second;
            nodes.pop();
            if (node != end) {
                body +=
                    "<li><a>" + QString::fromStdString(node->token()) + "</a>";
                nodes.push({node + 1, end});
                if (node->branches()) {
                    nodes.push({node->begin(), node->end()});
                    body += "<ul>";
                }
                else
                    body += "</li>";
            }
            else
                body += "</ul>";
        }
        emit treeChanged(body);
    }
    catch(const calculate::BaseError& error) {
        emit errorRaised(error.what());
    }
}

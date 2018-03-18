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
        using Lexer = calculate::Parser::Lexer;
        std::shared_ptr<Lexer> lexer = _parser->lexer();

        using Expression = calculate::Parser::Expression;
        Expression tree = _parser->from_infix(expression.toStdString());

        using NodeIterator = decltype(tree.begin());
        emit infixChanged(QString::fromStdString(tree.infix()));
        emit postfixChanged(QString::fromStdString(tree.postfix()));
        emit resultChanged(QString::fromStdString(lexer->to_string(tree)));

        std::vector<Expression> init{std::move(tree)};
        std::stack<std::pair<NodeIterator, NodeIterator>> nodes;
        QString body{};
        QString node_template =
            "<div class='spacer'></div>"
            "<div class='node'><a>{token}</a><span>{value}</span></div>";

        nodes.push({init.begin(), init.end()});
        body += "<ul>";
        while (!nodes.empty()) {
            auto node = nodes.top().first, end = nodes.top().second;
            nodes.pop();
            if (node != end) {
                body += "<li>";
                body += QString{node_template}
                    .replace("{token}", node->token().c_str())
                    .replace("{value}", lexer->to_string(*node).c_str());
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

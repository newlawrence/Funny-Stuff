#include <stack>
#include <vector>

#include <QHBoxLayout>
#include <QVBoxLayout>
#include <QSizePolicy>
#include <QSpacerItem>
#include <QWebChannel>

#include "window.hpp"


MainWindow::MainWindow(QWidget* parent) :
        QMainWindow{parent},
        _main_widget{new QWidget{}},
        _expression_box{new QLineEdit{""}},
        _infix_box{new QLabel{""}},
        _postfix_box{new QLabel{""}},
        _result_box{new QLabel{""}},
        _tree_view{new QWebEngineView{}},
        _message_handler{new MessageHandler{this}},
        _parser{nullptr},
        _header{},
        _footer{}
{
    auto lexer = calculate::make_lexer<double>({
        calculate::default_real,
        calculate::default_name,
        R"_(^[^A-Za-z\d.(),_\s]$)_"
    });
    _parser = std::make_unique<calculate::Parser>(lexer);

    setWindowTitle("Expression Tree Viewer");
    setWindowIcon(QIcon{":exprview.png"});
    resize(320, 480);

    auto form_layout = new QVBoxLayout{};
    auto add = [](auto label, auto box) noexcept {
        auto layout = new QHBoxLayout{};
        label->setBuddy(box);
        box->setAlignment(Qt::AlignRight);
        layout->addWidget(label);
        layout->addWidget(box);
        return layout;
    };

    auto expression_layout = add(new QLabel{"Expression:"}, _expression_box);
    auto infix_layout = add(new QLabel{"Infix:"}, _infix_box);
    auto postfix_layout = add(new QLabel{"Postfix:"}, _postfix_box);
    auto result_layout = add(new QLabel{"<b>Result:</b>"}, _result_box);

    form_layout->addLayout(expression_layout);
    form_layout->addLayout(infix_layout);
    form_layout->addLayout(postfix_layout);
    form_layout->addWidget(_tree_view);
    form_layout->addLayout(result_layout);

    _main_widget->setLayout(form_layout);
    setCentralWidget(_main_widget);

    auto channel = new QWebChannel(_tree_view->page());
    channel->registerObject("message_handler", _message_handler);
    _tree_view->page()->setWebChannel(channel);
    _tree_view->page()->load(QUrl{"qrc:/index.html"});
    _tree_view->show();

    _header = "<html><head><link rel='stylesheet' href='qrc:///style.css'>"
              "</head><body><div id='tree'>";
    _footer = "</div></body></html>";

    connect(
        _expression_box,
        &QLineEdit::textChanged,
        this,
        &MainWindow::renderTree
    );
}


void MainWindow::renderTree(const QString& expression) {
    try {
        using Expression = calculate::Parser::Expression;
        Expression tree = _parser->from_infix(expression.toStdString());

        using NodeIterator = decltype(tree.begin());
        _infix_box->setText(QString::fromStdString(tree.infix()));
        _postfix_box->setText(QString::fromStdString(tree.postfix()));

        QString value = QString::fromStdString(
            "<font color='red'><b>" +
            _parser->lexer()->to_string(tree) +
            "</font></b>"
        );
        _result_box->setText(value);

        std::vector<Expression> init{std::move(tree)};
        std::stack<std::pair<NodeIterator, NodeIterator>> nodes;
        QString body{};

        nodes.push({init.begin(), init.end()});
        body += "<ul>";
        while (!nodes.empty()) {
            auto node = nodes.top().first, end = nodes.top().second;
            nodes.pop();
            if (node != end) {
                body += "<li><a>" + QString::fromStdString(node->token()) + "</a>";
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
        _tree_view->setHtml(_header + body + _footer);
        _expression_box->setFocus();
    }
    catch(const calculate::BaseError& error) {
        _infix_box->setText("");
        _postfix_box->setText("");
        _result_box->setText("");

        _message_handler->setText(error.what());
        _expression_box->setFocus();
    }
}

#include <stack>
#include <vector>

#include <QFile>

#include <QHBoxLayout>
#include <QVBoxLayout>
#include <QSizePolicy>
#include <QSpacerItem>

#include "frame.hpp"


MainWindow::MainWindow(QWidget *parent) :
        QMainWindow{parent},
        _main_widget{new QWidget{}},
        _expression_box{new QLineEdit{""}},
        _infix_box{new QLabel{""}},
        _postfix_box{new QLabel{""}},
        _result_box{new QLabel{""}},
        _tree_view{new QWebEngineView{}},
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

    auto expression_layout = new QHBoxLayout{};
    auto expression_label = new QLabel{"Expression"};
    expression_label->setBuddy(_expression_box);
    _expression_box->setAlignment(Qt::AlignRight);
    expression_layout->addWidget(expression_label);
    expression_layout->addWidget(_expression_box);

    auto infix_layout = new QHBoxLayout{};
    auto infix_label = new QLabel{"Infix:"};
    infix_label->setBuddy(_infix_box);
    _infix_box->setAlignment(Qt::AlignRight);
    infix_layout->addWidget(infix_label);
    infix_layout->addWidget(_infix_box);

    auto postfix_layout = new QHBoxLayout{};
    auto postfix_label = new QLabel{"Postfix:"};
    postfix_label->setBuddy(_postfix_box);
    _postfix_box->setAlignment(Qt::AlignRight);
    postfix_layout->addWidget(postfix_label);
    postfix_layout->addWidget(_postfix_box);

    auto result_layout = new QHBoxLayout{};
    auto result_label = new QLabel{"<b>Result:</b>"};
    result_label->setBuddy(_result_box);
    _result_box->setAlignment(Qt::AlignRight);
    result_layout->addWidget(result_label);
    result_layout->addWidget(_result_box);

    form_layout->addLayout(expression_layout);
    form_layout->addLayout(infix_layout);
    form_layout->addLayout(postfix_layout);

    form_layout->addWidget(_tree_view);
    form_layout->addLayout(result_layout);
    _main_widget->setLayout(form_layout);
    setCentralWidget(_main_widget);

    QFile file{":style.css"};
    file.open(QFile::ReadOnly | QFile::Text);
    _header = "<html><head><style>";
    _header += file.readAll();
    _header += "</style></head><body><div class=\"tree\">";
    _footer += "</div></body></html>";
    file.close();
    _tree_view->setHtml("");

    connect(
        _expression_box,
        &QLineEdit::textChanged,
        this,
        &MainWindow::render_tree
    );
}

MainWindow::~MainWindow() {}


void MainWindow::render_tree(const QString& expression) {
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
        _tree_view->setHtml(_header + body + _footer);
        _expression_box->setFocus();
    }
    catch(const calculate::BaseError& error) {
        _infix_box->setText("");
        _postfix_box->setText("");
        _result_box->setText("");

        _tree_view->setHtml(QString::fromStdString(
            "<div style='text-align:center;'>" +
            std::string{error.what()} +
            "</div>"
        ));

        _expression_box->setFocus();
    }
}

#include <stack>
#include <vector>

#include <QFile>

#include <QLabel>
#include <QHBoxLayout>
#include <QVBoxLayout>
#include <QSizePolicy>
#include <QSpacerItem>

#include "frame.hpp"


MainWindow::MainWindow(QWidget *parent) :
        QMainWindow{parent},
        _main_widget{new QWidget{}},
        _expression_box{new QLineEdit{""}},
        _tree_view{new QWebEngineView{}},
        _parser{nullptr},
        _header{},
        _footer{}
{
    QFile file{":style.css"};
    auto form_layout = new QVBoxLayout{};
    auto expression_layout = new QHBoxLayout{};
    auto expression_label = new QLabel{"Expression"};
    calculate::Lexer<double> lexer{
        {"(", ")", ",", "."},
        {
            R"_(^(?:\d+\.?\d*|\.\d+)+(?:[eE][+\-]?\d+)?$)_",
            R"_(^[A-Za-z_]+[A-Za-z_\d]*$)_",
            R"_(^[^A-Za-z\d.(),_\s]$)_",
            R"_(((?:\d+\.?\d*|\.\d+)+(?:[eE][+\-]?\d+)?)|)_"
            R"_(([A-Za-z_]+[A-Za-z_\d]*)|)_"
            R"_(([^A-Za-z\d\.(),_\s])|)_"
            R"_((\()|(\))|(,)|(\.))_"
        }
    };

    setWindowTitle("Expression Tree Viewer");
    setWindowIcon(QIcon{":exprview.png"});
    resize(280, 380);

    expression_label->setBuddy(_expression_box);
    expression_layout->addWidget(expression_label);
    expression_layout->addWidget(_expression_box);

    form_layout->addLayout(expression_layout);
    form_layout->addWidget(_tree_view);
    _main_widget->setLayout(form_layout);
    setCentralWidget(_main_widget);

    file.open(QFile::ReadOnly | QFile::Text);
    _header = "<html><head><style>";
    _header += file.readAll();
    _header += "</style></head><body><div class=\"tree\">";
    _footer += "</div></body></html>";
    file.close();

    _parser = std::make_unique<calculate::DefaultParser>(lexer);
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
        auto tree = _parser->parse(expression.toStdString());
        using Expression = calculate::DefaultParser::Expression;
        using NodeIterator = decltype(tree.begin());
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
    catch(const calculate::BaseError&) {
        _tree_view->setHtml("");
        _expression_box->setFocus();
    }
}

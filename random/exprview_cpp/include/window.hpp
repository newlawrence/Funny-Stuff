#ifndef _WINDOW_HPP_
#define _WINDOW_HPP_

#include <memory>

#include <QMainWindow>

#include <QWidget>
#include <QLabel>
#include <QLineEdit>
#include <QWebEngineView>

#include "message.hpp"
#include "tree.hpp"


class MainWindow : public QMainWindow {
    Q_OBJECT

    QWidget* _main_widget;
    QLineEdit* _expression_box;
    QLabel* _infix_box;
    QLabel* _postfix_box;
    QLabel* _result_box;
    QWebEngineView* _tree_view;

    MessageHandler* _message_handler;
    TreeHandler* _tree_handler;

public:
    explicit MainWindow(QWidget* parent=nullptr);

    void handleError(const QString& text);
};

#endif

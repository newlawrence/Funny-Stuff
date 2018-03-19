#ifndef _WINDOW_HPP_
#define _WINDOW_HPP_

#include <memory>

#include <QMainWindow>

#include <QWidget>
#include <QLabel>
#include <QLineEdit>
#include <QWebEngineView>

#include "error.hpp"
#include "tree.hpp"


class MainWindow : public QMainWindow {
    Q_OBJECT

    QWidget* _main_widget;
    QLineEdit* _expression_box;
    QLineEdit* _infix_box;
    QLineEdit* _postfix_box;
    QLineEdit* _result_box;
    QWebEngineView* _tree_view;

    ErrorHandler* _error_handler;
    TreeHandler* _tree_handler;

public:
    explicit MainWindow(QWidget* parent=nullptr);

public slots:
    void handleError(const QString& text);
};

#endif

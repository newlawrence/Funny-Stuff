#ifndef _FRAME_HPP_
#define _FRAME_HPP_

#include <memory>

#include <QMainWindow>

#include <QWidget>
#include <QLineEdit>
#include <QWebEngineView>

#include "calculate.hpp"


class MainWindow : public QMainWindow {
    Q_OBJECT

    QWidget* _main_widget;
    QLineEdit* _expression_box;
    QWebEngineView* _tree_view;

    std::unique_ptr<calculate::Parser> _parser;
    QString _header;
    QString _footer;

public:
    MainWindow(QWidget *parent=nullptr);
    ~MainWindow();

    void render_tree(const QString&);
};

#endif

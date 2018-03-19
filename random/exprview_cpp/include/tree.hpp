#ifndef _TREE_HPP_
#define _TREE_HPP_

#include <QObject>
#include <QString>

#include "calculate.hpp"


class TreeHandler : public QObject {
    Q_OBJECT

    std::unique_ptr<calculate::Parser> _parser;

public:
    explicit TreeHandler(QObject* parent=nullptr);

signals:
    void infixChanged(const QString& expression);
    void postfixChanged(const QString& expression);
    void resultChanged(const QString& expression);
    void treeChanged(const QString& expression);
    void errorRaised(const QString& expression);

public slots:
    void renderTree(const QString& expression);
};

#endif

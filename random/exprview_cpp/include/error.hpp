#ifndef _MESSAGE_HPP_
#define _MESSAGE_HPP_

#include <QObject>
#include <QString>


class ErrorHandler : public QObject {
    Q_OBJECT
    Q_PROPERTY(QString text MEMBER _text NOTIFY textChanged FINAL)

    QString _text;

public:
    explicit ErrorHandler(QObject* parent=nullptr);

signals:
    void textChanged(const QString& text);

public slots:
    void setText(const QString& text);
};

#endif

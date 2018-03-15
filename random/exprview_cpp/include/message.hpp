#ifndef _MESSAGE_HPP_
#define _MESSAGE_HPP_

#include <QObject>
#include <QString>


class MessageHandler : public QObject {
    Q_OBJECT

    QString _text;

public:
    explicit MessageHandler(QObject* parent=nullptr);

    void setText(const QString& text);

signals:
    void textChanged(const QString& text);
};

#endif

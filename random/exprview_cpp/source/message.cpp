#include "message.hpp"


MessageHandler::MessageHandler(QObject* parent) :
        QObject{parent},
        _text{"Empty expression"}
{}

void MessageHandler::setText(const QString& text) {
    _text = text;
    emit textChanged(_text);
}

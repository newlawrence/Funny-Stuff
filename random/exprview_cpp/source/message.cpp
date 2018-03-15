#include "message.hpp"


MessageHandler::MessageHandler(QObject* parent) : QObject{parent} {}

void MessageHandler::setText(const QString& text) {
    if (text == _text)
        return;
    _text = text;
    emit textChanged(_text);
}

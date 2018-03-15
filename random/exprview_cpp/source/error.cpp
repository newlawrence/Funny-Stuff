#include "error.hpp"


ErrorHandler::ErrorHandler(QObject* parent) :
        QObject{parent},
        _text{"Empty expression"}
{}

void ErrorHandler::setText(const QString& text) {
    _text = text;
    emit textChanged(_text);
}

QT += core gui widgets webchannel webenginewidgets
CONFIG += c++14

greaterThan(QT_MAJOR_VERSION, 5): QT += widgets webenginewidgets

TARGET = Exprview
TEMPLATE = app

DEFINES += QT_DEPRECATED_WARNINGS
INCLUDEPATH += include

SOURCES += \
    source/error.cpp \
    source/tree.cpp \
    source/window.cpp \
    source/main.cpp

HEADERS += \
    include/error.hpp \
    include/tree.hpp \
    include/window.hpp

RESOURCES += \
    exprview.qrc

macx: ICON = resource/icon/exprview.icns
win32: RC_ICONS += resource/icon/exprview.ico

QT += core gui widgets webenginewidgets
CONFIG += c++14

greaterThan(QT_MAJOR_VERSION, 4): QT += widgets

TARGET = Exprview
TEMPLATE = app

DEFINES += QT_DEPRECATED_WARNINGS
INCLUDEPATH += include

SOURCES += \
    source/frame.cpp \
    source/main.cpp

HEADERS += \
    include/frame.hpp

RESOURCES += \
    resource/resource.qrc

macx: ICON = resource/exprview.icns
win32: RC_ICONS += resource/exprview.ico

QT += core gui widgets webenginewidgets
CONFIG += c++14

greaterThan(QT_MAJOR_VERSION, 5): QT += widgets webenginewidgets

TARGET = Exprview
TEMPLATE = app

DEFINES += QT_DEPRECATED_WARNINGS
INCLUDEPATH += include

SOURCES += \
    source/main.cpp \
    source/message.cpp \
    source/tree.cpp \
    source/window.cpp

HEADERS += \
    include/message.hpp \
    include/tree.hpp \
    include/window.hpp

RESOURCES += \
    resource/resource.qrc

macx: ICON = resource/exprview.icns
win32: RC_ICONS += resource/exprview.ico

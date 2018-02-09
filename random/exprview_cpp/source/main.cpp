#include <QApplication>

#include "frame.hpp"


int main(int argc, char *argv[]) {
    QApplication::setAttribute(Qt::AA_EnableHighDpiScaling);
    QApplication application{argc, argv};

    MainWindow window{};
    window.show();

    return application.exec();
}

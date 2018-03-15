#include <QApplication>

#include "window.hpp"


int main(int argc, char *argv[]) {
    QApplication::setAttribute(Qt::AA_EnableHighDpiScaling);
    QApplication application{argc, argv};

    MainWindow main_window{};
    main_window.show();

    return application.exec();
}

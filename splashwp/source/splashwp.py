'''
[Splash WhatsApp] - WhatsApp listener client that displays messages on
                    screen.
File: splashwp.py - contains the main program.

Copyright (c) <2014> Alberto Lorenzo <alorenzo.md@gmail.com>
'''

__author__ = 'Alberto Lorenzo'
__version__ = '1.1.0'
__date__ = '25/06/2014'
__email__ = 'alorenzo.md@gmail.com'
__license__ = 'GNU GPLv3'

# Settings for showned messages.
settings = {'foreground': '#000080',
            'background': '#FFFF80',
            'size': 72,
            'charsPerLine': 60}

import sys
import os
import platform

# Select Qt binding
if '-pyqt5' in sys.argv:
    import PyQt5 as QtBinding
    import PyQt5.QtCore as QtCore
    import PyQt5.QtGui as QtGui
    import PyQt5.QtWidgets as QtWidgets
    QtCore.Signal = QtCore.pyqtSignal
elif '-pyqt4' in sys.argv:
    import PyQt4 as QtBinding
    import PyQt4.QtCore as QtCore
    import PyQt4.QtGui as QtGui
    QtWidgets = QtGui
    QtCore.Signal = QtCore.pyqtSignal
elif '-pyside' in sys.argv:
    import PySide as QtBinding
    import PySide.QtCore as QtCore
    import PySide.QtGui as QtGui
    QtWidgets = QtGui
else:    # Autodetect Qt binding
    try:
        import PyQt5 as QtBinding
        import PyQt5.QtCore as QtCore
        import PyQt5.QtGui as QtGui
        import PyQt5.QtWidgets as QtWidgets
        QtCore.Signal = QtCore.pyqtSignal
    except ImportError:
        try:
            import PyQt4 as QtBinding
            import PyQt4.QtCore as QtCore
            import PyQt4.QtGui as QtGui
            QtWidgets = QtGui
            QtCore.Signal = QtCore.pyqtSignal
        except ImportError:
            import PySide as QtBinding
            import PySide.QtCore as QtCore
            import PySide.QtGui as QtGui
            QtWidgets = QtGui

# Needed to deactivate all Yowsup log messages which are active by default.
from Yowsup.Common.debugger import Debugger

import splashwp_wpclient as wpclient
import splashwp_textutils as textutils


class MainForm(QtWidgets.QDialog):
    '''SplashWhats main (and only) dialog.
    '''

    # Qt's new style signals
    reconnect = QtCore.Signal()

    def __init__(self, parent=None):
        '''MainForm's constructor.

        Not needed:
          parent.
        '''

        super().__init__(parent)

        # Handles to WhatsApp client and message window.
        self.wpclient = None
        self.splash = None

        Debugger.enabled = False    # Deactivate all Yowsup log messages.

        # Widgets creation block.
        self.browser = QtWidgets.QTextBrowser()
        self.localPhoneBox = QtWidgets.QLineEdit('')
        self.localPhoneLabel = QtWidgets.QLabel(self.tr('&Local phone:'))
        self.localPhoneLabel.setBuddy(self.localPhoneBox)
        self.localPhoneBox.setAlignment(QtCore.Qt.AlignRight)
        self.passwordBox = QtWidgets.QLineEdit('')
        self.passwordLabel = QtWidgets.QLabel(self.tr('&Password:'))
        self.passwordLabel.setBuddy(self.passwordBox)
        self.passwordBox.setAlignment(QtCore.Qt.AlignRight)
        self.passwordBox.setEchoMode(QtWidgets.QLineEdit.Password)
        self.phoneBox = QtWidgets.QLineEdit('')
        self.phoneLabel = QtWidgets.QLabel(self.tr('&Remote phone:'))
        self.phoneLabel.setBuddy(self.phoneBox)
        self.phoneBox.setAlignment(QtCore.Qt.AlignRight)
        self.connectButton = QtWidgets.QPushButton(self.tr('&Connect'))

        # Widgets laying up block.
        self.layout1 = QtWidgets.QVBoxLayout()
        self.layout10 = QtWidgets.QHBoxLayout()
        self.layout11 = QtWidgets.QHBoxLayout()
        self.layout10.addWidget(self.localPhoneLabel)
        self.layout10.addStretch()
        self.layout10.addWidget(self.localPhoneBox)
        self.layout1.addLayout(self.layout10)
        self.layout11.addWidget(self.passwordLabel)
        self.layout11.addStretch()
        self.layout11.addWidget(self.passwordBox)
        self.layout1.addLayout(self.layout11)
        self.group1 = QtWidgets.QGroupBox(self.tr('WhatsApp local account'))
        self.group1.setLayout(self.layout1)
        self.layout2 = QtWidgets.QVBoxLayout()
        self.layout20 = QtWidgets.QHBoxLayout()
        self.layout21 = QtWidgets.QHBoxLayout()
        self.layout20.addWidget(self.phoneLabel)
        self.layout20.addStretch()
        self.layout20.addWidget(self.phoneBox)
        self.layout2.addLayout(self.layout20)
        self.layout21.addStretch()
        self.layout21.addWidget(self.connectButton)
        self.layout2.addLayout(self.layout21)
        self.group2 = QtWidgets.QGroupBox(self.tr('WhatsApp remote account'))
        self.group2.setLayout(self.layout2)
        self.mainLayout = QtWidgets.QVBoxLayout()
        self.mainLayout.addWidget(self.browser)
        self.mainLayout.addWidget(self.group1)
        self.mainLayout.addWidget(self.group2)
        self.setLayout(self.mainLayout)

        self.browser.append('<font color=red><b> -*-*-*- [Splash WhatsApp] '
                            '-*-*-*-</b></font>')
        self.browser.append('<font color=red>Copyright © 2014 Alberto '
                            'Lorenzo</font>')

        # Setting window properties. Some properties are platform dependent,
        # so the flags for Linux and Windows differ.
        # TODO: test on Mac.
        self.setWindowTitle('Splash WhatsApp [{0}]'.format(QtBinding.__name__))
        if platform.system() == 'Linux':
            self.setWindowFlags(QtCore.Qt.WindowSystemMenuHint |
                                QtCore.Qt.WindowTitleHint)
        else:
            self.setWindowFlags(QtCore.Qt.WindowSystemMenuHint |
                                QtCore.Qt.WindowTitleHint |
                                QtCore.Qt.WindowMinimizeButtonHint)
        self.setWindowIcon(QtGui.QIcon('splashwp.png'))

        self.connectButton.clicked.connect(self.onClicked)
        self.reconnect.connect(self.onConnect)

    def onClicked(self):
        '''Function called each time 'Connect' button is clicked.
        '''

        # If a message is currently been displayed, it is hidden.
        if self.splash:
            self.splash.close()
            self.splash = None    # Garbage collects the old message.

        # Prevents the user to click until a new connection has been tried.
        self.connectButton.setEnabled(False)

        # If a connection is currently set and it was succesfull, tell the
        # client to force a disconnection (after that, the client itself will
        # sent the 'reconnect' signal); if not, emit the signal for the
        # reconnection.
        if self.wpclient:
            if self.wpclient.connected:
                self.wpclient.disconnect(self.tr('closed by user.'))
                return
        self.reconnect.emit()

    def onConnect(self):
        '''Function called if the 'reconnect' signal is catched up from the
        MainForm or from the WhatsApp client.
        '''

        self.wpclient = wpclient.WhatsAppClient(self.localPhoneBox.text(),
                                                self.passwordBox.text(),
                                                self.phoneBox.text())

        # Those signals allows the new client interactuate with the MainForm.
        self.wpclient.logMessage.connect(self.onLogMessage)
        self.wpclient.splashMessage.connect(self.onSplash)
        self.wpclient.splashImage.connect(self.onSplashImage)
        self.wpclient.reconnect.connect(self.onConnect)

        self.wpclient.login()

        # Once the process or connection (or reconnection) is finished, the
        # user can try another connection.
        self.connectButton.setEnabled(True)

    def onLogMessage(self, text):
        '''Function that displays log messages from the WhatsApp client in
        the MainForm's browser widget.

        Args:
          text (str): text to be appended to the browser.
        '''

        self.browser.append(text)

    def onSplash(self, text):
        '''Function that creates the dialog with the message that will be
        displayed as a splash screen.

        Args:
          text (str): the text to be shown.
        '''

        text = textutils.splitIntoLines(text, settings['charsPerLine'])
        text = textutils.parseCommands(text)

        # The splash message is created as a top level window because that
        # way it's easier to center it on the screen.
        self.splash = QtWidgets.QLabel('<font color=' + settings['foreground']
                                       + ' size=' + str(settings['size']) + '>'
                                       + text + '</font>')
        self.splash.setAlignment(QtCore.Qt.AlignCenter)
        self.__splashSettings(self.splash)

    def onSplashImage(self, text):
        '''Function that creates the a dialog with a received image that will
        be displayed as a splash screen.

        Args:
          text (str): the path to the image to be shown.
        '''

        self.splash = QtWidgets.QLabel()
        self.splash.image = QtGui.QPixmap(text)
        self.splash.setPixmap(self.splash.image)
        self.__splashSettings(self.splash)

    def __splashSettings(self, widget):
        '''Makes a widget behave like a splash widget.

        Args:
          widget (QtWidget): the widget to be set up.
        '''

        # Send key press event to the MainForm
        widget.keyPressEvent = lambda event: self.keyPressEvent(event)

        # As in the MainForm, window properties are a bit platform dependent.
        # TODO: test on Mac.
        if platform.system() == 'Linux':
            widget.setWindowFlags(QtCore.Qt.FramelessWindowHint |
                                  QtCore.Qt.WindowStaysOnTopHint)
        else:
            widget.setWindowFlags(QtCore.Qt.SplashScreen |
                                  QtCore.Qt.WindowStaysOnTopHint)
        widget.setStyleSheet('background-color:' + settings['background'])
        widget.show()

        # Center the message on the screen.
        sG = QtWidgets.QApplication.desktop().screenGeometry()
        x = (sG.width() - widget.width()) // 2
        y = (sG.height() - widget.height()) // 2
        widget.move(x, y)

    def keyPressEvent(self, event):
        '''Function called when a key press event is detected. Clears the
        current displayed message (if any) on spacebar key pressed.

        Args:
          event (...): contains information about the event.
        '''

        if event.key() == QtCore.Qt.Key_Space:
            if self.splash:
                self.splash.close()
                self.splash = None

        event.accept()    # Avoids event promoting

    def closeEvent(self, event):
        '''Function called when the MainForm is closed.

        Not needed:
          event.
        '''

        # Ensure the disconnection from the WhatsApp servers and close the
        # displayed message (if any).
        if self.wpclient:
            self.wpclient.disconnect(self.tr('closing the application.'))
            self.wpclient = None
        if self.splash:
            self.splash.close()
            self.splash = None

if __name__ == '__main__':
    app = QtWidgets.QApplication(sys.argv)

    # Installing translators to user defined and Qt's strings.
    locale = QtCore.QLocale.system().name()
    translator = QtCore.QTranslator()
    translator.load(os.path.join(
        os.path.abspath(os.path.dirname(__file__)),
        'locale/splashwp_' + locale))
    app.installTranslator(translator)
    qtTranslator = QtCore.QTranslator()
    qtTranslator.load('qt_' + locale,
                      QtCore.QLibraryInfo
                      .location(QtCore.QLibraryInfo.TranslationsPath))
    app.installTranslator(qtTranslator)

    form = MainForm()
    form.show()
    sys.exit(app.exec_())

'''
[Splash WhatsApp] - WhatsApp listener client that displays messages on
                    screen.
File: splashwp_wpclient.py - implementation of the WhatsApp listener client.

Copyright (c) <2014> Alberto Lorenzo <alorenzo.md@gmail.com>
'''

__author__ = 'Alberto Lorenzo'
__version__ = '1.1.0'
__date__ = '25/06/2014'
__email__ = 'alorenzo.md@gmail.com'
__license__ = 'GNU GPLv3'

import sys
import time
import base64

# Select Qt binding
if '-pyqt5' in sys.argv:
    import PyQt5.QtCore as QtCore
    QtCore.Signal = QtCore.pyqtSignal
elif '-pyqt4' in sys.argv:
    import PyQt4.QtCore as QtCore
    QtCore.Signal = QtCore.pyqtSignal
elif '-pyside' in sys.argv:
    import PySide.QtCore as QtCore
else:    # Autodetect Qt binding
    try:
        import PyQt5.QtCore as QtCore
        QtCore.Signal = QtCore.pyqtSignal
    except ImportError:
        try:
            import PyQt4.QtCore as QtCore
            QtCore.Signal = QtCore.pyqtSignal
        except ImportError:
            import PySide.QtCore as QtCore

from Yowsup.connectionmanager import YowsupConnectionManager
from Yowsup.Media.downloader import MediaDownloader


class WhatsAppClient(QtCore.QObject):
    '''A class, able to handle WhatsApp events and emit signals compatible
    with PyQt, specialized in listening to messages.
    '''

    # Qt's new style signals
    reconnect = QtCore.Signal()
    logMessage = QtCore.Signal(str)
    splashMessage = QtCore.Signal(str)
    splashImage = QtCore.Signal(str)

    def __init__(self, user, password, phone):
        '''WhatsAppClient's constructor.

        Args:
          user (str): the local phone number.
          password (str): the WhatsApp password of 'user'.
          phone (str): the remote phone number.
        '''

        super().__init__()

        self.user = user
        try:
            self.password = base64.b64decode(bytes(password.encode('utf-8')))
        except base64.binascii.Error:    # Lets Yowsup handle the error.
            self.password = bytes(password.encode('utf-8'))
        # Users are identified in WhatsApp by their phone number (plus the
        # code) followed by the domain '@s.whatsapp.net'.
        self.phone = phone + '@s.whatsapp.net'
        self.connected = False

        # Yowsup managers and signals setting up.
        connectionManager = YowsupConnectionManager()
        connectionManager.setAutoPong(True)
        self.signalsInterface = connectionManager.getSignalsInterface()
        self.methodsInterface = connectionManager.getMethodsInterface()

        self.signalsInterface.registerListener('auth_success',
                                               self.onAuthSuccess)
        self.signalsInterface.registerListener('auth_fail',
                                               self.onAuthFailed)
        self.signalsInterface.registerListener('message_received',
                                               self.onMessageReceived)
        self.signalsInterface.registerListener('image_received',
                                               self.onImageReceived)
        self.signalsInterface.registerListener('disconnected',
                                               self.onDisconnected)

    def onAuthSuccess(self, user):
        '''Function called if the authentication process succeeds.

        Args:
          user (str): the local phone number.
        '''
        self.connected = True
        self.log(self.tr('<font color=green><b>Done!</b></font>'))
        self.log(self.tr('<b>Waiting</b> for messages from '
                         '<font color=orange>+{0}</font>.')
                 .format(self.phone[:self.phone.index('@')]))
        # Very important, without this call all messages wil be ignored.
        self.methodsInterface.call('ready')
        # Sets 'available' state for the mobile WhatsApp apps.
        self.methodsInterface.call('presence_sendAvailable')
        # Remote phone will be informed that the application is listening by
        # sending this message.
        self.methodsInterface.call("message_send",
                                   (self.phone,
                                    self.tr('[Splash WhatsApp] connected '
                                            'to: +{0}')
                                    .format(self.user)))

    def onAuthFailed(self, user, error):
        '''Function called if the authentication process fails.

        Args:
          user (str): the local phone number.
          error (str): the error description.
        '''

        # By now, the only error catched is 'invalid', which is very criptic.
        if error == 'invalid':
            error = self.tr('wrong user or password.')
        self.log(self.tr('<font color=red><b>Error:</b></font> {0}')
                 .format(error))

    def onMessageReceived(self, messageid, jid, content, timestamp,
                          wantsReceipt, pushName, isBroadcast):
        '''Function called when a message is received.

        Args:
          messageid (str): a handle to the message.
          jid (str): the sender WhatsApp account (number + domain).
          content (str): the text of the message.
          wantsReceipt (bool): tells if sender expects reception notification.

        Not needed:
          timestamp, pushName, isBroadcast.
        '''

        # Only listens to messages sent from the specified remote phone
        # number.
        if jid == self.phone:
            self.log(self.tr('<font color=orange>+{0}</font> sent:')
                     .format(self.phone[:self.phone.index('@')]))
            self.log('<font color=blue>' + content + '</font>')
            self.splash(content)
            # With this call, sender it's informed that the message has been
            # received (second tick in the mobile app). It prevents WhatsApp
            # servers to keep sending the message every time the local
            # account connect to them.
            if wantsReceipt:
                self.methodsInterface.call('message_ack', (jid, messageid))

    def onImageReceived(self, messageid, jid, preview, url, size, wantsReceipt,
                        isBroadcast):
        '''Function called when an image is received.

        Args:
          messageid (str): a handle to the message.
          jid (str): the sender WhatsApp account (number + domain).
          url (str): the url which the image is stored in.
          wantsReceipt (bool): tells if sender expects reception notification.

        Not needed:
          preview, size, isBroadcast.
        '''

        self.log(self.tr('<font color=orange>+{0}</font> sent an image.')
                 .format(self.phone[:self.phone.index('@')]))
        downloader = MediaDownloader(successClbk=lambda path:
                                     self.splashImage.emit(path),
                                     errorClbk=lambda:
                                     self.log('<font color=red>' +
                                              self.tr('Reception failed.') +
                                              '</font>'))
        downloader.download(url)
        if jid == self.phone:
            if wantsReceipt:
                self.methodsInterface.call('message_ack', (jid, messageid))

    def onDisconnected(self, reason):
        '''Function called in case of a disconnection of WhatsApp servers.

        Args;
          reason (str): the reason of the disconnection.
        '''

        # By now, the only reason catched is dns, whic is very criptic.
        if reason == 'dns':
            reason = self.tr('DNS error.')
        elif reason == 'closed':    # Don't know why this happens
            reason = self.tr('unknown reason.')
        self.log(self.tr('<b>Disconnection:</b> {0}').format(reason))

        # If the user has closed the previous connection (by clicking on the
        # 'Connect' button), 'reconnect' signal is emitted. This is the way
        # of setting a new connection if local or remote phone numbers has
        # been changed.
        if reason == self.tr('closed by user.'):
            self.reconnect.emit()

    def login(self):
        '''Function to connect to WhatsApp servers and start the
        comunication.
        '''

        self.log(self.tr('<b>Connecting</b> to <font color=orange>+{0}'
                         '</font>...').format(self.user))
        self.methodsInterface.call('auth_login', (self.user, self.password))

    def disconnect(self, reason):
        '''Function to force a disconnection from WhatsApp servers.

        Args:
          reason (str): the reason of the disconnection.
        '''

        # Remote user is informed of the disconnection by sending a message
        # to it.
        self.methodsInterface.call('message_send',
                                   (self.phone,
                                    self.tr('[Splash WhatsApp] '
                                            'disconnected')))
        self.connected = False

        # Time is given to ensure that information message is sent before the
        # disconnection.
        time.sleep(0.5)
        self.methodsInterface.call('disconnect', (reason,))

    def log(self, text):
        '''Function that emits a signal with a text, suitable for a PyQt
        widget, like a QTextBrowser, to display that text.

        Args:
          text (str): the text to be displayed.
        '''

        self.logMessage.emit(text)

    def splash(self, text):
        '''Function that emits a signal with a text, suitable for a PyQt
        widget to display that text. The same as 'log' function, it is used
        to differentiate messages only to be logged, from the ones which are
        also been showned as splash screens.

        Args:
          text (str): the text to be displayed.
        '''

        self.splashMessage.emit(text)

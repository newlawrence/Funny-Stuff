#!/usr/bin/env python

import os, os.path
import sys
import copy

import lxml.etree
import calculate

import PyQt5
from PyQt5 import QtCore, QtGui, QtWidgets

try:
    from PyQt5.QtWebKitWidgets import QWebView
except ImportError:
    from PyQt5.QtWebEngineWidgets import QWebEngineView as QWebView


qt_path = os.path.dirname(PyQt5.__file__)
app_path = os.path.abspath(getattr(sys, '_MEIPASS', os.getcwd()))
plugin_path = os.path.join(qt_path)
os.environ['QT_QPA_PLATFORM_PLUGIN_PATH'] = plugin_path


class MainForm(QtWidgets.QWidget):

    def __init__(self):
        super().__init__()

        self.setWindowTitle('Expression Tree Viewer')
        self.setWindowIcon(QtGui.QIcon(os.path.join(app_path, 'icon.png')))
        self.resize(400, 300)
        self.form_layout = QtWidgets.QVBoxLayout()

        self.expression_layout = QtWidgets.QHBoxLayout()
        self.expression_label = QtWidgets.QLabel('Expression')
        self.expression_box = QtWidgets.QLineEdit('')
        self.expression_label.setBuddy(self.expression_box)
        self.expression_layout.addWidget(self.expression_label)
        self.expression_layout.addWidget(self.expression_box)
        self.expression_layout.addItem(QtWidgets.QSpacerItem(
            40, 20,
            QtWidgets.QSizePolicy.Expanding,
            QtWidgets.QSizePolicy.Minimum
        ))

        self.tree_view = QWebView()
        self.tree_view.setHtml('')

        self.form_layout.addLayout(self.expression_layout)
        self.form_layout.addWidget(self.tree_view)
        self.expression_box.textChanged.connect(self.render_expression)

        self.setLayout(self.form_layout)
        self.page = lxml.etree.Element('html')
        self.head = lxml.etree.SubElement(self.page, 'head')
        self.body = lxml.etree.SubElement(self.page, 'body')
        self.style = lxml.etree.SubElement(self.head, 'style')
        with open(os.path.join(app_path, 'styles.css'), 'r') as file_handler:
            self.style.text = file_handler.read()

    def render_expression(self):
        try:
            expression = calculate.parse(self.expression_box.text())
        except calculate.exceptions.BaseCalculateException:
            self.tree_view.setHtml('')
            self.expression_box.setFocus()
            return None

        page = copy.deepcopy(self.page)
        tree_string = expression.tree()
        tree_string = tree_string.replace('[', '').replace(']', '')
        tree_string = tree_string.replace('|', ' ').replace('\\_', '  ')
        tree_string = tree_string.replace('id', '+')
        tree_string = tree_string.replace('neg', '-')
        tree_list = tree_string.split('\n')

        head = lxml.etree.Element('div')
        head.attrib['class'] = 'tree'
        lxml.etree.SubElement(head, 'ul')
        levels = [[lxml.etree.SubElement(head[0], 'li')]]
        level = 0

        parent = lambda: levels[level - 1][-1]
        child = lambda: levels[level][-1]

        lxml.etree.SubElement(child(), 'a')
        child()[0].text = tree_list[0]

        for element in tree_list[1:]:
            level = element.count(' ') // 3
            if level > len(levels) - 1:
                levels.append([])

            if parent()[-1].tag != 'ul':
                lxml.etree.SubElement(parent(), 'ul')
            levels[level].append(lxml.etree.SubElement(parent()[1], 'li'))
            lxml.etree.SubElement(child(), 'a')
            child()[0].text = element.replace(' ', '')

        page[1].insert(0, head)
        self.tree_view.setHtml(lxml.etree.tostring(page).decode())
        self.expression_box.setFocus()


if __name__ == '__main__':
    app = QtWidgets.QApplication(sys.argv)
    app.setAttribute(QtCore.Qt.AA_EnableHighDpiScaling, True)
    form = MainForm()
    form.show()
    sys.exit(app.exec_())

# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file 'resources/ui/webbrowser_widget.ui'
#
# Created: Fri Nov 23 12:45:18 2012
#      by: PyQt4 UI code generator 4.9.1
#
# WARNING! All changes made in this file will be lost!

from PyQt4 import QtCore, QtGui

try:
    _fromUtf8 = QtCore.QString.fromUtf8
except AttributeError:
    _fromUtf8 = lambda s: s

class Ui_webbrowser_widget(object):
    def setupUi(self, webbrowser_widget):
        webbrowser_widget.setObjectName(_fromUtf8("webbrowser_widget"))
        webbrowser_widget.resize(402, 326)
        self.layout_main = QtGui.QVBoxLayout(webbrowser_widget)
        self.layout_main.setMargin(4)
        self.layout_main.setObjectName(_fromUtf8("layout_main"))
        self.widget = QtGui.QWidget(webbrowser_widget)
        sizePolicy = QtGui.QSizePolicy(QtGui.QSizePolicy.Preferred, QtGui.QSizePolicy.Fixed)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.widget.sizePolicy().hasHeightForWidth())
        self.widget.setSizePolicy(sizePolicy)
        self.widget.setObjectName(_fromUtf8("widget"))
        self.horizontalLayout = QtGui.QHBoxLayout(self.widget)
        self.horizontalLayout.setMargin(0)
        self.horizontalLayout.setMargin(0)
        self.horizontalLayout.setObjectName(_fromUtf8("horizontalLayout"))
        self.button_back = QtGui.QPushButton(self.widget)
        sizePolicy = QtGui.QSizePolicy(QtGui.QSizePolicy.Fixed, QtGui.QSizePolicy.Fixed)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.button_back.sizePolicy().hasHeightForWidth())
        self.button_back.setSizePolicy(sizePolicy)
        self.button_back.setText(_fromUtf8(""))
        self.button_back.setFlat(True)
        self.button_back.setObjectName(_fromUtf8("button_back"))
        self.horizontalLayout.addWidget(self.button_back)
        self.button_osdoc = QtGui.QPushButton(self.widget)
        self.button_osdoc.setText(_fromUtf8(""))
        self.button_osdoc.setFlat(True)
        self.button_osdoc.setObjectName(_fromUtf8("button_osdoc"))
        self.horizontalLayout.addWidget(self.button_osdoc)
        self.button_forum = QtGui.QPushButton(self.widget)
        self.button_forum.setText(_fromUtf8(""))
        self.button_forum.setFlat(True)
        self.button_forum.setObjectName(_fromUtf8("button_forum"))
        self.horizontalLayout.addWidget(self.button_forum)
        self.edit_url = QtGui.QLineEdit(self.widget)
        self.edit_url.setReadOnly(True)
        self.edit_url.setObjectName(_fromUtf8("edit_url"))
        self.horizontalLayout.addWidget(self.edit_url)
        self.label_load_progress = QtGui.QLabel(self.widget)
        sizePolicy = QtGui.QSizePolicy(QtGui.QSizePolicy.Fixed, QtGui.QSizePolicy.Preferred)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.label_load_progress.sizePolicy().hasHeightForWidth())
        self.label_load_progress.setSizePolicy(sizePolicy)
        font = QtGui.QFont()
        font.setItalic(True)
        self.label_load_progress.setFont(font)
        self.label_load_progress.setObjectName(_fromUtf8("label_load_progress"))
        self.horizontalLayout.addWidget(self.label_load_progress)
        self.layout_main.addWidget(self.widget)

        self.retranslateUi(webbrowser_widget)
        QtCore.QMetaObject.connectSlotsByName(webbrowser_widget)

    def retranslateUi(self, webbrowser_widget):
        webbrowser_widget.setWindowTitle(QtGui.QApplication.translate("webbrowser_widget", "Form", None, QtGui.QApplication.UnicodeUTF8))
        self.button_back.setToolTip(QtGui.QApplication.translate("webbrowser_widget", "Go back", None, QtGui.QApplication.UnicodeUTF8))
        self.button_osdoc.setToolTip(QtGui.QApplication.translate("webbrowser_widget", "Open OpenSesame documentation area", None, QtGui.QApplication.UnicodeUTF8))
        self.button_forum.setToolTip(QtGui.QApplication.translate("webbrowser_widget", "Open cogsci.nl forum", None, QtGui.QApplication.UnicodeUTF8))
        self.edit_url.setToolTip(QtGui.QApplication.translate("webbrowser_widget", "Address", None, QtGui.QApplication.UnicodeUTF8))
        self.label_load_progress.setToolTip(QtGui.QApplication.translate("webbrowser_widget", "Progress", None, QtGui.QApplication.UnicodeUTF8))
        self.label_load_progress.setText(QtGui.QApplication.translate("webbrowser_widget", "50%", None, QtGui.QApplication.UnicodeUTF8))


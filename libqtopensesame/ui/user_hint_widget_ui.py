# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file 'resources/ui/user_hint_widget.ui'
#
# Created: Thu Mar 14 21:01:43 2013
#      by: PyQt4 UI code generator 4.9.1
#
# WARNING! All changes made in this file will be lost!

from PyQt4 import QtCore, QtGui

try:
    _fromUtf8 = QtCore.QString.fromUtf8
except AttributeError:
    _fromUtf8 = lambda s: s

class Ui_user_hint_widget(object):
    def setupUi(self, user_hint_widget):
        user_hint_widget.setObjectName(_fromUtf8("user_hint_widget"))
        user_hint_widget.resize(406, 37)
        self.horizontalLayout = QtGui.QHBoxLayout(user_hint_widget)
        self.horizontalLayout.setObjectName(_fromUtf8("horizontalLayout"))
        self.label_user_hint = QtGui.QLabel(user_hint_widget)
        self.label_user_hint.setObjectName(_fromUtf8("label_user_hint"))
        self.horizontalLayout.addWidget(self.label_user_hint)
        self.button_edit_script = QtGui.QPushButton(user_hint_widget)
        sizePolicy = QtGui.QSizePolicy(QtGui.QSizePolicy.Fixed, QtGui.QSizePolicy.Fixed)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.button_edit_script.sizePolicy().hasHeightForWidth())
        self.button_edit_script.setSizePolicy(sizePolicy)
        self.button_edit_script.setObjectName(_fromUtf8("button_edit_script"))
        self.horizontalLayout.addWidget(self.button_edit_script)

        self.retranslateUi(user_hint_widget)
        QtCore.QMetaObject.connectSlotsByName(user_hint_widget)

    def retranslateUi(self, user_hint_widget):
        user_hint_widget.setWindowTitle(QtGui.QApplication.translate("user_hint_widget", "Form", None, QtGui.QApplication.UnicodeUTF8))
        self.label_user_hint.setToolTip(QtGui.QApplication.translate("user_hint_widget", "A list of user hints", None, QtGui.QApplication.UnicodeUTF8))
        self.label_user_hint.setText(QtGui.QApplication.translate("user_hint_widget", "User hints", None, QtGui.QApplication.UnicodeUTF8))
        self.button_edit_script.setToolTip(QtGui.QApplication.translate("user_hint_widget", "Click to open script editor", None, QtGui.QApplication.UnicodeUTF8))
        self.button_edit_script.setText(QtGui.QApplication.translate("user_hint_widget", "Edit script", None, QtGui.QApplication.UnicodeUTF8))


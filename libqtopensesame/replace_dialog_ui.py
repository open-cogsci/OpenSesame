# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file 'resources/replace_dialog.ui'
#
# Created: Thu Mar 17 17:48:18 2011
#      by: PyQt4 UI code generator 4.7.4
#
# WARNING! All changes made in this file will be lost!

from PyQt4 import QtCore, QtGui

class Ui_Dialog(object):
    def setupUi(self, Dialog):
        Dialog.setObjectName("Dialog")
        Dialog.resize(390, 107)
        self.verticalLayout = QtGui.QVBoxLayout(Dialog)
        self.verticalLayout.setObjectName("verticalLayout")
        self.widget = QtGui.QWidget(Dialog)
        self.widget.setObjectName("widget")
        self.formLayout = QtGui.QFormLayout(self.widget)
        self.formLayout.setMargin(0)
        self.formLayout.setObjectName("formLayout")
        self.label = QtGui.QLabel(self.widget)
        self.label.setObjectName("label")
        self.formLayout.setWidget(0, QtGui.QFormLayout.LabelRole, self.label)
        self.label_2 = QtGui.QLabel(self.widget)
        self.label_2.setObjectName("label_2")
        self.formLayout.setWidget(1, QtGui.QFormLayout.LabelRole, self.label_2)
        self.edit_search = QtGui.QLineEdit(self.widget)
        self.edit_search.setObjectName("edit_search")
        self.formLayout.setWidget(0, QtGui.QFormLayout.FieldRole, self.edit_search)
        self.edit_replace = QtGui.QLineEdit(self.widget)
        self.edit_replace.setObjectName("edit_replace")
        self.formLayout.setWidget(1, QtGui.QFormLayout.FieldRole, self.edit_replace)
        self.verticalLayout.addWidget(self.widget)
        self.widget_2 = QtGui.QWidget(Dialog)
        self.widget_2.setObjectName("widget_2")
        self.horizontalLayout = QtGui.QHBoxLayout(self.widget_2)
        self.horizontalLayout.setMargin(0)
        self.horizontalLayout.setObjectName("horizontalLayout")
        self.button_search = QtGui.QPushButton(self.widget_2)
        icon = QtGui.QIcon()
        icon.addPixmap(QtGui.QPixmap(":/icons/search.png"), QtGui.QIcon.Normal, QtGui.QIcon.Off)
        self.button_search.setIcon(icon)
        self.button_search.setObjectName("button_search")
        self.horizontalLayout.addWidget(self.button_search)
        self.button_replace = QtGui.QPushButton(self.widget_2)
        icon1 = QtGui.QIcon()
        icon1.addPixmap(QtGui.QPixmap(":/icons/replace.png"), QtGui.QIcon.Normal, QtGui.QIcon.Off)
        self.button_replace.setIcon(icon1)
        self.button_replace.setObjectName("button_replace")
        self.horizontalLayout.addWidget(self.button_replace)
        self.button_replace_all = QtGui.QPushButton(self.widget_2)
        self.button_replace_all.setIcon(icon1)
        self.button_replace_all.setObjectName("button_replace_all")
        self.horizontalLayout.addWidget(self.button_replace_all)
        self.button_close = QtGui.QPushButton(self.widget_2)
        icon2 = QtGui.QIcon()
        icon2.addPixmap(QtGui.QPixmap(":/icons/close.png"), QtGui.QIcon.Normal, QtGui.QIcon.Off)
        self.button_close.setIcon(icon2)
        self.button_close.setObjectName("button_close")
        self.horizontalLayout.addWidget(self.button_close)
        self.verticalLayout.addWidget(self.widget_2)

        self.retranslateUi(Dialog)
        QtCore.QObject.connect(self.button_close, QtCore.SIGNAL("clicked()"), Dialog.accept)
        QtCore.QMetaObject.connectSlotsByName(Dialog)

    def retranslateUi(self, Dialog):
        Dialog.setWindowTitle(QtGui.QApplication.translate("Dialog", "Search/ Replace", None, QtGui.QApplication.UnicodeUTF8))
        self.label.setText(QtGui.QApplication.translate("Dialog", "Search for", None, QtGui.QApplication.UnicodeUTF8))
        self.label_2.setText(QtGui.QApplication.translate("Dialog", "Replace with", None, QtGui.QApplication.UnicodeUTF8))
        self.edit_search.setToolTip(QtGui.QApplication.translate("Dialog", "Search term", None, QtGui.QApplication.UnicodeUTF8))
        self.edit_replace.setToolTip(QtGui.QApplication.translate("Dialog", "Replacement term", None, QtGui.QApplication.UnicodeUTF8))
        self.button_search.setToolTip(QtGui.QApplication.translate("Dialog", "Search and select a single occurence", None, QtGui.QApplication.UnicodeUTF8))
        self.button_search.setText(QtGui.QApplication.translate("Dialog", "Search", None, QtGui.QApplication.UnicodeUTF8))
        self.button_replace.setToolTip(QtGui.QApplication.translate("Dialog", "Replace the current selection", None, QtGui.QApplication.UnicodeUTF8))
        self.button_replace.setText(QtGui.QApplication.translate("Dialog", "Replace", None, QtGui.QApplication.UnicodeUTF8))
        self.button_replace_all.setToolTip(QtGui.QApplication.translate("Dialog", "Replace all occurences", None, QtGui.QApplication.UnicodeUTF8))
        self.button_replace_all.setText(QtGui.QApplication.translate("Dialog", "Replace all", None, QtGui.QApplication.UnicodeUTF8))
        self.button_close.setToolTip(QtGui.QApplication.translate("Dialog", "Close this dialog", None, QtGui.QApplication.UnicodeUTF8))
        self.button_close.setText(QtGui.QApplication.translate("Dialog", "Close", None, QtGui.QApplication.UnicodeUTF8))

import icons_rc

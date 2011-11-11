# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file 'resources/replace_dialog.ui'
#
# Created: Fri Nov 11 12:19:19 2011
#      by: PyQt4 UI code generator 4.8.5
#
# WARNING! All changes made in this file will be lost!

from PyQt4 import QtCore, QtGui

try:
    _fromUtf8 = QtCore.QString.fromUtf8
except AttributeError:
    _fromUtf8 = lambda s: s

class Ui_Dialog(object):
    def setupUi(self, Dialog):
        Dialog.setObjectName(_fromUtf8("Dialog"))
        Dialog.resize(390, 107)
        Dialog.setWindowTitle(QtGui.QApplication.translate("Dialog", "Search/ Replace", None, QtGui.QApplication.UnicodeUTF8))
        self.verticalLayout = QtGui.QVBoxLayout(Dialog)
        self.verticalLayout.setObjectName(_fromUtf8("verticalLayout"))
        self.widget = QtGui.QWidget(Dialog)
        self.widget.setObjectName(_fromUtf8("widget"))
        self.formLayout = QtGui.QFormLayout(self.widget)
        self.formLayout.setMargin(0)
        self.formLayout.setMargin(0)
        self.formLayout.setObjectName(_fromUtf8("formLayout"))
        self.label = QtGui.QLabel(self.widget)
        self.label.setText(QtGui.QApplication.translate("Dialog", "Search for", None, QtGui.QApplication.UnicodeUTF8))
        self.label.setObjectName(_fromUtf8("label"))
        self.formLayout.setWidget(0, QtGui.QFormLayout.LabelRole, self.label)
        self.label_2 = QtGui.QLabel(self.widget)
        self.label_2.setText(QtGui.QApplication.translate("Dialog", "Replace with", None, QtGui.QApplication.UnicodeUTF8))
        self.label_2.setObjectName(_fromUtf8("label_2"))
        self.formLayout.setWidget(1, QtGui.QFormLayout.LabelRole, self.label_2)
        self.edit_search = QtGui.QLineEdit(self.widget)
        self.edit_search.setToolTip(QtGui.QApplication.translate("Dialog", "Search term", None, QtGui.QApplication.UnicodeUTF8))
        self.edit_search.setObjectName(_fromUtf8("edit_search"))
        self.formLayout.setWidget(0, QtGui.QFormLayout.FieldRole, self.edit_search)
        self.edit_replace = QtGui.QLineEdit(self.widget)
        self.edit_replace.setToolTip(QtGui.QApplication.translate("Dialog", "Replacement term", None, QtGui.QApplication.UnicodeUTF8))
        self.edit_replace.setObjectName(_fromUtf8("edit_replace"))
        self.formLayout.setWidget(1, QtGui.QFormLayout.FieldRole, self.edit_replace)
        self.verticalLayout.addWidget(self.widget)
        self.widget_2 = QtGui.QWidget(Dialog)
        self.widget_2.setObjectName(_fromUtf8("widget_2"))
        self.horizontalLayout = QtGui.QHBoxLayout(self.widget_2)
        self.horizontalLayout.setMargin(0)
        self.horizontalLayout.setMargin(0)
        self.horizontalLayout.setObjectName(_fromUtf8("horizontalLayout"))
        self.button_search = QtGui.QPushButton(self.widget_2)
        self.button_search.setToolTip(QtGui.QApplication.translate("Dialog", "Search and select a single occurence", None, QtGui.QApplication.UnicodeUTF8))
        self.button_search.setText(QtGui.QApplication.translate("Dialog", "Search", None, QtGui.QApplication.UnicodeUTF8))
        icon = QtGui.QIcon()
        icon.addPixmap(QtGui.QPixmap(_fromUtf8(":/icons/search.png")), QtGui.QIcon.Normal, QtGui.QIcon.Off)
        self.button_search.setIcon(icon)
        self.button_search.setObjectName(_fromUtf8("button_search"))
        self.horizontalLayout.addWidget(self.button_search)
        self.button_replace = QtGui.QPushButton(self.widget_2)
        self.button_replace.setToolTip(QtGui.QApplication.translate("Dialog", "Replace the current selection", None, QtGui.QApplication.UnicodeUTF8))
        self.button_replace.setText(QtGui.QApplication.translate("Dialog", "Replace", None, QtGui.QApplication.UnicodeUTF8))
        icon1 = QtGui.QIcon()
        icon1.addPixmap(QtGui.QPixmap(_fromUtf8(":/icons/replace.png")), QtGui.QIcon.Normal, QtGui.QIcon.Off)
        self.button_replace.setIcon(icon1)
        self.button_replace.setObjectName(_fromUtf8("button_replace"))
        self.horizontalLayout.addWidget(self.button_replace)
        self.button_replace_all = QtGui.QPushButton(self.widget_2)
        self.button_replace_all.setToolTip(QtGui.QApplication.translate("Dialog", "Replace all occurences", None, QtGui.QApplication.UnicodeUTF8))
        self.button_replace_all.setText(QtGui.QApplication.translate("Dialog", "Replace all", None, QtGui.QApplication.UnicodeUTF8))
        self.button_replace_all.setIcon(icon1)
        self.button_replace_all.setObjectName(_fromUtf8("button_replace_all"))
        self.horizontalLayout.addWidget(self.button_replace_all)
        self.button_close = QtGui.QPushButton(self.widget_2)
        self.button_close.setToolTip(QtGui.QApplication.translate("Dialog", "Close this dialog", None, QtGui.QApplication.UnicodeUTF8))
        self.button_close.setText(QtGui.QApplication.translate("Dialog", "Close", None, QtGui.QApplication.UnicodeUTF8))
        icon2 = QtGui.QIcon()
        icon2.addPixmap(QtGui.QPixmap(_fromUtf8(":/icons/close.png")), QtGui.QIcon.Normal, QtGui.QIcon.Off)
        self.button_close.setIcon(icon2)
        self.button_close.setObjectName(_fromUtf8("button_close"))
        self.horizontalLayout.addWidget(self.button_close)
        self.verticalLayout.addWidget(self.widget_2)

        self.retranslateUi(Dialog)
        QtCore.QObject.connect(self.button_close, QtCore.SIGNAL(_fromUtf8("clicked()")), Dialog.accept)
        QtCore.QMetaObject.connectSlotsByName(Dialog)

    def retranslateUi(self, Dialog):
        pass

import icons_rc

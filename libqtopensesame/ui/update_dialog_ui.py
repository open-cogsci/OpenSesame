# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file 'resources/ui/update_dialog.ui'
#
# Created: Thu Jul  5 19:55:55 2012
#      by: PyQt4 UI code generator 4.9.1
#
# WARNING! All changes made in this file will be lost!

from PyQt4 import QtCore, QtGui

try:
    _fromUtf8 = QtCore.QString.fromUtf8
except AttributeError:
    _fromUtf8 = lambda s: s

class Ui_update_dialog(object):
    def setupUi(self, update_dialog):
        update_dialog.setObjectName(_fromUtf8("update_dialog"))
        update_dialog.resize(400, 299)
        self.verticalLayout = QtGui.QVBoxLayout(update_dialog)
        self.verticalLayout.setMargin(8)
        self.verticalLayout.setObjectName(_fromUtf8("verticalLayout"))
        self.widget = QtGui.QWidget(update_dialog)
        sizePolicy = QtGui.QSizePolicy(QtGui.QSizePolicy.Preferred, QtGui.QSizePolicy.Fixed)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.widget.sizePolicy().hasHeightForWidth())
        self.widget.setSizePolicy(sizePolicy)
        self.widget.setStyleSheet(_fromUtf8("color: rgb(255, 255, 255);\n"
"background-color: #729fcf;"))
        self.widget.setObjectName(_fromUtf8("widget"))
        self.horizontalLayout = QtGui.QHBoxLayout(self.widget)
        self.horizontalLayout.setMargin(5)
        self.horizontalLayout.setMargin(0)
        self.horizontalLayout.setObjectName(_fromUtf8("horizontalLayout"))
        self.label_update_dialog = QtGui.QLabel(self.widget)
        sizePolicy = QtGui.QSizePolicy(QtGui.QSizePolicy.Fixed, QtGui.QSizePolicy.Preferred)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.label_update_dialog.sizePolicy().hasHeightForWidth())
        self.label_update_dialog.setSizePolicy(sizePolicy)
        self.label_update_dialog.setText(_fromUtf8(""))
        self.label_update_dialog.setPixmap(QtGui.QPixmap(_fromUtf8(":/icons/update_large.png")))
        self.label_update_dialog.setObjectName(_fromUtf8("label_update_dialog"))
        self.horizontalLayout.addWidget(self.label_update_dialog)
        self.label_2 = QtGui.QLabel(self.widget)
        font = QtGui.QFont()
        font.setPointSize(11)
        font.setBold(True)
        font.setWeight(75)
        self.label_2.setFont(font)
        self.label_2.setObjectName(_fromUtf8("label_2"))
        self.horizontalLayout.addWidget(self.label_2)
        self.verticalLayout.addWidget(self.widget)
        self.textedit_notification = QtGui.QTextBrowser(update_dialog)
        font = QtGui.QFont()
        font.setFamily(_fromUtf8("Monospace"))
        self.textedit_notification.setFont(font)
        self.textedit_notification.setObjectName(_fromUtf8("textedit_notification"))
        self.verticalLayout.addWidget(self.textedit_notification)
        self.checkbox_auto_check_update = QtGui.QCheckBox(update_dialog)
        self.checkbox_auto_check_update.setObjectName(_fromUtf8("checkbox_auto_check_update"))
        self.verticalLayout.addWidget(self.checkbox_auto_check_update)
        self.buttonBox = QtGui.QDialogButtonBox(update_dialog)
        self.buttonBox.setOrientation(QtCore.Qt.Horizontal)
        self.buttonBox.setStandardButtons(QtGui.QDialogButtonBox.Close)
        self.buttonBox.setObjectName(_fromUtf8("buttonBox"))
        self.verticalLayout.addWidget(self.buttonBox)

        self.retranslateUi(update_dialog)
        QtCore.QObject.connect(self.buttonBox, QtCore.SIGNAL(_fromUtf8("accepted()")), update_dialog.accept)
        QtCore.QObject.connect(self.buttonBox, QtCore.SIGNAL(_fromUtf8("rejected()")), update_dialog.reject)
        QtCore.QMetaObject.connectSlotsByName(update_dialog)

    def retranslateUi(self, update_dialog):
        update_dialog.setWindowTitle(QtGui.QApplication.translate("update_dialog", "OpenSesame has checked for updates ...", None, QtGui.QApplication.UnicodeUTF8))
        self.label_2.setText(QtGui.QApplication.translate("update_dialog", "OpenSesame has checked for updates ...", None, QtGui.QApplication.UnicodeUTF8))
        self.checkbox_auto_check_update.setText(QtGui.QApplication.translate("update_dialog", "Check for updates on start-up", None, QtGui.QApplication.UnicodeUTF8))


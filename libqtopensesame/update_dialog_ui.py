# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file 'resources/update_dialog.ui'
#
# Created: Sun May 29 15:09:19 2011
#      by: PyQt4 UI code generator 4.7.4
#
# WARNING! All changes made in this file will be lost!

from PyQt4 import QtCore, QtGui

class Ui_Dialog(object):
    def setupUi(self, Dialog):
        Dialog.setObjectName("Dialog")
        Dialog.resize(400, 299)
        self.verticalLayout = QtGui.QVBoxLayout(Dialog)
        self.verticalLayout.setMargin(8)
        self.verticalLayout.setObjectName("verticalLayout")
        self.widget = QtGui.QWidget(Dialog)
        sizePolicy = QtGui.QSizePolicy(QtGui.QSizePolicy.Preferred, QtGui.QSizePolicy.Fixed)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.widget.sizePolicy().hasHeightForWidth())
        self.widget.setSizePolicy(sizePolicy)
        self.widget.setStyleSheet("color: rgb(255, 255, 255);\n"
"background-color: #729fcf;")
        self.widget.setObjectName("widget")
        self.horizontalLayout = QtGui.QHBoxLayout(self.widget)
        self.horizontalLayout.setMargin(4)
        self.horizontalLayout.setObjectName("horizontalLayout")
        self.label = QtGui.QLabel(self.widget)
        sizePolicy = QtGui.QSizePolicy(QtGui.QSizePolicy.Fixed, QtGui.QSizePolicy.Preferred)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.label.sizePolicy().hasHeightForWidth())
        self.label.setSizePolicy(sizePolicy)
        self.label.setText("")
        self.label.setPixmap(QtGui.QPixmap(":/icons/update_large.png"))
        self.label.setObjectName("label")
        self.horizontalLayout.addWidget(self.label)
        self.label_2 = QtGui.QLabel(self.widget)
        font = QtGui.QFont()
        font.setPointSize(11)
        font.setWeight(75)
        font.setBold(True)
        self.label_2.setFont(font)
        self.label_2.setObjectName("label_2")
        self.horizontalLayout.addWidget(self.label_2)
        self.verticalLayout.addWidget(self.widget)
        self.textedit_notification = QtGui.QTextBrowser(Dialog)
        font = QtGui.QFont()
        font.setFamily("Monospace")
        self.textedit_notification.setFont(font)
        self.textedit_notification.setObjectName("textedit_notification")
        self.verticalLayout.addWidget(self.textedit_notification)
        self.checkbox_auto_check_update = QtGui.QCheckBox(Dialog)
        self.checkbox_auto_check_update.setObjectName("checkbox_auto_check_update")
        self.verticalLayout.addWidget(self.checkbox_auto_check_update)
        self.buttonBox = QtGui.QDialogButtonBox(Dialog)
        self.buttonBox.setOrientation(QtCore.Qt.Horizontal)
        self.buttonBox.setStandardButtons(QtGui.QDialogButtonBox.Close)
        self.buttonBox.setObjectName("buttonBox")
        self.verticalLayout.addWidget(self.buttonBox)

        self.retranslateUi(Dialog)
        QtCore.QObject.connect(self.buttonBox, QtCore.SIGNAL("accepted()"), Dialog.accept)
        QtCore.QObject.connect(self.buttonBox, QtCore.SIGNAL("rejected()"), Dialog.reject)
        QtCore.QMetaObject.connectSlotsByName(Dialog)

    def retranslateUi(self, Dialog):
        Dialog.setWindowTitle(QtGui.QApplication.translate("Dialog", "OpenSesame has checked for updates ...", None, QtGui.QApplication.UnicodeUTF8))
        self.label_2.setText(QtGui.QApplication.translate("Dialog", "OpenSesame has checked for updates ...", None, QtGui.QApplication.UnicodeUTF8))
        self.checkbox_auto_check_update.setText(QtGui.QApplication.translate("Dialog", "Check for updates on start-up", None, QtGui.QApplication.UnicodeUTF8))

import icons_rc

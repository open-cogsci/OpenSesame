# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file 'resources/ui/notification_dialog.ui'
#
# Created: Wed Oct  9 14:51:38 2013
#      by: PyQt4 UI code generator 4.10
#
# WARNING! All changes made in this file will be lost!

from PyQt4 import QtCore, QtGui

try:
    _fromUtf8 = QtCore.QString.fromUtf8
except AttributeError:
    def _fromUtf8(s):
        return s

try:
    _encoding = QtGui.QApplication.UnicodeUTF8
    def _translate(context, text, disambig):
        return QtGui.QApplication.translate(context, text, disambig, _encoding)
except AttributeError:
    def _translate(context, text, disambig):
        return QtGui.QApplication.translate(context, text, disambig)

class Ui_notification_dialog(object):
    def setupUi(self, notification_dialog):
        notification_dialog.setObjectName(_fromUtf8("notification_dialog"))
        notification_dialog.resize(400, 300)
        self.verticalLayout = QtGui.QVBoxLayout(notification_dialog)
        self.verticalLayout.setMargin(8)
        self.verticalLayout.setObjectName(_fromUtf8("verticalLayout"))
        self.widget = QtGui.QWidget(notification_dialog)
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
        self.horizontalLayout.setObjectName(_fromUtf8("horizontalLayout"))
        self.label_notification = QtGui.QLabel(self.widget)
        sizePolicy = QtGui.QSizePolicy(QtGui.QSizePolicy.Fixed, QtGui.QSizePolicy.Preferred)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.label_notification.sizePolicy().hasHeightForWidth())
        self.label_notification.setSizePolicy(sizePolicy)
        self.label_notification.setText(_fromUtf8(""))
        self.label_notification.setPixmap(QtGui.QPixmap(_fromUtf8(":/icons/about_large.png")))
        self.label_notification.setObjectName(_fromUtf8("label_notification"))
        self.horizontalLayout.addWidget(self.label_notification)
        self.label_title = QtGui.QLabel(self.widget)
        font = QtGui.QFont()
        font.setPointSize(11)
        font.setBold(True)
        font.setWeight(75)
        self.label_title.setFont(font)
        self.label_title.setObjectName(_fromUtf8("label_title"))
        self.horizontalLayout.addWidget(self.label_title)
        self.verticalLayout.addWidget(self.widget)
        self.textedit_notification = QtGui.QTextBrowser(notification_dialog)
        font = QtGui.QFont()
        font.setFamily(_fromUtf8("Monospace"))
        self.textedit_notification.setFont(font)
        self.textedit_notification.setObjectName(_fromUtf8("textedit_notification"))
        self.verticalLayout.addWidget(self.textedit_notification)
        self.buttonBox = QtGui.QDialogButtonBox(notification_dialog)
        self.buttonBox.setOrientation(QtCore.Qt.Horizontal)
        self.buttonBox.setStandardButtons(QtGui.QDialogButtonBox.Close)
        self.buttonBox.setObjectName(_fromUtf8("buttonBox"))
        self.verticalLayout.addWidget(self.buttonBox)

        self.retranslateUi(notification_dialog)
        QtCore.QObject.connect(self.buttonBox, QtCore.SIGNAL(_fromUtf8("accepted()")), notification_dialog.accept)
        QtCore.QObject.connect(self.buttonBox, QtCore.SIGNAL(_fromUtf8("rejected()")), notification_dialog.reject)
        QtCore.QMetaObject.connectSlotsByName(notification_dialog)

    def retranslateUi(self, notification_dialog):
        notification_dialog.setWindowTitle(_translate("notification_dialog", "OpenSesame says ...", None))
        self.label_title.setText(_translate("notification_dialog", "OpenSesame says ...", None))


# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file 'resources/ui/text_input_dialog.ui'
#
# Created: Sun Nov 18 18:16:40 2012
#      by: PyQt4 UI code generator 4.9.1
#
# WARNING! All changes made in this file will be lost!

from PyQt4 import QtCore, QtGui

try:
    _fromUtf8 = QtCore.QString.fromUtf8
except AttributeError:
    _fromUtf8 = lambda s: s

class Ui_text_input_dialog(object):
    def setupUi(self, text_input_dialog):
        text_input_dialog.setObjectName(_fromUtf8("text_input_dialog"))
        text_input_dialog.resize(608, 233)
        self.verticalLayout = QtGui.QVBoxLayout(text_input_dialog)
        self.verticalLayout.setMargin(8)
        self.verticalLayout.setObjectName(_fromUtf8("verticalLayout"))
        self.widget = QtGui.QWidget(text_input_dialog)
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
        self.label_text_input = QtGui.QLabel(self.widget)
        sizePolicy = QtGui.QSizePolicy(QtGui.QSizePolicy.Fixed, QtGui.QSizePolicy.Preferred)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.label_text_input.sizePolicy().hasHeightForWidth())
        self.label_text_input.setSizePolicy(sizePolicy)
        self.label_text_input.setText(_fromUtf8(""))
        self.label_text_input.setPixmap(QtGui.QPixmap(_fromUtf8(":/icons/about_large.png")))
        self.label_text_input.setObjectName(_fromUtf8("label_text_input"))
        self.horizontalLayout.addWidget(self.label_text_input)
        self.label_message = QtGui.QLabel(self.widget)
        font = QtGui.QFont()
        font.setPointSize(11)
        font.setBold(True)
        font.setWeight(75)
        self.label_message.setFont(font)
        self.label_message.setObjectName(_fromUtf8("label_message"))
        self.horizontalLayout.addWidget(self.label_message)
        self.verticalLayout.addWidget(self.widget)
        self.textedit_input = QtGui.QTextEdit(text_input_dialog)
        self.textedit_input.setAcceptRichText(False)
        self.textedit_input.setObjectName(_fromUtf8("textedit_input"))
        self.verticalLayout.addWidget(self.textedit_input)
        self.buttonBox = QtGui.QDialogButtonBox(text_input_dialog)
        self.buttonBox.setOrientation(QtCore.Qt.Horizontal)
        self.buttonBox.setStandardButtons(QtGui.QDialogButtonBox.Cancel|QtGui.QDialogButtonBox.Ok)
        self.buttonBox.setObjectName(_fromUtf8("buttonBox"))
        self.verticalLayout.addWidget(self.buttonBox)

        self.retranslateUi(text_input_dialog)
        QtCore.QObject.connect(self.buttonBox, QtCore.SIGNAL(_fromUtf8("accepted()")), text_input_dialog.accept)
        QtCore.QObject.connect(self.buttonBox, QtCore.SIGNAL(_fromUtf8("rejected()")), text_input_dialog.reject)
        QtCore.QMetaObject.connectSlotsByName(text_input_dialog)

    def retranslateUi(self, text_input_dialog):
        text_input_dialog.setWindowTitle(QtGui.QApplication.translate("text_input_dialog", "OpenSesame says ...", None, QtGui.QApplication.UnicodeUTF8))
        self.label_message.setText(QtGui.QApplication.translate("text_input_dialog", "Message", None, QtGui.QApplication.UnicodeUTF8))


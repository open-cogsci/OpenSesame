# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file 'resources/ui/start_new_dialog.ui'
#
# Created: Thu Jul  5 19:55:56 2012
#      by: PyQt4 UI code generator 4.9.1
#
# WARNING! All changes made in this file will be lost!

from PyQt4 import QtCore, QtGui

try:
    _fromUtf8 = QtCore.QString.fromUtf8
except AttributeError:
    _fromUtf8 = lambda s: s

class Ui_start_new_dialog(object):
    def setupUi(self, start_new_dialog):
        start_new_dialog.setObjectName(_fromUtf8("start_new_dialog"))
        start_new_dialog.resize(669, 255)
        self.verticalLayout_2 = QtGui.QVBoxLayout(start_new_dialog)
        self.verticalLayout_2.setSpacing(12)
        self.verticalLayout_2.setObjectName(_fromUtf8("verticalLayout_2"))
        self.widget_2 = QtGui.QWidget(start_new_dialog)
        sizePolicy = QtGui.QSizePolicy(QtGui.QSizePolicy.Preferred, QtGui.QSizePolicy.Fixed)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.widget_2.sizePolicy().hasHeightForWidth())
        self.widget_2.setSizePolicy(sizePolicy)
        self.widget_2.setStyleSheet(_fromUtf8("background-color: #729fcf;\n"
"color: rgb(255, 255, 255);"))
        self.widget_2.setObjectName(_fromUtf8("widget_2"))
        self.horizontalLayout = QtGui.QHBoxLayout(self.widget_2)
        self.horizontalLayout.setMargin(5)
        self.horizontalLayout.setMargin(0)
        self.horizontalLayout.setObjectName(_fromUtf8("horizontalLayout"))
        self.label_start_new = QtGui.QLabel(self.widget_2)
        sizePolicy = QtGui.QSizePolicy(QtGui.QSizePolicy.Fixed, QtGui.QSizePolicy.Preferred)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.label_start_new.sizePolicy().hasHeightForWidth())
        self.label_start_new.setSizePolicy(sizePolicy)
        self.label_start_new.setText(_fromUtf8(""))
        self.label_start_new.setPixmap(QtGui.QPixmap(_fromUtf8(":/icons/experiment_large.png")))
        self.label_start_new.setObjectName(_fromUtf8("label_start_new"))
        self.horizontalLayout.addWidget(self.label_start_new)
        self.label_4 = QtGui.QLabel(self.widget_2)
        font = QtGui.QFont()
        font.setPointSize(11)
        font.setBold(True)
        font.setWeight(75)
        self.label_4.setFont(font)
        self.label_4.setObjectName(_fromUtf8("label_4"))
        self.horizontalLayout.addWidget(self.label_4)
        self.verticalLayout_2.addWidget(self.widget_2)
        self.widget = QtGui.QWidget(start_new_dialog)
        self.widget.setObjectName(_fromUtf8("widget"))
        self.horizontalLayout_2 = QtGui.QHBoxLayout(self.widget)
        self.horizontalLayout_2.setSpacing(8)
        self.horizontalLayout_2.setMargin(0)
        self.horizontalLayout_2.setMargin(0)
        self.horizontalLayout_2.setObjectName(_fromUtf8("horizontalLayout_2"))
        self.frame_2 = QtGui.QFrame(self.widget)
        self.frame_2.setFrameShape(QtGui.QFrame.NoFrame)
        self.frame_2.setFrameShadow(QtGui.QFrame.Raised)
        self.frame_2.setObjectName(_fromUtf8("frame_2"))
        self.verticalLayout = QtGui.QVBoxLayout(self.frame_2)
        self.verticalLayout.setSpacing(12)
        self.verticalLayout.setMargin(0)
        self.verticalLayout.setObjectName(_fromUtf8("verticalLayout"))
        self.widget_4 = QtGui.QWidget(self.frame_2)
        self.widget_4.setObjectName(_fromUtf8("widget_4"))
        self.horizontalLayout_4 = QtGui.QHBoxLayout(self.widget_4)
        self.horizontalLayout_4.setMargin(0)
        self.horizontalLayout_4.setMargin(0)
        self.horizontalLayout_4.setObjectName(_fromUtf8("horizontalLayout_4"))
        self.label_template = QtGui.QLabel(self.widget_4)
        sizePolicy = QtGui.QSizePolicy(QtGui.QSizePolicy.Fixed, QtGui.QSizePolicy.Preferred)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.label_template.sizePolicy().hasHeightForWidth())
        self.label_template.setSizePolicy(sizePolicy)
        self.label_template.setText(_fromUtf8(""))
        self.label_template.setPixmap(QtGui.QPixmap(_fromUtf8(":/icons/wizard_large.png")))
        self.label_template.setAlignment(QtCore.Qt.AlignLeading|QtCore.Qt.AlignLeft|QtCore.Qt.AlignVCenter)
        self.label_template.setObjectName(_fromUtf8("label_template"))
        self.horizontalLayout_4.addWidget(self.label_template)
        self.label_5 = QtGui.QLabel(self.widget_4)
        font = QtGui.QFont()
        font.setPointSize(16)
        font.setBold(True)
        font.setWeight(75)
        self.label_5.setFont(font)
        self.label_5.setAlignment(QtCore.Qt.AlignLeading|QtCore.Qt.AlignLeft|QtCore.Qt.AlignVCenter)
        self.label_5.setObjectName(_fromUtf8("label_5"))
        self.horizontalLayout_4.addWidget(self.label_5)
        self.verticalLayout.addWidget(self.widget_4)
        self.list_templates = QtGui.QListWidget(self.frame_2)
        self.list_templates.setAlternatingRowColors(True)
        self.list_templates.setObjectName(_fromUtf8("list_templates"))
        self.verticalLayout.addWidget(self.list_templates)
        self.button_template = QtGui.QPushButton(self.frame_2)
        icon = QtGui.QIcon()
        icon.addPixmap(QtGui.QPixmap(_fromUtf8(":/icons/wizard.png")), QtGui.QIcon.Normal, QtGui.QIcon.Off)
        self.button_template.setIcon(icon)
        self.button_template.setIconSize(QtCore.QSize(16, 16))
        self.button_template.setObjectName(_fromUtf8("button_template"))
        self.verticalLayout.addWidget(self.button_template)
        self.horizontalLayout_2.addWidget(self.frame_2)
        self.label_or = QtGui.QLabel(self.widget)
        font = QtGui.QFont()
        font.setPointSize(16)
        self.label_or.setFont(font)
        self.label_or.setAlignment(QtCore.Qt.AlignCenter)
        self.label_or.setObjectName(_fromUtf8("label_or"))
        self.horizontalLayout_2.addWidget(self.label_or)
        self.frame = QtGui.QFrame(self.widget)
        self.frame.setFrameShape(QtGui.QFrame.NoFrame)
        self.frame.setFrameShadow(QtGui.QFrame.Raised)
        self.frame.setObjectName(_fromUtf8("frame"))
        self.verticalLayout_3 = QtGui.QVBoxLayout(self.frame)
        self.verticalLayout_3.setSpacing(12)
        self.verticalLayout_3.setMargin(0)
        self.verticalLayout_3.setObjectName(_fromUtf8("verticalLayout_3"))
        self.widget_5 = QtGui.QWidget(self.frame)
        self.widget_5.setObjectName(_fromUtf8("widget_5"))
        self.horizontalLayout_5 = QtGui.QHBoxLayout(self.widget_5)
        self.horizontalLayout_5.setMargin(0)
        self.horizontalLayout_5.setMargin(0)
        self.horizontalLayout_5.setObjectName(_fromUtf8("horizontalLayout_5"))
        self.label_recent = QtGui.QLabel(self.widget_5)
        sizePolicy = QtGui.QSizePolicy(QtGui.QSizePolicy.Fixed, QtGui.QSizePolicy.Preferred)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.label_recent.sizePolicy().hasHeightForWidth())
        self.label_recent.setSizePolicy(sizePolicy)
        self.label_recent.setText(_fromUtf8(""))
        self.label_recent.setPixmap(QtGui.QPixmap(_fromUtf8(":/icons/experiment_large.png")))
        self.label_recent.setObjectName(_fromUtf8("label_recent"))
        self.horizontalLayout_5.addWidget(self.label_recent)
        self.label_2 = QtGui.QLabel(self.widget_5)
        font = QtGui.QFont()
        font.setPointSize(16)
        font.setBold(True)
        font.setWeight(75)
        self.label_2.setFont(font)
        self.label_2.setObjectName(_fromUtf8("label_2"))
        self.horizontalLayout_5.addWidget(self.label_2)
        self.verticalLayout_3.addWidget(self.widget_5)
        self.list_recent = QtGui.QListWidget(self.frame)
        self.list_recent.setAlternatingRowColors(True)
        self.list_recent.setObjectName(_fromUtf8("list_recent"))
        self.verticalLayout_3.addWidget(self.list_recent)
        self.widget_3 = QtGui.QWidget(self.frame)
        self.widget_3.setObjectName(_fromUtf8("widget_3"))
        self.horizontalLayout_3 = QtGui.QHBoxLayout(self.widget_3)
        self.horizontalLayout_3.setMargin(0)
        self.horizontalLayout_3.setMargin(0)
        self.horizontalLayout_3.setObjectName(_fromUtf8("horizontalLayout_3"))
        self.button_recent = QtGui.QPushButton(self.widget_3)
        icon1 = QtGui.QIcon()
        icon1.addPixmap(QtGui.QPixmap(_fromUtf8(":/icons/browse.png")), QtGui.QIcon.Normal, QtGui.QIcon.Off)
        self.button_recent.setIcon(icon1)
        self.button_recent.setIconSize(QtCore.QSize(16, 16))
        self.button_recent.setObjectName(_fromUtf8("button_recent"))
        self.horizontalLayout_3.addWidget(self.button_recent)
        self.button_browse = QtGui.QPushButton(self.widget_3)
        self.button_browse.setIcon(icon1)
        self.button_browse.setIconSize(QtCore.QSize(16, 16))
        self.button_browse.setObjectName(_fromUtf8("button_browse"))
        self.horizontalLayout_3.addWidget(self.button_browse)
        self.verticalLayout_3.addWidget(self.widget_3)
        self.horizontalLayout_2.addWidget(self.frame)
        self.verticalLayout_2.addWidget(self.widget)

        self.retranslateUi(start_new_dialog)
        QtCore.QMetaObject.connectSlotsByName(start_new_dialog)

    def retranslateUi(self, start_new_dialog):
        start_new_dialog.setWindowTitle(QtGui.QApplication.translate("start_new_dialog", "New experiment", None, QtGui.QApplication.UnicodeUTF8))
        self.label_4.setText(QtGui.QApplication.translate("start_new_dialog", "How would you like to begin?", None, QtGui.QApplication.UnicodeUTF8))
        self.label_5.setText(QtGui.QApplication.translate("start_new_dialog", "Templates", None, QtGui.QApplication.UnicodeUTF8))
        self.button_template.setText(QtGui.QApplication.translate("start_new_dialog", "Start from template", None, QtGui.QApplication.UnicodeUTF8))
        self.label_or.setText(QtGui.QApplication.translate("start_new_dialog", "or", None, QtGui.QApplication.UnicodeUTF8))
        self.label_2.setText(QtGui.QApplication.translate("start_new_dialog", "Recent experiments", None, QtGui.QApplication.UnicodeUTF8))
        self.button_recent.setText(QtGui.QApplication.translate("start_new_dialog", "Open recent", None, QtGui.QApplication.UnicodeUTF8))
        self.button_browse.setText(QtGui.QApplication.translate("start_new_dialog", "Browse", None, QtGui.QApplication.UnicodeUTF8))


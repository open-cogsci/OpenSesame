# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file 'resources/new_loop_sequence.ui'
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
        Dialog.resize(411, 197)
        Dialog.setWindowTitle(QtGui.QApplication.translate("Dialog", "Dialog", None, QtGui.QApplication.UnicodeUTF8))
        self.verticalLayout = QtGui.QVBoxLayout(Dialog)
        self.verticalLayout.setObjectName(_fromUtf8("verticalLayout"))
        self.widget_3 = QtGui.QWidget(Dialog)
        self.widget_3.setObjectName(_fromUtf8("widget_3"))
        self.horizontalLayout_3 = QtGui.QHBoxLayout(self.widget_3)
        self.horizontalLayout_3.setMargin(0)
        self.horizontalLayout_3.setMargin(0)
        self.horizontalLayout_3.setObjectName(_fromUtf8("horizontalLayout_3"))
        self.label_icon = QtGui.QLabel(self.widget_3)
        sizePolicy = QtGui.QSizePolicy(QtGui.QSizePolicy.Fixed, QtGui.QSizePolicy.Preferred)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.label_icon.sizePolicy().hasHeightForWidth())
        self.label_icon.setSizePolicy(sizePolicy)
        self.label_icon.setText(_fromUtf8(""))
        self.label_icon.setPixmap(QtGui.QPixmap(_fromUtf8(":/icons/loop_large.png")))
        self.label_icon.setObjectName(_fromUtf8("label_icon"))
        self.horizontalLayout_3.addWidget(self.label_icon)
        self.label_explanation = QtGui.QLabel(self.widget_3)
        self.label_explanation.setText(QtGui.QApplication.translate("Dialog", "Explanation\n"
"", None, QtGui.QApplication.UnicodeUTF8))
        self.label_explanation.setWordWrap(True)
        self.label_explanation.setObjectName(_fromUtf8("label_explanation"))
        self.horizontalLayout_3.addWidget(self.label_explanation)
        self.verticalLayout.addWidget(self.widget_3)
        spacerItem = QtGui.QSpacerItem(20, 40, QtGui.QSizePolicy.Minimum, QtGui.QSizePolicy.Expanding)
        self.verticalLayout.addItem(spacerItem)
        self.widget_2 = QtGui.QWidget(Dialog)
        self.widget_2.setObjectName(_fromUtf8("widget_2"))
        self.horizontalLayout = QtGui.QHBoxLayout(self.widget_2)
        self.horizontalLayout.setSpacing(12)
        self.horizontalLayout.setMargin(0)
        self.horizontalLayout.setMargin(0)
        self.horizontalLayout.setObjectName(_fromUtf8("horizontalLayout"))
        self.groupBox = QtGui.QGroupBox(self.widget_2)
        self.groupBox.setTitle(QtGui.QApplication.translate("Dialog", "Create new item to use", None, QtGui.QApplication.UnicodeUTF8))
        self.groupBox.setObjectName(_fromUtf8("groupBox"))
        self.verticalLayout_2 = QtGui.QVBoxLayout(self.groupBox)
        self.verticalLayout_2.setContentsMargins(0, 8, 0, 0)
        self.verticalLayout_2.setObjectName(_fromUtf8("verticalLayout_2"))
        self.combobox_new = QtGui.QComboBox(self.groupBox)
        self.combobox_new.setObjectName(_fromUtf8("combobox_new"))
        self.verticalLayout_2.addWidget(self.combobox_new)
        self.button_new = QtGui.QPushButton(self.groupBox)
        self.button_new.setText(QtGui.QApplication.translate("Dialog", "Create", None, QtGui.QApplication.UnicodeUTF8))
        icon = QtGui.QIcon()
        icon.addPixmap(QtGui.QPixmap(_fromUtf8(":/icons/add.png")), QtGui.QIcon.Normal, QtGui.QIcon.Off)
        self.button_new.setIcon(icon)
        self.button_new.setIconSize(QtCore.QSize(16, 16))
        self.button_new.setObjectName(_fromUtf8("button_new"))
        self.verticalLayout_2.addWidget(self.button_new)
        self.horizontalLayout.addWidget(self.groupBox)
        self.groupBox_2 = QtGui.QGroupBox(self.widget_2)
        self.groupBox_2.setTitle(QtGui.QApplication.translate("Dialog", "Select existing item to use", None, QtGui.QApplication.UnicodeUTF8))
        self.groupBox_2.setObjectName(_fromUtf8("groupBox_2"))
        self.verticalLayout_3 = QtGui.QVBoxLayout(self.groupBox_2)
        self.verticalLayout_3.setContentsMargins(0, 8, 0, 0)
        self.verticalLayout_3.setObjectName(_fromUtf8("verticalLayout_3"))
        self.combobox_select = QtGui.QComboBox(self.groupBox_2)
        self.combobox_select.setObjectName(_fromUtf8("combobox_select"))
        self.verticalLayout_3.addWidget(self.combobox_select)
        self.button_select = QtGui.QPushButton(self.groupBox_2)
        self.button_select.setText(QtGui.QApplication.translate("Dialog", "Select", None, QtGui.QApplication.UnicodeUTF8))
        icon1 = QtGui.QIcon()
        icon1.addPixmap(QtGui.QPixmap(_fromUtf8(":/icons/apply.png")), QtGui.QIcon.Normal, QtGui.QIcon.Off)
        self.button_select.setIcon(icon1)
        self.button_select.setIconSize(QtCore.QSize(16, 16))
        self.button_select.setObjectName(_fromUtf8("button_select"))
        self.verticalLayout_3.addWidget(self.button_select)
        self.horizontalLayout.addWidget(self.groupBox_2)
        self.verticalLayout.addWidget(self.widget_2)
        self.widget = QtGui.QWidget(Dialog)
        self.widget.setObjectName(_fromUtf8("widget"))
        self.horizontalLayout_2 = QtGui.QHBoxLayout(self.widget)
        self.horizontalLayout_2.setMargin(0)
        self.horizontalLayout_2.setMargin(0)
        self.horizontalLayout_2.setObjectName(_fromUtf8("horizontalLayout_2"))
        spacerItem1 = QtGui.QSpacerItem(40, 20, QtGui.QSizePolicy.Expanding, QtGui.QSizePolicy.Minimum)
        self.horizontalLayout_2.addItem(spacerItem1)
        self.button_cancel = QtGui.QPushButton(self.widget)
        self.button_cancel.setText(QtGui.QApplication.translate("Dialog", "Cancel", None, QtGui.QApplication.UnicodeUTF8))
        icon2 = QtGui.QIcon()
        icon2.addPixmap(QtGui.QPixmap(_fromUtf8(":/icons/delete.png")), QtGui.QIcon.Normal, QtGui.QIcon.Off)
        self.button_cancel.setIcon(icon2)
        self.button_cancel.setIconSize(QtCore.QSize(16, 16))
        self.button_cancel.setObjectName(_fromUtf8("button_cancel"))
        self.horizontalLayout_2.addWidget(self.button_cancel)
        self.verticalLayout.addWidget(self.widget)

        self.retranslateUi(Dialog)
        QtCore.QObject.connect(self.button_cancel, QtCore.SIGNAL(_fromUtf8("clicked()")), Dialog.accept)
        QtCore.QMetaObject.connectSlotsByName(Dialog)

    def retranslateUi(self, Dialog):
        pass

import icons_rc

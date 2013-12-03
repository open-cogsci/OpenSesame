# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file 'resources/ui/font_widget.ui'
#
# Created: Fri Nov 29 16:39:02 2013
#      by: PyQt4 UI code generator 4.10.3
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

class Ui_font_widget(object):
    def setupUi(self, font_widget):
        font_widget.setObjectName(_fromUtf8("font_widget"))
        font_widget.resize(265, 171)
        self.gridLayout = QtGui.QGridLayout(font_widget)
        self.gridLayout.setMargin(0)
        self.gridLayout.setSpacing(4)
        self.gridLayout.setObjectName(_fromUtf8("gridLayout"))
        self.label = QtGui.QLabel(font_widget)
        self.label.setObjectName(_fromUtf8("label"))
        self.gridLayout.addWidget(self.label, 0, 0, 1, 1)
        self.combobox_family = QtGui.QComboBox(font_widget)
        self.combobox_family.setObjectName(_fromUtf8("combobox_family"))
        self.combobox_family.addItem(_fromUtf8(""))
        self.combobox_family.addItem(_fromUtf8(""))
        self.combobox_family.addItem(_fromUtf8(""))
        self.combobox_family.addItem(_fromUtf8(""))
        self.combobox_family.addItem(_fromUtf8(""))
        self.combobox_family.addItem(_fromUtf8(""))
        self.combobox_family.addItem(_fromUtf8(""))
        self.combobox_family.addItem(_fromUtf8(""))
        self.gridLayout.addWidget(self.combobox_family, 0, 1, 1, 1)
        self.label_2 = QtGui.QLabel(font_widget)
        self.label_2.setObjectName(_fromUtf8("label_2"))
        self.gridLayout.addWidget(self.label_2, 1, 0, 1, 1)
        self.spinbox_size = QtGui.QSpinBox(font_widget)
        self.spinbox_size.setMinimum(1)
        self.spinbox_size.setMaximum(1024)
        self.spinbox_size.setObjectName(_fromUtf8("spinbox_size"))
        self.gridLayout.addWidget(self.spinbox_size, 1, 1, 1, 1)
        self.checkbox_italic = QtGui.QCheckBox(font_widget)
        font = QtGui.QFont()
        font.setItalic(True)
        self.checkbox_italic.setFont(font)
        self.checkbox_italic.setObjectName(_fromUtf8("checkbox_italic"))
        self.gridLayout.addWidget(self.checkbox_italic, 2, 0, 1, 1)
        self.checkbox_bold = QtGui.QCheckBox(font_widget)
        font = QtGui.QFont()
        font.setBold(True)
        font.setWeight(75)
        self.checkbox_bold.setFont(font)
        self.checkbox_bold.setObjectName(_fromUtf8("checkbox_bold"))
        self.gridLayout.addWidget(self.checkbox_bold, 3, 0, 1, 1)
        self.frame = QtGui.QFrame(font_widget)
        self.frame.setFrameShape(QtGui.QFrame.StyledPanel)
        self.frame.setFrameShadow(QtGui.QFrame.Raised)
        self.frame.setObjectName(_fromUtf8("frame"))
        self.horizontalLayout = QtGui.QHBoxLayout(self.frame)
        self.horizontalLayout.setMargin(4)
        self.horizontalLayout.setObjectName(_fromUtf8("horizontalLayout"))
        self.label_example = QtGui.QLabel(self.frame)
        self.label_example.setAlignment(QtCore.Qt.AlignCenter)
        self.label_example.setObjectName(_fromUtf8("label_example"))
        self.horizontalLayout.addWidget(self.label_example)
        self.gridLayout.addWidget(self.frame, 2, 1, 2, 1)

        self.retranslateUi(font_widget)
        QtCore.QMetaObject.connectSlotsByName(font_widget)

    def retranslateUi(self, font_widget):
        font_widget.setWindowTitle(_translate("font_widget", "Form", None))
        self.label.setText(_translate("font_widget", "Font family", None))
        self.combobox_family.setItemText(0, _translate("font_widget", "mono", None))
        self.combobox_family.setItemText(1, _translate("font_widget", "sans", None))
        self.combobox_family.setItemText(2, _translate("font_widget", "serif", None))
        self.combobox_family.setItemText(3, _translate("font_widget", "arabic", None))
        self.combobox_family.setItemText(4, _translate("font_widget", "chinese-japanese-korean", None))
        self.combobox_family.setItemText(5, _translate("font_widget", "hebrew", None))
        self.combobox_family.setItemText(6, _translate("font_widget", "hindi", None))
        self.combobox_family.setItemText(7, _translate("font_widget", "other ...", None))
        self.label_2.setText(_translate("font_widget", "Font size", None))
        self.spinbox_size.setSuffix(_translate("font_widget", " pt", None))
        self.checkbox_italic.setText(_translate("font_widget", "Italic", None))
        self.checkbox_bold.setText(_translate("font_widget", "Bold", None))
        self.label_example.setText(_translate("font_widget", "Example", None))


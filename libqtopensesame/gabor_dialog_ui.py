# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file 'resources/gabor_dialog.ui'
#
# Created: Wed Jun 15 14:15:00 2011
#      by: PyQt4 UI code generator 4.8.3
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
        Dialog.resize(450, 479)
        self.verticalLayout = QtGui.QVBoxLayout(Dialog)
        self.verticalLayout.setObjectName(_fromUtf8("verticalLayout"))
        self.widget_2 = QtGui.QWidget(Dialog)
        sizePolicy = QtGui.QSizePolicy(QtGui.QSizePolicy.Preferred, QtGui.QSizePolicy.Fixed)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.widget_2.sizePolicy().hasHeightForWidth())
        self.widget_2.setSizePolicy(sizePolicy)
        self.widget_2.setStyleSheet(_fromUtf8("background-color: #4e9a06;\n"
"color: rgb(255, 255, 255);"))
        self.widget_2.setObjectName(_fromUtf8("widget_2"))
        self.horizontalLayout = QtGui.QHBoxLayout(self.widget_2)
        self.horizontalLayout.setMargin(5)
        self.horizontalLayout.setMargin(0)
        self.horizontalLayout.setObjectName(_fromUtf8("horizontalLayout"))
        self.label = QtGui.QLabel(self.widget_2)
        sizePolicy = QtGui.QSizePolicy(QtGui.QSizePolicy.Fixed, QtGui.QSizePolicy.Preferred)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.label.sizePolicy().hasHeightForWidth())
        self.label.setSizePolicy(sizePolicy)
        self.label.setText(_fromUtf8(""))
        self.label.setPixmap(QtGui.QPixmap(_fromUtf8(":/icons/gabor.png")))
        self.label.setObjectName(_fromUtf8("label"))
        self.horizontalLayout.addWidget(self.label)
        self.label_2 = QtGui.QLabel(self.widget_2)
        font = QtGui.QFont()
        font.setPointSize(11)
        font.setWeight(75)
        font.setBold(True)
        self.label_2.setFont(font)
        self.label_2.setObjectName(_fromUtf8("label_2"))
        self.horizontalLayout.addWidget(self.label_2)
        self.verticalLayout.addWidget(self.widget_2)
        self.widget = QtGui.QWidget(Dialog)
        font = QtGui.QFont()
        font.setPointSize(8)
        self.widget.setFont(font)
        self.widget.setObjectName(_fromUtf8("widget"))
        self.formLayout = QtGui.QFormLayout(self.widget)
        self.formLayout.setMargin(0)
        self.formLayout.setVerticalSpacing(12)
        self.formLayout.setObjectName(_fromUtf8("formLayout"))
        self.label_3 = QtGui.QLabel(self.widget)
        self.label_3.setObjectName(_fromUtf8("label_3"))
        self.formLayout.setWidget(0, QtGui.QFormLayout.LabelRole, self.label_3)
        self.spin_orient = QtGui.QDoubleSpinBox(self.widget)
        self.spin_orient.setMaximum(360.0)
        self.spin_orient.setObjectName(_fromUtf8("spin_orient"))
        self.formLayout.setWidget(0, QtGui.QFormLayout.FieldRole, self.spin_orient)
        self.label_4 = QtGui.QLabel(self.widget)
        self.label_4.setObjectName(_fromUtf8("label_4"))
        self.formLayout.setWidget(1, QtGui.QFormLayout.LabelRole, self.label_4)
        self.spin_size = QtGui.QSpinBox(self.widget)
        self.spin_size.setMinimum(1)
        self.spin_size.setMaximum(1000)
        self.spin_size.setProperty(_fromUtf8("value"), 96)
        self.spin_size.setObjectName(_fromUtf8("spin_size"))
        self.formLayout.setWidget(1, QtGui.QFormLayout.FieldRole, self.spin_size)
        self.label_5 = QtGui.QLabel(self.widget)
        self.label_5.setObjectName(_fromUtf8("label_5"))
        self.formLayout.setWidget(2, QtGui.QFormLayout.LabelRole, self.label_5)
        self.combobox_env = QtGui.QComboBox(self.widget)
        self.combobox_env.setObjectName(_fromUtf8("combobox_env"))
        self.combobox_env.addItem(_fromUtf8(""))
        self.combobox_env.addItem(_fromUtf8(""))
        self.combobox_env.addItem(_fromUtf8(""))
        self.combobox_env.addItem(_fromUtf8(""))
        self.formLayout.setWidget(2, QtGui.QFormLayout.FieldRole, self.combobox_env)
        self.label_6 = QtGui.QLabel(self.widget)
        self.label_6.setObjectName(_fromUtf8("label_6"))
        self.formLayout.setWidget(3, QtGui.QFormLayout.LabelRole, self.label_6)
        self.spin_stdev = QtGui.QDoubleSpinBox(self.widget)
        self.spin_stdev.setMaximum(1000.0)
        self.spin_stdev.setProperty(_fromUtf8("value"), 12.0)
        self.spin_stdev.setObjectName(_fromUtf8("spin_stdev"))
        self.formLayout.setWidget(3, QtGui.QFormLayout.FieldRole, self.spin_stdev)
        self.label_7 = QtGui.QLabel(self.widget)
        self.label_7.setObjectName(_fromUtf8("label_7"))
        self.formLayout.setWidget(4, QtGui.QFormLayout.LabelRole, self.label_7)
        self.spin_freq = QtGui.QDoubleSpinBox(self.widget)
        self.spin_freq.setSuffix(_fromUtf8(""))
        self.spin_freq.setMaximum(1000.0)
        self.spin_freq.setProperty(_fromUtf8("value"), 0.1)
        self.spin_freq.setObjectName(_fromUtf8("spin_freq"))
        self.formLayout.setWidget(4, QtGui.QFormLayout.FieldRole, self.spin_freq)
        self.label_8 = QtGui.QLabel(self.widget)
        self.label_8.setObjectName(_fromUtf8("label_8"))
        self.formLayout.setWidget(5, QtGui.QFormLayout.LabelRole, self.label_8)
        self.spin_phase = QtGui.QDoubleSpinBox(self.widget)
        self.spin_phase.setMaximum(1.0)
        self.spin_phase.setSingleStep(0.1)
        self.spin_phase.setObjectName(_fromUtf8("spin_phase"))
        self.formLayout.setWidget(5, QtGui.QFormLayout.FieldRole, self.spin_phase)
        self.label_10 = QtGui.QLabel(self.widget)
        self.label_10.setObjectName(_fromUtf8("label_10"))
        self.formLayout.setWidget(6, QtGui.QFormLayout.LabelRole, self.label_10)
        self.edit_color1 = QtGui.QLineEdit(self.widget)
        self.edit_color1.setObjectName(_fromUtf8("edit_color1"))
        self.formLayout.setWidget(6, QtGui.QFormLayout.FieldRole, self.edit_color1)
        self.label_9 = QtGui.QLabel(self.widget)
        self.label_9.setObjectName(_fromUtf8("label_9"))
        self.formLayout.setWidget(7, QtGui.QFormLayout.LabelRole, self.label_9)
        self.edit_color2 = QtGui.QLineEdit(self.widget)
        self.edit_color2.setObjectName(_fromUtf8("edit_color2"))
        self.formLayout.setWidget(7, QtGui.QFormLayout.FieldRole, self.edit_color2)
        self.label_11 = QtGui.QLabel(self.widget)
        self.label_11.setObjectName(_fromUtf8("label_11"))
        self.formLayout.setWidget(8, QtGui.QFormLayout.LabelRole, self.label_11)
        self.combobox_bgmode = QtGui.QComboBox(self.widget)
        self.combobox_bgmode.setObjectName(_fromUtf8("combobox_bgmode"))
        self.combobox_bgmode.addItem(_fromUtf8(""))
        self.combobox_bgmode.addItem(_fromUtf8(""))
        self.formLayout.setWidget(8, QtGui.QFormLayout.FieldRole, self.combobox_bgmode)
        self.verticalLayout.addWidget(self.widget)
        self.buttonBox = QtGui.QDialogButtonBox(Dialog)
        self.buttonBox.setOrientation(QtCore.Qt.Horizontal)
        self.buttonBox.setStandardButtons(QtGui.QDialogButtonBox.Cancel|QtGui.QDialogButtonBox.Ok)
        self.buttonBox.setCenterButtons(False)
        self.buttonBox.setObjectName(_fromUtf8("buttonBox"))
        self.verticalLayout.addWidget(self.buttonBox)

        self.retranslateUi(Dialog)
        QtCore.QObject.connect(self.buttonBox, QtCore.SIGNAL(_fromUtf8("accepted()")), Dialog.accept)
        QtCore.QObject.connect(self.buttonBox, QtCore.SIGNAL(_fromUtf8("rejected()")), Dialog.reject)
        QtCore.QMetaObject.connectSlotsByName(Dialog)

    def retranslateUi(self, Dialog):
        Dialog.setWindowTitle(QtGui.QApplication.translate("Dialog", "Dialog", None, QtGui.QApplication.UnicodeUTF8))
        self.label_2.setText(QtGui.QApplication.translate("Dialog", "Insert Gabor patch", None, QtGui.QApplication.UnicodeUTF8))
        self.label_3.setText(QtGui.QApplication.translate("Dialog", "<!DOCTYPE HTML PUBLIC \"-//W3C//DTD HTML 4.0//EN\" \"http://www.w3.org/TR/REC-html40/strict.dtd\">\n"
"<html><head><meta name=\"qrichtext\" content=\"1\" /><style type=\"text/css\">\n"
"p, li { white-space: pre-wrap; }\n"
"</style></head><body style=\" font-family:\'Ubuntu\'; font-size:9pt; font-weight:400; font-style:normal;\">\n"
"<p style=\" margin-top:0px; margin-bottom:0px; margin-left:0px; margin-right:0px; -qt-block-indent:0; text-indent:0px;\">Orientation</p>\n"
"<p style=\" margin-top:0px; margin-bottom:0px; margin-left:0px; margin-right:0px; -qt-block-indent:0; text-indent:0px;\"><span style=\" font-style:italic;\">in degrees (0 .. 360)</span></p></body></html>", None, QtGui.QApplication.UnicodeUTF8))
        self.spin_orient.setSuffix(QtGui.QApplication.translate("Dialog", "deg", None, QtGui.QApplication.UnicodeUTF8))
        self.label_4.setText(QtGui.QApplication.translate("Dialog", "<!DOCTYPE HTML PUBLIC \"-//W3C//DTD HTML 4.0//EN\" \"http://www.w3.org/TR/REC-html40/strict.dtd\">\n"
"<html><head><meta name=\"qrichtext\" content=\"1\" /><style type=\"text/css\">\n"
"p, li { white-space: pre-wrap; }\n"
"</style></head><body style=\" font-family:\'Ubuntu\'; font-size:9pt; font-weight:400; font-style:normal;\">\n"
"<p style=\" margin-top:0px; margin-bottom:0px; margin-left:0px; margin-right:0px; -qt-block-indent:0; text-indent:0px;\">Size</p>\n"
"<p style=\" margin-top:0px; margin-bottom:0px; margin-left:0px; margin-right:0px; -qt-block-indent:0; text-indent:0px;\"><span style=\" font-style:italic;\">in pixels</span></p></body></html>", None, QtGui.QApplication.UnicodeUTF8))
        self.spin_size.setSuffix(QtGui.QApplication.translate("Dialog", "px", None, QtGui.QApplication.UnicodeUTF8))
        self.label_5.setText(QtGui.QApplication.translate("Dialog", "Envelope", None, QtGui.QApplication.UnicodeUTF8))
        self.combobox_env.setItemText(0, QtGui.QApplication.translate("Dialog", "gaussian", None, QtGui.QApplication.UnicodeUTF8))
        self.combobox_env.setItemText(1, QtGui.QApplication.translate("Dialog", "linear", None, QtGui.QApplication.UnicodeUTF8))
        self.combobox_env.setItemText(2, QtGui.QApplication.translate("Dialog", "circular (sharp edge)", None, QtGui.QApplication.UnicodeUTF8))
        self.combobox_env.setItemText(3, QtGui.QApplication.translate("Dialog", "rectangle (no envelope)", None, QtGui.QApplication.UnicodeUTF8))
        self.label_6.setText(QtGui.QApplication.translate("Dialog", "<!DOCTYPE HTML PUBLIC \"-//W3C//DTD HTML 4.0//EN\" \"http://www.w3.org/TR/REC-html40/strict.dtd\">\n"
"<html><head><meta name=\"qrichtext\" content=\"1\" /><style type=\"text/css\">\n"
"p, li { white-space: pre-wrap; }\n"
"</style></head><body style=\" font-family:\'Ubuntu\'; font-size:8pt; font-weight:400; font-style:normal;\">\n"
"<p style=\" margin-top:0px; margin-bottom:0px; margin-left:0px; margin-right:0px; -qt-block-indent:0; text-indent:0px;\"><span style=\" font-size:9pt;\">Standard deviation</span></p>\n"
"<p style=\" margin-top:0px; margin-bottom:0px; margin-left:0px; margin-right:0px; -qt-block-indent:0; text-indent:0px;\"><span style=\" font-size:9pt; font-style:italic;\">in pixels, only applies to the Gaussian envelope</span></p></body></html>", None, QtGui.QApplication.UnicodeUTF8))
        self.spin_stdev.setSuffix(QtGui.QApplication.translate("Dialog", "px", None, QtGui.QApplication.UnicodeUTF8))
        self.label_7.setText(QtGui.QApplication.translate("Dialog", "<!DOCTYPE HTML PUBLIC \"-//W3C//DTD HTML 4.0//EN\" \"http://www.w3.org/TR/REC-html40/strict.dtd\">\n"
"<html><head><meta name=\"qrichtext\" content=\"1\" /><style type=\"text/css\">\n"
"p, li { white-space: pre-wrap; }\n"
"</style></head><body style=\" font-family:\'Ubuntu\'; font-size:9pt; font-weight:400; font-style:normal;\">\n"
"<p style=\" margin-top:0px; margin-bottom:0px; margin-left:0px; margin-right:0px; -qt-block-indent:0; text-indent:0px;\">Frequence</p>\n"
"<p style=\" margin-top:0px; margin-bottom:0px; margin-left:0px; margin-right:0px; -qt-block-indent:0; text-indent:0px;\"><span style=\" font-style:italic;\">in cycles/ pixel</span></p></body></html>", None, QtGui.QApplication.UnicodeUTF8))
        self.label_8.setText(QtGui.QApplication.translate("Dialog", "<!DOCTYPE HTML PUBLIC \"-//W3C//DTD HTML 4.0//EN\" \"http://www.w3.org/TR/REC-html40/strict.dtd\">\n"
"<html><head><meta name=\"qrichtext\" content=\"1\" /><style type=\"text/css\">\n"
"p, li { white-space: pre-wrap; }\n"
"</style></head><body style=\" font-family:\'Ubuntu\'; font-size:9pt; font-weight:400; font-style:normal;\">\n"
"<p style=\" margin-top:0px; margin-bottom:0px; margin-left:0px; margin-right:0px; -qt-block-indent:0; text-indent:0px;\">Phase</p>\n"
"<p style=\" margin-top:0px; margin-bottom:0px; margin-left:0px; margin-right:0px; -qt-block-indent:0; text-indent:0px;\"><span style=\" font-style:italic;\">in cycles (0 .. 1)</span></p></body></html>", None, QtGui.QApplication.UnicodeUTF8))
        self.label_10.setText(QtGui.QApplication.translate("Dialog", "<!DOCTYPE HTML PUBLIC \"-//W3C//DTD HTML 4.0//EN\" \"http://www.w3.org/TR/REC-html40/strict.dtd\">\n"
"<html><head><meta name=\"qrichtext\" content=\"1\" /><style type=\"text/css\">\n"
"p, li { white-space: pre-wrap; }\n"
"</style></head><body style=\" font-family:\'Ubuntu\'; font-size:9pt; font-weight:400; font-style:normal;\">\n"
"<p style=\" margin-top:0px; margin-bottom:0px; margin-left:0px; margin-right:0px; -qt-block-indent:0; text-indent:0px;\">Color 1</p>\n"
"<p style=\" margin-top:0px; margin-bottom:0px; margin-left:0px; margin-right:0px; -qt-block-indent:0; text-indent:0px;\"><span style=\" font-style:italic;\">E.g., \'white\' or \'#FFFFFF\'</span></p></body></html>", None, QtGui.QApplication.UnicodeUTF8))
        self.edit_color1.setText(QtGui.QApplication.translate("Dialog", "white", None, QtGui.QApplication.UnicodeUTF8))
        self.label_9.setText(QtGui.QApplication.translate("Dialog", "<!DOCTYPE HTML PUBLIC \"-//W3C//DTD HTML 4.0//EN\" \"http://www.w3.org/TR/REC-html40/strict.dtd\">\n"
"<html><head><meta name=\"qrichtext\" content=\"1\" /><style type=\"text/css\">\n"
"p, li { white-space: pre-wrap; }\n"
"</style></head><body style=\" font-family:\'Ubuntu\'; font-size:8pt; font-weight:400; font-style:normal;\">\n"
"<p style=\" margin-top:0px; margin-bottom:0px; margin-left:0px; margin-right:0px; -qt-block-indent:0; text-indent:0px;\"><span style=\" font-size:9pt;\">Color 2</span></p>\n"
"<p style=\" margin-top:0px; margin-bottom:0px; margin-left:0px; margin-right:0px; -qt-block-indent:0; text-indent:0px;\"><span style=\" font-size:9pt; font-style:italic;\">E.g., \'black\' or \'#000000\'</span></p></body></html>", None, QtGui.QApplication.UnicodeUTF8))
        self.edit_color2.setText(QtGui.QApplication.translate("Dialog", "black", None, QtGui.QApplication.UnicodeUTF8))
        self.label_11.setText(QtGui.QApplication.translate("Dialog", "Background color", None, QtGui.QApplication.UnicodeUTF8))
        self.combobox_bgmode.setItemText(0, QtGui.QApplication.translate("Dialog", "Color average", None, QtGui.QApplication.UnicodeUTF8))
        self.combobox_bgmode.setItemText(1, QtGui.QApplication.translate("Dialog", "Color 2", None, QtGui.QApplication.UnicodeUTF8))

import icons_rc

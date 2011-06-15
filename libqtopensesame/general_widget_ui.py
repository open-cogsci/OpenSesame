# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file 'resources/general_widget.ui'
#
# Created: Wed Jun 15 14:14:59 2011
#      by: PyQt4 UI code generator 4.8.3
#
# WARNING! All changes made in this file will be lost!

from PyQt4 import QtCore, QtGui

try:
    _fromUtf8 = QtCore.QString.fromUtf8
except AttributeError:
    _fromUtf8 = lambda s: s

class Ui_Form(object):
    def setupUi(self, Form):
        Form.setObjectName(_fromUtf8("Form"))
        Form.resize(775, 580)
        self.verticalLayout = QtGui.QVBoxLayout(Form)
        self.verticalLayout.setMargin(0)
        self.verticalLayout.setObjectName(_fromUtf8("verticalLayout"))
        self.widget = QtGui.QWidget(Form)
        sizePolicy = QtGui.QSizePolicy(QtGui.QSizePolicy.Preferred, QtGui.QSizePolicy.Fixed)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.widget.sizePolicy().hasHeightForWidth())
        self.widget.setSizePolicy(sizePolicy)
        self.widget.setObjectName(_fromUtf8("widget"))
        self.gridLayout = QtGui.QGridLayout(self.widget)
        self.gridLayout.setMargin(0)
        self.gridLayout.setMargin(0)
        self.gridLayout.setObjectName(_fromUtf8("gridLayout"))
        self.label = QtGui.QLabel(self.widget)
        self.label.setObjectName(_fromUtf8("label"))
        self.gridLayout.addWidget(self.label, 0, 0, 1, 1)
        self.combobox_start = QtGui.QComboBox(self.widget)
        self.combobox_start.setObjectName(_fromUtf8("combobox_start"))
        self.gridLayout.addWidget(self.combobox_start, 0, 1, 1, 5)
        self.label_2 = QtGui.QLabel(self.widget)
        self.label_2.setObjectName(_fromUtf8("label_2"))
        self.gridLayout.addWidget(self.label_2, 2, 0, 1, 1)
        self.spinbox_width = QtGui.QSpinBox(self.widget)
        self.spinbox_width.setMinimum(1)
        self.spinbox_width.setMaximum(10000)
        self.spinbox_width.setObjectName(_fromUtf8("spinbox_width"))
        self.gridLayout.addWidget(self.spinbox_width, 2, 1, 1, 1)
        self.spinbox_height = QtGui.QSpinBox(self.widget)
        self.spinbox_height.setMinimum(1)
        self.spinbox_height.setMaximum(10000)
        self.spinbox_height.setObjectName(_fromUtf8("spinbox_height"))
        self.gridLayout.addWidget(self.spinbox_height, 2, 3, 1, 1)
        self.label_3 = QtGui.QLabel(self.widget)
        sizePolicy = QtGui.QSizePolicy(QtGui.QSizePolicy.Fixed, QtGui.QSizePolicy.Preferred)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.label_3.sizePolicy().hasHeightForWidth())
        self.label_3.setSizePolicy(sizePolicy)
        self.label_3.setObjectName(_fromUtf8("label_3"))
        self.gridLayout.addWidget(self.label_3, 2, 2, 1, 1)
        self.label_6 = QtGui.QLabel(self.widget)
        self.label_6.setObjectName(_fromUtf8("label_6"))
        self.gridLayout.addWidget(self.label_6, 3, 0, 1, 1)
        self.spinbox_compensation = QtGui.QSpinBox(self.widget)
        self.spinbox_compensation.setMinimum(-100)
        self.spinbox_compensation.setMaximum(100)
        self.spinbox_compensation.setObjectName(_fromUtf8("spinbox_compensation"))
        self.gridLayout.addWidget(self.spinbox_compensation, 3, 1, 1, 3)
        self.label_5 = QtGui.QLabel(self.widget)
        self.label_5.setObjectName(_fromUtf8("label_5"))
        self.gridLayout.addWidget(self.label_5, 3, 4, 1, 1)
        self.edit_background = QtGui.QLineEdit(self.widget)
        sizePolicy = QtGui.QSizePolicy(QtGui.QSizePolicy.Preferred, QtGui.QSizePolicy.Fixed)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.edit_background.sizePolicy().hasHeightForWidth())
        self.edit_background.setSizePolicy(sizePolicy)
        self.edit_background.setObjectName(_fromUtf8("edit_background"))
        self.gridLayout.addWidget(self.edit_background, 3, 5, 1, 1)
        self.edit_foreground = QtGui.QLineEdit(self.widget)
        sizePolicy = QtGui.QSizePolicy(QtGui.QSizePolicy.Preferred, QtGui.QSizePolicy.Fixed)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.edit_foreground.sizePolicy().hasHeightForWidth())
        self.edit_foreground.setSizePolicy(sizePolicy)
        self.edit_foreground.setObjectName(_fromUtf8("edit_foreground"))
        self.gridLayout.addWidget(self.edit_foreground, 2, 5, 1, 1)
        self.label_4 = QtGui.QLabel(self.widget)
        self.label_4.setObjectName(_fromUtf8("label_4"))
        self.gridLayout.addWidget(self.label_4, 2, 4, 1, 1)
        self.label_8 = QtGui.QLabel(self.widget)
        self.label_8.setObjectName(_fromUtf8("label_8"))
        self.gridLayout.addWidget(self.label_8, 1, 0, 1, 1)
        self.combobox_backend = QtGui.QComboBox(self.widget)
        self.combobox_backend.setObjectName(_fromUtf8("combobox_backend"))
        self.gridLayout.addWidget(self.combobox_backend, 1, 1, 1, 5)
        self.verticalLayout.addWidget(self.widget)
        self.checkbox_show_script = QtGui.QCheckBox(Form)
        self.checkbox_show_script.setObjectName(_fromUtf8("checkbox_show_script"))
        self.verticalLayout.addWidget(self.checkbox_show_script)
        self.spacer = QtGui.QWidget(Form)
        sizePolicy = QtGui.QSizePolicy(QtGui.QSizePolicy.Preferred, QtGui.QSizePolicy.Expanding)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.spacer.sizePolicy().hasHeightForWidth())
        self.spacer.setSizePolicy(sizePolicy)
        self.spacer.setObjectName(_fromUtf8("spacer"))
        self.verticalLayout_2 = QtGui.QVBoxLayout(self.spacer)
        self.verticalLayout_2.setMargin(0)
        self.verticalLayout_2.setMargin(0)
        self.verticalLayout_2.setObjectName(_fromUtf8("verticalLayout_2"))
        self.label_7 = QtGui.QLabel(self.spacer)
        self.label_7.setText(_fromUtf8(""))
        self.label_7.setPixmap(QtGui.QPixmap(_fromUtf8(":/icons/opensesame_l.png")))
        self.label_7.setAlignment(QtCore.Qt.AlignBottom|QtCore.Qt.AlignRight|QtCore.Qt.AlignTrailing)
        self.label_7.setObjectName(_fromUtf8("label_7"))
        self.verticalLayout_2.addWidget(self.label_7)
        self.label_opensesame = QtGui.QLabel(self.spacer)
        sizePolicy = QtGui.QSizePolicy(QtGui.QSizePolicy.Preferred, QtGui.QSizePolicy.Fixed)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.label_opensesame.sizePolicy().hasHeightForWidth())
        self.label_opensesame.setSizePolicy(sizePolicy)
        self.label_opensesame.setAlignment(QtCore.Qt.AlignBottom|QtCore.Qt.AlignRight|QtCore.Qt.AlignTrailing)
        self.label_opensesame.setObjectName(_fromUtf8("label_opensesame"))
        self.verticalLayout_2.addWidget(self.label_opensesame)
        self.verticalLayout.addWidget(self.spacer)

        self.retranslateUi(Form)
        QtCore.QMetaObject.connectSlotsByName(Form)

    def retranslateUi(self, Form):
        Form.setWindowTitle(QtGui.QApplication.translate("Form", "Form", None, QtGui.QApplication.UnicodeUTF8))
        self.label.setText(QtGui.QApplication.translate("Form", "<!DOCTYPE HTML PUBLIC \"-//W3C//DTD HTML 4.0//EN\" \"http://www.w3.org/TR/REC-html40/strict.dtd\">\n"
"<html><head><meta name=\"qrichtext\" content=\"1\" /><style type=\"text/css\">\n"
"p, li { white-space: pre-wrap; }\n"
"</style></head><body style=\" font-family:\'Ubuntu\'; font-size:9pt; font-weight:400; font-style:normal;\">\n"
"<p style=\" margin-top:0px; margin-bottom:0px; margin-left:0px; margin-right:0px; -qt-block-indent:0; text-indent:0px;\">Entry point</p>\n"
"<p style=\" margin-top:0px; margin-bottom:0px; margin-left:0px; margin-right:0px; -qt-block-indent:0; text-indent:0px;\"><span style=\" font-size:8pt; font-style:italic;\">first item to run</span></p></body></html>", None, QtGui.QApplication.UnicodeUTF8))
        self.combobox_start.setToolTip(QtGui.QApplication.translate("Form", "This is item (typically a sequence) is the starting point for your experiment.", None, QtGui.QApplication.UnicodeUTF8))
        self.label_2.setText(QtGui.QApplication.translate("Form", "<!DOCTYPE HTML PUBLIC \"-//W3C//DTD HTML 4.0//EN\" \"http://www.w3.org/TR/REC-html40/strict.dtd\">\n"
"<html><head><meta name=\"qrichtext\" content=\"1\" /><style type=\"text/css\">\n"
"p, li { white-space: pre-wrap; }\n"
"</style></head><body style=\" font-family:\'Ubuntu\'; font-size:9pt; font-weight:400; font-style:normal;\">\n"
"<p style=\" margin-top:0px; margin-bottom:0px; margin-left:0px; margin-right:0px; -qt-block-indent:0; text-indent:0px;\">Display resolution</p>\n"
"<p style=\" margin-top:0px; margin-bottom:0px; margin-left:0px; margin-right:0px; -qt-block-indent:0; text-indent:0px;\"><span style=\" font-size:8pt; font-style:italic;\">in pixels (width x height)</span></p></body></html>", None, QtGui.QApplication.UnicodeUTF8))
        self.spinbox_width.setToolTip(QtGui.QApplication.translate("Form", "The display resolution (width) in pixels", None, QtGui.QApplication.UnicodeUTF8))
        self.spinbox_width.setSuffix(QtGui.QApplication.translate("Form", "px", None, QtGui.QApplication.UnicodeUTF8))
        self.spinbox_height.setToolTip(QtGui.QApplication.translate("Form", "The display resolution (height) in pixels", None, QtGui.QApplication.UnicodeUTF8))
        self.spinbox_height.setSuffix(QtGui.QApplication.translate("Form", "px", None, QtGui.QApplication.UnicodeUTF8))
        self.label_3.setText(QtGui.QApplication.translate("Form", "x", None, QtGui.QApplication.UnicodeUTF8))
        self.label_6.setText(QtGui.QApplication.translate("Form", "<!DOCTYPE HTML PUBLIC \"-//W3C//DTD HTML 4.0//EN\" \"http://www.w3.org/TR/REC-html40/strict.dtd\">\n"
"<html><head><meta name=\"qrichtext\" content=\"1\" /><style type=\"text/css\">\n"
"p, li { white-space: pre-wrap; }\n"
"</style></head><body style=\" font-family:\'Ubuntu\'; font-size:9pt; font-weight:400; font-style:normal;\">\n"
"<p style=\" margin-top:0px; margin-bottom:0px; margin-left:0px; margin-right:0px; -qt-block-indent:0; text-indent:0px;\">Timing compensation</p>\n"
"<p style=\" margin-top:0px; margin-bottom:0px; margin-left:0px; margin-right:0px; -qt-block-indent:0; text-indent:0px;\"><span style=\" font-size:8pt; font-style:italic;\">in milliseconds</span></p></body></html>", None, QtGui.QApplication.UnicodeUTF8))
        self.spinbox_compensation.setToolTip(QtGui.QApplication.translate("Form", "Automatic timing compensation. Positive values will decrease durations, negative values will increase durations (of sketchpads etc.)", None, QtGui.QApplication.UnicodeUTF8))
        self.spinbox_compensation.setSuffix(QtGui.QApplication.translate("Form", "ms", None, QtGui.QApplication.UnicodeUTF8))
        self.label_5.setText(QtGui.QApplication.translate("Form", "<!DOCTYPE HTML PUBLIC \"-//W3C//DTD HTML 4.0//EN\" \"http://www.w3.org/TR/REC-html40/strict.dtd\">\n"
"<html><head><meta name=\"qrichtext\" content=\"1\" /><style type=\"text/css\">\n"
"p, li { white-space: pre-wrap; }\n"
"</style></head><body style=\" font-family:\'Ubuntu\'; font-size:9pt; font-weight:400; font-style:normal;\">\n"
"<p style=\" margin-top:0px; margin-bottom:0px; margin-left:0px; margin-right:0px; -qt-block-indent:0; text-indent:0px;\">Background color</p>\n"
"<p style=\" margin-top:0px; margin-bottom:0px; margin-left:0px; margin-right:0px; -qt-block-indent:0; text-indent:0px;\"><span style=\" font-size:8pt; font-style:italic;\">E.g., &quot;black&quot; or &quot;#000000&quot;</span></p></body></html>", None, QtGui.QApplication.UnicodeUTF8))
        self.edit_background.setToolTip(QtGui.QApplication.translate("Form", "Default background color", None, QtGui.QApplication.UnicodeUTF8))
        self.edit_foreground.setToolTip(QtGui.QApplication.translate("Form", "Default foreground color", None, QtGui.QApplication.UnicodeUTF8))
        self.label_4.setText(QtGui.QApplication.translate("Form", "<!DOCTYPE HTML PUBLIC \"-//W3C//DTD HTML 4.0//EN\" \"http://www.w3.org/TR/REC-html40/strict.dtd\">\n"
"<html><head><meta name=\"qrichtext\" content=\"1\" /><style type=\"text/css\">\n"
"p, li { white-space: pre-wrap; }\n"
"</style></head><body style=\" font-family:\'Ubuntu\'; font-size:9pt; font-weight:400; font-style:normal;\">\n"
"<p style=\" margin-top:0px; margin-bottom:0px; margin-left:0px; margin-right:0px; -qt-block-indent:0; text-indent:0px;\">Foreground color</p>\n"
"<p style=\" margin-top:0px; margin-bottom:0px; margin-left:0px; margin-right:0px; -qt-block-indent:0; text-indent:0px;\"><span style=\" font-size:8pt; font-style:italic;\">E.g., &quot;white&quot; or &quot;#FFFFFF&quot;</span></p></body></html>", None, QtGui.QApplication.UnicodeUTF8))
        self.label_8.setText(QtGui.QApplication.translate("Form", "<!DOCTYPE HTML PUBLIC \"-//W3C//DTD HTML 4.0//EN\" \"http://www.w3.org/TR/REC-html40/strict.dtd\">\n"
"<html><head><meta name=\"qrichtext\" content=\"1\" /><style type=\"text/css\">\n"
"p, li { white-space: pre-wrap; }\n"
"</style></head><body style=\" font-family:\'Ubuntu\'; font-size:9pt; font-weight:400; font-style:normal;\">\n"
"<p style=\" margin-top:0px; margin-bottom:0px; margin-left:0px; margin-right:0px; -qt-block-indent:0; text-indent:0px;\">Back-end</p>\n"
"<p style=\" margin-top:0px; margin-bottom:0px; margin-left:0px; margin-right:0px; -qt-block-indent:0; text-indent:0px;\"><span style=\" font-size:8pt; font-style:italic;\">The layer controlling display, sound and input</span></p></body></html>", None, QtGui.QApplication.UnicodeUTF8))
        self.checkbox_show_script.setToolTip(QtGui.QApplication.translate("Form", "Toggle the visibility of the script editor", None, QtGui.QApplication.UnicodeUTF8))
        self.checkbox_show_script.setText(QtGui.QApplication.translate("Form", "Show script editor", None, QtGui.QApplication.UnicodeUTF8))
        self.label_opensesame.setText(QtGui.QApplication.translate("Form", "<!DOCTYPE HTML PUBLIC \"-//W3C//DTD HTML 4.0//EN\" \"http://www.w3.org/TR/REC-html40/strict.dtd\">\n"
"<html><head><meta name=\"qrichtext\" content=\"1\" /><style type=\"text/css\">\n"
"p, li { white-space: pre-wrap; }\n"
"</style></head><body style=\" font-family:\'Ubuntu\'; font-size:9pt; font-weight:400; font-style:normal;\">\n"
"<p align=\"right\" style=\" margin-top:0px; margin-bottom:0px; margin-left:0px; margin-right:0px; -qt-block-indent:0; text-indent:0px;\"><span style=\" font-size:11pt; font-weight:600;\">OpenSesame [version]</span></p>\n"
"<p align=\"right\" style=\" margin-top:0px; margin-bottom:0px; margin-left:0px; margin-right:0px; -qt-block-indent:0; text-indent:0px;\"><span style=\" font-weight:600; font-style:italic;\">[codename]</span></p>\n"
"<p align=\"right\" style=\" margin-top:0px; margin-bottom:0px; margin-left:0px; margin-right:0px; -qt-block-indent:0; text-indent:0px;\">Copyright Sebastiaan Mathôt (2010-2011)</p>\n"
"<p align=\"right\" style=\" margin-top:0px; margin-bottom:0px; margin-left:0px; margin-right:0px; -qt-block-indent:0; text-indent:0px;\"><a href=\"http://www.cogsci.nl/opensesame\"><span style=\" text-decoration: underline; color:#0000ff;\">http://www.cogsci.nl/opensesame</span></a></p></body></html>", None, QtGui.QApplication.UnicodeUTF8))

import icons_rc

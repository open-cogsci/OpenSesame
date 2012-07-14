# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file 'resources/ui/general_script_editor.ui'
#
# Created: Sat Jul 14 17:34:50 2012
#      by: PyQt4 UI code generator 4.9.1
#
# WARNING! All changes made in this file will be lost!

from PyQt4 import QtCore, QtGui

try:
    _fromUtf8 = QtCore.QString.fromUtf8
except AttributeError:
    _fromUtf8 = lambda s: s

class Ui_widget_general_script_editor(object):
    def setupUi(self, widget_general_script_editor):
        widget_general_script_editor.setObjectName(_fromUtf8("widget_general_script_editor"))
        widget_general_script_editor.resize(400, 300)
        self.layout_vbox = QtGui.QVBoxLayout(widget_general_script_editor)
        self.layout_vbox.setMargin(4)
        self.layout_vbox.setObjectName(_fromUtf8("layout_vbox"))
        self.widget = QtGui.QWidget(widget_general_script_editor)
        sizePolicy = QtGui.QSizePolicy(QtGui.QSizePolicy.Preferred, QtGui.QSizePolicy.Fixed)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.widget.sizePolicy().hasHeightForWidth())
        self.widget.setSizePolicy(sizePolicy)
        self.widget.setObjectName(_fromUtf8("widget"))
        self.horizontalLayout = QtGui.QHBoxLayout(self.widget)
        self.horizontalLayout.setSpacing(16)
        self.horizontalLayout.setMargin(4)
        self.horizontalLayout.setMargin(0)
        self.horizontalLayout.setObjectName(_fromUtf8("horizontalLayout"))
        self.label_warning_icon = QtGui.QLabel(self.widget)
        sizePolicy = QtGui.QSizePolicy(QtGui.QSizePolicy.Fixed, QtGui.QSizePolicy.Fixed)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.label_warning_icon.sizePolicy().hasHeightForWidth())
        self.label_warning_icon.setSizePolicy(sizePolicy)
        self.label_warning_icon.setObjectName(_fromUtf8("label_warning_icon"))
        self.horizontalLayout.addWidget(self.label_warning_icon)
        self.label = QtGui.QLabel(self.widget)
        sizePolicy = QtGui.QSizePolicy(QtGui.QSizePolicy.Preferred, QtGui.QSizePolicy.Fixed)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.label.sizePolicy().hasHeightForWidth())
        self.label.setSizePolicy(sizePolicy)
        self.label.setWordWrap(True)
        self.label.setObjectName(_fromUtf8("label"))
        self.horizontalLayout.addWidget(self.label)
        self.layout_vbox.addWidget(self.widget)

        self.retranslateUi(widget_general_script_editor)
        QtCore.QMetaObject.connectSlotsByName(widget_general_script_editor)

    def retranslateUi(self, widget_general_script_editor):
        widget_general_script_editor.setWindowTitle(QtGui.QApplication.translate("widget_general_script_editor", "Form", None, QtGui.QApplication.UnicodeUTF8))
        self.label_warning_icon.setText(QtGui.QApplication.translate("widget_general_script_editor", "ICON", None, QtGui.QApplication.UnicodeUTF8))
        self.label.setText(QtGui.QApplication.translate("widget_general_script_editor", "<b>General script editor</b><br />\n"
"Edit your experiment in script form", None, QtGui.QApplication.UnicodeUTF8))


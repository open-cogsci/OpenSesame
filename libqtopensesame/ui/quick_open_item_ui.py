# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file 'resources/ui/quick_open_item.ui'
#
# Created: Fri Jul  4 14:44:35 2014
#      by: PyQt4 UI code generator 4.10.4
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

class Ui_quick_open_item(object):
    def setupUi(self, quick_open_item):
        quick_open_item.setObjectName(_fromUtf8("quick_open_item"))
        quick_open_item.setWindowModality(QtCore.Qt.ApplicationModal)
        quick_open_item.resize(308, 216)
        icon = QtGui.QIcon.fromTheme(_fromUtf8("forward"))
        quick_open_item.setWindowIcon(icon)
        self.verticalLayout = QtGui.QVBoxLayout(quick_open_item)
        self.verticalLayout.setSpacing(2)
        self.verticalLayout.setMargin(2)
        self.verticalLayout.setObjectName(_fromUtf8("verticalLayout"))
        self.filter_line_edit = QtGui.QLineEdit(quick_open_item)
        self.filter_line_edit.setObjectName(_fromUtf8("filter_line_edit"))
        self.verticalLayout.addWidget(self.filter_line_edit)
        self.items_list_widget = QtGui.QListWidget(quick_open_item)
        self.items_list_widget.setObjectName(_fromUtf8("items_list_widget"))
        self.verticalLayout.addWidget(self.items_list_widget)

        self.retranslateUi(quick_open_item)
        QtCore.QMetaObject.connectSlotsByName(quick_open_item)

    def retranslateUi(self, quick_open_item):
        quick_open_item.setWindowTitle(_translate("quick_open_item", "Quick open item", None))
        self.filter_line_edit.setPlaceholderText(_translate("quick_open_item", "Search by item name or type", None))


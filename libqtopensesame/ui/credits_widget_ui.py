# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file 'resources/ui/credits_widget.ui'
#
# Created: Tue Feb  5 15:54:19 2013
#      by: PyQt4 UI code generator 4.9.1
#
# WARNING! All changes made in this file will be lost!

from PyQt4 import QtCore, QtGui

try:
    _fromUtf8 = QtCore.QString.fromUtf8
except AttributeError:
    _fromUtf8 = lambda s: s

class Ui_widget_credits(object):
    def setupUi(self, widget_credits):
        widget_credits.setObjectName(_fromUtf8("widget_credits"))
        widget_credits.resize(868, 55)
        sizePolicy = QtGui.QSizePolicy(QtGui.QSizePolicy.Preferred, QtGui.QSizePolicy.MinimumExpanding)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(widget_credits.sizePolicy().hasHeightForWidth())
        widget_credits.setSizePolicy(sizePolicy)
        self.verticalLayout = QtGui.QVBoxLayout(widget_credits)
        self.verticalLayout.setMargin(0)
        self.verticalLayout.setObjectName(_fromUtf8("verticalLayout"))
        spacerItem = QtGui.QSpacerItem(20, 2, QtGui.QSizePolicy.Minimum, QtGui.QSizePolicy.Expanding)
        self.verticalLayout.addItem(spacerItem)
        self.widget_container = QtGui.QWidget(widget_credits)
        sizePolicy = QtGui.QSizePolicy(QtGui.QSizePolicy.Preferred, QtGui.QSizePolicy.Fixed)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.widget_container.sizePolicy().hasHeightForWidth())
        self.widget_container.setSizePolicy(sizePolicy)
        self.widget_container.setObjectName(_fromUtf8("widget_container"))
        self.horizontalLayout = QtGui.QHBoxLayout(self.widget_container)
        self.horizontalLayout.setSpacing(0)
        self.horizontalLayout.setMargin(0)
        self.horizontalLayout.setMargin(0)
        self.horizontalLayout.setObjectName(_fromUtf8("horizontalLayout"))
        self.widget_credits_2 = QtGui.QWidget(self.widget_container)
        self.widget_credits_2.setObjectName(_fromUtf8("widget_credits_2"))
        self.verticalLayout_3 = QtGui.QVBoxLayout(self.widget_credits_2)
        self.verticalLayout_3.setSpacing(0)
        self.verticalLayout_3.setMargin(0)
        self.verticalLayout_3.setMargin(0)
        self.verticalLayout_3.setObjectName(_fromUtf8("verticalLayout_3"))
        self.widget_social = QtGui.QWidget(self.widget_credits_2)
        self.widget_social.setObjectName(_fromUtf8("widget_social"))
        self.horizontalLayout_2 = QtGui.QHBoxLayout(self.widget_social)
        self.horizontalLayout_2.setSpacing(4)
        self.horizontalLayout_2.setMargin(0)
        self.horizontalLayout_2.setMargin(0)
        self.horizontalLayout_2.setObjectName(_fromUtf8("horizontalLayout_2"))
        self.label_facebook = QtGui.QLabel(self.widget_social)
        self.label_facebook.setObjectName(_fromUtf8("label_facebook"))
        self.horizontalLayout_2.addWidget(self.label_facebook)
        self.label_twitter = QtGui.QLabel(self.widget_social)
        self.label_twitter.setObjectName(_fromUtf8("label_twitter"))
        self.horizontalLayout_2.addWidget(self.label_twitter)
        self.label_website = QtGui.QLabel(self.widget_social)
        self.label_website.setObjectName(_fromUtf8("label_website"))
        self.horizontalLayout_2.addWidget(self.label_website)
        self.label_cogscinl = QtGui.QLabel(self.widget_social)
        self.label_cogscinl.setObjectName(_fromUtf8("label_cogscinl"))
        self.horizontalLayout_2.addWidget(self.label_cogscinl)
        spacerItem1 = QtGui.QSpacerItem(40, 20, QtGui.QSizePolicy.Expanding, QtGui.QSizePolicy.Minimum)
        self.horizontalLayout_2.addItem(spacerItem1)
        self.verticalLayout_3.addWidget(self.widget_social)
        self.horizontalLayout.addWidget(self.widget_credits_2)
        spacerItem2 = QtGui.QSpacerItem(40, 20, QtGui.QSizePolicy.Expanding, QtGui.QSizePolicy.Minimum)
        self.horizontalLayout.addItem(spacerItem2)
        self.label_opensesame = QtGui.QLabel(self.widget_container)
        sizePolicy = QtGui.QSizePolicy(QtGui.QSizePolicy.Preferred, QtGui.QSizePolicy.Minimum)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.label_opensesame.sizePolicy().hasHeightForWidth())
        self.label_opensesame.setSizePolicy(sizePolicy)
        self.label_opensesame.setAlignment(QtCore.Qt.AlignBottom|QtCore.Qt.AlignRight|QtCore.Qt.AlignTrailing)
        self.label_opensesame.setObjectName(_fromUtf8("label_opensesame"))
        self.horizontalLayout.addWidget(self.label_opensesame)
        self.verticalLayout.addWidget(self.widget_container)

        self.retranslateUi(widget_credits)
        QtCore.QMetaObject.connectSlotsByName(widget_credits)

    def retranslateUi(self, widget_credits):
        widget_credits.setWindowTitle(QtGui.QApplication.translate("widget_credits", "Form", None, QtGui.QApplication.UnicodeUTF8))
        self.label_facebook.setToolTip(QtGui.QApplication.translate("widget_credits", "Visit Facebook page", None, QtGui.QApplication.UnicodeUTF8))
        self.label_facebook.setText(QtGui.QApplication.translate("widget_credits", "F", None, QtGui.QApplication.UnicodeUTF8))
        self.label_twitter.setToolTip(QtGui.QApplication.translate("widget_credits", "Visit Twitter page", None, QtGui.QApplication.UnicodeUTF8))
        self.label_twitter.setText(QtGui.QApplication.translate("widget_credits", "T", None, QtGui.QApplication.UnicodeUTF8))
        self.label_website.setToolTip(QtGui.QApplication.translate("widget_credits", "Visit cogsci.nl", None, QtGui.QApplication.UnicodeUTF8))
        self.label_website.setText(QtGui.QApplication.translate("widget_credits", "H", None, QtGui.QApplication.UnicodeUTF8))
        self.label_cogscinl.setText(QtGui.QApplication.translate("widget_credits", "<html><head/><body><p>COGSCIdotNL // cognitive science and more</p></body></html>", None, QtGui.QApplication.UnicodeUTF8))
        self.label_opensesame.setText(QtGui.QApplication.translate("widget_credits", "OpenSesame [version] [codename]\n"
"Copyright Sebastiaan Mathôt (2010-2013)", None, QtGui.QApplication.UnicodeUTF8))


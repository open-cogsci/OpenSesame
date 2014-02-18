# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file 'resources/ui/credits_widget.ui'
#
# Created: Fri Jan  3 14:35:01 2014
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
        self.horizontalLayout.setObjectName(_fromUtf8("horizontalLayout"))
        self.widget_credits_2 = QtGui.QWidget(self.widget_container)
        self.widget_credits_2.setObjectName(_fromUtf8("widget_credits_2"))
        self.verticalLayout_3 = QtGui.QVBoxLayout(self.widget_credits_2)
        self.verticalLayout_3.setSpacing(0)
        self.verticalLayout_3.setMargin(0)
        self.verticalLayout_3.setObjectName(_fromUtf8("verticalLayout_3"))
        self.widget_social = QtGui.QWidget(self.widget_credits_2)
        self.widget_social.setObjectName(_fromUtf8("widget_social"))
        self.horizontalLayout_2 = QtGui.QHBoxLayout(self.widget_social)
        self.horizontalLayout_2.setSpacing(4)
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
        self.label_contribute = QtGui.QLabel(self.widget_social)
        self.label_contribute.setOpenExternalLinks(True)
        self.label_contribute.setObjectName(_fromUtf8("label_contribute"))
        self.horizontalLayout_2.addWidget(self.label_contribute)
        self.label_donate = QtGui.QLabel(self.widget_social)
        self.label_donate.setOpenExternalLinks(True)
        self.label_donate.setObjectName(_fromUtf8("label_donate"))
        self.horizontalLayout_2.addWidget(self.label_donate)
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
        widget_credits.setWindowTitle(_translate("widget_credits", "Form", None))
        self.label_facebook.setToolTip(_translate("widget_credits", "Visit Facebook page", None))
        self.label_facebook.setText(_translate("widget_credits", "F", None))
        self.label_twitter.setToolTip(_translate("widget_credits", "Visit Twitter page", None))
        self.label_twitter.setText(_translate("widget_credits", "T", None))
        self.label_website.setToolTip(_translate("widget_credits", "Visit cogsci.nl", None))
        self.label_website.setText(_translate("widget_credits", "H", None))
        self.label_cogscinl.setText(_translate("widget_credits", "<html><head/><body><p>COGSCIdotNL // cognitive science and more</p></body></html>", None))
        self.label_contribute.setText(_translate("widget_credits", "<a href=\"http://osdoc.cogsci.nl/contribute/\">Contribute</a>", None))
        self.label_donate.setText(_translate("widget_credits", "<a href=\"http://osdoc.cogsci.nl/donate/\">Donate</a>", None))
        self.label_opensesame.setText(_translate("widget_credits", "OpenSesame [version] [codename]\n"
"Copyright Sebastiaan Mathôt (2010-2014)", None))


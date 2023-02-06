# -*- coding:utf-8 -*-

"""
This file is part of OpenSesame.

OpenSesame is free software: you can redistribute it and/or modify
it under the terms of the GNU General Public License as published by
the Free Software Foundation, either version 3 of the License, or
(at your option) any later version.

OpenSesame is distributed in the hope that it will be useful,
but WITHOUT ANY WARRANTY; without even the implied warranty of
MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
GNU General Public License for more details.

You should have received a copy of the GNU General Public License
along with OpenSesame.  If not, see <http://www.gnu.org/licenses/>.
"""

from libopensesame.py3compat import *
from libqtopensesame.misc import config
from libqtopensesame.widgets.base_widget import BaseWidget
from qtpy import QtWidgets, QtCore
from libqtopensesame.misc.translate import translation_context
_ = translation_context(u'unused_widget', category=u'core')


class UnusedWidget(BaseWidget):

    """
    desc:
            The unused items widget.
    """

    tab_name = u'__unused__'

    def __init__(self, main_window):
        """
        desc:
                Constructor.

        arguments:
                main_window:
                        desc:	The main-window object.
                        type:	qtopensesame
        """

        super().__init__(main_window)
        header_hbox = QtWidgets.QHBoxLayout()
        header_hbox.addWidget(self.theme.qlabel(u"unused"))
        header_label = QtWidgets.QLabel()
        header_label.setText(_(u"<b><font size='5'>Unused</font></b>"))
        header_hbox.addWidget(header_label)
        header_hbox.addStretch()
        self.purge_button = QtWidgets.QPushButton(self.theme.qicon(u"purge"),
                                                  _(u"Permanently delete unused items"))
        self.purge_button.setIconSize(QtCore.QSize(16, 16))
        self.purge_button.clicked.connect(self.purge_unused)
        purge_hbox = QtWidgets.QHBoxLayout()
        purge_hbox.addWidget(self.purge_button)
        purge_hbox.addStretch()
        purge_widget = QtWidgets.QWidget()
        purge_widget.setLayout(purge_hbox)
        vbox = QtWidgets.QVBoxLayout()
        vbox.addWidget(purge_widget)
        vbox.addStretch()
        self.setLayout(vbox)
        self.__unused_tab__ = True

    def purge_unused(self):
        """
        desc:
                Purges all unused items.
        """

        resp = QtWidgets.QMessageBox.question(self.main_window.ui.centralwidget,
            _(u"Permanently delete items?"),
            _(u"Are you sure you want to permanently delete all unused items? This action cannot be undone."),
            QtWidgets.QMessageBox.Yes, QtWidgets.QMessageBox.No)
        if resp == QtWidgets.QMessageBox.No:
            return
        self.extension_manager.fire(u'prepare_purge_unused_items')
        self.overview_area.locked = True
        for item_name in self.experiment.items.unused():
            self.experiment.items[item_name].close_tab()
            del self.experiment.items[item_name]
        self.overview_area.locked = False
        self.experiment.build_item_tree()
        self.purge_button.setDisabled(True)
        self.extension_manager.fire(u'purge_unused_items')

    def on_activate(self):
        """
        desc:
                Is called when the widget becomes visible.
        """

        self.purge_button.setDisabled(len(self.experiment.items.unused()) == 0)


# Alias for backwards compatibility
unused_widget = UnusedWidget

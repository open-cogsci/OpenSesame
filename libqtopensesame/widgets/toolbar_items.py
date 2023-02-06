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
from qtpy import QtCore, QtWidgets
from collections import OrderedDict
from libopensesame import plugins
from libopensesame.oslogging import oslogger
from libqtopensesame.misc.base_subcomponent import BaseSubcomponent
from libqtopensesame.widgets.toolbar_items_label import ToolbarItemsLabel
from libqtopensesame.widgets.toolbar_items_item import ToolbarItemsItem
from libqtopensesame.misc.translate import translation_context
_ = translation_context(u'toolbar_items', category=u'core')


class ToolbarItems(BaseSubcomponent, QtWidgets.QToolBar):

    r"""The item toolbar, which allows you to insert items into the experiment
    through drag and drop.
    """
    def __init__(self, parent):
        r"""Constructor.

        Parameters
        ----------
        parent : QWidget
            The parent.
        """
        super().__init__(parent)
        self.setup(parent)
        self.orientationChanged.connect(self.build)
        for child in self.children():
            if isinstance(child, QtWidgets.QToolButton):
                self._expand_button = child
                break

    def add_content(self, content):
        r"""Add double rows of content to the toolbar.

        Parameters
        ----------
        content : list
            A list of content widgets.
        """
        for i, c in enumerate(content):
            if not i % 2:
                if i > 0:
                    self.addWidget(w)
                if self.orientation() == QtCore.Qt.Horizontal:
                    l = QtWidgets.QVBoxLayout()
                    l.setContentsMargins(6, 6, 6, 6)
                else:
                    l = QtWidgets.QHBoxLayout()
                    l.setContentsMargins(6, 6, 6, 6)
                l.setSpacing(12)
                w = QtWidgets.QWidget()
                w.setLayout(l)
            l.addWidget(c)
        if not i % 2:
            l.addStretch()
        self.addWidget(w)

    def build(self):
        r"""Populates the toolbar with items."""
        # This function is called first when no experiment has been loaded yet.
        try:
            self.experiment
        except:
            return
        self.clear()
        if self.orientation() == QtCore.Qt.Vertical:
            self.addWidget(ToolbarItemsLabel(self, _(u'Commonly used')))
        # Add the core items
        self.add_content([ToolbarItemsItem(self, item)
                          for item in self.experiment.core_items])
        # Create a dictionary of plugins by category. We also maintain a list
        # to preserve the order of the categories.
        cat_dict = OrderedDict()
        for plugin in plugins.list_plugins(mode=self.main_window.mode):
            cat = plugins.plugin_category(plugin)
            if cat not in cat_dict:
                cat_dict[cat] = []
            cat_dict[cat].append(plugin)
        # Add the plugins
        for cat, cat_plugins in cat_dict.items():
            self.addSeparator()
            if self.orientation() == QtCore.Qt.Vertical:
                self.addWidget(ToolbarItemsLabel(self, cat))
            content = []
            for plugin in cat_plugins:
                oslogger.debug(u"adding plugin '%s'" % plugin)
                pixmap = self.theme.qpixmap(plugins.plugin_icon_large(plugin))
                content.append(ToolbarItemsItem(self, plugin, pixmap))
            self.add_content(content)

    def collapse(self):
        r"""Collapses the item toolbar if is was expanded."""
        if self._expand_button.isChecked():
            self._expand_button.click()


# Alias for backwards compatibility
toolbar_items = ToolbarItems

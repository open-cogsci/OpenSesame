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
from libqtopensesame.misc.base_subcomponent import base_subcomponent
from libqtopensesame.misc.translate import translation_context
_ = translation_context(u'item_view_button', category=u'core')


class item_view_button(base_subcomponent, QtWidgets.QPushButton):

    """
    desc:
            The view button in the top-right of the edit controls.
    """

    def __init__(self, item):
        """
        desc:
                Constructor.

        arguments:
                item:
                        desc:	An item.
                        type:	qtitem.
        """

        super(item_view_button, self).__init__(item.main_window)
        self.item = item
        self.setup(item)
        self.set_view_icon(u'controls')
        self.setIconSize(QtCore.QSize(16, 16))
        self.menu_view = QtWidgets.QMenu()
        self.menu_view.addAction(self.view_controls_icon(),
                                 _(u'View controls'), self.item.set_view_controls)
        self.menu_view.addAction(self.view_script_icon(), _(u'View script'),
                                 self.item.set_view_script)
        self.menu_view.addAction(self.view_split_icon(), _(u'Split view'),
                                 self.item.set_view_split)
        self.setMenu(self.menu_view)
        self.setToolTip(_(u'Select view'))

    def view_controls_icon(self):
        """
        returns:
                desc:	The icon for the controls view.
                type: 	QIcon
        """

        return self.theme.qicon(u'os-view-controls')

    def view_script_icon(self):
        """
        returns:
                desc:	The icon for the script view.
                type: 	QIcon
        """

        return self.theme.qicon(u'os-view-script')

    def view_split_icon(self):
        """
        returns:
                desc:	The icon for the split view.
                type: 	QIcon
        """

        return self.theme.qicon(u'os-view-split')

    def set_view_icon(self, view):
        """
        desc:
                Sets the icon of the button according to a view.

        arguments:
                view:
                        desc:	'controls', 'script', or 'split'.
                        type:	unicode
        """

        if view == u'controls':
            self.setIcon(self.view_controls_icon())
        elif view == u'script':
            self.setIcon(self.view_script_icon())
        else:
            self.setIcon(self.view_split_icon())

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
from qtpy import QtWidgets, QtGui
from libqtopensesame.misc.base_subcomponent import BaseSubcomponent
from libqtopensesame.misc.translate import translation_context
_ = translation_context(u'popup_menu', category=u'core')


class PopupMenu(QtWidgets.QMenu, BaseSubcomponent):

    r"""A simple pop-up menu that is shown at the cursor position to obtain a
    user response.
    """
    def __init__(self, main_window, actions, cancel=True, title=None):
        r"""Constructor.

        Parameters
        ----------
        main_window : QWidget
            The main-window object.
        actions : list
            A list of actions, where each action is (response code, text, icon
            name) tuple.
        cancel : bool, optional
            Indicates whether a cancel option should be shown.
        """
        QtWidgets.QMenu.__init__(self, main_window)
        self.setup(main_window)

        if title is not None:
            action = QtWidgets.QAction(self.theme.qicon(u'dialog-information'),
                                       title, self)
            action._id = None
            action.setDisabled(True)
            self.addAction(action)
            self.addSeparator()

        for _id, text, icon in actions:
            action = QtWidgets.QAction(self.theme.qicon(icon), text, self)
            action._id = _id
            self.addAction(action)
        if cancel:
            self.addSeparator()
            action = QtWidgets.QAction(self.theme.qicon(u'edit-clear'),
                                       _(u'Cancel'), self)
            action._id = None
            self.addAction(action)

    def show(self):
        r"""Shows the pop-up menu.

        Returns
        -------
        A response code or None if the popup was cancelled.
        """
        action = self.exec_(QtGui.QCursor.pos())
        if action is None:
            return None
        return action._id


# Alias for backwards compatibility
popup_menu = PopupMenu

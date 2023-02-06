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
from qtpy import QtWidgets
from libqtopensesame.misc.base_subcomponent import BaseSubcomponent
from libqtopensesame.misc.translate import translation_context
_ = translation_context(u'confirmation', category=u'core')


class Confirmation(QtWidgets.QMessageBox, BaseSubcomponent):

    r"""A simple yes/ no/ cancel confirmation dialog."""
    def __init__(self, main_window, msg, title=None, allow_cancel=False,
                 default=u'no'):
        r"""Constructor.

        Parameters
        ----------
        main_window : QWidget
            The main-window object.
        msg : unicode, str
            The message.
        title : str, NoneType
            A Window title or None for a default title.
        allow_cancel : bool
            Indicates whether a cancel button should be included, in addition
            to the yes and no buttons.
        default : str
            The button that is active by default, 'no', 'yes', or 'cancel'
        """
        QtWidgets.QMessageBox.__init__(self, main_window)
        self.setup(main_window)
        self.yes = self.addButton(QtWidgets.QMessageBox.Yes)
        self.no = self.addButton(QtWidgets.QMessageBox.No)
        if allow_cancel:
            self.cancel = self.addButton(QtWidgets.QMessageBox.Cancel)
        else:
            self.cancel = None
        if default == u'no':
            self.setDefaultButton(QtWidgets.QMessageBox.No)
        elif default == u'yes':
            self.setDefaultButton(QtWidgets.QMessageBox.Yes)
        elif default == u'cancel' and allow_cancel:
            self.setDefaultButton(QtWidgets.QMessageBox.Cancel)
        if title is None:
            title = _(u'Please confirm')
        self.setWindowTitle(title)
        self.setText(msg)

    def show(self):
        r"""Shows the confirmation dialog.

        Returns
        -------
        bool, NoneType
            True if confirmed, False disconfirmed, and None if cancelled.
        """
        self.exec_()
        button = self.clickedButton()
        if self.cancel is not None and button is self.cancel:
            return None
        return button == self.yes


# Alias for backwards compatibility
confirmation = Confirmation

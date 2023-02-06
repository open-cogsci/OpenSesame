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
from qtpy import QtCore, QtWidgets, QtGui
from libqtopensesame.widgets.base_widget import BaseWidget
from libqtopensesame.misc.translate import translation_context
_ = translation_context(u'color_edit', category=u'core')


class ColorEdit(BaseWidget):

    r"""A colorpicker widget that emulates a QLineEdit."""
    textChanged = QtCore.Signal('QString')
    textEdited = QtCore.Signal('QString')

    def __init__(self, main_window):
        r"""Constructor.

        Parameters
        ----------
        main_window : qtopensesame
            The main-window object.
        """
        super().__init__(main_window)
        self.edit = QtWidgets.QLineEdit()
        self._parent = None
        self.edit.setSizePolicy(QtWidgets.QSizePolicy.Minimum,
                                QtWidgets.QSizePolicy.Minimum)
        self.edit.editingFinished.connect(self.apply)
        self.editingFinished = self.edit.editingFinished
        self.button = QtWidgets.QPushButton()
        self.button.setIconSize(QtCore.QSize(16, 16))
        self.button.clicked.connect(self.colorpicker)
        layout = QtWidgets.QHBoxLayout()
        layout.setContentsMargins(0, 0, 0, 0)
        layout.addWidget(self.edit)
        layout.addWidget(self.button)
        self.setLayout(layout)

    def colorpicker(self):
        r"""Picks a color with the colorpicker dialog."""
        _color = QtWidgets.QColorDialog.getColor(QtGui.QColor(u'white'),
                                                 self._parent, _(u'Pick a color'))
        if not _color.isValid():
            return
        self.setText(_color.name())
        self.apply()

    def text(self):
        r"""Gets text (emulate QLineEdit behavior).

        Returns
        -------
        QString
            A color text.
        """
        return self.edit.text()

    def setText(self, s):
        """
        dsc:
                Sets text (emulate QLineEdit behavior).

        arguments:
                s:
                        desc:	Text.
                        type:	unicode
        """
        self.edit.setText(safe_decode(s))

    def apply(self):
        r"""Emits a 'set_color' signal to indicate that a color has been
        picked.
        """
        self.textChanged.emit(self.text())
        self.textEdited.emit(self.text())

    def initialize(self, experiment=None, color=None, parent=None):
        r"""Initializes the widget. This is necessary to apply the theme and
        give the fields initial values.

        Parameters
        ----------
        experiment : experiment, NoneType, optional
            The experiment object or None if it is already available via the
            base_component property.
        color : unicode, NoneType, optional
        parent, optional
            A parent QWidget.
        """
        if parent is not None:
            self._parent = parent
        else:
            self._parent = self.main_window
        if experiment is None:
            experiment = self.experiment
        if color is None:
            color = experiment.var.get(u'foreground', _eval=False)
        self.setText(color)
        self.button.setIcon(self.theme.qicon(u'os-color-picker'))


# Alias for backwards compatibility
color_edit = ColorEdit

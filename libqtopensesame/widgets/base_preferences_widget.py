# coding=utf-8

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
import functools
from qtpy.QtWidgets import (
    QCheckBox,
    QSpinBox,
    QDoubleSpinBox,
    QKeySequenceEdit,
    QLineEdit,
    QComboBox,
    QFontComboBox
)
from qtpy.QtGui import QKeySequence, QFont
from libopensesame.oslogging import oslogger
from libqtopensesame.widgets.base_widget import BaseWidget
from libqtopensesame.misc.config import cfg


class BasePreferencesWidget(BaseWidget):

    def __init__(self, main_window, ui):
        """
        desc:
                Constructor.

        arguments:
                main_window:	A qtopensesame object.
                ui:			A ui file.
        """

        super().__init__(main_window, ui=ui)
        self._its_me = False
        self._before_init_widgets()
        self._init_widgets()
        self._after_init_widgets()
        self.extension_manager.register_extension(self)

    def _before_init_widgets(self):
        """
        desc:
                Can be implemented to perform some actions before the rest of
                the widgets are initialized.
        """

        pass

    def _after_init_widgets(self):
        """
        desc:
                Can be implemented to perform some actions after the rest of
                the widgets have been initialized.
        """

        pass

    def _init_widgets(self):
        """
        desc:
                Introspects the widgets and automatically binds them to settings.
        """

        for name in dir(self.ui):
            if not name.startswith('cfg_'):
                continue
            setting = name[4:]
            if setting not in cfg:
                oslogger.warning('unknown setting {}'.format(setting))
            widget = getattr(self.ui, name)

            def change_setting(setting, value):
                if self._its_me:
                    return
                if isinstance(value, QKeySequence):
                    value = value.toString()
                elif isinstance(value, QFont):
                    value = value.family()
                elif isinstance(value, QLineEdit):
                    value = value.text()
                cfg[setting] = value
                self._its_me = True
                self.extension_manager.fire(
                    'setting_changed',
                    setting=setting,
                    value=value
                )
                self._its_me = False

            change_setting = functools.partial(change_setting, setting)
            if isinstance(widget, QCheckBox):
                widget.setChecked(cfg[setting])
                widget.toggled.connect(change_setting)
            elif isinstance(widget, QLineEdit):
                widget.setText(cfg[setting])
                widget.editingFinished.connect(
                    functools.partial(change_setting, widget)
                )
            elif isinstance(widget, (QSpinBox, QDoubleSpinBox)):
                widget.setValue(cfg[setting])
                widget.valueChanged.connect(change_setting)
            elif isinstance(widget, QKeySequenceEdit):
                widget.setKeySequence(QKeySequence(cfg[setting]))
                widget.keySequenceChanged.connect(change_setting)
            elif isinstance(widget, QFontComboBox):
                widget.setCurrentFont(QFont(cfg[setting]))
                widget.currentFontChanged.connect(change_setting)
            elif isinstance(widget, QComboBox):
                widget.setCurrentText(cfg[setting])
                widget.currentTextChanged.connect(change_setting)
            else:
                oslogger.warning('invalid QWidget with name {}'.format(name))

    def event_setting_changed(self, setting, value):
        """
        desc:
                Update the controls if settings have been changed by someone
                else.

        arguments:
                setting:	The name of the changed setting
                value:	The new value
        """

        if self._its_me:
            return
        name = 'cfg_{}'.format(setting)
        if not hasattr(self.ui, name):
            return
        self._its_me = True
        widget = getattr(self.ui, name)
        if isinstance(widget, QCheckBox):
            widget.setChecked(bool(value))
        elif isinstance(widget, QLineEdit):
            widget.setText(value)
        elif isinstance(widget, (QSpinBox, QDoubleSpinBox)):
            try:
                widget.setValue(value)
            except TypeError:
                oslogger.warning(
                    'invalid value {} for {}', format(value, setting)
                )
        elif isinstance(widget, QKeySequenceEdit):
            try:
                widget.setKeySequence(QKeySequence(value))
            except TypeError:
                oslogger.warning(
                    'invalid value {} for {}', format(value, setting)
                )
        elif isinstance(widget, QFontComboBox):
            try:
                widget.setCurrentFont(QFont(value))
            except TypeError:
                oslogger.warning(
                    'invalid value {} for {}', format(value, setting)
                )
        elif isinstance(widget, QComboBox):
            try:
                widget.setCurrentText(value)
            except TypeError:
                oslogger.warning(
                    'invalid value {} for {}', format(value, setting)
                )
        else:
            oslogger.warn('invalid QWidget with name {}'.format(name))
        self._its_me = False

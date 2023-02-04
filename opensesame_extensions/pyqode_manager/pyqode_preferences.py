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
import pygments.styles
from libqtopensesame.widgets.base_preferences_widget import (
    BasePreferencesWidget
)
from libqtopensesame.misc.config import cfg


class PyQodePreferences(BasePreferencesWidget):

    def __init__(self, main_window):

        super(PyQodePreferences, self).__init__(
            main_window,
            ui=u'extensions.pyqode_manager.preferences'
        )

    def _before_init_widgets(self):

        for style in pygments.styles.get_all_styles():
            self.ui.cfg_pyqode_color_scheme.addItem(style)
        self.ui.cfg_pyqode_fixed_width_nchar.setEnabled(
            cfg.pyqode_fixed_width
        )
        self.ui.label_fixed_width_nchar.setEnabled(
            cfg.pyqode_fixed_width
        )
        self.ui.cfg_pyqode_pep8_ignore.setEnabled(
            cfg.pyqode_pep8_validation
        )
        self.ui.label_pep8_ignore.setEnabled(
            cfg.pyqode_pep8_validation
        )
        self.ui.cfg_pyqode_code_completion_excluded_mimetypes.setEnabled(
            cfg.pyqode_code_completion
        )
        self.ui.label_pyqode_code_completion_excluded_mimetypes.setEnabled(
            cfg.pyqode_code_completion
        )
        self.ui.cfg_pyqode_indentation.currentTextChanged.connect(
            self._toggle_indentation
        )
        self.ui.cfg_pyqode_autopep8_aggressive.setEnabled(
            cfg.pyqode_autopep8
        )
        self._toggle_indentation(cfg.pyqode_indentation)

    def _toggle_indentation(self, indentation):

        self.ui.cfg_pyqode_tab_length.setEnabled(indentation == 'spaces')
        self.ui.label_tab_length.setEnabled(indentation == 'spaces')

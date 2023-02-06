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
from libqtopensesame.dialogs.base_dialog import BaseDialog


class PatchSettings(BaseDialog):

    """
    desc:
            A patch settings dialog, inherited by the gabor and noise settings.
    """

    # Maps the GUI names onto valid keyword values
    env_map = {
        u'gaussian': u'gaussian',
        u'linear': u'linear',
        u'circular (sharp edge)': u'circular',
        u'rectangular (no envelope)': u'rectangular',
    }
    bgmode_map = {
        u'Color average': u'avg',
        u'Color 2': u'col2',
    }

    def __init__(self, main_window):
        """
        desc:
                Constructor.

        arguments:
                main_window:	The main window object.
        """

        super().__init__(main_window, ui=self.ui_file())
        self.ui.combobox_env.currentIndexChanged.connect(self.apply_env)
        self.ui.edit_color1.initialize()
        self.ui.edit_color2.initialize(color=self.experiment.var.background)
        self.ui.apply_env()

    def ui_file(self):
        """
        returns:
                desc:	The ui file.
                type:	unicode
        """

        raise NotImplementedError()

    def apply_env(self):
        """
        desc:
                Enables/ disables the stdev control based on the env combobox.
        """

        self.ui.spinbox_stdev.setEnabled(
            self.ui.combobox_env.currentText() == u'gaussian')

    def get_properties(self):
        """
        desc:
                Gets the Gabor properties.

        returns:
                desc:	A dictionary with properties.
                type:	dict
        """

        raise NotImplementedError()

    def set_properties(self, properties):
        """
        desc:
                Fills the dialog controls based on a properties dictionary.

        arguments:
                properties:
                        desc:	A properties dictionary.
                        type:	dict
        """

        raise NotImplementedError()

    def _spinbox_properties(self, *spinbox_vars):
        """
        desc:
                Gets the properties of all enabled spinboxes.

        argument-list:
                spinbox_vars:	A list of variables that are defined through spinbox
                                                widgets.

        returns:
                A dictionary with (var, value) mappings
        """

        return {
            var: getattr(self.ui, u'spinbox_%s' % var).value()
            for var in spinbox_vars
            if getattr(self.ui, u'spinbox_%s' % var).isEnabled()
        }

    def _combobox_properties(self, *combobox_vars):
        """
        desc:
                Gets the properties of all enabled comboboxes.

        argument-list:
                combobox_vars:	A list of (var, options) tuples of variables that
                                                are defined through combobox widgets.

        returns:
                A dictionary with (var, value) mappings
        """

        return {
            var: options[getattr(self.ui, u'combobox_%s' % var).currentText()]
            for var, options in combobox_vars
            if getattr(self.ui, u'combobox_%s' % var).isEnabled()
        }

    def _set_spinbox(self, spinbox, var, properties):
        """
        desc:
                Safely sets a spinbox based on a variable, or disables the spinbox
                if the value is not numeric.

        desc:
                spinbox:	A QSpinBox
                var:		A variable name
                properties:	A properties dict
        """

        if isinstance(properties[var], (int, float)):
            spinbox.setEnabled(True)
            spinbox.setValue(properties[var])
        else:
            spinbox.setEnabled(False)

    def _set_combobox(self, options, combobox, var, properties):
        """
        desc:
                Safely sets a combobox based on a variable, or disables the combobox
                if the value is not among the combobox options.

        arguments:
                options:	A dictionary with options
                combobox:	QComboBox
                var:		A variable name
                properties:	A properties dict
        """

        for key, val in options.items():
            if val == properties[var]:
                i = combobox.findText(key)
                combobox.setCurrentIndex(i)
                combobox.setEnabled(True)
                return
        combobox.setEnabled(False)


# Alias for backwards compatibility
patch_settings = PatchSettings

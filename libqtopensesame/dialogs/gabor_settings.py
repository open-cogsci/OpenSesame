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
from qtpy import QtWidgets
from libqtopensesame.dialogs.patch_settings import PatchSettings
from libopensesame.py3compat import *


class GaborSettings(PatchSettings):

    r"""A gabor settings dialog."""
    def ui_file(self):
        """
        returns:
                desc:	The ui file.
                type:	unicode
        """
        return u'dialogs.gabor_settings'

    def get_properties(self):
        r"""Gets the Gabor properties.

        Returns
        -------
        dict
            A dictionary with properties.
        """
        if self.exec_() != QtWidgets.QDialog.Accepted:
            return None

        properties = self._spinbox_properties(
            u'orient',
            u'freq',
            u'size',
            u'stdev',
            u'phase'
        )
        properties.update(self._combobox_properties(
            (u'env', self.env_map),
            (u'bgmode', self.bgmode_map)
        ))
        properties[u'color1'] = self.ui.edit_color1.text()
        properties[u'color2'] = self.ui.edit_color2.text()
        return properties

    def set_properties(self, properties):
        r"""Fills the dialog controls based on a properties dictionary.

        Parameters
        ----------
        properties : dict
            A properties dictionary.
        """
        self._set_spinbox(self.ui.spinbox_orient, u'orient', properties)
        self._set_spinbox(self.ui.spinbox_size, u'size', properties)
        self._set_spinbox(self.ui.spinbox_stdev, u'stdev', properties)
        self._set_spinbox(self.ui.spinbox_freq, u'freq', properties)
        self._set_spinbox(self.ui.spinbox_phase, u'phase', properties)
        self.ui.edit_color1.setText(properties[u'color1'])
        self.ui.edit_color2.setText(properties[u'color2'])
        self._set_combobox(
            self.env_map,
            self.ui.combobox_env,
            u'env',
            properties
        )
        self._set_combobox(
            self.bgmode_map,
            self.ui.combobox_bgmode,
            u'bgmode',
            properties
        )


# Alias for backwards compatibility
gabor_settings = GaborSettings

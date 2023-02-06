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
from libqtopensesame.widgets.base_widget import BaseWidget
from libqtopensesame.misc.translate import translation_context
_ = translation_context(u'general_script_editor', category=u'core')


class GeneralScriptEditor(BaseWidget):

    r"""The general script editor."""
    def __init__(self, main_window):
        r"""Constructor.

        Parameters
        ----------
        main_window
            A qtopensesame object.
        """
        from pyqode_extras.widgets import OpenSesameCodeEdit
        super().__init__(main_window, ui=u'widgets.general_script_editor')
        self.ui.editor = OpenSesameCodeEdit()
        self.extension_manager.fire(
            u'register_editor',
            editor=self.ui.editor,
            mime_type='text/opensesame'
        )
        self.ui.layout_vbox.addWidget(self.ui.editor)
        self.ui.button_apply.clicked.connect(self._apply)
        self.tab_name = u'__general_script__'

    def _apply(self):
        r"""Confirms and applies the script changes."""
        resp = QtWidgets.QMessageBox.question(
            self.main_window,
            _(u'Apply?'),
            _(u'Are you sure you want to apply the changes to the general script?'),
            QtWidgets.QMessageBox.Yes,
            QtWidgets.QMessageBox.No
        )
        if resp == QtWidgets.QMessageBox.No:
            return
        self.main_window.regenerate(self.ui.editor.toPlainText())

    def on_activate(self):
        r"""Refreshes the tab when it is activated."""
        self.refresh()

    def refresh(self):
        r"""Refreshes the contents of the general script."""
        self.ui.editor.setPlainText(
            self.main_window.experiment.to_string(),
            u'text/generic',
            u'utf-8'
        )


# Alias for backwards compatibility
general_script_editor = GeneralScriptEditor

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
from qtpy.QtWidgets import QSizePolicy
from qtpy.QtCore import Qt
import ast
from libopensesame.inline_script import InlineScript as InlineScriptRuntime
from libopensesame.oslogging import oslogger
from libqtopensesame.items.qtplugin import QtPlugin
from libqtopensesame.misc.translate import translation_context
from pyqode.core.api.utils import TextHelper
_ = translation_context(u'inline_script', category=u'item')


class InlineScript(InlineScriptRuntime, QtPlugin):
    """The inline_script GUI controls"""
    
    description = _(u'Executes Python code')
    help_url = u'manual/python/about'
    ext = u'.py'
    mime_type = u'text/x-python'

    def __init__(self, name, experiment, string=None):
        self._var_cache = None
        InlineScriptRuntime.__init__(self, name, experiment, string)
        QtPlugin.__init__(self)

    def apply_edit_changes(self):
        sp = self._pyqode_prepare_editor.toPlainText()
        sr = self._pyqode_run_editor.toPlainText()
        self._set_modified()
        self.var._prepare = sp
        self.var._run = sr
        super().apply_edit_changes()

    def _set_modified(self, prepare=False, run=False):
        self._pyqode_prepare_editor.document().setModified(prepare)
        self._pyqode_run_editor.document().setModified(run)
        self._pyqode_tab_bar.setTabText(
            0, ('* ' if prepare else '') + _('Prepare'))
        self._pyqode_tab_bar.setTabText(
            1, ('* ' if prepare else '') + _('Run'))

    def set_focus(self):
        self._pyqode_tab_widget.setFocus()

    def init_edit_widget(self):
        from pyqode.core.widgets import SplittableCodeEditTabWidget

        super().init_edit_widget(stretch=False)
        self._pyqode_tab_widget = SplittableCodeEditTabWidget(
            tabs_movable=False,
            plus_button=False,
            tab_context_menu=False,
            empty_context_menu=False
        )
        self._pyqode_tab_widget.setSizePolicy(
            QSizePolicy.Expanding,
            QSizePolicy.Expanding
        )
        self._pyqode_tab_bar = self._pyqode_tab_widget.main_tab_widget.tabBar()
        self._pyqode_tab_bar.setTabsClosable(False)
        self._pyqode_prepare_editor = \
            self._pyqode_tab_widget.create_new_document('Prepare', self.ext)
        self._pyqode_run_editor = \
            self._pyqode_tab_widget.create_new_document('Run', self.ext)
        self._pyqode_run_editor.focusOutEvent = self._editor_focus_out
        self._pyqode_prepare_editor.focusOutEvent = self._editor_focus_out
        self._set_modified()
        self.extension_manager.fire(
            u'register_editor',
            editor=self._pyqode_run_editor
        )
        self.extension_manager.fire(
            u'register_editor',
            editor=self._pyqode_prepare_editor
        )
        self.edit_vbox.addWidget(self._pyqode_tab_widget)
        if not self.var._run and self.var._prepare:
            self._pyqode_tab_widget.main_tab_widget.setCurrentIndex(0)
        else:
            self._pyqode_tab_widget.main_tab_widget.setCurrentIndex(1)

    def edit_widget(self):
        super().edit_widget()
        _prepare = safe_decode(self.var._prepare)
        if _prepare != self._pyqode_prepare_editor.toPlainText():
            self._pyqode_prepare_editor.setPlainText(
                _prepare,
                mime_type=self.mime_type
            )
        _run = safe_decode(self.var._run)
        if _run != self._pyqode_run_editor.toPlainText():
            self._pyqode_run_editor.setPlainText(
                _run,
                mime_type=self.mime_type
            )

    def get_ready(self):
        if self.container_widget is None:
            return
        self.apply_edit_changes()
        
    def open_tab(self, select_in_tree=True, **kwargs):
        super().open_tab(select_in_tree=select_in_tree, **kwargs)
        if 'phase' not in kwargs:
            return
        tab_index = 1 if kwargs['phase'] == 'run' else 0
        self._pyqode_tab_widget.main_tab_widget.setCurrentIndex(tab_index)
        # The line number is allways passed as the first optional argument
        if 'args' in kwargs:
            line = int(kwargs['args'][0])
            edit = self._pyqode_tab_widget.main_tab_widget.currentWidget()
            TextHelper(edit).goto_line(line, move=True)

    def var_info(self):
        if self._var_cache is None:
            script = self.var.get('_prepare', _eval=False, default='') + \
                self.var.get('_run', _eval=False, default='')
            self._var_cache = [
                (key, None) for key in self._extract_assignments(script)]
        return super().var_info() + self._var_cache
    
    def _extract_assignments(self, script):
        """Extracts variables that are assigned in the script.
        
        Parameters
        ----------
        script: str
        
        Returns
        -------
        list
            A list of extracted variable names
        """
        def inner(body, only_globals=False):
            assignments = []
            for element in body:
                if isinstance(element, ast.Attribute):
                    assignments += [target.attr for target in element.targets
                                    if element.value == 'var']
                elif isinstance(element, ast.Assign) and not only_globals:
                    for target in element.targets:
                        if isinstance(target, ast.Attribute):
                            # Oldschool assignments to variable store
                            if target.value.id == 'var':
                                assignments.append(target.attr)
                        else:
                            assignments.append(target.id)
                elif isinstance(element, ast.Global):
                    assignments += element.names
                elif hasattr(element, 'body'):
                    assignments += inner(
                        element.body,
                        only_globals=isinstance(element, ast.FunctionDef))
            return assignments
        
        return inner(ast.parse(script).body)


# Alias for backwards compatibility
inline_script = InlineScript

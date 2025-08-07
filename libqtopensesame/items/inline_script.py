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
from libopensesame.py3compat import safe_decode
from qtpy.QtWidgets import QSizePolicy, QTabWidget, QVBoxLayout, QWidget
import ast
from libopensesame.inline_script import InlineScript as InlineScriptRuntime
from libopensesame.oslogging import oslogger
from libqtopensesame.items.qtplugin import QtPlugin
from libqtopensesame.misc.translate import translation_context
from pyqt_code_editor.code_editors import create_editor
from pyqt_code_editor.environment_manager import environment_manager
_ = translation_context('inline_script', category='item')


# This import prefix helps Jedi know about the Python workspace API
IMPORT_PREFIX = '''from libopensesame.python_workspace_api import (
    # Core factory functions
    Experiment, Form, Canvas, Keyboard, Mouse, Sampler, Synth,
    # Canvas elements
    Rect, Line, Text, Ellipse, Circle, FixDot, Gabor, NoisePatch, Image, Arrow,
    Polygon,
    # Widget factories
    Label, Button, ImageWidget, ImageButton, TextInput, RatingScale, Checkbox,
    # Utility functions
    copy_sketchpad, reset_feedback, set_subject_nr, sometimes, pause,
    register_cleanup_function, xy_from_polar, xy_to_polar, xy_distance,
    xy_circle, xy_grid, xy_random
)

# Available objects with type hints for Jedi
from libopensesame.experiment import Experiment
exp: Experiment = None  # type: ignore
from libopensesame.var_store import VarStore
var: VarStore = None # type: ignore
from libopensesame.item_store import ItemStore
items: ItemStore = None  # type: ignore
from openexp._clock.clock import Clock
clock: Clock = None  # type: ignore
from openexp._log.log import Log
log: Log = None  # type: ignore
from libopensesame.response_store import ResponseStore
responses: ResponseStore = None  # type: ignore
data_files: list = None  # type: ignore
AbortCoroutines: Exception = None  # type: ignore
from libopensesame.file_pool_store import FilePoolStore
pool: FilePoolStore = None  # type: ignore
win: object = None  # type: ignore
'''


class InlineScript(InlineScriptRuntime, QtPlugin):
    """The inline_script GUI controls"""
    
    description = _('Executes Python code')
    help_url = 'manual/python/about'
    language = 'python'

    def __init__(self, name, experiment, string=None):
        self._var_cache = None
        InlineScriptRuntime.__init__(self, name, experiment, string)
        QtPlugin.__init__(self)

    def apply_edit_changes(self):
        sp = self._prepare_editor.toPlainText()
        sr = self._run_editor.toPlainText()
        self._prepare_editor.set_modified(False)
        self._run_editor.set_modified(False)
        self.var._prepare = sp
        self.var._run = sr
        self._var_cache = None
        super().apply_edit_changes()
        
    def _prepare_modified(self, editor, modified):
        self._tab_widget.setTabText(
            0, ('* ' if modified else '') + _('Prepare'))
        
    def _run_modified(self, editor, modified):
        self._tab_widget.setTabText(
            1, ('* ' if modified else '') + _('Run'))

    def set_focus(self):
        self._tab_widget.setFocus()

    def init_edit_widget(self):
        super().init_edit_widget(stretch=False)
        
        # Create tab widget manually since pyqt_code_editor doesn't provide one
        self._tab_widget = QTabWidget()
        self._tab_widget.setSizePolicy(
            QSizePolicy.Expanding,
            QSizePolicy.Expanding
        )
        self._tab_widget.setTabsClosable(False)
        self._tab_widget.currentChanged.connect(self.update_script_prefix)
        
        # Create prepare phase editor
        prepare_container = QWidget()
        prepare_layout = QVBoxLayout(prepare_container)
        prepare_layout.setContentsMargins(0, 0, 0, 0)
        self._prepare_editor = create_editor(language=self.language,
                                             parent=prepare_container)
        self._prepare_editor.modification_changed.connect(self._prepare_modified)
        prepare_layout.addWidget(self._prepare_editor)
        
        # Create run phase editor
        run_container = QWidget()
        run_layout = QVBoxLayout(run_container)
        run_layout.setContentsMargins(0, 0, 0, 0)
        self._run_editor = create_editor(language=self.language,
                                         parent=run_container)
        self._run_editor.modification_changed.connect(self._run_modified)
        run_layout.addWidget(self._run_editor)
        
        # Add tabs
        self._tab_widget.addTab(prepare_container, _('Prepare'))
        self._tab_widget.addTab(run_container, _('Run'))
        
        # Set up focus out events
        self._run_editor.lost_focus.connect(self._editor_focus_out)
        self._prepare_editor.lost_focus.connect(self._editor_focus_out)
        
        self.edit_vbox.addWidget(self._tab_widget)
        
        # Set initial tab
        if not self.var._run and self.var._prepare:
            self._tab_widget.setCurrentIndex(0)
        else:
            self._tab_widget.setCurrentIndex(1)

    def edit_widget(self):
        super().edit_widget()
        _prepare = safe_decode(self.var._prepare)
        if _prepare != self._prepare_editor.toPlainText():
            self._prepare_editor.setPlainText(_prepare)
        _run = safe_decode(self.var._run)
        if _run != self._run_editor.toPlainText():
            self._run_editor.setPlainText(_run)

    def get_ready(self):
        if self.container_widget is None:
            return
        self.apply_edit_changes()
        
    def update_script_prefix(self):
        """Determines the prefix for the inline script. This consists of a set of
        manually crafted import statements and object definitions as specified
        in IMPORT_PREFIX, followed by the prepare and run scripts of all items
        except the phase of the current one.
        """
        scripts = [IMPORT_PREFIX]
        index = self._tab_widget.currentIndex()
        for item in self.experiment.items.values():
            if item.item_type != 'inline_script':
                continue
            if item != self or index == 1:
                scripts.append(f'''
# START_PREPARE_PHASE (item: {item.name})
{item.var._prepare}
# END_PREPARE_PHASE (item: {item.name})
''')        
            if item != self or index == 0:
                scripts.append(f'''
# START_RUN_PHASE (item: {item.name})
{item.var._run}
# END_RUN_PHASE (item: {item.name})
''')
        environment_manager.prefix = '\n'.join(scripts)
        
    def open_tab(self, select_in_tree=True, **kwargs):
        super().open_tab(select_in_tree=select_in_tree, **kwargs)
        if 'phase' not in kwargs:
            return
        tab_index = 1 if kwargs['phase'] == 'run' else 0
        self._tab_widget.setCurrentIndex(tab_index)
        # The line number is always passed as the first optional argument
        if 'args' in kwargs:
            line = int(kwargs['args'][0])
            edit = self._prepare_editor if tab_index == 0 else self._run_editor
            # Move cursor to the specified line
            cursor = edit.textCursor()
            cursor.movePosition(cursor.Start)
            cursor.movePosition(cursor.Down, cursor.MoveAnchor, line - 1)
            edit.setTextCursor(cursor)
            edit.centerCursor()
            
    def show_tab(self):
        self.update_script_prefix()
        super().show_tab()

    def var_info(self):
        if self._var_cache is None:
            script = self.var.get('_prepare', _eval=False, default='') + \
                self.var.get('_run', _eval=False, default='')
            self._var_cache = [
                (key, None) for key in self._extract_assignments(script)]
        return super().var_info() + self._var_cache
    
    @staticmethod
    def _extract_assignments(script):
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
        
        try:
            return inner(ast.parse(script).body)
        except Exception as e:
            oslogger.debug(f'failed to extract assignments: {e}')
            return []


# Alias for backwards compatibility
inline_script = InlineScript
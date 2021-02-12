#-*- coding:utf-8 -*-

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
import re
import types
from openexp.canvas_elements import ElementFactory
from libopensesame import python_workspace_api as api
from libopensesame.widgets.widget_factory import WidgetFactory
from libqtopensesame.misc.config import cfg
from libopensesame.oslogging import oslogger
from libqtopensesame.extensions import base_extension
from pyqode.core import icons
from pyqode.core.widgets import SplittableCodeEditTabWidget
from pyqode_extras.widgets import (
	PythonCodeEdit,
	FallbackCodeEdit
)
from pyqode.core.api import ColorScheme
from pyqode.core.api.panel import Panel
from pyqode.core.panels import LineNumberPanel, FoldingPanel, MarginPanel
from pyqode.core.modes import (
	PygmentsSH,
	RightMarginMode,
	CodeCompletionMode,
	AutoCompleteMode,
	BreakpointMode
)
from pyqode.python.modes import (
	sh,
	PyAutoCompleteMode,
	CalltipsMode
)
from pyqode.core.managers import backend
from qtpy.QtGui import QFontMetrics
from qtpy.QtWidgets import QPlainTextEdit


class pyqode_manager(base_extension):

	"""
	desc:
		Keeps track of all PyQode editor instances, which need to be explicitly
		closed. And also modifies their behavior somewhat.
	"""

	def _is_opensesame_api_object(self, name, obj):

		if name.startswith(u'safe_'):
			return False
		if isinstance(obj, types.FunctionType):
			return True
		if isinstance(obj, type) and issubclass(
			obj, (WidgetFactory, ElementFactory)):
				return True
		return False

	def _register_opensesame_builtins(self):

		builtins = [
			u'exp',
			u'var',
			u'pool',
			u'items',
			u'clock',
			u'log',
			u'responses',
			u'data_files',
			u'AbortCoroutines'
		] + [
			name
			for name, obj in api.__dict__.items()
			if self._is_opensesame_api_object(name, obj)
		]
		sh.PythonSH.PROG = re.compile(
			sh.make_python_patterns(additional_builtins=builtins),
			re.S
		)
		
	def settings_widget(self):
		
		from pyqode_preferences import PyQodePreferences
		return PyQodePreferences(self.main_window)

	def event_startup(self):

		backend.comm = oslogger.debug
		if self.main_window.mode == u'default':
			self._register_opensesame_builtins()
		icons.USE_QTAWESOME = True
		icons.QTA_OPTIONS = {
			'color': self.main_window.palette().text().color().name(),
			'color_disabled': self.main_window.palette().mid().color().name(),
			'color_info': '#66d9ef',
			'color_warning': '#e6db74',
			'color_error': '#f92672'
		}
		SplittableCodeEditTabWidget.editors = {}
		SplittableCodeEditTabWidget.fallback_editor = FallbackCodeEdit
		SplittableCodeEditTabWidget.register_code_edit(PythonCodeEdit)
		SplittableCodeEditTabWidget.register_code_edit(FallbackCodeEdit)
		# Syntax is broken for TextCodeEdit, so we don't use it for now
		# SplittableCodeEditTabWidget.register_code_edit(TextCodeEdit)
		self._editors = []
		self._breakpoints = {}
		self._auto_backend_restart = True

	def event_close(self):

		self._auto_backend_restart = False
		oslogger.debug(u'closing ({})'.format(len(self._editors)))
		while self._editors:
			self._editors.pop().close()
		self._auto_backend_restart = True

	def event_prepare_delete_item(self, name):

		item = self.item_store[name]
		if item.container_widget is None:
			return
		if item.item_type == u'inline_script':
			self.event_unregister_editor(item._pyqode_run_editor)
			self.event_unregister_editor(item._pyqode_prepare_editor)
		if hasattr(self, u'auto_editor'):
			for editor in self.auto_editor.values():
				self.event_unregister_editor(editor)
		self.event_unregister_editor(item._script_widget)

	def event_run_experiment(self, fullscreen):

		self._auto_backend_restart = False
		for editor in self._editors:
			editor.backend.suspend()
		self._auto_backend_restart = True

	def event_end_experiment(self, ret_val):

		for editor in self._editors:
			editor.backend.resume()
			self._register_backend_process(editor)

	def event_prepare_purge_unused_items(self):

		for name in self.item_store.unused():
			self.event_prepare_delete_item(name)

	def event_open_experiment(self, path):

		self.event_close()

	def event_prepare_regenerate(self):

		self.event_close()

	def event_register_editor(self, editor, mime_type=u'text/plain'):

		if editor in self._editors:
			oslogger.debug('editor already registered')
			return
		editor._auto_reset_stylesheet = False
		self._editors.append(editor)		
		if 'PythonSH' in editor.modes.keys():
			pass
		elif 'TextSH' in editor.modes.keys():
			editor.modes.get('TextSH').color_scheme = safe_str(
				cfg.pyqode_color_scheme
			)
		elif 'PygmentsSH' in editor.modes.keys():
			editor.modes.get('PygmentsSH').color_scheme = safe_str(
				cfg.pyqode_color_scheme
			)
		else:
			sh = PygmentsSH(
				editor.document(),
				color_scheme=ColorScheme('monokai')
			)
			sh.set_mime_type(mime_type)
			editor.modes.append(sh)
		if cfg.pyqode_enable_breakpoints:
			editor.modes.append(BreakpointMode(breakpoints=self._breakpoints))
		editor.font_size = cfg.pyqode_font_size
		editor.font_name = cfg.pyqode_font_name
		editor.setLineWrapMode(
			QPlainTextEdit.WidgetWidth
			if cfg.pyqode_line_wrap
			else QPlainTextEdit.NoWrap
		)
		editor.action_duplicate_line.setShortcut(
			cfg.pyqode_shortcut_duplicate_line
		)
		editor.action_swap_line_up.setShortcut(
			cfg.pyqode_shortcut_swap_line_up
		)
		editor.action_swap_line_down.setShortcut(
			cfg.pyqode_shortcut_swap_line_down
		)
		editor._auto_reset_stylesheet = True
		editor._reset_stylesheet()
		editor.setTabStopWidth(
			QFontMetrics(
				editor.font()
			).averageCharWidth() * cfg.pyqode_tab_length
		)
		# This function is defined here so to keep the editor in the scope.
		# This is necessary in case the backend crashes and it needs to be
		# restarted.
		def auto_restart():
			if editor._closed or not self._auto_backend_restart:
				return
			oslogger.warning(
				u'restarting backend: {}'.format(editor.__class__.__name__)
			)
			if editor.backend._share_id in editor.backend.SHARE_COUNT:
				del editor.backend.SHARE_COUNT[editor.backend._share_id]
			editor.backend._process = None
			editor.backend.resume()
			self._register_backend_process(editor)
		try:
			editor.backend._process.error.connect(auto_restart)
			self._register_backend_process(editor)
		except RuntimeError:
			auto_restart()
		oslogger.debug(u'registering {}'.format(editor))

	def event_unregister_editor(self, editor):

		if editor is None:
			return
		self._auto_backend_restart = False
		editor.close()
		if editor in self._editors:
			self._editors.remove(editor)
		oslogger.debug(u'unregistering ({})'.format(len(self._editors)))
		self._auto_backend_restart = True
		
	def event_setting_changed(self, setting, value):
		
		fnc = '_setting_{}'.format(setting)
		if hasattr(self, fnc):
			getattr(self, fnc)(value)
			
	def provide_pyqode_breakpoints(self):
		
		return self._breakpoints

	def event_pyqode_suspend_auto_backend_restart(self):
		
		self._auto_backend_restart = False

	def event_pyqode_resume_auto_backend_restart(self):
		
		self._auto_backend_restart = True

	def event_pyqode_set_breakpoints(self, breakpoints):
		
		self._breakpoints = breakpoints

	def event_pyqode_clear_breakpoints(self):
		
		self.extension_manager.fire(
			'notify',
			message=_(u'Cleared {} breakpoint(s) in {} file(s)'.format(
				sum(len(lines) for lines in self._breakpoints.values()),
				len(self._breakpoints))
			)
		)
		self._breakpoints.clear()
		for editor in self._editors:
			if 'BreakpointMode' not in editor.modes.keys():
				continue
			editor.modes.get('BreakpointMode').clear_messages()
			editor.repaint()
			
	def _register_backend_process(self, editor):
		
		self.extension_manager.fire(
			'register_subprocess',
			pid=editor.backend._process.processId(),
			description='BackendProcess:{}'.format(
				editor.__class__.__name__
			)
		)

	def _setting_pyqode_show_line_numbers(self, show_line_numbers):

		self._toggle_panel(
			'pyqode_show_line_numbers',
			show_line_numbers,
			LineNumberPanel,
			Panel.Position.LEFT
		)

	def _setting_pyqode_line_wrap(self, line_wrap):

		cfg.pyqode_line_wrap = line_wrap
		for editor in self._editors:
			editor.setLineWrapMode(
				QPlainTextEdit.WidgetWidth
				if cfg.pyqode_line_wrap
				else QPlainTextEdit.NoWrap
			)

	def _setting_pyqode_code_completion(self, code_completion):

		editors = self._editors
		self._editors = [
			e for e in editors
			if isinstance(e, FallbackCodeEdit) and
			e.language not in cfg.pyqode_code_completion_excluded_mimetypes
		]
		for mode in (
			CodeCompletionMode,
			AutoCompleteMode
		):
			self._toggle_mode('pyqode_code_completion', code_completion, mode)
		self._editors = [
			e for e in editors
			if isinstance(e, PythonCodeEdit) and
			e.language not in cfg.pyqode_code_completion_excluded_mimetypes
		]
		for mode in (
			CodeCompletionMode,
			PyAutoCompleteMode,
			CalltipsMode
		):
			self._toggle_mode('pyqode_code_completion', code_completion, mode)
		self._editors = editors

	def _setting_pyqode_fixed_width(self, fixed_width):

		self._toggle_panel(
			'pyqode_fixed_width',
			fixed_width,
			MarginPanel,
			Panel.Position.LEFT,
			nchar=cfg.pyqode_fixed_width_nchar
		)

	def _setting_pyqode_show_whitespaces(self, show_whitespaces):

		cfg.pyqode_show_whitespaces = show_whitespaces
		for editor in self._editors:
			editor.show_whitespaces = cfg.pyqode_show_whitespaces

	def _setting_pyqode_right_margin(self, show_right_margin):

		self._toggle_mode(
			'pyqode_right_margin',
			show_right_margin,
			RightMarginMode
		)

	def _setting_pyqode_code_folding(self, code_folding):

		self._toggle_panel(
			'pyqode_code_folding',
			code_folding,
			FoldingPanel,
			Panel.Position.LEFT
		)

	def event_pyqode_select_indentation_mode(self):

		def _select_indentation_mode(mode):

			cfg.pyqode_indentation = mode
			for editor in self._editors:
				if 'AutodetectIndentationMode' not in editor.modes.keys():
					continue
				editor.modes.get('AutodetectIndentationMode')._autodetect_indentation()

		haystack = [
			(_('autodetect'), 'autodetect', _select_indentation_mode),
			(_('spaces'), 'spaces', _select_indentation_mode),
			(_('tabs'), 'tabs', _select_indentation_mode)
		]
		self.extension_manager.fire(
			u'quick_select',
			haystack=haystack,
			placeholder_text=_(u'Select indentation mode …')
		)

	def _toggle_mode(self, config, enabled, cls, **kwargs):

		cfg[config] = enabled
		for editor in self._editors:
			if enabled:
				if cls.__name__ in editor.modes.keys():
					continue
				editor.modes.append(cls(**kwargs))
			else:
				if cls.__name__ not in editor.modes.keys():
					continue
				editor.modes.remove(cls.__name__)
			editor.viewport().repaint()

	def _toggle_panel(self, config, enabled, cls, pos, **kwargs):

		cfg[config] = enabled
		for editor in self._editors:
			if enabled:
				if cls.__name__ in editor.panels._panels[pos]:
					continue
				panel = cls(**kwargs)
				editor.panels.append(panel, position=pos)
				editor.panels.refresh()
				panel.show()
			else:
				if cls.__name__ not in editor.panels._panels[pos]:
					continue
				editor.panels.remove(cls.__name__)
				editor.panels.refresh()

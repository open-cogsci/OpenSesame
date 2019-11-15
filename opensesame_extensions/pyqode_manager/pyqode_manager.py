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
from libqtopensesame.misc.config import cfg
from libopensesame.oslogging import oslogger
from libqtopensesame.extensions import base_extension
from pyqode.core.widgets import SplittableCodeEditTabWidget
from pyqode_extras.widgets import (
	PythonCodeEdit,
	FallbackCodeEdit,
	TextCodeEdit
)
from pyqode.core.api import ColorScheme
from pyqode.core.api.panel import Panel
from pyqode.core.panels import LineNumberPanel, FoldingPanel
from pyqode.core.modes import PygmentsSH, RightMarginMode
from pyqode.core.managers import backend
from qtpy.QtGui import QFontMetrics
from qtpy.QtWidgets import QPlainTextEdit


class pyqode_manager(base_extension):

	"""
	desc:
		Keeps track of all PyQode editor instances, which need to be explicitly
		closed. And also modifies their behavior somewhat.
	"""

	def event_startup(self):

		backend.comm = oslogger.debug
		SplittableCodeEditTabWidget.editors = {}
		SplittableCodeEditTabWidget.fallback_editor = FallbackCodeEdit
		SplittableCodeEditTabWidget.register_code_edit(PythonCodeEdit)
		SplittableCodeEditTabWidget.register_code_edit(FallbackCodeEdit)
		# Syntax is broken for TextCodeEdit, so we don't use it for now
		# SplittableCodeEditTabWidget.register_code_edit(TextCodeEdit)
		self._editors = []

	def event_close(self):

		oslogger.debug(u'closing ({})'.format(len(self._editors)))
		while self._editors:
			self._editors.pop().close()

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

		for editor in self._editors:
			editor.backend.suspend()

	def event_end_experiment(self, ret_val):

		for editor in self._editors:
			editor.backend.resume()

	def event_prepare_purge_unused_items(self):

		for name in self.item_store.unused():
			self.event_prepare_delete_item(name)

	def event_open_experiment(self, path):

		self.event_close()

	def event_prepare_regenerate(self):

		self.event_close()

	def event_register_editor(self, editor, mime_type=u'text/plain'):

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
		editor.font_size = cfg.pyqode_font_size
		editor.font_name = cfg.pyqode_font_name
		editor.show_whitespaces = cfg.pyqode_show_whitespaces
		editor.tab_length = cfg.pyqode_tab_length
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
		oslogger.debug(u'registering {}'.format(editor))

	def event_unregister_editor(self, editor):

		if editor is None:
			return
		editor.close()
		if editor in self._editors:
			self._editors.remove(editor)
		oslogger.debug(u'unregistering ({})'.format(len(self._editors)))

	def event_pyqode_set_line_wrap(self, line_wrap):

		cfg.pyqode_line_wrap = line_wrap
		for editor in self._editors:
			editor.setLineWrapMode(
				QPlainTextEdit.WidgetWidth
				if cfg.pyqode_line_wrap
				else QPlainTextEdit.NoWrap
			)

	def event_pyqode_set_show_whitespaces(self, show_whitespaces):

		cfg.pyqode_show_whitespaces = show_whitespaces
		for editor in self._editors:
			editor.show_whitespaces = cfg.pyqode_show_whitespaces

	def event_pyqode_set_show_right_margin(self, show_right_margin):

		self._toggle_mode(
			'pyqode_right_margin',
			show_right_margin,
			RightMarginMode
		)

	def event_pyqode_set_show_line_numbers(self, show_line_numbers):

		self._toggle_panel(
			'pyqode_show_line_numbers',
			show_line_numbers,
			LineNumberPanel,
			Panel.Position.LEFT
		)

	def event_pyqode_set_code_folding(self, code_folding):

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

	def _toggle_mode(self, config, enabled, cls):

		cfg[config] = enabled
		for editor in self._editors:
			if enabled:
				if cls.__name__ in editor.modes.keys():
					continue
				editor.modes.append(cls())
			else:
				if cls.__name__ not in editor.modes.keys():
					continue
				editor.modes.remove(cls.__name__)
			editor.viewport().repaint()

	def _toggle_panel(self, config, enabled, cls, pos):

		cfg[config] = enabled
		for editor in self._editors:
			if enabled:
				if cls.__name__ in editor.panels._panels[pos]:
					continue
				panel = cls()
				editor.panels.append(panel, position=pos)
				editor.panels.refresh()
				panel.show()
			else:
				if cls.__name__ not in editor.panels._panels[pos]:
					continue
				editor.panels.remove(cls.__name__)
				editor.panels.refresh()

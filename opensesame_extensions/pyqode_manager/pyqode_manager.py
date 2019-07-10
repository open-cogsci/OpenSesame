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
from pyqode.core.widgets import SplittableCodeEditTabWidget, TextCodeEdit
from python_code_edit import PythonCodeEdit
from pyqode.core.api import ColorScheme
from pyqode.core.modes import PygmentsSH
from qtpy.QtGui import QFontMetrics


class pyqode_manager(base_extension):

	"""
	desc:
		Keeps track of all PyQode editor instances, which need to be explicitly
		closed. And also modifies their behavior somewhat.
	"""

	def event_startup(self):

		SplittableCodeEditTabWidget().register_code_edit(PythonCodeEdit)
		SplittableCodeEditTabWidget().register_code_edit(TextCodeEdit)
		self._editors = []

	def event_close(self):

		oslogger.debug(u'closing ({})'.format(len(self._editors)))
		while self._editors:
			self._editors.pop().close()

	def event_prepare_delete_item(self, name):

		item = self.item_store[name]
		if item.item_type == u'inline_script':
			self.event_unregister_editor(item._pyqode_run_editor)
			self.event_unregister_editor(item._pyqode_prepare_editor)
		if hasattr(self, u'auto_editor'):
			for editor in self.auto_editor.values():
				self.event_unregister_editor(editor)
		self.event_unregister_editor(item._script_widget)

	def event_prepare_purge_unused_items(self):

		for name in self.item_store.unused():
			self.event_prepare_delete_item(name)

	def event_open_experiment(self, path):

		self.event_close()

	def event_prepare_regenerate(self):

		self.event_close()

	def event_register_editor(self, editor, mime_type=u'text/plain'):

		self._editors.append(editor)
		if u'PythonSH' in editor.modes.keys():
			pass
		elif u'TextSH' in editor.modes.keys():
			editor.modes.get(u'TextSH').color_scheme = cfg.pyqode_color_scheme
		else:
			sh = PygmentsSH(
				editor.document(),
				color_scheme=ColorScheme(u'monokai')
			)
			sh.set_mime_type(mime_type)
			editor.modes.append(sh)
		editor.font_size = cfg.pyqode_font_size
		editor.font_name = cfg.pyqode_font_name
		editor.show_whitespaces = cfg.pyqode_show_whitespaces
		editor.tab_length = cfg.pyqode_tab_length
		editor.setTabStopWidth(
			QFontMetrics(
				editor.font()
			).averageCharWidth() * cfg.pyqode_tab_length
		)
		editor.use_spaces_instead_of_tabs = cfg.pyqode_use_spaces_instead_of_tabs
		editor.action_duplicate_line.setShortcut(u'Ctrl+Shift+D')
		oslogger.debug(u'registering {}'.format(editor))

	def event_unregister_editor(self, editor):

		editor.close()
		self._editors.remove(editor)
		oslogger.debug(u'unregistering ({})'.format(len(self._editors)))

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
from qtpy.QtWidgets import QSizePolicy
from qtpy.QtCore import Qt
from libopensesame.inline_script import inline_script as inline_script_runtime
from libqtopensesame.items.qtplugin import qtplugin
from libqtopensesame.items.qtitem import wait_cursor
from libqtopensesame.misc.translate import translation_context
_ = translation_context(u'inline_script', category=u'item')


class inline_script(inline_script_runtime, qtplugin):

	"""The inline_script GUI controls"""

	description = _(u'Executes Python code')
	help_url = u'manual/python/about'
	ext = u'.py'
	mime_type = u'text/x-python'

	def __init__(self, name, experiment, string=None):

		"""See item."""

		inline_script_runtime.__init__(self, name, experiment, string)
		qtplugin.__init__(self)

	def apply_edit_changes(self):

		"""See qtitem."""

		sp = self._pyqode_prepare_editor.toPlainText()
		sr = self._pyqode_run_editor.toPlainText()
		self._set_modified()
		self.var._prepare = sp
		self.var._run = sr
		qtplugin.apply_edit_changes(self)

	def _set_modified(self, prepare=False, run=False):

		"""
		desc:
			Sets the modified status of the editors.
		"""

		self._pyqode_prepare_editor.document().setModified(prepare)
		self._pyqode_run_editor.document().setModified(run)
		self._pyqode_tab_bar.setTabText(
			0,
			(u'* ' if prepare else u'') + _(u'Prepare')
		)
		self._pyqode_tab_bar.setTabText(
			1,
			(u'* ' if prepare else u'') + _(u'Run')
		)

	def set_focus(self):

		"""
		desc:
			Allows the item to focus the most important widget.
		"""

		self._pyqode_tab_widget.setFocus()

	@wait_cursor
	def init_edit_widget(self):

		"""See qtitem."""

		from pyqode.core.widgets import SplittableCodeEditTabWidget

		qtplugin.init_edit_widget(self, stretch=False)
		self._pyqode_tab_widget = SplittableCodeEditTabWidget()
		self._pyqode_tab_widget.setSizePolicy(
			QSizePolicy.Expanding,
			QSizePolicy.Expanding
		)
		self._pyqode_tab_widget.main_tab_widget.setCornerWidget(None)
		self._pyqode_tab_bar = self._pyqode_tab_widget.main_tab_widget.tabBar()
		self._pyqode_tab_bar.setTabsClosable(False)
		self._pyqode_tab_bar.setContextMenuPolicy(Qt.NoContextMenu)
		self._pyqode_tab_widget.main_tab_widget.setMovable(False)
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

		"""See qtitem."""

		qtplugin.edit_widget(self)
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

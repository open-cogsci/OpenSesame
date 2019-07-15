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
from libopensesame.oslogging import oslogger
from pyqode.core import api
from libqtopensesame.misc.config import cfg
from libqtopensesame.misc.translate import translation_context
_ = translation_context(u'pyqode_manager', category=u'extension')


class AutodetectIndentationMode(api.Mode):

	"""Automatically sets indentation based on editor contents."""

	def on_install(self, editor):

		super(AutodetectIndentationMode, self).on_install(editor)
		self.editor.new_text_set.connect(self._autodetect_indentation)
		self._autodetect_indentation()

	def _autodetect_indentation(self):

		if cfg.pyqode_indentation == 'spaces':
			self._set_space_indentation()
			return
		if cfg.pyqode_indentation == 'tabs':
			self._set_tab_indentation()
			return
		code = self.editor.toPlainText()
		match_tabs = re.findall(u'(?<=\n)\t+', code)
		match_spaces = re.findall(
			u'(?<=\n)({})+'.format(u' ' * cfg.pyqode_tab_length),
			code
		)
		if len(match_tabs) > len(match_spaces):
			oslogger.debug(u'detected tab-based indentation')
			self._set_tab_indentation()
		else:
			oslogger.debug(u'detected space-based indentation')
			self._set_space_indentation()

	def _set_tab_indentation(self):

		if hasattr(self.editor, u'space_indentation_modes'):
			for mode in self.editor.space_indentation_modes:
				mode.enabled = False
		if hasattr(self.editor, u'tab_indentation_modes'):
			for mode in self.editor.tab_indentation_modes:
				mode.enabled = True
		self.editor.use_spaces_instead_of_tabs = False

	def _set_space_indentation(self):

		if hasattr(self.editor, u'space_indentation_modes'):
			for mode in self.editor.space_indentation_modes:
				mode.enabled = True
		if hasattr(self.editor, u'tab_indentation_modes'):
			for mode in self.editor.tab_indentation_modes:
				mode.enabled = False
		self.editor.use_spaces_instead_of_tabs = True

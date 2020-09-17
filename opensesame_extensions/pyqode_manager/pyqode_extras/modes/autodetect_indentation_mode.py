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

THRESHOLD = 500


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
		code = self.editor.toPlainText().replace(u'\u2029', u'\n')
		tab_length = self._guess_indentation_width(code)
		match_tabs = re.findall(u'((?<=\n)\t+)|(\A\t+)', code)
		match_spaces = re.findall(
			u'((?<=\n){indent}+)|(\A{indent}+)'.format(
				indent=u' ' * tab_length
			),
			code
		)
		if len(match_tabs) > len(match_spaces):
			oslogger.debug(u'detected tab-based indentation')
			self._set_tab_indentation()
		else:
			oslogger.debug(
				u'detected space-based indentation (width={})'.format(
					tab_length
				)
			)
			self._set_space_indentation(tab_length)

	def _set_tab_indentation(self):

		self.editor.use_spaces_instead_of_tabs = False

	def _set_space_indentation(self, tab_length):

		self.editor.use_spaces_instead_of_tabs = True
		self.editor.tab_length = tab_length

	def _guess_indentation_width(self, code):
		
		i2 = i3 = i4 = 0
		for line in code.splitlines():
			n_indent = len(line) - len(line.lstrip(u' '))
			if not n_indent % 4:
				i4 += 1
				i3 -= 1
			elif not n_indent % 2:
				i2 += 1
				i4 -= 1
				i3 -= 1
			elif not n_indent % 3:
				i3 += 1
				i2 -= 1
				i4 -= 1
			if i4 - i2 > THRESHOLD and i4 - i3 > THRESHOLD:
				return 4
			if i3 - i2 > THRESHOLD and i3 - i4 > THRESHOLD:
				return 3
			if i2 - i3 > THRESHOLD and i2 - i3 > THRESHOLD:
				return 2
		if i4 > max(i2, i3):
			return 4
		if i3 > max(i2, i4):
			return 3
		if i2 > max(i4, i3):
			return 2
		return cfg.pyqode_tab_length

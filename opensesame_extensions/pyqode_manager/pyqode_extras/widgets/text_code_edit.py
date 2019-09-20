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
import sys
from libqtopensesame.misc.config import cfg
from pyqode.core.managers import BackendManager
from pyqode.core.backend import server
from pyqode.core import panels, modes
from pyqode.core.api import (
	CodeEdit,
	Panel,
	SyntaxHighlighter,
	ColorScheme
)


class TextSH(SyntaxHighlighter):

	def highlight_block(self, text, user_data):

		pass


class TextCodeEdit(CodeEdit):

	mimetypes = ['text/x-plain', 'text/x-log', 'text/plain']

	def __init__(self, parent=None):

		_reset_stylesheet = self._reset_stylesheet
		self._reset_stylesheet = lambda: None
		super(TextCodeEdit, self).__init__(parent)
		self._backend = BackendManager(self)
		self.backend.start(
			server.__file__,
			sys.executable,
			reuse=True,
			share_id='text'
		)
		# append panels
		self.panels.append(
			panels.SearchAndReplacePanel(),
			Panel.Position.BOTTOM
		)
		self.panels.append(panels.FoldingPanel())
		self.panels.append(panels.LineNumberPanel())
		# append modes
		self.modes.append(modes.AutoCompleteMode())
		self.modes.append(modes.ExtendedSelectionMode())
		self.modes.append(modes.CaseConverterMode())
		self.modes.append(modes.FileWatcherMode())
		self.modes.append(modes.CaretLineHighlighterMode())
		self.modes.append(modes.RightMarginMode())
		self.modes.append(
			TextSH(
				self.document(),
				color_scheme=ColorScheme(cfg.pyqode_color_scheme)
			)
		)
		self.modes.append(modes.ZoomMode())
		self.modes.append(modes.CodeCompletionMode())
		self.modes.append(modes.AutoIndentMode())
		self.modes.append(modes.IndenterMode())
		self.modes.append(modes.SymbolMatcherMode())
		self.panels.append(panels.EncodingPanel(), Panel.Position.TOP)
		self.panels.append(panels.ReadOnlyPanel(), Panel.Position.TOP)
		self._reset_stylesheet = _reset_stylesheet

	def setPlainText(self, txt, mime_type='', encoding=''):

		super(TextCodeEdit, self).setPlainText(
			txt,
			mime_type,
			encoding
		)

	def clone(self):

		clone = self.__class__(parent=self.parent())
		return clone

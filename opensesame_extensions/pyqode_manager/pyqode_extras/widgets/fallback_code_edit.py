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
from pyqode.core import panels, modes
from pyqode.core.backend import server
from pyqode.core.api import (
	CodeEdit,
	Panel,
	CharBasedFoldDetector,
	IndentFoldDetector,
	ColorScheme
)

# For markdown it's annoying if quotes are autocompleted
DISABLE_AUTO_COMPLETE_QUOTES = ['markdown']


class FallbackCodeEdit(CodeEdit):

	# generic
	mimetypes = []

	#: the list of mimetypes that use char based fold detector
	_char_based_mimetypes = [
		'text/x-php',
		'text/x-c++hdr',
		'text/x-c++src',
		'text/x-chdr',
		'text/x-csrc',
		'text/x-csharp',
		'text/x-plain',
		'application/javascript'
	]

	def __init__(self, parent=None):

		super(FallbackCodeEdit, self).__init__(parent)
		self.backend.start(
			server.__file__,
			sys.executable,
			reuse=False
		)
		if cfg.pyqode_show_line_numbers:
			self.panels.append(panels.LineNumberPanel())
		self.panels.append(
			panels.SearchAndReplacePanel(),
			Panel.Position.BOTTOM
		)
		if cfg.pyqode_code_folding:
			self.panels.append(panels.FoldingPanel())
		self.modes.append(modes.CursorHistoryMode())
		self.modes.append(modes.AutoCompleteMode())
		self.modes.append(modes.ExtendedSelectionMode())
		self.modes.append(modes.CaseConverterMode())
		self.modes.append(modes.FileWatcherMode())
		if cfg.pyqode_highlight_caret_line:
			self.modes.append(modes.CaretLineHighlighterMode())
		if cfg.pyqode_right_margin:
			self.modes.append(modes.RightMarginMode())
		self.modes.append(modes.PygmentsSyntaxHighlighter(
			self.document(),
			color_scheme=ColorScheme(cfg.pyqode_color_scheme))
		)
		self.modes.append(modes.ZoomMode())
		self.modes.append(modes.CodeCompletionMode())
		self.modes.append(modes.AutoIndentMode())
		self.modes.append(modes.IndenterMode())
		self.modes.append(modes.SymbolMatcherMode())
		self.modes.append(modes.SmartBackSpaceMode())
		self.panels.append(panels.EncodingPanel(), Panel.Position.TOP)
		self.panels.append(panels.ReadOnlyPanel(), Panel.Position.TOP)

	def setPlainText(self, txt, mime_type='', encoding=''):

		if not mime_type:
			mime_type = self.file.mimetype
		if not encoding:
			encoding = self.file.encoding
		if mime_type != u'text/x-plain':
			try:
				self.syntax_highlighter.set_lexer_from_mime_type(mime_type)
			except Exception:
				# The syntax_highlighter may not exist, or there may not be a lexer
				# for the mime type
				pass
			else:
				if mime_type in self._char_based_mimetypes:
					self.syntax_highlighter.fold_detector = CharBasedFoldDetector()
				else:
					self.syntax_highlighter.fold_detector = IndentFoldDetector()
		if self.language in DISABLE_AUTO_COMPLETE_QUOTES:
			self._disable_auto_complete_for_quotes()
		else:
			self._enable_auto_complete_for_quotes()
		super(FallbackCodeEdit, self).setPlainText(txt, mime_type, encoding)

	def _enable_auto_complete_for_quotes(self):

		try:
			auto_complete_mode = self.modes.get('AutoCompleteMode')
		except KeyError:
			oslogger.debug('AutoCompleteMode not enabled')
			return
		auto_complete_mode.MAPPING['\''] = '\''
		auto_complete_mode.MAPPING['"'] = '"'

	def _disable_auto_complete_for_quotes(self):

		try:
			auto_complete_mode = self.modes.get('AutoCompleteMode')
		except KeyError:
			oslogger.debug('AutoCompleteMode not enabled')
			return
		if '\'' not in auto_complete_mode.MAPPING:
			return
		del auto_complete_mode.MAPPING['\'']
		del auto_complete_mode.MAPPING['"']

	def clone(self):

		clone = self.__class__(parent=self.parent())
		return clone

	@property
	def language(self):

		filenames = self.syntax_highlighter._lexer.filenames
		if u'*.R' in filenames:
			return u'R'
		if u'*.md' in filenames:
			return u'markdown'
		return None

	def __repr__(self):

		return 'FallbackCodeEdit(path={}, language={})'.format(
			self.file.path,
			self.language
		)

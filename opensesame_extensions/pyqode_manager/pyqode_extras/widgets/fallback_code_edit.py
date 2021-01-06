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
from libopensesame.oslogging import oslogger
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
from pyqode_extras.modes import AutodetectIndentationMode

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
		self._start_backend()
		self.show_whitespaces = cfg.pyqode_show_whitespaces
		if cfg.pyqode_image_annotations:
			self.panels.append(
				panels.ImageAnnotationsPanel(),
				panels.ImageAnnotationsPanel.Position.RIGHT
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
		self.modes.append(modes.ExtendedSelectionMode())
		self.modes.append(modes.CaseConverterMode())
		self.modes.append(modes.LineSorterMode())
		self.modes.append(modes.FileWatcherMode())
		if cfg.pyqode_highlight_caret_line:
			self.modes.append(modes.CaretLineHighlighterMode())
		self.modes.append(modes.PygmentsSyntaxHighlighter(
			self.document(),
			color_scheme=ColorScheme(cfg.pyqode_color_scheme))
		)
		self.modes.append(modes.ZoomMode())
		self.modes.append(modes.AutoIndentMode())
		self.modes.append(modes.IndenterMode())
		self.modes.append(modes.SymbolMatcherMode())
		self.modes.append(modes.SmartBackSpaceMode())
		self.modes.append(AutodetectIndentationMode())
		self.panels.append(panels.EncodingPanel(), Panel.Position.TOP)
		self.panels.append(panels.ReadOnlyPanel(), Panel.Position.TOP)
		if cfg.pyqode_fixed_width:
			self.panels.append(
				panels.MarginPanel(nchar=cfg.pyqode_fixed_width_nchar),
				Panel.Position.LEFT
			)
		if cfg.pyqode_right_margin:
			rmm = modes.RightMarginMode()
			self.modes.append(rmm)
			try:
				rmm.color = self.syntax_highlighter.formats['comment'] \
					.foreground().color()
			except Exception as e:  # Don't know how safe this is
				pass
		self._set_comment_mode()
		
	def _start_backend(self):
		
		self._backend.start(
			server.__file__,
			sys.executable,
			reuse=True
		)
		
	def _set_comment_mode(self):
		
		comment_prefix = self.comment_prefix
		if comment_prefix:
			if 'CommentsMode' in self.modes.keys():
				self.modes.get('CommentsMode').prefix = comment_prefix
			else:
				self.modes.append(modes.CommentsMode(prefix=comment_prefix))
		elif 'CommentsMode' in self.modes.keys():
			self.modes.remove('CommentsMode')

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
		if (
			cfg.pyqode_code_completion and
			self.language not in cfg.pyqode_code_completion_excluded_mimetypes
		):
			self.modes.append(modes.AutoCompleteMode())
			self.modes.append(modes.CodeCompletionMode())
			# The AutoIndentMode should catch key presses after the
			# CodeCompletionMode, otherwise code completions will have an ugly
			# newline in it. Toggling the state accomplishes this, although
			# it's an ugly hack.
			if 'AutoIndentMode' in self.modes.keys():
				auto_indent_mode = self.modes.get('AutoIndentMode')
				if auto_indent_mode.enabled:
					auto_indent_mode.enabled = False
					auto_indent_mode.enabled = True
		self._set_comment_mode()

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
		if u'*.js' in filenames:
			return u'javascript'
		return u'unknown'
		
	@property
	def comment_prefix(self):
		
		lang = self.language
		if lang == 'R':
			return '# '
		if lang == 'javascript':
			return '// '

	def __repr__(self):

		return 'FallbackCodeEdit(path={}, language={})'.format(
			self.file.path,
			self.language
		)

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
import sys
from pyqode.core.api import ColorScheme
from pyqode.python.backend import server
from pyqode.core import api
from pyqode.core import modes
from pyqode.core import panels
from pyqode.python import modes as pymodes
from pyqode.python import panels as pypanels
from pyqode.python.backend.workers import defined_names
from pyqode.python.folding import PythonFoldDetector
from pyqode.python.widgets.code_edit import PyCodeEditBase


class PythonCodeEdit(PyCodeEditBase):

	"""
	desc:
		A slightly modified version of the default PyCodeEdit that takes into
		account the OpenSesame configuration.
	"""

	DARK_STYLE = 0
	LIGHT_STYLE = 1

	mimetypes = ['text/x-python']

	def __init__(self, parent):

		super(PythonCodeEdit, self).__init__(
			parent=parent,
			create_default_actions=True
		)
		self.backend.start(
			server.__file__,
			sys.executable,
			reuse=False
		)
		self.setLineWrapMode(self.NoWrap)
		self.modes.append(modes.OutlineMode(defined_names))
		self.panels.append(
			panels.SearchAndReplacePanel(),
			panels.SearchAndReplacePanel.Position.BOTTOM
		)
		self.panels.append(panels.FoldingPanel())
		self.panels.append(panels.LineNumberPanel())
		self.panels.append(panels.CheckerPanel())
		self.panels.append(
			panels.GlobalCheckerPanel(),
			panels.GlobalCheckerPanel.Position.RIGHT
		)
		self.add_separator()
		self.modes.append(modes.ExtendedSelectionMode())
		self.modes.append(modes.CaseConverterMode())
		self.modes.append(modes.FileWatcherMode())
		self.modes.append(modes.ZoomMode())
		self.modes.append(modes.SymbolMatcherMode())
		self.modes.append(modes.OccurrencesHighlighterMode())
		self.modes.append(pymodes.CommentsMode())
		if cfg.pyqode_highlight_caret_line:
			self.modes.append(modes.CaretLineHighlighterMode())
		if cfg.pyqode_right_margin:
			self.modes.append(modes.RightMarginMode())
		if cfg.pyqode_code_completion:
			self.modes.append(modes.CodeCompletionMode())
			self.modes.append(pymodes.PyAutoCompleteMode())
			self.modes.append(pymodes.CalltipsMode())
		if cfg.pyqode_smart_editing:
			self.modes.append(pymodes.PyAutoIndentMode())
			self.modes.append(pymodes.PyIndenterMode())
			self.modes.append(modes.SmartBackSpaceMode())
		else:
			self.modes.append(modes.IndenterMode())
		if cfg.pyqode_pyflakes_validation:
			self.modes.append(pymodes.PyFlakesChecker())
		if cfg.pyqode_pep8_validation:
			self.modes.append(pymodes.PEP8CheckerMode())
		self.modes.append(pymodes.PythonSH(
			self.document(),
			color_scheme=ColorScheme(cfg.pyqode_color_scheme))
		)
		self.syntax_highlighter.fold_detector = PythonFoldDetector()
		self.panels.append(panels.EncodingPanel(), api.Panel.Position.TOP)
		self.panels.append(panels.ReadOnlyPanel(), api.Panel.Position.TOP)

	def clone(self):

		clone = self.__class__(
			parent=self.parent(),
			server_script=self.backend.server_script,
			interpreter=self.backend.interpreter,
			args=self.backend.args,
			color_scheme=self.syntax_highlighter.color_scheme.name
		)
		return clone

	def __repr__(self):
		return 'PythonCodeEdit(path=%r)' % self.file.path

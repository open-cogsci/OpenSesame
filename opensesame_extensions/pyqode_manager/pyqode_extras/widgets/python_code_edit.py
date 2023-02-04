# -*- coding:utf-8 -*-

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
import sys
from pyqode.core.api import ColorScheme
from pyqode.python.backend import server
from pyqode.core import api
from pyqode.core import modes
from pyqode.core import panels
from pyqode.core.managers import BackendManager
from pyqode.python import modes as pymodes
from pyqode.python.backend.workers import defined_names
from pyqode.python.folding import PythonFoldDetector
from pyqode.python.widgets.code_edit import PyCodeEditBase
from pyqode_extras.modes import (
    ConvertIndentationMode,
    AutodetectIndentationMode
)


class PythonCodeEdit(PyCodeEditBase):

    """
    desc:
            A slightly modified version of the default PyCodeEdit that takes into
            account the OpenSesame configuration.
    """

    DARK_STYLE = 0
    LIGHT_STYLE = 1

    mimetypes = ['text/x-python']
    language = u'python'

    def __init__(self, parent):

        # PsychoPy deletes the _ built-in
        if '_' not in __builtins__:
            oslogger.warning('re-installing missing gettext built-in')
            import gettext
            gettext.NullTranslations().install()
        _reset_stylesheet = self._reset_stylesheet
        self._reset_stylesheet = lambda: None
        super(PythonCodeEdit, self).__init__(parent=parent)
        self._word_separators = [
            '~', '!', '@', '#', '$', '%', '^', '&', '*', '(', ')', '+', '{',
            '}', '|', ':', "<", ">", "?", ",", "/", ";", '[',
            ']', '\\', '\n', '\t', '=', '-', ' ', u'\u2029', u'.'
        ]
        self.show_whitespaces = cfg.pyqode_show_whitespaces
        self._backend = BackendManager(self)
        self._start_backend()
        self.setLineWrapMode(self.NoWrap)
        self.modes.append(ConvertIndentationMode())
        self.panels.append(
            panels.SearchAndReplacePanel(),
            panels.SearchAndReplacePanel.Position.BOTTOM
        )
        if cfg.pyqode_image_annotations:
            self.panels.append(
                panels.ImageAnnotationsPanel(),
                panels.ImageAnnotationsPanel.Position.RIGHT
            )
        if cfg.pyqode_code_folding:
            self.panels.append(panels.FoldingPanel())
        if cfg.pyqode_show_line_numbers:
            self.panels.append(panels.LineNumberPanel())
        self.panels.append(panels.CheckerPanel())
        self.panels.append(
            panels.GlobalCheckerPanel(),
            panels.GlobalCheckerPanel.Position.RIGHT
        )
        self.add_separator()
        self.modes.append(modes.ExtendedSelectionMode())
        self.modes.append(modes.CaseConverterMode())
        self.modes.append(modes.LineSorterMode())
        self.modes.append(modes.FileWatcherMode())
        self.modes.append(modes.ZoomMode())
        self.modes.append(modes.SymbolMatcherMode())
        if cfg.pyqode_autopep8 and hasattr(pymodes, 'AutoPEP8') and py3:
            self.modes.append(pymodes.AutoPEP8(
                lookbehind=cfg.pyqode_autopep8_lookbehind,
                aggressive=cfg.pyqode_autopep8_aggressive,
                ignore=cfg.pyqode_pep8_ignore.split(u';')
            ))
        self.modes.append(pymodes.CommentsMode())
        if cfg.pyqode_highlight_caret_line:
            self.modes.append(modes.CaretLineHighlighterMode())
        if (
                cfg.pyqode_code_completion and
                self.language not in cfg.pyqode_code_completion_excluded_mimetypes
        ):
            self.modes.append(modes.CodeCompletionMode())
            self.modes.append(pymodes.PyAutoCompleteMode())
            self.modes.append(pymodes.CalltipsMode())
        self.modes.append(modes.SmartBackSpaceMode())
        self.modes.append(modes.IndenterMode())
        self.modes.append(pymodes.PyAutoIndentMode())
        self.modes.append(AutodetectIndentationMode())
        if cfg.pyqode_pyflakes_validation:
            flakes = pymodes.PyFlakesChecker()
            flakes.set_ignore_rules([
                i.strip() for i in cfg.pyqode_pyflakes_ignore.split(u';')
            ])
            self.modes.append(flakes)
        if cfg.pyqode_pep8_validation:
            pep8 = pymodes.PEP8CheckerMode()
            pep8.set_ignore_rules([
                i.strip() for i in cfg.pyqode_pep8_ignore.split(u';')
            ])
            self.modes.append(pep8)
        self.panels.append(panels.EncodingPanel(), api.Panel.Position.TOP)
        self.panels.append(panels.ReadOnlyPanel(), api.Panel.Position.TOP)
        if cfg.pyqode_fixed_width:
            self.panels.append(
                panels.MarginPanel(nchar=cfg.pyqode_fixed_width_nchar),
                api.Panel.Position.LEFT
            )
        # The PythonSH requires that _reset_stylesheet isn't dummied out
        self._reset_stylesheet = _reset_stylesheet
        self.modes.append(pymodes.PythonSH(
            self.document(),
            color_scheme=ColorScheme(cfg.pyqode_color_scheme))
        )
        self.syntax_highlighter.fold_detector = PythonFoldDetector()
        if cfg.pyqode_right_margin:
            rmm = modes.RightMarginMode()
            self.modes.append(rmm)
            try:
                rmm.color = self.syntax_highlighter.formats['comment'] \
                    .foreground().color()
            except Exception as e:  # Don't know how safe this is
                pass

    def _start_backend(self):

        self.backend.start(
            server.__file__,
            sys.executable,
            reuse=True,
            share_id='python'
        )

    def _init_actions(self, create_standard_actions):

        super(PythonCodeEdit, self)._init_actions(create_standard_actions)
        self.action_duplicate_line.setShortcut(u'Ctrl+Shift+D')

    def clone(self):

        clone = self.__class__(parent=self.parent())
        return clone

    def __repr__(self):

        return 'PythonCodeEdit(path=%r)' % self.file.path

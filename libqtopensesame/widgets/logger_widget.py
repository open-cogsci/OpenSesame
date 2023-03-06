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
from qtpy import QtWidgets
from libqtopensesame.widgets.base_widget import BaseWidget
from libqtopensesame.misc.translate import translation_context
from libqtopensesame.dialogs.text_input import TextInput
_ = translation_context(u'logger', category=u'item')


class LoggerWidget(BaseWidget):
    """The logger widget

    Parameters
    ----------
    logger: logger
        A logger object.
    """
    
    def __init__(self, logger):
        super().__init__(logger.main_window, ui=u'widgets.logger')
        self.logger = logger

    def update(self):
        self.ui.textedit_include.setPlainText('\n'.join(self.logger.logvars))
        self.ui.textedit_exclude.setPlainText(
            '\n'.join(self.logger.exclude_vars))


# Alias for backwards compatibility
logger_widget = LoggerWidget

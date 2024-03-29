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
from libopensesame.feedback import Feedback as FeedbackRuntime
from libqtopensesame.items.qtplugin import QtPlugin
from libqtopensesame.items.feedpad import Feedpad
from libqtopensesame.misc.translate import translation_context
_ = translation_context(u'feeback', category=u'item')


class Feedback(Feedpad, QtPlugin, FeedbackRuntime):

    r"""The feedback controls are implemented in feedpad."""
    description = _(u'Provides feedback to the participant')

    def __init__(self, name, experiment, string=None):

        FeedbackRuntime.__init__(self, name, experiment, string)
        QtPlugin.__init__(self)

    def init_edit_widget(self):

        Feedpad.init_edit_widget(self)
        self.auto_add_widget(self.sketchpad_widget.ui.checkbox_reset_variables,
                             u'reset_variables')


# Alias for backwards compatibility
feedback = Feedback

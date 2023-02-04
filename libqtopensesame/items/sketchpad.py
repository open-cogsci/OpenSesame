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
from libopensesame.sketchpad import sketchpad as sketchpad_runtime
from libqtopensesame.items.qtplugin import qtplugin
from libqtopensesame.items.feedpad import feedpad
from libqtopensesame.misc.translate import translation_context
_ = translation_context(u'sketchpad', category=u'item')


class sketchpad(feedpad, qtplugin, sketchpad_runtime):

    """
    desc:
            The sketchpad controls are implemented in feedpad.
    """

    description = _(u'Displays stimuli')

    def __init__(self, name, experiment, string=None):

        sketchpad_runtime.__init__(self, name, experiment, string)
        qtplugin.__init__(self)

    def init_edit_widget(self):
        """
        desc:
                Initializes the widget.
        """

        feedpad.init_edit_widget(self)
        self.sketchpad_widget.ui.widget_settings_reset_variables.hide()

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
from libqtopensesame.misc.base_subcomponent import base_subcomponent
from qtpy import QtCore, QtWidgets
from libqtopensesame.misc.translate import translation_context
_ = translation_context(u'sketchpad', category=u'item')


class sketchpad_element_button(base_subcomponent, QtWidgets.QPushButton):

    """
    desc:
            A element-tool button for the sketchpad widget.
    """

    def __init__(self, sketchpad_widget, element):
        """
        desc:
                Constructor.

        arguments:
                sketchpad_widget:
                        type:	sketchpad-widget
                element:
                        type:	base_element
        """

        super(sketchpad_element_button, self).__init__(sketchpad_widget)
        self.element = element
        self.sketchpad_widget = sketchpad_widget
        self.setup(sketchpad_widget)
        self.setFlat(True)
        self.setCheckable(True)
        self.setIcon(self.theme.qicon(u'os-%s' % self.name))
        self.setToolTip(_(u'Draw %s element') % self.name)
        self.clicked.connect(self.select)

    def select(self, checked):
        """
        desc:
                Select this element tool.
        """

        self.sketchpad_widget.unselect_all_tools()
        self.setChecked(True)
        self.sketchpad_widget.select_element_tool(self.element)

    @property
    def name(self):
        return self.element.__name__

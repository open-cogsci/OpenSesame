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
from libqtopensesame.misc.base_subcomponent import BaseSubcomponent
from qtpy.QtWidgets import QPushButton
from libqtopensesame.misc.translate import translation_context
from libopensesame.misc import snake_case
_ = translation_context(u'sketchpad', category=u'item')


class SketchpadElementButton(BaseSubcomponent, QPushButton):

    r"""A element-tool button for the sketchpad widget."""
    def __init__(self, sketchpad_widget, element):
        r"""Constructor.

        Parameters
        ----------
        sketchpad_widget : sketchpad-widget
        element : base_element
        """
        super().__init__(sketchpad_widget)
        self.element = element
        self.sketchpad_widget = sketchpad_widget
        self.setup(sketchpad_widget)
        self.setFlat(True)
        self.setCheckable(True)
        self.setIcon(self.theme.qicon(u'os-%s' % self.name))
        self.setToolTip(_(u'Draw %s element') % self.name)
        self.clicked.connect(self.select)

    def select(self, checked):
        r"""Select this element tool."""
        self.sketchpad_widget.unselect_all_tools()
        self.setChecked(True)
        self.sketchpad_widget.select_element_tool(self.element)

    @property
    def name(self):
        return snake_case(self.element.__name__)


# Alias for backwards compatibility
sketchpad_element_button = SketchpadElementButton

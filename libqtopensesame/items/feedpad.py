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
from libqtopensesame.misc.sketchpad_canvas import sketchpad_canvas
from libqtopensesame.widgets.sketchpad_widget import sketchpad_widget
from libqtopensesame.items.qtplugin import qtplugin
from libqtopensesame import sketchpad_elements
from libqtopensesame.validators import duration_validator


class feedpad(object):

    """
    desc:
            Controls for the sketchpad item.
    """

    help_url = u'manual/stimuli/visual'
    lazy_init = True

    def init_edit_widget(self):
        """
        desc:
                Initializes the widget.
        """

        qtplugin.init_edit_widget(self, False)
        self.canvas = sketchpad_canvas(self)
        self.sketchpad_widget = sketchpad_widget(self)
        self.add_widget(self.sketchpad_widget)
        self.auto_add_widget(self.sketchpad_widget.ui.edit_duration,
                             u'duration')
        self.sketchpad_widget.ui.edit_duration.setValidator(
            duration_validator(self))
        self.first_refresh = True
        self._lock = False

    def apply_script_changes(self):
        """See qtitem."""

        # Without this hack, the script changes will automatically trigger a
        # draw(), which triggers a call to apply_edit_changes, which updates the
        # script. To avoid this feedback loop, temporarily disable apply edit
        # changes.
        f = self.apply_edit_changes
        self.apply_edit_changes = lambda: None
        qtplugin.apply_script_changes(self)
        self.apply_edit_changes = f

    def element_module(self):
        """
        returns:
                desc:	The module that contains the sketchpad elements.
                type:	module
        """

        return sketchpad_elements

    def set_focus(self):
        """
        desc:
                Allows the item to focus the most important widget.
        """

        self.sketchpad_widget.ui.edit_duration.setFocus()

    def edit_widget(self):
        """
        desc:
                Updates the widget.
        """

        qtplugin.edit_widget(self)
        self.sketchpad_widget.initialize()
        self.sketchpad_widget.draw()
        if self.first_refresh:
            self.sketchpad_widget.center()
            self.sketchpad_widget.zoom_fit()
            self.first_refresh = False

    def add_element(self, element):
        """
        desc:
                Adds an element to the sketchpad.

        arguments:
                element:
                        desc:	The element to add.
                        type:	base_element
        """

        if element is None:
            return
        self.elements.append(element)
        self.draw()
        for element in self.elements:
            element.select(False)
        element.select()

    def selected_elements(self):
        """
        desc:
                Gets selected elements.

        returns:
                desc:	A list of selected elements.
                type:	list
        """

        l = []
        for element in self.elements:
            if element.selected:
                l.append(element)
        return l

    def remove_elements(self, elements):
        """
        desc:
                Removes elements.

        arguments:
                elements:
                        desc:	A list of elements to be removed.
                        type:	list
        """

        for element in elements:
            self.elements.remove(element)

    def move_elements(self, elements, dx=0, dy=0):
        """
        desc:
                Moves elements.

        arguments:
                elements:
                        desc:	A list of elements to be moved.
                        type:	list

        keywords:
                dx:
                        desc:	A horizontal displacement.
                        type:	[int, float]
                dy:
                        desc:	A vertical displacement
                        type:	[int, float]
        """

        for element in elements:
            element.move(dx, dy)

    def topleft_elements_pos(self, elements):
        """
        desc:
                Gets the top-left position of a set of elements.

        arguments:
                elements:
                        desc:	A list of elements.
                        type:	list

        returns:
                desc:		An (x,y) tuple with the top-left position.
                type:		tuple.
        """

        lx = []
        ly = []
        for element in elements:
            x, y = element.get_pos()
            lx.append(x)
            ly.append(y)
        return min(lx), min(ly)

    def set_elements_pos(self, elements, x=0, y=0):
        """
        desc:
                Sets position of elements.

        arguments:
                elements:
                        desc:	A list of elements to be positioned.
                        type:	list

        keywords:
                x:
                        desc:	A horizontal position.
                        type:	[int, float]
                y:
                        desc:	A vertical position
                        type:	[int, float]
        """

        mx, my = self.topleft_elements_pos(elements)
        for element in elements:
            dx, dy = element.get_pos()
            dx -= mx
            dy -= my
            element.set_pos(x+dx, y+dy)

    def min_z_index(self):
        """
        desc:
                Gets the z-index of the top item (i.e. in front of all other items).

        returns:
                desc:	A z-index.
                type:	int
        """

        return min([
            element.z_index
            for element in self.elements
            if isinstance(element.z_index, (int, float))
        ])

    def max_z_index(self):
        """
        desc:
                Gets the z-index of the bottom item (i.e. below all other items).

        returns:
                desc:	A z-index.
                type:	int
        """

        return max([
            element.z_index
            for element in self.elements
            if isinstance(element.z_index, (int, float))
        ])

    @property
    def current_color(self):
        return self.sketchpad_widget.current_color

    @property
    def current_penwidth(self):
        return self.sketchpad_widget.current_penwidth

    @property
    def current_arrow_head_width(self):
        return self.sketchpad_widget.current_arrow_head_width

    @property
    def current_arrow_body_width(self):
        return self.sketchpad_widget.current_arrow_body_width

    @property
    def current_arrow_body_length(self):
        return self.sketchpad_widget.current_arrow_body_length

    @property
    def current_scale(self):
        return self.sketchpad_widget.current_scale

    @property
    def current_rotation(self):
        return self.sketchpad_widget.current_rotation

    @property
    def current_show_if(self):
        return self.sketchpad_widget.current_show_if

    @property
    def current_fill(self):
        return self.sketchpad_widget.current_fill

    @property
    def current_center(self):
        return self.sketchpad_widget.current_center

    @property
    def current_font_family(self):
        return self.sketchpad_widget.current_font_family

    @property
    def current_font_size(self):
        return self.sketchpad_widget.current_font_size

    @property
    def current_font_bold(self):
        return self.sketchpad_widget.current_font_bold

    @property
    def current_font_italic(self):
        return self.sketchpad_widget.current_font_italic

    @property
    def current_html(self):
        return self.sketchpad_widget.current_html

    @property
    def draw(self):
        return self.sketchpad_widget.draw

    @property
    def set_cursor_pos(self):
        return self.sketchpad_widget.set_cursor_pos

    @property
    def graphics_view(self):
        return self.sketchpad_widget.ui.graphics_view

    @property
    def zoom_diff(self):
        return self.sketchpad_widget.zoom_diff

    @property
    def show_element_settings(self):
        return self.sketchpad_widget.show_element_settings

    @property
    def select_pointer_tool(self):
        return self.sketchpad_widget.select_pointer_tool

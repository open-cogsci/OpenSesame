# -*- coding:utf-8 -*-

"""
This file is part of openexp.

openexp is free software: you can redistribute it and/or modify
it under the terms of the GNU General Public License as published by
the Free Software Foundation, either version 3 of the License, or
(at your option) any later version.

openexp is distributed in the hope that it will be useful,
but WITHOUT ANY WARRANTY; without even the implied warranty of
MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
GNU General Public License for more details.

You should have received a copy of the GNU General Public License
along with openexp.  If not, see <http://www.gnu.org/licenses/>.
"""

from libopensesame.py3compat import *
from libopensesame.exceptions import osexception
from qtpy import QtWidgets, QtGui
from libqtopensesame.misc.translate import translation_context
from libqtopensesame.dialogs.text_input import TextInput
_ = translation_context(u'sketchpad', category=u'item')


class BaseElement:

    """
    desc:
            A base class for the sketchpad-element GUIs.
    """

    def __init__(self, sketchpad, string=None, properties=None):
        """
        desc:
                Constructor.

        arguments:
                sketchpad:	A sketchpad object.
                type:		sketchpad

        keywords:
                string:
                        desc:	An element-definition string.
                        type:	[str, unicode, NoneType]
                properties:
                        desc:	A dictionary with element properties. If a dictionary
                                        is provided, the string keyword is ignored, and a
                                        definition string is created from the properties dict.
                        type:	[dict, NoneType]
        """

        if properties is not None:
            string = u'draw %s' % (self.__class__.__name__)
            for var, val in properties.items():
                string += u' %s="%s"' % (var, val)
        super(base_element, self).__init__(sketchpad, string)
        # The GUI canvas uses the OpenSesame frame of reference, so we don't
        # need to convert the coordinates.
        self.fix_coordinates = False
        self.selected = False
        self.highlighted = False
        self.graphics_item = None

    @property
    def main_window(self):
        return self.experiment.main_window

    @property
    def theme(self):
        return self.experiment.main_window.theme

    @property
    def console(self):
        return self.experiment.main_window.console

    def draw(self):
        """
        desc:
                Draw this element, without redrawing the entire sketchpad.
        """

        self.graphics_item = super(base_element, self).draw()
        self.graphics_item.element = self
        self.graphics_item.setToolTip(self.to_string())
        self.update()

    def move(self, dx=0, dy=0):
        """
        desc:
                Moves the element position.

        keywords:
                dx:		The horizontal movement.
                dy:		The vertical movement.
        """

        for var, val in self.properties.items():
            if var in [u'x', u'x1', u'x2'] and \
                    isinstance(self.properties[var], (int, float)):
                self.properties[var] += dx
            if var in [u'y', u'y1', u'y2'] and \
                    isinstance(self.properties[var], (int, float)):
                self.properties[var] += dy

    def set_pos(self, x=0, y=0):
        """
        desc:
                Sets the element position.

        keywords:
                x:		The horizontal position.
                y:		The vertical position.
        """

        self.properties[u'x'] = x
        self.properties[u'y'] = y

    def get_pos(self):
        """
        desc:
                Gets the element position.

        returns:
                desc:	An (x,y) tuple.
                type:	tuple
        """

        if u'x' in self.properties:
            return self.properties[u'x'], self.properties[u'y']
        return self.properties[u'x1'], self.properties[u'y1']

    def update(self):
        """
        desc:
                Redraws this element.
        """

        if self.graphics_item is None:
            # Sometimes update is called before draw, and the graphics_item
            # doesn't exist yet.
            return
        if self.highlighted:
            self.graphics_item.setGraphicsEffect(self.highlighted_effect())
        elif self.selected:
            self.graphics_item.setGraphicsEffect(self.selected_effect())
        else:
            self.graphics_item.setGraphicsEffect(None)

    def highlight(self, highlighted=True):
        """
        desc:
                Sets the highlight status of the element and redraws.

        arguments:
                highlighted:	A bool indicating the highlight status.
        """

        self.highlighted = highlighted
        self.update()

    def select(self, selected=True):
        """
        desc:
                Sets the selected status of the element and redraws.

        arguments:
                selected:	A bool indicating the selected status.
        """

        self.selected = selected
        self.update()

    def selected_effect(self):
        """
        desc:
                Creates the selected effect.

        returns:
                A QGraphicsEffect object.
        """

        effect = QtWidgets.QGraphicsDropShadowEffect()
        effect.setColor(QtGui.QColor('#00FF00'))
        effect.setBlurRadius(32)
        effect.setOffset(8, 8)
        return effect

    def highlighted_effect(self):
        """
        desc:
                Creates the highlighted effect.

        returns:
                A QGraphicsEffect object.
        """

        effect = QtWidgets.QGraphicsOpacityEffect()
        return effect

    def get_property(self, name, _type=str, fallback=None):
        """
        desc:
                Gets an element property.

        arguments:
                name:	The property name.

        keywords:
                _type:		The property type.
                fallback:	A fallback value, in case the value cannot be cast to
                                        the requested type.

        returns:
                The property in the specified type, or None if the property doesn't
                exist.
        """

        properties = self.eval_properties()
        if name not in properties:
            return None
        val = properties[name]
        if _type == str:
            return str(val)
        if _type == int:
            try:
                return int(val)
            except ValueError:
                return fallback
        if _type == float:
            try:
                return float(val)
            except ValueError:
                return fallback
        if _type == bool:
            if isinstance(val, str):
                if val in (u'yes', u'1'):
                    return True
                if val in (u'no', u'0'):
                    return False
                return fallback
            return bool(val)
        raise osexception(u'Unknown type: %s' % _type)

    def set_property(self, name, val, yes_no=False):
        """
        desc:
                Sets an element property.

        arguments:
                name:	The property name.
                val:	The property value.

        keywords:
                yes_no:	Indicates whether the value should be treated as a bool and
                                recoded to yes/ no.
        """

        if name not in self.properties:
            return None
        if yes_no:
            if val:
                val = u'yes'
            else:
                val = u'no'
        self.properties[name] = val

    def script_validator(self, s):
        """
        desc:
                Validates an element script.

        arguments:
                s:
                        desc:	An element script.
                        type:	str

        returns:
                desc:	True if the script is valid, False otherwise.
                type:	bool
        """

        return u'\n' not in s

    def show_script_edit_dialog(self):
        """
        desc:
                Shows the script-edit dialog.
        """

        old_string = self.to_string()
        string = TextInput(self.sketchpad._edit_widget,
                           msg=_(u'Element script'), content=self.to_string(),
                           validator=self.script_validator).get_input()
        if string is None:
            return
        try:
            self.from_string(string)
        except osexception as e:
            self.experiment.notify(e)
            self.console.write(e)
            self.from_string(old_string)
            return
        self.sketchpad.draw()

    def show_edit_dialog(self):
        """
        desc:
                Shows an edit dialog for the element, typically to edit the element
                script.
        """

        self.show_script_edit_dialog()

    def show_context_menu(self, pos):
        """
        desc:
                Shows a context menu for the element.

        arguments:
                pos:
                        type:	QPoint
        """

        from libqtopensesame._input.popup_menu import popup_menu
        pm = popup_menu(self.main_window, [
            (0, _(u'Edit script'), u'utilities-terminal'),
            (1, _(u'Raise to front'), u'go-top'),
            (2, _(u'Lower to bottom'), u'go-bottom'),
            (3, _(u'Specify polar coordinates'), u'accessories-calculator'),
            (4, _(u'Delete'), u'edit-delete'),
        ])
        resp = pm.show()
        if resp is None:
            return
        if resp == 0:
            self.show_script_edit_dialog()
        elif resp == 1:
            self.properties[u'z_index'] = self.sketchpad.min_z_index() - 1
        elif resp == 2:
            self.properties[u'z_index'] = self.sketchpad.max_z_index() + 1
        elif resp == 3:
            self.show_polar_coordinates_dialog()
        elif resp == 4:
            self.sketchpad.remove_elements([self])
        self.sketchpad.draw()

    @classmethod
    def mouse_press(cls, sketchpad, pos):
        """
        desc:
                A static method that processes mouse clicks and returns an element
                object when one has been created.

        arguments:
                sketchpad:	A sketchpad object.
                pos:		An (x,y) tuple with mouse-click coordinates.

        returns:
                An element object, or None if no element was created.
        """

        return None

    @classmethod
    def mouse_release(cls, sketchpad, pos):
        """
        desc:
                A static method that processes mouse releases and returns an element
                object when one has been created.

        arguments:
                sketchpad:	A sketchpad object.
                pos:		An (x,y) tuple with mouse-release coordinates.

        returns:
                An element object, or None if no element was created.
        """

        pass

    @classmethod
    def mouse_move(cls, sketchpad, pos):
        """
        desc:
                A static method that processes mouse moves, and gives elements the
                opportunity to update their preview.

        arguments:
                sketchpad:	A sketchpad object.
                pos:		An (x,y) tuple with mousecoordinates.
        """

        pass

    @classmethod
    def reset(cls, sketchpad):

        pass

    @staticmethod
    def requires_text():
        """
        desc:
                Indicates whether the element requires text settings.

        returns:
                type:	bool
        """

        return False

    @staticmethod
    def requires_name():
        """
        desc:
                Indicates whether the element requires name settings.

        returns:
                type:	bool
        """

        return True

    @staticmethod
    def requires_penwidth():
        """
        desc:
                Indicates whether the element requires penwidth settings.

        returns:
                type:	bool
        """

        return False

    @staticmethod
    def requires_color():
        """
        desc:
                Indicates whether the element requires color settings.

        returns:
                type:	bool
        """

        return False

    @staticmethod
    def requires_arrow_head_width():
        """
        desc:
                Indicates whether the element requires arrow_head_width settings.

        returns:
                type:	bool
        """

        return False

    @staticmethod
    def requires_arrow_body_width():
        """
        desc:
                Indicates whether the element requires arrow_body_width settings.

        returns:
                type:	bool
        """

        return False

    @staticmethod
    def requires_arrow_body_length():
        """
        desc:
                Indicates whether the element requires arrow_body_length settings.

        returns:
                type:	bool
        """

        return False

    @staticmethod
    def requires_scale():
        """
        desc:
                Indicates whether the element requires scale settings.

        returns:
                type:	bool
        """

        return False

    @staticmethod
    def requires_rotation():
        """
        desc:
                Indicates whether the element requires rotation settings.

        returns:
                type:	bool
        """

        return False

    @staticmethod
    def requires_fill():
        """
        desc:
                Indicates whether the element requires fill settings.

        returns:
                type:	bool
        """

        return False

    @staticmethod
    def requires_center():
        """
        desc:
                Indicates whether the element requires center settings.

        returns:
                type:	bool
        """

        return False

    @staticmethod
    def requires_show_if():
        """
        desc:
                Indicates whether the element requires show-if settings.

        returns:
                type:	bool
        """

        return True

    @staticmethod
    def cursor():
        """
        desc:
                Indicates which cursor should be shown when the element tool is
                selected.

        returns:
                desc:	A Qt::CursorShape value
                type:	int
        """

        return u'cursor-pencil', 3, 28

    def show_polar_coordinates_dialog(self):
        """
        desc:
                The dialog for calculating cartesian coordinates from polar
                coordinates.
        """

        from libqtopensesame.dialogs.polar_coordinates import polar_coordinates

        d = polar_coordinates(self.sketchpad._edit_widget)
        xy = d.get_xy()
        if xy is None:
            return
        self.properties.update({u'x': xy[0], u'y': xy[1]})
        self.sketchpad.draw()


# Alias for backwards compatibility
base_element = BaseElement

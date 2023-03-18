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
from qtpy import QtCore, QtGui, QtWidgets
from libopensesame.exceptions import OSException
from libqtopensesame import sketchpad_elements
from libqtopensesame.widgets.sketchpad_element_button import \
    SketchpadElementButton
from libqtopensesame.widgets.base_widget import BaseWidget
from libqtopensesame.validators import CondValidator


class SketchpadWidget(BaseWidget):
    """The sketchpad controls. Most of the actual work is handled by
    libqtopensesame.misc.sketchpad_canvas.

    Parameters
    ----------
    sketchpad : sketchpad
        A sketchpad object.
    """
    
    def __init__(self, sketchpad):
        super().__init__(sketchpad.main_window, ui='widgets.sketchpad')
        self.sketchpad = sketchpad
        self.initialized = False
        self.margin = 50
        self.canvas = self.sketchpad.canvas
        self.arrow_cursor = QtGui.QCursor(
            self.theme.qpixmap('os-pointer', size=32), 8, 4)
        self.ui.graphics_view.setScene(self.canvas)
        self.ui.graphics_view.setMouseTracking(True)
        self.ui.button_pointer.clicked.connect(self.select_pointer_tool)
        self.ui.spinbox_zoom.valueChanged.connect(self.zoom)
        self.ui.spinbox_scale.valueChanged.connect(self.apply_scale)
        self.ui.spinbox_rotation.valueChanged.connect(self.apply_rotation)
        self.ui.spinbox_penwidth.valueChanged.connect(self.apply_penwidth)
        self.ui.edit_color.textEdited.connect(self.apply_color)
        self.ui.edit_show_if.editingFinished.connect(self.apply_show_if)
        self.ui.edit_show_if.setValidator(
            CondValidator(self, default='always'))
        self.ui.edit_name.editingFinished.connect(self.apply_name)
        self.ui.spinbox_arrow_head_width.valueChanged.connect(
            self.apply_arrow_head_width)
        self.ui.spinbox_arrow_body_width.valueChanged.connect(
            self.apply_arrow_body_width)
        self.ui.spinbox_arrow_body_length.valueChanged.connect(
            self.apply_arrow_body_length)
        self.ui.checkbox_center.toggled.connect(self.apply_center)
        self.ui.checkbox_fill.toggled.connect(self.apply_fill)
        self.ui.checkbox_html.toggled.connect(self.apply_html)
        self.ui.widget_font.font_changed.connect(self.apply_font)
        self.ui.checkbox_grid.toggled.connect(self.apply_grid)
        self.ui.spinbox_grid.valueChanged.connect(self.apply_grid)
        self.ui.button_zoom_fit.clicked.connect(self.zoom_fit)
        self.ui.button_zoom_1.clicked.connect(self.zoom_1)
        # Set the minimum height of the settings widget to the height that it
        # has when all controls are visible. This prevents the display from
        # jumping.
        self.ui.widget_settings.adjustSize()
        self.ui.widget_settings.setMinimumHeight(
            self.ui.widget_settings.height())
        self.build_toolbar()
        self.selected_element_tool = None
        self.set_size()
        self.init_settings()
        self.select_pointer_tool()

    @property
    def elements(self):
        return self.sketchpad.elements

    def apply_grid(self):
        if not self.ui.checkbox_grid.isChecked():
            self.canvas.grid = 1
        else:
            self.canvas.grid = self.ui.spinbox_grid.value()
        self.draw(refresh=True)

    def apply_font(self, family, size, italic, bold):
        r"""Applies changes to the font settings.

        Parameters
        ----------
        family : QString
            Font family.
        size : int
            Font size
        italic : bool
            Font italic setting
        bold : bool
            Font bold setting
        """
        for element in self.sketchpad.selected_elements():
            element.set_property('font_family', str(family))
            if size >= 0:
                element.set_property('font_size', size)
            element.set_property('font_italic', italic, yes_no=True)
            element.set_property('font_bold', bold, yes_no=True)
        self.draw()

    def apply_html(self, html):
        for element in self.sketchpad.selected_elements():
            element.set_property('html', html, yes_no=True)
        self.draw()

    def apply_fill(self, fill):
        for element in self.sketchpad.selected_elements():
            element.set_property('fill', int(fill))
        self.draw()

    def apply_scale(self, scale):
        for element in self.sketchpad.selected_elements():
            element.set_property('scale', scale)
        self.draw()

    def apply_rotation(self, rotation):
        for element in self.sketchpad.selected_elements():
            element.set_property('rotation', rotation)
        self.draw()

    def apply_center(self, center):
        for element in self.sketchpad.selected_elements():
            element.set_property('center', int(center))
        self.draw()

    def apply_color(self, color):
        color = str(color)
        for element in self.sketchpad.selected_elements():
            element.set_property('color', color)
        self.draw()

    def apply_show_if(self):
        show_if = self.ui.edit_show_if.text()
        for element in self.sketchpad.selected_elements():
            element.set_property('show_if', show_if)
            self.ui.edit_show_if.setText(show_if)
        self.draw()

    def apply_name(self):
        name = self.ui.edit_name.text()
        for element in self.sketchpad.selected_elements():
            element.set_property('name', name)
        self.draw()

    def apply_penwidth(self, penwidth):
        for element in self.sketchpad.selected_elements():
            element.set_property('penwidth', penwidth)
        self.draw()

    def apply_arrow_body_width(self, arrow_body_width):
        for element in self.sketchpad.selected_elements():
            element.set_property('arrow_body_width', arrow_body_width)
        self.draw()

    def apply_arrow_head_width(self, arrow_head_width):
        for element in self.sketchpad.selected_elements():
            element.set_property('arrow_head_width', arrow_head_width)
        self.draw()

    def apply_arrow_body_length(self, arrow_body_length):
        for element in self.sketchpad.selected_elements():
            element.set_property('arrow_body_length', arrow_body_length)
        self.draw()

    def show_element_settings(self, element):
        r"""Shows all the settings that are required by an element, and updates
        these settings based on the element.

        Parameters
        ----------
        element
            A sketchpad element.
        """
        # Float/ int properties need to be checked before they are apllied
        for prop, _type in [
                ('penwidth', int),
                ('arrow_head_width', float),
                ('arrow_body_width', float),
                ('arrow_body_length', float),
                ('scale', float),
                ('rotation', int),
                ('show_if', str),
                ('name', str),
                ('color', str),
                ('center', bool),
                ('fill', bool)
        ]:
            # Check if the selected element requires the property
            req_fnc = getattr(element, 'requires_%s' % prop)
            if not req_fnc():
                continue
            # Check if the property can be retrieved. If not, that means it's
            # variably defined, or it has an invalid type.
            try:
                val = element.get_property(prop, _type=_type)
            except OSException:
                continue
            # Adjust the widget
            if _type in (int, float):
                spinbox = getattr(self.ui, 'spinbox_%s' % prop)
                if val is None:
                    spinbox.setEnabled(False)
                    spinbox.setValue(0)
                elif isinstance(val, (int, float)):
                    spinbox.setEnabled(True)
                    if isinstance(spinbox, QtWidgets.QSpinBox):
                        val = int(val)
                    spinbox.setValue(val)
            elif _type == bool:
                checkbox = getattr(self.ui, 'checkbox_%s' % prop)
                if val is None:
                    checkbox.setEnabled(False)
                    checkbox.setChecked(False)
                else:
                    checkbox.setEnabled(True)
                    checkbox.setChecked(val)
            else:
                edit = getattr(self.ui, 'edit_%s' % prop)
                edit.setText(val)
        # Text needs special treatment
        if element.requires_text():
            family = element.get_property('font_family')
            size = element.get_property('font_size', _type=int)
            bold = element.get_property('font_bold', _type=bool)
            italic = element.get_property('font_italic', _type=bool)
            if None in (family, size, bold, italic):
                self.ui.widget_font.setEnabled(False)
            else:
                self.ui.widget_font.setEnabled(True)
                self.ui.widget_font.set_font(family=family, size=size,
                                             bold=bold, italic=italic)
            val = element.get_property('html', _type=bool)
            if val is None:
                self.ui.checkbox_html.setEnabled(False)
                self.ui.checkbox_html.setChecked(False)
            else:
                self.ui.checkbox_html.setEnabled(True)
                self.ui.checkbox_html.setChecked(val)
        self.show_element_tool_settings(element)

    def zoom_fit(self):
        r"""Sets the best-fitting zoom level."""
        w = self.sketchpad.var.width
        h = self.sketchpad.var.height
        l = -w/2
        t = -h/2
        self.ui.graphics_view.fitInView(l, t, w, h,
                                        mode=QtCore.Qt.KeepAspectRatio)
        zoom = self.ui.graphics_view.transform().m11()
        self.ui.spinbox_zoom.setValue(zoom)

    def zoom_1(self):
        r"""Sets the zoom level to 1 (no zoom)."""
        self.zoom(1)
        self.ui.spinbox_zoom.setValue(1)

    def zoom(self, value):
        r"""Sets the canvas zoom level.

        Parameters
        ----------
        value : float
            The zoom level, where 1 is normaal zoom.
        """
        t = QtGui.QTransform()
        t.scale(value, value)
        self.ui.graphics_view.setTransform(t, combine=False)

    def zoom_diff(self, diff, adjust=.0005):
        r"""Changes the zoom level by a given proportion. This function is used
        mostly for zoom-by-scroll.

        Parameters
        ----------
        diff : float
            The zoom difference.
        adjust : float, optional
            A value that is multiplied with `diff` to get a sensible zoom
            speed.
        """
        zoom = self.ui.spinbox_zoom.value() + .0005 * diff
        self.ui.spinbox_zoom.setValue(zoom)

    def initialize(self):
        r"""Initializes the sketchpad widget."""
        if self.initialized:
            return
        self.ui.edit_color.initialize(experiment=self.experiment, parent=self)
        self.ui.widget_font.initialize(experiment=self.experiment, parent=self)
        self.initialized = True

    def init_settings(self):
        r"""Fills the controls with the correct starting values."""
        if self.ui.edit_color.text() == '':
            self.ui.edit_color.setText(self.sketchpad.var.get('foreground'))
        if self.ui.edit_show_if.text() == '':
            self.ui.edit_show_if.setText('always')

    def build_toolbar(self):
        r"""Builds the element-tool toolbar."""
        self.element_buttons = [self.ui.button_pointer]
        for element in sketchpad_elements.elements[::-1]:
            b = SketchpadElementButton(self, element)
            self.ui.layout_tools.insertWidget(1, b)
            self.element_buttons.append(b)

    def select_pointer_tool(self):
        r"""Selects the pointer tool."""
        self.unselect_all_tools()
        self.ui.button_pointer.setChecked(True)
        self.ui.widget_settings_text.setVisible(False)
        self.ui.widget_settings_color.setVisible(False)
        self.ui.widget_settings_penwidth.setVisible(False)
        self.ui.widget_settings_arrow_head_width.setVisible(False)
        self.ui.widget_settings_arrow_body_width.setVisible(False)
        self.ui.widget_settings_arrow_body_length.setVisible(False)
        self.ui.widget_settings_scale.setVisible(False)
        self.ui.widget_settings_rotation.setVisible(False)
        self.ui.widget_settings_fill.setVisible(False)
        self.ui.widget_settings_center.setVisible(False)
        self.ui.widget_settings_show_if.setVisible(False)
        self.ui.widget_settings_name.setVisible(False)
        self.ui.graphics_view.setCursor(self.arrow_cursor)

    def select_element_tool(self, element):
        r"""Selects an element tool."""
        self.selected_element_tool = element
        self.show_element_tool_settings(element)
        cursor = element.cursor()
        if isinstance(cursor, tuple):
            pixmap, hotx, hoty = cursor
            cursor = QtGui.QCursor(
                self.theme.qpixmap(pixmap, size=32), hotx, hoty)
        self.ui.graphics_view.setCursor(cursor)

    def show_element_tool_settings(self, element):
        r"""Shows the settings that are applicable to a given element."""
        self.ui.widget_settings_text.setVisible(element.requires_text())
        self.ui.widget_settings_color.setVisible(element.requires_color())
        self.ui.widget_settings_penwidth.setVisible(
            element.requires_penwidth())
        self.ui.widget_settings_arrow_head_width.setVisible(
            element.requires_arrow_head_width())
        self.ui.widget_settings_arrow_body_width.setVisible(
            element.requires_arrow_body_width())
        self.ui.widget_settings_arrow_body_length.setVisible(
            element.requires_arrow_body_length())
        self.ui.widget_settings_scale.setVisible(element.requires_scale())
        self.ui.widget_settings_rotation.setVisible(
            element.requires_rotation())
        self.ui.widget_settings_fill.setVisible(element.requires_fill())
        self.ui.widget_settings_center.setVisible(element.requires_center())
        self.ui.widget_settings_show_if.setVisible(element.requires_show_if())
        self.ui.widget_settings_name.setVisible(
            element.requires_name() and
            len(self.sketchpad.selected_elements()) < 2
        )

    def unselect_all_tools(self):
        r"""Unselects all tools."""
        self.selected_element_tool = None
        for b in self.element_buttons:
            b.setChecked(False)

    def sizeHint(self):
        r"""Provides a size hint for the widget, so that it can become small.

        Returns
        -------
        QSize
            A size hint.
        """
        return QtCore.QSize(0, 0)

    def set_size(self):
        r"""Sets the size of the QGraphicsView to the experiment resolution."""
        w = self.sketchpad.var.width
        h = self.sketchpad.var.height
        self.ui.graphics_view.setSceneRect(-self.margin-w/2, -self.margin-h/2,
                                           w+2*self.margin, h+2*self.margin)

    def draw(self, refresh=False):
        r"""Clears and redraws the sketchpad canvas.

        Parameters
        ----------
        refresh : bool, optional
            Indicates whether the entire sketchpad should be refreshed, which
            is necessary to repaint the background.
        """
        def z_sort(element):
            if isinstance(element.z_index, (int, float)):
                return -element.z_index
            return 0

        if refresh or \
                self.canvas.background_color != self.sketchpad.var.background:
            self.canvas.invalidate()
        self.canvas.clear()
        self.elements.sort(key=z_sort)
        for element in self.elements:
            element.draw()
        for notification in self.canvas.notifications:
            self.extension_manager.fire('notify', message=notification,
                                        category='info')
        self.sketchpad.apply_edit_changes()

    def center(self):
        r"""Centers the canvas view."""
        self.ui.graphics_view.centerOn(0, 0)

    def set_cursor_pos(self, xy):
        r"""Updates the cursor-position indicator.

        Parameters
        ----------
        xy
            An (x,y) tuple with the cursor position.
        """
        self.ui.label_cursor_pos.setText('%d,%d' % xy)

    def current_color(self):
        return str(self.ui.edit_color.text())

    def current_penwidth(self):
        return self.ui.spinbox_penwidth.value()

    def current_scale(self):
        return self.ui.spinbox_scale.value()

    def current_rotation(self):
        return self.ui.spinbox_rotation.value()

    def current_arrow_body_width(self):
        return self.ui.spinbox_arrow_body_width.value()

    def current_arrow_body_length(self):
        return self.ui.spinbox_arrow_body_length.value()

    def current_arrow_head_width(self):
        return self.ui.spinbox_arrow_head_width.value()

    def current_fill(self):
        return int(self.ui.checkbox_fill.isChecked())

    def current_center(self):
        return int(self.ui.checkbox_center.isChecked())

    def current_show_if(self):
        return self.ui.edit_show_if.text()

    def current_font_family(self):
        return self.ui.widget_font.family

    def current_font_size(self):
        return self.ui.widget_font.size

    def current_font_bold(self):
        return 'yes' if self.ui.widget_font.bold else 'no'

    def current_font_italic(self):
        return 'yes' if self.ui.widget_font.italic else 'no'

    def current_html(self):
        return 'yes' if self.ui.checkbox_html.isChecked() else 'no'


# Alias for backwards compatibility
sketchpad_widget = SketchpadWidget

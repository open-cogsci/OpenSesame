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
from libopensesame.oslogging import oslogger
from qtpy import QtWidgets
from libqtopensesame.widgets.general_header_widget import GeneralHeaderWidget
from libqtopensesame.widgets.base_widget import BaseWidget
from openexp._color.color import Color
from openexp import backend
from libqtopensesame.misc.translate import translation_context
_ = translation_context(u'general_properties', category=u'core')


class GeneralProperties(BaseWidget):

    """The QWidget for the general properties tab."""
    backend_format = u'%s [%s]'

    def __init__(self, main_window):
        r"""Constructor.

        Parameters
        ----------
        main_window
            A qtopensesame object.
        """
        super().__init__(main_window, ui=u'widgets.general_properties')
        self.lock = False
        # Set the header, with the icon, label and script button
        self.header_widget = GeneralHeaderWidget(self, self.main_window)
        header_hbox = QtWidgets.QHBoxLayout()
        header_hbox.addWidget(self.theme.qlabel(u"experiment"))
        header_hbox.addWidget(self.header_widget)
        header_hbox.addStretch()
        header_hbox.setContentsMargins(0, 0, 0, 0)
        header_hbox.setSpacing(12)
        header_widget = QtWidgets.QWidget()
        header_widget.setLayout(header_hbox)
        self.ui.container_layout.insertWidget(0, header_widget)
        # Initialize the color and font widgets
        self.ui.edit_foreground.initialize(self.experiment)
        self.ui.edit_background.initialize(self.experiment)
        self.ui.widget_font.initialize(self.experiment)
        # Set the backend combobox
        for name, info in backend.backend_info(self.experiment).items():
            desc = info[u"description"]
            icon = info[u"icon"]
            self.ui.combobox_backend.addItem(self.main_window.theme.qicon(
                icon), self.backend_format % (name, desc))
        self.quick_connect(
            slot=self.main_window.ui.tabwidget.open_general_script,
            signals=[self.ui.button_script_editor.clicked],
        )
        self.quick_connect(
            slot=self.main_window.ui.tabwidget.open_backend_settings,
            signals=[self.ui.button_backend_settings.clicked]
        )
        self.quick_connect(
            slot=self.apply_changes,
            signals=[
                self.ui.combobox_backend.currentIndexChanged,
                self.ui.spinbox_width.editingFinished,
                self.ui.spinbox_height.editingFinished,
                self.ui.checkbox_disable_garbage_collection.stateChanged,
                self.ui.edit_foreground.textEdited,
                self.ui.edit_background.textEdited,
                self.ui.widget_font.font_changed,
            ])
        self.tab_name = u'__general_properties__'
        self.on_activate = self.refresh

    def set_header_label(self):
        r"""Sets the general header based on the experiment title and
        description.
        """
        self.header_widget.set_name(self.experiment.var.title)
        self.header_widget.set_desc(self.experiment.var.description)

    def apply_changes(self):
        r"""Applies changes to the general tab."""
        # Skip if the general tab is locked and lock it otherwise
        if self.lock:
            return
        self.lock = True

        self.main_window.set_busy(True)
        self.main_window.extension_manager.fire(u'prepare_change_experiment')
        # Set the title and the description
        title = self.experiment.syntax.sanitize(
            self.header_widget.edit_name.text())
        if title != self.experiment.var.title:
            self.experiment.var.title = title
            self.experiment.build_item_tree()
        desc = self.experiment.syntax.sanitize(
            self.header_widget.edit_desc.text())
        self.experiment.var.description = desc
        # Set the backend
        if self.ui.combobox_backend.isEnabled():
            i = self.ui.combobox_backend.currentIndex()
            _backend = list(backend.backend_info(self.experiment).values())[i]
            self.experiment.var.canvas_backend = _backend[u"canvas"]
            self.experiment.var.keyboard_backend = _backend[u"keyboard"]
            self.experiment.var.mouse_backend = _backend[u"mouse"]
            self.experiment.var.sampler_backend = _backend[u"sampler"]
            self.experiment.var.clock_backend = _backend[u"clock"]
            self.experiment.var.color_backend = _backend[u"color"]
        else:
            oslogger.debug(
                u'not setting back-end, because a custom backend is selected'
            )
        # Set the display width
        width = self.ui.spinbox_width.value()
        height = self.ui.spinbox_height.value()
        if self.experiment.var.width != width or \
                self.experiment.var.height != height:
            self.main_window.update_resolution(width, height)
        # Set the foreground color
        foreground = self.experiment.syntax.sanitize(
            self.ui.edit_foreground.text())
        refs = []
        try:
            refs = self.experiment.get_refs(foreground)
            Color.to_hex(foreground)
        except Exception as e:
            if refs == []:
                self.notify(e)
                foreground = self.experiment.var.foreground
                self.ui.edit_foreground.setText(foreground)
        self.experiment.var.foreground = foreground
        # Set the background color
        background = self.experiment.syntax.sanitize(
            self.ui.edit_background.text())
        refs = []
        try:
            refs = self.experiment.get_refs(background)
            Color.to_hex(background)
        except Exception as e:
            if refs == []:
                self.notify(e)
                background = self.experiment.var.background
                self.ui.edit_background.setText(background)
        self.experiment.var.background = foreground
        self.experiment.var.background = background
        # Set the font
        self.experiment.var.font_family = self.ui.widget_font.family
        self.experiment.var.font_size = self.ui.widget_font.size
        self.experiment.var.font_italic = self.ui.widget_font.italic
        self.experiment.var.font_bold = self.ui.widget_font.bold
        # Other checkboxes
        self.experiment.var.disable_garbage_collection = \
            self.ui.checkbox_disable_garbage_collection.isChecked()
        # Refresh the interface and unlock the general tab
        self.lock = False
        self.main_window.extension_manager.fire(u'change_experiment')
        self.main_window.set_busy(False)

    def refresh(self):
        r"""Updates the controls of the general tab."""
        # Lock the general tab to prevent a recursive loop
        self.lock = True
        # Set the header containing the titel etc
        self.set_header_label()
        # Select the backend
        _backend = backend.backend_match(self.experiment)
        if _backend == u"custom":
            self.ui.combobox_backend.setDisabled(True)
        else:
            self.ui.combobox_backend.setDisabled(False)
            desc = backend.backend_info(self.experiment)[
                _backend][u"description"]
            i = self.ui.combobox_backend.findText(
                self.backend_format % (_backend, desc))
            self.ui.combobox_backend.setCurrentIndex(i)
        # Set the resolution
        try:
            self.ui.spinbox_width.setValue(int(self.experiment.var.width))
            self.ui.spinbox_height.setValue(int(self.experiment.var.height))
        except ValueError:
            self.experiment.notify(
                _(u"Failed to parse the resolution. Expecting positive numeric values.")
            )
        # Set the colors
        self.ui.edit_foreground.setText(safe_decode(
            self.experiment.var.foreground))
        self.ui.edit_background.setText(safe_decode(
            self.experiment.var.background))
        self.ui.widget_font.initialize(self.experiment)
        self.ui.checkbox_disable_garbage_collection.setChecked(
            self.experiment.var.disable_garbage_collection == u'yes')
        # Release the general tab
        self.lock = False


# Alias for backwards compatibility
general_properties = GeneralProperties

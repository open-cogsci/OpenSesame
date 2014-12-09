#-*- coding:utf-8 -*-

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

from libopensesame import debug
from PyQt4 import QtCore, QtGui
from libopensesame import misc
from libqtopensesame.misc import _
import libopensesame.exceptions
from libqtopensesame.widgets.general_header_widget import general_header_widget
from libqtopensesame.widgets.base_widget import base_widget
from libqtopensesame.items import experiment
from libqtopensesame.misc import config
import openexp.backend_info
import sip

class general_properties(base_widget):

	"""The QWidget for the general properties tab."""

	backend_format = u'%s [%s]'

	def __init__(self, main_window):

		"""
		desc:
			Constructor.

		arguments:
			main_window:	A qtopensesame object.
		"""

		super(general_properties, self).__init__(main_window,
			ui=u'widgets.general_properties')

		# Set the header, with the icon, label and script button
		self.header_widget = general_header_widget(self, self.main_window)
		header_hbox = QtGui.QHBoxLayout()
		header_hbox.addWidget(self.experiment.label_image(u"experiment"))
		header_hbox.addWidget(self.header_widget)
		header_hbox.addStretch()
		header_widget = QtGui.QWidget()
		header_widget.setLayout(header_hbox)
		self.ui.container_layout.insertWidget(0, header_widget)

		# Initialize the color and font widgets
		self.ui.edit_foreground.initialize(self.experiment)
		self.ui.edit_foreground.textEdited.connect(self.apply_changes)
		self.ui.edit_background.initialize(self.experiment)
		self.ui.edit_background.textEdited.connect(self.apply_changes)
		self.ui.widget_font.initialize(self.experiment)
		self.ui.widget_font.font_changed.connect(self.apply_changes)

		# Connect the rest
		self.ui.spinbox_width.editingFinished.connect(self.apply_changes)
		self.ui.spinbox_height.editingFinished.connect(self.apply_changes)
		self.ui.button_script_editor.clicked.connect(
			self.main_window.ui.tabwidget.open_general_script)
		self.ui.button_backend_settings.clicked.connect(
			self.main_window.ui.tabwidget.open_backend_settings)

		# Set the backend combobox
		for backend in openexp.backend_info.backend_list:
			desc = openexp.backend_info.backend_list[backend][u"description"]
			icon = openexp.backend_info.backend_list[backend][u"icon"]
			self.ui.combobox_backend.addItem(self.main_window.theme.qicon(
				icon), self.backend_format % (backend, desc))
		self.ui.combobox_backend.currentIndexChanged.connect(self.apply_changes)

		# Bi-directional-text support
		self.ui.checkbox_bidi.stateChanged.connect(self.apply_changes)

		self.tab_name = u'__general_properties__'
		self.on_activate = self.refresh

	def set_header_label(self):

		"""
		desc:
			Sets the general header based on the experiment title and
			description.
		"""

		self.header_widget.edit_name.setText(self.experiment.title)
		self.header_widget.label_name.setText(
			u"<font size='5'><b>%s</b> - Experiment</font>&nbsp;&nbsp;&nbsp;<font color='gray'><i>Click to edit</i></font>" \
			% self.experiment.title)
		self.header_widget.edit_desc.setText(self.experiment.description)
		self.header_widget.label_desc.setText(self.experiment.description)

	def apply_changes(self):

		"""
		desc:
			Applies changes to the general tab.
		"""

		# Skip if the general tab is locked and lock it otherwise
		if self.lock:
			return
		self.lock = True

		debug.msg()
		rebuild_item_tree = False
		self.main_window.set_busy(True)
		# Set the title and the description
		title = self.experiment.sanitize(self.header_widget.edit_name.text())
		if title != self.experiment.get(u'title'):
			self.experiment.set(u"title", title)
			self.experiment.build_item_tree()
		desc = self.experiment.sanitize(self.header_widget.edit_desc.text())
		self.experiment.set(u"description", desc)

		# Set the backend
		if self.ui.combobox_backend.isEnabled():
			i = self.ui.combobox_backend.currentIndex()
			backend = openexp.backend_info.backend_list.values()[i]
			self.experiment.set(u"canvas_backend", backend[u"canvas"])
			self.experiment.set(u"keyboard_backend", backend[u"keyboard"])
			self.experiment.set(u"mouse_backend", backend[u"mouse"])
			self.experiment.set(u"sampler_backend", backend[u"sampler"])
			self.experiment.set(u"synth_backend", backend[u"synth"])
		else:
			debug.msg(
				u'not setting back-end, because a custom backend is selected')

		# Set the display width
		width = self.ui.spinbox_width.value()
		if self.experiment.get(u"width") != width:
			self.main_window.update_resolution(width,
				self.experiment.get(u"height"))

		# Set the display height
		height = self.ui.spinbox_height.value()
		if self.experiment.get(u"height") != height:
			self.main_window.update_resolution(self.experiment.get(u"width"),
				height)

		# Set the foreground color
		foreground = self.experiment.sanitize(self.ui.edit_foreground.text())
		refs = []
		try:
			refs = self.experiment.get_refs(foreground)
			self.experiment.color_check(foreground)
		except Exception as e:
			if refs == []:
				self.experiment.notify(e)
				foreground = self.experiment.get(u"foreground")
				self.ui.edit_foreground.setText(foreground)
		self.experiment.set(u"foreground", foreground)

		# Set the background color
		background = self.experiment.sanitize(self.ui.edit_background.text())
		refs = []
		try:
			refs = self.experiment.get_refs(background)
			self.experiment.color_check(background)
		except Exception as e:
			if refs == []:
				self.experiment.notify(e)
				background = self.experiment.get(u"background")
				self.ui.edit_background.setText(background)
		self.experiment.set(u"background", foreground)
		self.experiment.set(u"background", background)

		# Set the font
		self.experiment.set(u'font_family', self.ui.widget_font.family)
		self.experiment.set(u'font_size', self.ui.widget_font.size)
		self.experiment.set(u'font_italic', self.ui.widget_font.italic)
		self.experiment.set(u'font_bold', self.ui.widget_font.bold)
		# Set bi-directional text
		self.experiment.set(u'bidi', self.ui.checkbox_bidi.isChecked())
		self.check_bidi()
		# Refresh the interface and unlock the general tab
		self.lock = False
		self.main_window.set_busy(False)

	def refresh(self):

		"""
		desc:
			Updates the controls of the general tab.
		"""

		debug.msg()

		# Lock the general tab to prevent a recursive loop
		self.lock = True

		# Set the header containing the titel etc
		self.set_header_label()

		# Select the backend
		backend = openexp.backend_info.match(self.experiment)
		if backend == u"custom":
			self.ui.combobox_backend.setDisabled(True)
		else:
			self.ui.combobox_backend.setDisabled(False)
			desc = openexp.backend_info.backend_list[backend][u"description"]
			i = self.ui.combobox_backend.findText(
				self.backend_format % (backend, desc))
			self.ui.combobox_backend.setCurrentIndex(i)

		# Set the resolution
		try:
			self.ui.spinbox_width.setValue(int(self.experiment.width))
			self.ui.spinbox_height.setValue(int(self.experiment.height))
		except:
			self.experiment.notify(
				_(u"Failed to parse the resolution. Expecting positive numeric values."))

		# Set the colors
		self.ui.edit_foreground.setText(self.experiment.unistr(
			self.experiment.foreground))
		self.ui.edit_background.setText(self.experiment.unistr(
			self.experiment.background))

		# Set the font
		self.ui.widget_font.initialize(self.experiment)
		# Set bidirectional text
		self.ui.checkbox_bidi.setChecked(self.experiment.get(u'bidi') == u'yes')
		self.check_bidi()
		# Release the general tab
		self.lock = False

	def check_bidi(self):
		
		"""
		desc:
			Shows the bidi-check message if bi-directional text support is
			enabled while python-bidi is not installed.
		"""
		
		if self.experiment.get(u'bidi') != u'yes':
			self.ui.label_bidi_check.hide()
			return
		try:
			import bidi
		except:
			bidi = None
		if bidi is None:
			self.ui.label_bidi_check.show()
		else:
			self.ui.label_bidi_check.hide()

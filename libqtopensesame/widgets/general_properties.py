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
from libqtopensesame.ui import general_widget_ui
from libqtopensesame.widgets import color_edit, inline_editor, header_widget
from libqtopensesame.items import experiment
from libqtopensesame.misc import config
import openexp.backend_info
import sip

class general_properties(QtGui.QWidget):

	"""The QWidget for the general properties tab"""
	
	backend_format = "%s [%s]"

	def __init__(self, parent=None):

		"""
		Constructor

		Keywords arguments:
		parent -- the parent QWidget
		"""

		self.main_window = parent
		QtGui.QWidget.__init__(self)

		# Set the header, with the icon, label and script button
		self.header_widget = general_header_widget(self.main_window.experiment)
		button_help = QtGui.QPushButton(self.main_window.experiment.icon( \
			"help"), "")
		button_help.setIconSize(QtCore.QSize(16, 16))
		button_help.clicked.connect(self.open_help_tab)
		button_help.setToolTip(_("Tell me more about OpenSesame!"))
		header_hbox = QtGui.QHBoxLayout()
		header_hbox.addWidget(self.main_window.experiment.label_image( \
			"experiment"))
		header_hbox.addWidget(self.header_widget)
		header_hbox.addStretch()
		header_hbox.addWidget(button_help)
		header_hbox.setContentsMargins(0, 0, 0, 16)
		header_widget = QtGui.QWidget()
		header_widget.setLayout(header_hbox)

		# The rest of the controls from the UI file
		w = QtGui.QWidget()
		self.ui = general_widget_ui.Ui_general_widget()
		self.ui.setupUi(w)
		self.main_window.theme.apply_theme(self)

		# Initialize the color and font widgets
		self.ui.edit_foreground.initialize(self.main_window.experiment)
		self.ui.edit_background.initialize(self.main_window.experiment)		
		QtCore.QObject.connect(self.ui.edit_foreground, QtCore.SIGNAL( \
			"set_color"), self.apply_changes)
		QtCore.QObject.connect(self.ui.edit_background, QtCore.SIGNAL( \
			"set_color"), self.apply_changes)			
		self.ui.widget_font.initialize(self.main_window.experiment)		
		QtCore.QObject.connect(self.ui.widget_font, QtCore.SIGNAL( \
			"font_changed"), self.apply_changes)			

		# Connect the rest
		self.ui.spinbox_width.editingFinished.connect(self.apply_changes)
		self.ui.spinbox_height.editingFinished.connect(self.apply_changes)
		self.ui.label_opensesame.setText(unicode( \
			self.ui.label_opensesame.text()).replace("[version]", \
			misc.version).replace("[codename]", misc.codename))			
		self.ui.label_website.mousePressEvent = self.open_website
		self.ui.label_facebook.mousePressEvent = self.open_facebook
		self.ui.label_twitter.mousePressEvent = self.open_twitter
		self.ui.button_script_editor.clicked.connect( \
			self.main_window.ui.tabwidget.open_general_script)

		# Set the backend combobox
		for backend in openexp.backend_info.backend_list:
			desc = openexp.backend_info.backend_list[backend]["description"]
			icon = openexp.backend_info.backend_list[backend]["icon"]
			self.ui.combobox_backend.addItem(self.main_window.theme.qicon( \
				icon), self.backend_format % (backend, desc))
		self.ui.combobox_backend.currentIndexChanged.connect(self.apply_changes)

		vbox = QtGui.QVBoxLayout()
		vbox.addWidget(header_widget)
		vbox.addWidget(w)

		self.setLayout(vbox)
		self.__general_tab__ = True

	def init_backend_settings(self, force=False):

		"""
		(Re-)initialize the backend settings controls

		Keywords arguments:
		force -- indicates if the initialization should occur even if the
				 controls are not shown (default=False)
		"""

		if force or self.ui.group_backend_settings.isChecked():
			for backend_type in ["canvas", "keyboard", "mouse", "synth", \
				"sampler"]:
				backend = self.main_window.experiment.get("%s_backend" \
					% backend_type)
				exec("from openexp._%s.%s import %s as _backend" % ( \
					backend_type, backend, backend))
				group = eval("self.ui.group_%s" % backend_type)
				layout = eval("self.ui.layout_%s" % backend_type)
				label = eval("self.ui.label_%s" % backend_type)

				# Horribly ugly wayo clear the previous settings
				while layout.count() > 1:
					w = layout.itemAt(1)
					layout.removeItem(w)
					w.widget().hide()
					sip.delete(w)

				if not hasattr(_backend, "settings") or _backend.settings == \
					None:
					label.setText(_("No settings for %s") % backend)
				else:
					label.setText(_("Settings for %s:") % backend)
					layout.addWidget(settings_widget( \
						self.main_window.experiment, _backend.settings, self))

	def toggle_spacer(self):

		"""Sets the visibility of the spacer"""

		hide = self.ui.group_backend_settings.isChecked() or \
			self.ui.group_script.isChecked()
		self.ui.spacer.setVisible(not hide)

	def toggle_backend_settings(self):

		"""
		Sets the visibility of the script editor based on the checkbox state
		"""

		show = self.ui.group_backend_settings.isChecked()
		if show:
			self.main_window.set_busy(True)
			self.init_backend_settings(force=True)
			self.main_window.set_busy(False)
		self.ui.scrollarea_backend_settings.setVisible(show)
		self.toggle_spacer()

	def toggle_script_editor(self):

		"""
		Sets the visibility of the script editor based on the checkbox state
		"""

		show = self.ui.group_script.isChecked()
		self.edit_script.setVisible(show)
		self.toggle_spacer()

	def set_header_label(self):

		"""
		Set the general header based on the experiment title and description
		"""

		self.header_widget.edit_name.setText(self.main_window.experiment.title)
		self.header_widget.label_name.setText( \
			"<font size='5'><b>%s</b> - Experiment</font>&nbsp;&nbsp;&nbsp;<font color='gray'><i>Click to edit</i></font>" \
			% self.main_window.experiment.title)
		self.header_widget.edit_desc.setText(self.main_window.experiment.description)
		self.header_widget.label_desc.setText(self.main_window.experiment.description)

	def open_help_tab(self):

		"""Open the general help tab"""

		self.main_window.open_general_help_tab()
		
	def open_website(self, dummy=None):
	
		"""Open the main website"""
		
		misc.open_url(config.get_config("url_website"))
		
	def open_facebook(self, dummy=None):
	
		"""Open Facebook page"""	

		misc.open_url(config.get_config("url_facebook"))

	def open_twitter(self, dummy=None):
	
		"""Open Twitter page"""	
	
		misc.open_url(config.get_config("url_twitter"))

	def apply_script(self):

		"""Apply changes to the general script"""

		self.main_window.set_busy(True)
		script = str(self.edit_script.edit.toPlainText())
		try:
			tmp = experiment.experiment(self.main_window, \
				self.main_window.experiment.title, 	script, \
				self.main_window.experiment.pool_folder)
		except libopensesame.exceptions.script_error as error:
			self.main_window.experiment.notify(_("Could not parse script: %s") \
				% error)
			self.edit_script.edit.setText( \
				self.main_window.experiment.to_string())
			return

		self.main_window.experiment = tmp
		self.main_window.close_other_tabs()
		self.edit_script.setModified(False)
		self.main_window.refresh()
		self.main_window.set_busy(False)

	def apply_changes(self):

		"""Apply changes to the general tab"""

		# Skip if the general tab is locked and lock it otherwise
		if self.lock:
			return
		self.lock = True

		debug.msg()
		rebuild_item_tree = False
		self.main_window.set_busy(True)
		# Set the title and the description
		title = self.main_window.experiment.sanitize( \
			self.header_widget.edit_name.text())
		self.main_window.experiment.set("title", title)
		desc = self.main_window.experiment.sanitize( \
			self.header_widget.edit_desc.text())
		self.main_window.experiment.set("description", desc)

		# Set the backend
		i = self.ui.combobox_backend.currentIndex()
		backend = openexp.backend_info.backend_list.values()[i]
		self.main_window.experiment.set("canvas_backend", backend["canvas"])
		self.main_window.experiment.set("keyboard_backend", backend["keyboard"])
		self.main_window.experiment.set("mouse_backend", backend["mouse"])
		self.main_window.experiment.set("sampler_backend", backend["sampler"])
		self.main_window.experiment.set("synth_backend", backend["synth"])

		# Set the display width
		width = self.ui.spinbox_width.value()
		if self.main_window.experiment.get("width") != width:
			self.main_window.update_resolution(width, \
				self.main_window.experiment.get("height"))

		# Set the display height
		height = self.ui.spinbox_height.value()
		if self.main_window.experiment.get("height") != height:
			self.main_window.update_resolution( \
				self.main_window.experiment.get("width"), height)

		# Set the foreground color
		foreground = self.main_window.experiment.sanitize( \
			self.ui.edit_foreground.text())
		refs = []
		try:
			refs = self.main_window.experiment.get_refs(foreground)
			self.main_window.experiment.color_check(foreground)
		except Exception as e:
			if refs == []:
				self.main_window.experiment.notify(str(e))
				foreground = self.main_window.experiment.get("foreground")
				self.ui.edit_foreground.setText(foreground)
		self.main_window.experiment.set("foreground", foreground)
		
		# Set the background color
		background = self.main_window.experiment.sanitize( \
			self.ui.edit_background.text())
		refs = []
		try:
			refs = self.main_window.experiment.get_refs(background)
			self.main_window.experiment.color_check(background)
		except Exception as e:
			if refs == []:
				self.main_window.experiment.notify(str(e))
				background = self.main_window.experiment.get("background")
				self.ui.edit_background.setText(background)
		self.main_window.experiment.set("background", foreground)
		self.main_window.experiment.set("background", background)
		
		# Set the font
		self.main_window.experiment.set('font_family', \
			self.ui.widget_font.family)		
		self.main_window.experiment.set('font_size', \
			self.ui.widget_font.size)
		self.main_window.experiment.set('font_italic', \
			self.ui.widget_font.italic)
		self.main_window.experiment.set('font_bold', \
			self.ui.widget_font.bold)
			
		# Refresh the interface and unlock the general tab
		self.main_window.refresh()
		self.lock = False
		self.main_window.set_busy(False)

	def refresh(self):

		"""Update the controls of the general tab"""

		debug.msg()

		# Lock the general tab to prevent a recursive loop
		self.lock = True

		# Set the header containing the titel etc
		self.set_header_label()

		# Select the backend
		backend = openexp.backend_info.match(self.main_window.experiment)
		if backend == "custom":
			self.ui.combobox_backend.setDisabled(True)
		else:
			self.ui.combobox_backend.setDisabled(False)
			desc = openexp.backend_info.backend_list[backend]["description"]
			i = self.ui.combobox_backend.findText(self.backend_format \
				% (backend, desc))
			self.ui.combobox_backend.setCurrentIndex(i)

		# Set the resolution
		try:
			self.ui.spinbox_width.setValue(int( \
				self.main_window.experiment.width))
			self.ui.spinbox_height.setValue(int( \
				self.main_window.experiment.height))
		except:
			self.main_window.experiment.notify( \
				_("Failed to parse the resolution. Expecting positive numeric values."))

		# Set the colors
		self.ui.edit_foreground.setText(str( \
			self.main_window.experiment.foreground))
		self.ui.edit_background.setText(str( \
			self.main_window.experiment.background))

		# Release the general tab
		self.lock = False

class settings_edit(QtGui.QLineEdit):

	"""An edit widget for a single variable"""

	def __init__(self, experiment, var, val, parent=None):

		"""
		Constructor

		Arguments:
		experiment -- the experiment
		var -- the variable name
		val -- the variable value

		Keywords arguments:
		parent -- parent QWidget (default=None)
		"""

		QtGui.QLineEdit.__init__(self, str(val))
		self._parent = parent
		self.var = var
		self.experiment = experiment
		self.editingFinished.connect(self.apply_setting)

	def apply_setting(self):

		"""Apply changes"""

		self.experiment.set(self.var, self.experiment.sanitize(self.text()))
		self._parent._parent.refresh()

class settings_widget(QtGui.QWidget):

	"""A widget containing a number of settings"""

	def __init__(self, experiment, settings, parent=None):

		"""
		Constructor

		Arguments:
		experiment -- the experiment
		settings -- the settings dictionary

		Keywords arguments:
		parent -- parent QWidget (default=None)
		"""

		QtGui.QWidget.__init__(self, parent)
		self._parent = parent
		self.experiment = experiment
		self.settings = settings
		self.layout = QtGui.QFormLayout(self)
		self.setLayout(self.layout)
		for var, desc in settings.items():
			if self.experiment.has(var):
				val = self.experiment.get(var)
			else:
				val = desc["default"]
			label = QtGui.QLabel()
			label.setText("%(name)s<br /><small><i>%(description)s</i></small>" % desc)
			label.setTextFormat(QtCore.Qt.RichText)
			edit = settings_edit(self.experiment, var, val, self)
			self.layout.addRow(label, edit)

class general_header_widget(header_widget.header_widget):

	"""
	The widget containing the clickable title and description of the experiment
	"""

	def __init__(self, item):

		"""
		Constructor

		Arguments:
		item -- the experiment
		"""

		header_widget.header_widget.__init__(self, item)
		self.label_name.setText( \
			"<font size='5'><b>%s</b> - Experiment</font>&nbsp;&nbsp;&nbsp;<font color='gray'><i>Click to edit</i></font>" \
			% self.item.get("title"))

	def restore_name(self):

		"""Apply the name change, hide the editable title and show the label"""

		self.item.main_window.general_tab_widget.apply_changes()
		self.label_name.setText( \
			"<font size='5'><b>%s</b> - Experiment</font>&nbsp;&nbsp;&nbsp;<font color='gray'><i>Click to edit</i></font>" \
			% self.item.get("title"))
		self.label_name.show()
		self.edit_name.setText(self.item.get("title"))
		self.edit_name.hide()

	def restore_desc(self):

		"""
		Apply the description change, hide the editable description and show the label
		"""

		self.item.main_window.general_tab_widget.apply_changes()
		self.label_desc.setText(self.item.get("description"))
		self.label_desc.show()
		self.edit_desc.setText(self.item.get("description"))
		self.edit_desc.hide()

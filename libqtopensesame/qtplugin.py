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

from PyQt4 import QtCore, QtGui
from libqtopensesame import qtitem, inline_editor, syntax_highlighter, \
	color_edit
import os.path

class qtplugin(qtitem.qtitem):

	"""Provides basic functionality for plugin GUIs"""

	def __init__(self, plugin_file):
	
		"""
		Constructor

		Arguments:
		plugin_file -- path to the plugin script
		"""
	
		# These lines makes sure that the icons and help file are recognized by
		# OpenSesame.
		self.experiment.resources["%s.png" % self.item_type] = os.path.join(os.path.split(plugin_file)[0], "%s.png" % self.item_type)
		self.experiment.resources["%s_large.png" % self.item_type] = os.path.join(os.path.split(plugin_file)[0], "%s_large.png" % self.item_type)			
		self.experiment.resources["%s.html" % self.item_type] = os.path.join(os.path.split(plugin_file)[0], "%s.html" % self.item_type)	
		
		self.auto_line_edit = {}
		self.auto_combobox = {}
		self.auto_spinbox = {}
		self.auto_slider = {}
		self.auto_editor = {}
		
		self.lock = False
			
		qtitem.qtitem.__init__(self)
		
	def edit_widget(self):
	
		"""Update the GUI controls"""
		
		qtitem.qtitem.edit_widget(self)
		
		for var, edit in self.auto_line_edit.iteritems():
			if self.has(var):
				try:
					edit.setText(self.experiment.unsanitize(self.get(var)))
				except Exception as e:
					self.experiment.notify("Failed to set control '%s': %s" % (var, e))
			else:
				edit.setText("")
				
		for var, combobox in self.auto_combobox.iteritems():
			if self.has(var):
				try:
					 combobox.setCurrentIndex(combobox.findText(self.experiment.unsanitize(self.get(var))))
				except Exception as e:
					self.experiment.notify("Failed to set control '%s': %s" % (var, e))
				
		for var, spinbox in self.auto_spinbox.iteritems():
			if self.has(var):
				try:
					 spinbox.setValue(self.get(var))
				except Exception as e:
					self.experiment.notify("Failed to set control '%s': %s" % (var, e))				
										
		for var, slider in self.auto_slider.iteritems():
			if self.has(var):
				try:
					slider.setValue(self.get(var))
				except Exception as e:
					self.experiment.notify("Failed to set control '%s': %s" % (var, e))
					
		for var, editor in self.auto_editor.iteritems():
			if self.has(var):
				try:
					editor.edit.setPlainText(self.experiment.unsanitize(self.get(var)))
				except Exception as e:
					self.experiment.notify("Failed to set control '%s': %s" % (var, e))
				
	def apply_edit_changes(self, rebuild=True):
	
		"""
		Apply the controls

		Keyword arguments:
		rebuild -- deprecated (does nothing) (default=True)
		"""		
		
		if not qtitem.qtitem.apply_edit_changes(self, False) or self.lock:
			return False
			
		for var, edit in self.auto_line_edit.iteritems():
			val = self.experiment.usanitize(edit.text()).strip()
			if val != "":
				self.set(var, val)
			elif self.experiment.has(var) or edit.default == None:
				self.unset(var)
			else:
				self.set(var, edit.default)
			
		for var, combobox in self.auto_combobox.iteritems():
			self.set(var, self.experiment.usanitize(combobox.currentText()))
			
		for var, spinbox in self.auto_spinbox.iteritems():
			self.set(var, spinbox.value())
			
		for var, slider in self.auto_slider.iteritems():
			self.set(var, slider.value())
			
		for var, editor in self.auto_editor.iteritems():
			self.set(var, self.experiment.usanitize(editor.edit.toPlainText()))
			editor.setModified(False)

		return True
		
	def add_control(self, label, widget, tooltip, default, min_width=None):
	
		"""
		Add a generic control

		Arguments:
		label -- a text label
		widget -- a control widget
		tooltip -- a tooltip string
		default -- a default value

		Keyword arguments:
		min_width -- a minimum width for the widget (default=None)
		"""
		
		if tooltip != None:
			try:
				widget.setToolTip(tooltip)				
			except:
				pass
		if min_width != None:
			widget.setMinimumWidth(min_width)
		widget.default = default
		row = self.edit_grid.rowCount()		
		self.edit_grid.addWidget(QtGui.QLabel(label), row, 0)
		self.edit_grid.addWidget(widget, row, 1)
		
	def add_line_edit_control(self, var, label, tooltip=None, default=None, min_width=None):
	
		"""
		Adds a QLineEdit control

		Arguments:
		var -- name of the associated variable
		label -- a label

		Keyword arguments:
		tooltip -- a tooltip (default=None)
		default -- a default value (default=None)
		min_width -- a minimum width for the widget (default=None)		
		"""		
		
		edit = QtGui.QLineEdit()
		edit.editingFinished.connect(self.apply_edit_changes)
		self.add_control(label, edit, tooltip, default, min_width)		
		if var != None:
			self.auto_line_edit[var] = edit		
		return edit
		
	def add_color_edit_control(self, var, label, tooltip=None, default=None, min_width=None):
	
		"""
		Adds a colorpicker control, consisting of a QLineEdit and QColorDialog.
		Some basic checking is done to ascertain that only valid color names or
		variably defined entries are accepted.		
		
		Arguments:
		var -- name of the associated variable
		label -- a label

		Keyword arguments:
		tooltip -- a tooltip (default=None)
		default -- a default value (default=None)
		min_width -- a minimum width for the widget (default=None)				
		"""
		
		edit = color_edit.color_edit(self.experiment)
		QtCore.QObject.connect(edit, QtCore.SIGNAL("set_color"), self.apply_edit_changes)
		self.add_control(label, edit, tooltip, default, min_width)		
		if var != None:
			self.auto_line_edit[var] = edit		
		return edit		
		
	def add_combobox_control(self, var, label, options, tooltip = None):
	
		"""
		Adds a QComboBox control

		Arguments:
		var -- name of the associated variable
		label -- a label
		options -- a list of options

		Keyword arguments:
		tooltip -- a tooltip (default=None)		
		"""
		
		combobox = QtGui.QComboBox()
		combobox.currentIndexChanged.connect(self.apply_edit_changes)
		for o in options:
			combobox.addItem(o)
		self.add_control(label, combobox, tooltip, None)
		
		if var != None:
			self.auto_combobox[var] = combobox
				
		return combobox
		
	def add_spinbox_control(self, var, label, min_val, max_val, prefix="", suffix="", tooltip=None):
	
		"""
		Adds a QSpinBox control

		Arguments:
		var -- name of the associated variable
		label -- a label
		min_val -- minimum value
		max_val -- maximum value		

		Keyword arguments:
		prefix -- a prefix string
		suffix -- a suffix string
		tooltip -- a tooltip (default=None)
		"""
		
		spinbox = QtGui.QSpinBox()
		spinbox.setMinimum(min_val)
		spinbox.setMaximum(max_val)
		spinbox.valueChanged.connect(self.apply_edit_changes)
		
		if prefix != "":
			spinbox.setPrefix(prefix)
		if suffix != "":
			spinbox.setSuffix(suffix)
			
		self.add_control(label, spinbox, tooltip, None)
		
		if var != None:
			self.auto_spinbox[var] = spinbox
			
		return spinbox
		
	def add_slider_control(self, var, label, min_val, max_val, left_label="", right_label="", tooltip=None, default=None):

		"""
		Adds a QSlider control

		Arguments:
		var -- name of the associated variable
		label -- a label
		min_val -- minimum value
		max_val -- maximum value		

		Keyword arguments:
		left_label -- a label for the left side
		right_label -- a label for the right side
		prefix -- a prefix string
		tooltip -- a tooltip (default=None)
		default -- a default value (default=None)
		"""		

		slider = QtGui.QSlider(QtCore.Qt.Horizontal)
		slider.setFocusPolicy(QtCore.Qt.NoFocus)
		slider.setGeometry(30, 40, 100, 30)
		slider.setRange(min_val, max_val)
		slider.setSingleStep(1000)
		if default != None:
			slider.setValue(default)

		#Take care of layout
		layout = QtGui.QHBoxLayout() 
		layout.setMargin(0) 
		layout.setSpacing(5)

		if left_label:
			llabel = QtGui.QLabel() 
			llabel.setText(left_label) 
			layout.addWidget(llabel) 
			layout.addWidget(slider)

		if right_label:
			rlabel = QtGui.QLabel() 
			rlabel.setText(right_label) 
			layout.addWidget(rlabel)  

		slider.valueChanged.connect(self.apply_edit_changes)

		if var != None:
			self.auto_slider[var] = slider

		widget = QtGui.QWidget()
		widget.setLayout(layout)

		self.add_control(label, widget, tooltip, default) 		
		
	def add_filepool_control(self, var, label, click_func, tooltip=None, default=None):
	
		"""
		Adds a control to select a file from the file pool. This is not fully
		automated, and a function has to specified that is called when a file
		is selected.

		Arguments:
		var -- name of the associated variable
		label -- a label
		click_func -- a function to be called when a file is selected

		Keyword arguments:
		tooltip -- a tooltip (default=None)
		default -- a default value (default=None)			
		"""
		
		edit = QtGui.QLineEdit()
		edit.editingFinished.connect(self.apply_edit_changes)
		edit.default = default
		
		if var != None:
			self.auto_line_edit[var] = edit
		
		button = QtGui.QPushButton(self.experiment.icon("browse"), "Browse")
		button.setIconSize(QtCore.QSize(16, 16))
		button.clicked.connect(click_func)
		
		hbox = QtGui.QHBoxLayout()
		hbox.setMargin(0)
		hbox.addWidget(edit)
		hbox.addWidget(button)
		
		widget = QtGui.QWidget()
		widget.setLayout(hbox)
				
		self.add_control(label, widget, tooltip, default)		
		
	def add_editor_control(self, var, label, syntax=False, tooltip=None, default=None):
	
		"""
		Adds a texteditor control (an extended QPlainTextEdit)

		Arguments:
		var -- name of the associated variable
		label -- a label


		Keyword arguments:
		syntax -- a boolean indicating whether Python syntax highlighting
				  should be activated (default=False)
		tooltip -- a tooltip (default=None)
		default -- a default value (default=None)						
		"""
	
		label = QtGui.QLabel(label)	
		if syntax:
			editor = inline_editor.inline_editor(self.experiment, syntax="python")
		else:
			editor = inline_editor.inline_editor(self.experiment)
		editor.apply.clicked.connect(self.apply_edit_changes)
		QtCore.QObject.connect(editor.edit, QtCore.SIGNAL("focusLost"), self.apply_edit_changes)		
		if var != None:
			self.auto_editor[var] = editor		
		self.edit_vbox.addWidget(label)			
		self.edit_vbox.addWidget(editor)					
				
	def add_text(self, msg):
	
		"""
		Adds a QLabel (for descriptions, no control)

		Arguments:
		msg -- text
		"""	
		
		row = self.edit_grid.rowCount()				
		self.edit_vbox.addWidget(QtGui.QLabel(msg))	
			
	def apply_button(self, label="Apply", icon="apply", tooltip="Apply changes"):
	
		"""
		Returns a right-outlined apply button. The widget is not added
		automatically to the controls.

		Keyword arguments:
		label -- a button label (default="Apply")
		icon -- an icon name (default="Apply")
		tooltip -- a tooltip (default="Apply changes")

		Returns:
		A QPushButton
		"""

		button_apply = QtGui.QPushButton(label)
		button_apply.setIcon(self.experiment.icon(icon))
		button_apply.setIconSize(QtCore.QSize(16, 16))
		button_apply.clicked.connect(self.apply_edit_changes)		
		button_apply.setToolTip(tooltip)
		hbox = QtGui.QHBoxLayout()
		hbox.setContentsMargins(0, 0, 0, 0)
		hbox.addStretch()
		hbox.addWidget(button_apply)		
		widget = QtGui.QWidget()
		widget.setLayout(hbox)		
		
		return widget
		
	def get_ready(self):
	
		"""
		Apply pending script changes

		Returns:
		True if changes have been made, False otherwise
		"""
		
		for var, editor in self.auto_editor.iteritems():
			if editor.isModified():
				if self.experiment.debug:
					print "qtplugin.finalize(): applying pending Python script changes"
				self.apply_edit_changes()
				return True
			
		return qtitem.qtitem.get_ready(self)		
				

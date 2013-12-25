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

import os
import sys
from PyQt4 import QtCore, QtGui
from libqtopensesame.items import qtitem
from libqtopensesame.misc import _
from libqtopensesame.widgets import color_edit, pool_widget
from libopensesame import debug, misc
from libqtopensesame.misc.config import cfg

class qtplugin(qtitem.qtitem):

	"""Provides basic functionality for plugin GUIs"""

	def __init__(self, plugin_file=None):

		"""
		Constructor.

		Arguments:
		plugin_file		-- The path to the plugin script. (default=None)
		"""

		if plugin_file != None:
			# The __file__ variable is generally a str, which will cause unicode
			# errors. Therefore, convert this here if necessary.
			if isinstance(plugin_file, str):
				plugin_file = plugin_file.decode(misc.filesystem_encoding())
			# These lines makes sure that the icons and help file are recognized
			# by OpenSesame.
			self.plugin_folder = os.path.dirname(plugin_file)
			self.experiment.resources[u'%s.png' % self.item_type] = \
				os.path.join(self.plugin_folder, u'%s.png' % self.item_type)
			self.experiment.resources[u'%s_large.png' % self.item_type] = \
				os.path.join(self.plugin_folder, u'%s_large.png' \
				% self.item_type)
			self.experiment.resources[u'%s.html' % self.item_type] = \
				os.path.join(self.plugin_folder, u'%s.html' \
				% self.item_type)
			self.experiment.resources[u'%s.md' % self.item_type] = \
				os.path.join(self.plugin_folder, u'%s.md' \
				% self.item_type)				
		self.lock = False
		qtitem.qtitem.__init__(self)

	def edit_widget(self):

		"""Updates the GUI controls."""

		qtitem.qtitem.edit_widget(self)
		self.auto_edit_widget()

	def apply_edit_changes(self, rebuild=True):

		"""
		Applies the controls.

		Keyword arguments:
		rebuild		-- DEPRECATED
		"""

		return qtitem.qtitem.apply_edit_changes(self, rebuild) and \
			self.auto_apply_edit_changes(rebuild)	

	def add_control(self, label, widget, tooltip=None, min_width=None):

		"""
		Adds a generic control QWidget.

		Arguments:
		label		--	A text label.
		widget		--	A control QWidget.

		Keyword arguments:
		tooltip		--	A tooltip text. (default=None)
		min_width	--	A minimum width for the widget. (default=None)
		"""

		if tooltip != None:
			try:
				widget.setToolTip(_(tooltip))
			except:
				pass
		if type(min_width) == int:
			widget.setMinimumWidth(min_width)
		row = self.edit_grid.rowCount()
		self.edit_grid.addWidget(QtGui.QLabel(_(label)), row, 0)
		self.edit_grid.addWidget(widget, row, 1)

	def add_line_edit_control(self, var, label, tooltip=None, default=None, \
		min_width=None):

		"""
		Adds a QLineEdit control that is linked to a variable.

		Arguments:
		var			--	Name of the associated variable.
		label 		--	Label text.

		Keyword arguments:
		tooltip 	--	A tooltip text. (default=None)
		default 	--	DEPRECATED
		min_width 	--	A minimum width for the widget. (default=None)
		
		Returns:
		A QLineEdit widget.
		"""

		edit = QtGui.QLineEdit()				
		edit.editingFinished.connect(self.apply_edit_changes)
		self.add_control(label, edit, tooltip, min_width)
		if var != None:
			self.auto_line_edit[var] = edit
		return edit
		
	def add_checkbox_control(self, var, label, tooltip=None):
	
		"""
		Adds a QCheckBox control that is linked to a variable.

		Arguments:
		var			--	Name of the associated variable.
		label 		--	Label text.

		Keyword arguments:
		tooltip 	--	A tooltip text. (default=None)
		
		Returns:
		A QCheckBox widget.
		"""
		
		checkbox = QtGui.QCheckBox(_(label))
		checkbox.toggled.connect(self.apply_edit_changes)
		self.add_control('', checkbox, tooltip)
		if var != None:
			self.auto_checkbox[var] = checkbox
		return checkbox
		
	def add_color_edit_control(self, var, label, tooltip=None, default=None, \
		min_width=None):

		"""
		Adds a colorpicker control, consisting of a QLineEdit and QColorDialog.
		Some basic checking is done to ascertain that only valid color names or
		variably defined entries are accepted.

		Arguments:
		var			--	Name of the associated variable.
		label 		--	Label text.

		Keyword arguments:
		tooltip 	--	A tooltip text. (default=None)
		default 	--	DEPRECATED
		min_width 	--	A minimum width for the widget. (default=None)
		
		Returns:
		A color_edit widget.
		"""

		edit = color_edit.color_edit()
		edit.initialize(self.experiment)
		QtCore.QObject.connect(edit, QtCore.SIGNAL('set_color'), \
			self.apply_edit_changes)
		self.add_control(label, edit, tooltip, min_width)
		if var != None:
			self.auto_line_edit[var] = edit
		return edit

	def add_combobox_control(self, var, label, options, tooltip=None):

		"""
		Adds a QComboBox control that is linked to a variable.

		Arguments:
		var			-- 	Name of the associated variable.
		label 		--	Label text.
		options 	--	A list of options.

		Keyword arguments:
		tooltip 	--	A tooltip text. (default=None)
		
		Returns:
		A QComboBox widget.
		"""

		combobox = QtGui.QComboBox()
		for o in options:
			combobox.addItem(o)			
		combobox.currentIndexChanged.connect(self.apply_edit_changes)			
		self.add_control(label, combobox, tooltip)
		if var != None:
			self.auto_combobox[var] = combobox
		return combobox

	def add_spinbox_control(self, var, label, min_val, max_val, prefix=u'', \
		suffix=u'', tooltip=None):

		"""
		Adds a QSpinBox control that is linked to a variable.

		Arguments:
		var			-- 	Name of the associated variable.
		label 		-- 	Label text.
		min_val 	-- 	A minimum value.
		max_val 	-- 	A maximum value.

		Keyword arguments:
		prefix 		-- 	A prefix text. (default=u'')
		suffix 		-- 	A suffix text. (default=u'')
		tooltip 	-- 	A tooltip text. (default=None)
		
		Returns:
		A QSpinBox widget.
		"""

		spinbox = QtGui.QSpinBox()
		spinbox.setMinimum(min_val)
		spinbox.setMaximum(max_val)
		spinbox.editingFinished.connect(self.apply_edit_changes)
		if prefix != u'':
			spinbox.setPrefix(prefix)
		if suffix != u'':
			spinbox.setSuffix(suffix)
		self.add_control(label, spinbox, tooltip)
		if var != None:
			self.auto_spinbox[var] = spinbox
		return spinbox

	def add_slider_control(self, var, label, min_val, max_val, left_label=u'', \
		right_label=u'', tooltip=None, default=None):

		"""
		Adds a QSlider control that is linked to a variable.

		Arguments:
		var			--	Name of the associated variable.
		label 		--	Label text.
		min_val 	--	A minimum value.
		max_val 	--	A maximum value.

		Keyword arguments:
		left_label 	--	A label for the left side (default="")
		right_label	--	A label for the right side (default="")
		tooltip		--	A tooltip text. (default=None)
		default		--	DEPRECATED
		
		Returns:
		A QSlider widget.
		"""

		slider = QtGui.QSlider(QtCore.Qt.Horizontal)
		slider.setFocusPolicy(QtCore.Qt.NoFocus)
		slider.setGeometry(30, 40, 100, 30)
		slider.setRange(min_val, max_val)
		slider.setSingleStep(1000)		
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
		self.add_control(label, widget, tooltip)
		return slider

	def add_filepool_control(self, var, label, click_func=None, tooltip=None, \
		default=None):

		"""
		Adds a control to select a file from the file pool, and is linked to a
		variable.

		Arguments:
		var			--	Name of the associated variable.
		label 		--	Label text.

		Keyword arguments:
		click_func 	--	A custom function to be called when a file is selected.
						If no click_func is specified, file selection will be
						handled automatically. (default=None)
		tooltip 	--	A tooltip text. (default=None)
		default		--	DEPRECATED
		
		Returns:
		A QLineEdit widget that contains the path of the selected file.
		"""	

		edit = QtGui.QLineEdit()		
		edit.editingFinished.connect(self.apply_edit_changes)
		if var != None:
			self.auto_line_edit[var] = edit
		if click_func == None:
			click_func = self.browse_pool_func(edit)
		button = QtGui.QPushButton(self.experiment.icon(u'browse'), u'Browse')
		button.setIconSize(QtCore.QSize(16, 16))
		button.clicked.connect(click_func)
		hbox = QtGui.QHBoxLayout()
		hbox.setMargin(0)
		hbox.addWidget(edit)
		hbox.addWidget(button)
		widget = QtGui.QWidget()
		widget.setLayout(hbox)
		self.add_control(label, widget, tooltip)
		return edit

	def add_editor_control(self, var, label, syntax=False, tooltip=None, \
		default=None):

		"""
		Adds a QProgEdit that is linked to a variable.

		Arguments:
		var			--	Name of the associated variable.
		label 		--	Label text.

		Keyword arguments:
		syntax 		--	A boolean indicating whether Python syntax highlighting
						should be activated. (default=False)
		tooltip		--	A tooltip text. (default=None)
		default		--	DEPRECATED
		
		Returns:
		A QProgEdit widget.
		"""
		
		from QProgEdit import QTabManager
		if syntax:
			lang = u'python'
		else:
			lang = u'text'
		qprogedit = QTabManager(handler=self.apply_edit_changes, defaultLang= \
			lang, cfg=cfg)
		qprogedit.addTab(label)
		if var != None:
			self.auto_editor[var] = qprogedit
		self.edit_vbox.addWidget(qprogedit)
		return qprogedit

	def add_text(self, msg):

		"""
		Adds a non-interactive QLabel for description purposes.

		Arguments:
		msg		--	A text message.
		
		Returns:
		A QLabel widget.
		"""

		row = self.edit_grid.rowCount()
		label = QtGui.QLabel(_(msg))
		label.setWordWrap(True)
		self.edit_vbox.addWidget(label)
		return label
		
	def add_stretch(self):
		
		"""Pad empty space below the controls"""
	
		self.edit_vbox.addStretch()

	def apply_button(self, label=u'Apply', icon=u'apply', \
		tooltip=u'Apply changes'):

		"""
		Returns a right-outlined apply QPushButton. The widget is not added
		automatically to the controls. I.e. you need to implement your own
		connections to make the button functional.

		Keyword arguments:
		label		-- A label text. (default=u'Apply')
		icon		-- An icon name. (default=u'Apply')
		tooltip		-- A tooltip text. (default=u'Apply changes')

		Returns:
		A QPushButton widget.
		"""

		button_apply = QtGui.QPushButton(_(label))
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

	def browse_pool_func(self, edit_widget):

		"""
		Returns a function to present a file dialog to browse the file pool.

		Arguments:
		edit_widget		--	A QLineEdit widget.
		
		Returns:
		A function that presents a filepool dialog and sets the edit_widget.
		"""

		def browse_pool():
			s = pool_widget.select_from_pool(self.experiment.main_window)
			if unicode(s) == "":
				return
			edit_widget.setText(s)
			self.apply_edit_changes()
		return browse_pool
		
	def get_ready(self):

		"""
		Applies pending script changes.

		Returns:
		True if changes have been made, False otherwise.
		"""

		for var, qprogedit in self.auto_editor.iteritems():
			if qprogedit.isModified():
				debug.msg(u'applying pending editor changes')
				self.apply_edit_changes()
				return True
		return qtitem.qtitem.get_ready(self)


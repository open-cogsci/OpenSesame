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

__author__ = "Sebastiaan Mathot"
__license__ = "GPLv3"

from PyQt4 import QtCore, QtGui
import os.path
import sip
from libopensesame import debug, exceptions, item
from libqtopensesame.widgets import inline_editor, header_widget
from libqtopensesame.misc import _

class qtitem(QtCore.QObject):

	"""Base class for the GUI controls of other items"""

	def __init__(self):

		"""Constructor"""

		QtCore.QObject.__init__(self)

		# The auto-widgets are stored in name -> (var, widget) dictionaries
		self.auto_line_edit = {}
		self.auto_combobox = {}
		self.auto_spinbox = {}
		self.auto_slider = {}
		self.auto_editor = {}
		self.auto_checkbox = {}
		self.sanity_criteria = {}

		self.init_edit_widget()
		self.init_script_widget()
		self.script_tab = None
		self.lock = False
		self.edit_mode = "edit"

		debug.msg("created %s" % self.name)

	def open_help_tab(self):

		"""Open the help tab"""

		path = self.experiment.help(self.item_type + ".html")
		if not os.path.exists(path):
			path = self.experiment.help("missing.html")
		self.experiment.main_window.ui.tabwidget.open_browser(path)

	def open_tab(self):

		"""Opens the correct tab based on the current edit mode"""

		if self.edit_mode == "edit":
			self.open_edit_tab()
		else:
			self.open_script_tab()

	def init_edit_widget(self, stretch=True):

		"""Build the GUI controls"""

		self.header = header_widget.header_widget(self)

		self.header_hbox = QtGui.QHBoxLayout()
		self.header_hbox.addWidget(self.experiment.label_image(self.item_type))
		self.header_hbox.addWidget(self.header)
		self.header_hbox.addStretch()
		self.header_hbox.setContentsMargins(0, 0, 0, 16)

		button = QtGui.QPushButton(self.experiment.icon("script"), "")
		button.setToolTip(_("Edit script"))
		button.setIconSize(QtCore.QSize(16, 16))
		QtCore.QObject.connect(button, QtCore.SIGNAL("clicked()"), \
			self.open_script_tab)
		self.header_hbox.addWidget(button)

		button = QtGui.QPushButton(self.experiment.icon("help"), "")
		button.setToolTip(_("Tell me more about the %s item") % self.item_type)
		button.setIconSize(QtCore.QSize(16, 16))
		QtCore.QObject.connect(button, QtCore.SIGNAL("clicked()"), \
			self.open_help_tab)
		self.header_hbox.addWidget(button)

		self.header_widget = QtGui.QWidget()
		self.header_widget.setLayout(self.header_hbox)

		self.edit_grid = QtGui.QGridLayout()
		self.edit_grid.setColumnStretch(2, 2)
		self.edit_grid_widget = QtGui.QWidget()
		self.edit_grid.setMargin(0)
		self.edit_grid_widget.setLayout(self.edit_grid)

		self.edit_vbox = QtGui.QVBoxLayout()
		self.edit_vbox.setMargin(16)
		self.edit_vbox.addWidget(self.header_widget)
		self.edit_vbox.addWidget(self.edit_grid_widget)
		if stretch:
			self.edit_vbox.addStretch()
		self._edit_widget = QtGui.QWidget()
		self._edit_widget.setLayout(self.edit_vbox)
		self._edit_widget.__edit_item__ = self.name

		return self._edit_widget

	def edit_widget(self, stretch=True):

		"""
		A dummy edit widget, to be overridden

		Keywords arguments:
		stretch -- a deprecated argument (default=True)
		"""

		if not stretch:
			debug.msg("passing the stretch argument is deprecated", \
				reason="deprecation")
		self.header.restore_name(False)
		self.header.refresh()
		self._edit_widget.__edit_item__ = self.name
		if not self.sanity_check():
			self.open_script_tab()
			return
		self.auto_edit_widget()
		return self._edit_widget

	def apply_name_change(self, rebuild=True):

		"""
		Apply an item name change

		Keywords arguments:
		rebuild -- a deprecated argument (default=True)
		"""

		debug.msg()

		# Sanitize the name, check if it is new and valid, and if so, rename
		new_name = self.experiment.sanitize(self.header.edit_name.text(), \
			strict=True, allow_vars=False)
		if new_name.lower() == self.name.lower():
			self.header.edit_name.setText(self.name)
			return
		valid = self.experiment.check_name(new_name)
		if valid != True:
			self.experiment.notify(valid)
			self.header.edit_name.setText(self.name)
			return
		old_name = self.name
		self.name = new_name
		self._edit_widget.__edit_item__	= new_name
		self.experiment.main_window.dispatch.event_name_change.emit(old_name, \
			new_name)

	def apply_edit_changes(self, rebuild=True):

		"""
		Apply the GUI controls

		Keywords arguments:
		rebuild -- specifies whether the overview area (item list) should be
				   rebuild (default=True)
		"""

		debug.msg(self.name)
		if self.experiment.main_window.lock_refresh:
			debug.msg("skipping, because refresh in progress")
			return False
		self.auto_apply_edit_changes()
		self.set("description", \
			self.experiment.sanitize(unicode( \
				self.header.edit_desc.text()).strip()))
		if self.description == "":
			self.description = "No description"
		self.header.label_desc.setText(self.description)
		self.experiment.main_window.dispatch.event_simple_change.emit(self.name)
		return True

	def close_edit_tab(self, index=None):

		"""
		Closes the edit tab (does nothing by default)

		Keywords arguments:
		index -- the index of the tab in the tab area (default=None)
		"""

		pass

	def open_edit_tab(self, index=None, focus=True):

		"""
		Opens/ shows the GUI control tab

		Keywords arguments:
		index -- the index of the tab (if it is already open) (default=None)
		focus -- indicates whether the tab should receive focus (default=True)
		"""

		debug.msg("%s (#%s)" % (self.name, hash(self)))

		# Switch to edit mode and close the script tab if it was open
		self.edit_mode = "edit"
		for i in range(self.experiment.ui.tabwidget.count()):
			w = self.experiment.ui.tabwidget.widget(i)
			if hasattr(w, "__script_item__") and w.__script_item__ == self.name:
				self.experiment.ui.tabwidget.removeTab(i)
				if index == None:
					index = i
				break

		# Focus the edit tab, instead of reopening, if it was already open
		for i in range(self.experiment.ui.tabwidget.count()):
			w = self.experiment.ui.tabwidget.widget(i)
			if hasattr(w, "__edit_item__") and w.__edit_item__ == self.name:
				index = i

		# Refresh the controls on the tab. In debug mode don't catch any errors
		if debug.enabled:
			widget = self.edit_widget()
		else:
			try:
				widget = self.edit_widget()
			except Exception as e:
				self.experiment.notify(_("%s (Edit the script to fix this)") \
					% e)
				self.open_script_tab()
				return

		# Open the tab or focus the tab if it was already open
		if index == None:
			self.edit_tab_index = self.experiment.ui.tabwidget.addTab(widget, \
				self.experiment.icon(self.item_type), "%s" % self.name)
		else:
			self.experiment.ui.tabwidget.insertTab(index, widget, \
				self.experiment.icon(self.item_type), "%s" % self.name)
			self.edit_tab_index = index
		if focus:
			self.experiment.ui.tabwidget.setCurrentIndex(self.edit_tab_index)

	def apply_script_and_close(self):

		"""Applies script changes and opens the edit tab"""

		self.apply_script_changes()
		self.experiment.main_window.select_item(self.name)

	def ignore_script_and_close(self):

		"""Applies script changes and opens the edit tab"""

		if self.edit_script.edit.isModified():
			resp = QtGui.QMessageBox.question( \
				self.experiment.main_window.ui.centralwidget, \
				_('Forget changes?'), \
				_('Are you sure you want to forget all changes to the script?'), \
				QtGui.QMessageBox.Yes, QtGui.QMessageBox.No)
			if resp == QtGui.QMessageBox.No:
				return
		self.experiment.main_window.select_item(self.name)

	def apply_script_changes(self, rebuild=True, catch=True):

		"""
		Apply changes to the script, by regenerating the item from the script

		Keywords arguments:
		rebuild -- specifies whether the overview area (item list) should be
				   rebuild (default=True)
		catch -- indicates if exceptions should be caught and shown in a
				 notification dialog (True) or not be caught (False)
				 (default=True)
		"""

		debug.msg(self.name)
		script = self.edit_script.edit.toPlainText()

		# Create a new item and make it a clone of the current item
		item = self.experiment.main_window.add_item(self.item_type, False, \
			name=self.name, interactive=False)
		if catch:
			try:
				self.experiment.items[item].from_string(script)
			except Exception as e:
				self.experiment.notify(unicode(e))
				return
		else:
			self.experiment.items[item].from_string(script)
		self.edit_script.setModified(False)
		self.experiment.items[item].name = self.name

		# Replace the current item
		self.experiment.items[self.name] = self.experiment.items[item]
		del self.experiment.items[item]
		self.experiment.items[self.name].init_script_widget()
		self.experiment.main_window.dispatch.event_script_change.emit(self.name)

	def strip_script_line(self, s):

		"""
		Strips unwanted characters from a line of script

		Arguments:
		s -- a line of script

		Returns:
		A stripped line of script
		"""

		if len(s) > 0 and s[0] == "\t":
			return s[1:] + "\n"
		return s + "\n"

	def init_script_widget(self):

		"""Build the script tab"""

		self.edit_script = inline_editor.inline_editor( \
			self.experiment, syntax="opensesame")
		script = ""
		for s in self.to_string().split("\n")[1:]:
			script += self.strip_script_line(s)
		self.edit_script.edit.setPlainText(script, set_modified=False)
		self.edit_script.apply.clicked.connect(self.apply_script_changes)

		button = QtGui.QPushButton(self.experiment.icon("apply"), \
			_("Apply and close"))
		button.setToolTip(_("Apply changes and resume normal editing"))
		button.setIconSize(QtCore.QSize(16, 16))
		button.clicked.connect(self.apply_script_and_close)
		self.edit_script.toolbar_hbox.addWidget(button)

		button = QtGui.QPushButton(self.experiment.icon("close"), \
			_("Forget changes and close"))
		button.setToolTip(_("Ignore changes and resume normal editing"))
		button.setIconSize(QtCore.QSize(16, 16))
		button.clicked.connect(self.ignore_script_and_close)
		self.edit_script.toolbar_hbox.addWidget(button)

		hbox = QtGui.QHBoxLayout()
		hbox.addWidget(self.experiment.label_image("%s" % self.item_type))
		hbox.addWidget(QtGui.QLabel(_("Editing script for <b>%s</b> - %s") % \
			(self.name, self.item_type)))
		hbox.addStretch()
		hbox.setContentsMargins(0,0,0,0)
		hwidget = QtGui.QWidget()
		hwidget.setLayout(hbox)

		vbox = QtGui.QVBoxLayout()
		vbox.addWidget(hwidget)
		vbox.addWidget(self.edit_script)
		self._script_widget = QtGui.QWidget()
		self._script_widget.setLayout(vbox)
		self._script_widget.__script_item__ = self.name

	def script_widget(self):

		"""
		Update the script tab

		Returns:
		The QWidget containing the script tab
		"""

		script = ""
		for s in self.to_string().split("\n")[1:]:
			script += self.strip_script_line(s)
		self.edit_script.edit.setPlainText(script)
		self._script_widget.__script_item__ = self.name
		return self._script_widget

	def open_script_tab(self, index=None, focus=True):

		"""
		Open/ show the script tab

		Keywords arguments:
		index -- the index of the tab (if it is already open) (default=None)
		focus -- indicates whether the tab should receive focus (default=True)
		"""

		debug.msg("%s (#%s)" % (self.name, hash(self)))
		self.edit_mode = "script"

		# Close the edit tab
		for i in range(self.experiment.ui.tabwidget.count()):
			w = self.experiment.ui.tabwidget.widget(i)
			if hasattr(w, "__edit_item__") and w.__edit_item__ == self.name:
				self.experiment.ui.tabwidget.removeTab(i)
				if index == None:
					index = i
				break

		for i in range(self.experiment.ui.tabwidget.count()):
			w = self.experiment.ui.tabwidget.widget(i)
			if hasattr(w, "__script_item__") and w.__script_item__ == self.name:
				index = i
		if index == None:
			self.script_tab_index = self.experiment.ui.tabwidget.addTab( \
				self.script_widget(), self.experiment.icon("script"), "%s" \
				% self.name)
		else:
			self.script_tab_index = index
			self.experiment.ui.tabwidget.insertTab(index, \
				self.script_widget(), self.experiment.icon("script"), "%s" \
				% self.name)
		if focus:
			self.experiment.ui.tabwidget.setCurrentIndex(self.script_tab_index)

	def close_script_tab(self, index=None):

		"""
		Close the script tab (does nothing by defaut)

		Keywords arguments:
		index -- the index of the tab in the tab area (default=None)
		"""

		pass

	def rename(self, from_name, to_name):

		"""
		Handle the renaming of an item (not necesarrily the currnet item)

		Arguments:
		from_name -- the old item name
		to_name -- the new item name
		"""

		if self.name == from_name:
			self.name = to_name

	def delete(self, item_name, item_parent=None, index=None):

		"""
		Delete an item (not necessarily the current one)

		Arguments:
		item_name -- the name of the item to be deleted

		Keywords arguments:
		item_parent -- the parent item (default=None)
		index -- the index of the item in the parent (default=None)
		"""

		pass

	def rename_var(self, item, from_name, to_name):

		"""
		A notification that a variable has been renamed

		Arguments:
		item -- the item doing the renaming
		from_name -- the old variable name
		to_name -- the new variable name
		"""

		pass

	def item_tree_widget(self, toplevel, icon=None, name=None, tooltip=None):

		"""
		Create a single item tree widget

		Arguments:
		toplevel -- the toplevel item

		Keyword arguments:
		icon -- an icon name or None for default (default=None)
		name -- the name of the item or None for default (default=None)
		tooltip -- the tooltip or None for default (default=None)

		Returns:
		A QTreeWidgetItem
		"""

		if name == None:
			name = self.name
		if icon == None:
			icon = self.item_type
		if tooltip == None:
			tooltip = _("Type: %s\nDescription: %s") % (self.item_type, \
				self.description)
		font = QtGui.QFont()
		font.setPointSize(8)
		font.setItalic(True)
		widget = QtGui.QTreeWidgetItem(toplevel)
		widget.setText(0, name)
		widget.setIcon(0, self.experiment.icon(icon))
		widget.name = name
		widget.setToolTip(0, tooltip)
		return widget

	def build_item_tree(self, toplevel=None, items=[]):

		"""
		Construct an item tree

		Keyword arguments:
		toplevel -- the toplevel widget (default = None)
		items -- a list of items that have been added, to prevent recursion
				 (default=[])
		"""

		toplevel.addChild(self.item_tree_widget(toplevel))

	def is_offspring(self, item):

		"""
		Checks if the item is offspring of the current item, in the sense that
		the current item is contained by the item

		Arguments:
		item -- the potential offspring

		Returns:
		True if the current item is offspring of the item, False otherwise
		"""

		return False

	def parents(self):

		"""
		Creates a list of all the items	that the current sequences is connected
		to upstream

		Returns:
		A list of item names
		"""

		l = [self.name]
		for item in self.experiment.items:
			if self.experiment.items[item].is_offspring(self.name):
				l.append(item)
		return l

	def variable_vars(self, exclude=[]):

		"""
		Determines if one of the variables of the current item is defined in
		terms of another variable

		Keywords arguments:
		exclude -- a list of variables that should not be checked

		Returns:
		True if there are variably defined variables, False otherwise
		"""

		for var in self.variables:
			if var not in exclude:
				val = self.variables[var]
				if type(val) in (unicode, str) and '[' in val:
					return True
		return False

	def get_ready(self):

		"""
		This function should be overridden to do any last-minute stuff that
		and item should do before an experiment is actually run, such as
		applying pending script changes.

		Returns:
		True if some action has been taken, False if nothing was done
		"""

		if self.edit_script.isModified():
			debug.msg("applying pending script changes")
			self.apply_script_changes(catch=False)
			return True
		return False

	def auto_edit_widget(self):

		"""Update the GUI controls based on the auto-widgets"""

		debug.msg()
		for var, edit in self.auto_line_edit.iteritems():
			edit.editingFinished.disconnect()
			if self.has(var):
				try:
					edit.setText(self.unistr(self.get(var, _eval=False)))
				except Exception as e:
					self.experiment.notify(_("Failed to set control '%s': %s") \
						% (var, e))
			else:
				edit.setText("")
			edit.editingFinished.connect(self.apply_edit_changes)

		for var, combobox in self.auto_combobox.iteritems():
			combobox.currentIndexChanged.disconnect()
			if self.has(var):
				try:
					combobox.setCurrentIndex(combobox.findText( \
						self.unistr(self.get(var, _eval=False))))
				except Exception as e:
					self.experiment.notify(_("Failed to set control '%s': %s") \
						% (var, e))
			combobox.currentIndexChanged.connect(self.apply_edit_changes)

		for var, spinbox in self.auto_spinbox.iteritems():
			spinbox.editingFinished.disconnect()
			if self.has(var):
				try:
					spinbox.setValue(self.get(var, _eval=False))
				except Exception as e:
					self.experiment.notify(_("Failed to set control '%s': %s") \
						% (var, e))
			spinbox.editingFinished.connect(self.apply_edit_changes)

		for var, slider in self.auto_slider.iteritems():
			slider.valueChanged.disconnect()
			if self.has(var):
				try:
					slider.setValue(self.get(var, _eval=False))
				except Exception as e:
					self.experiment.notify(_("Failed to set control '%s': %s") \
						% (var, e))
			slider.valueChanged.connect(self.apply_edit_changes)

		for var, checkbox in self.auto_checkbox.iteritems():
			checkbox.toggled.disconnect()
			if self.has(var):
				try:
					checkbox.setChecked(self.get(var, _eval=False) == "yes")
				except Exception as e:
					self.experiment.notify(_("Failed to set control '%s': %s") \
						% (var, e))
			checkbox.toggled.connect(self.apply_edit_changes)

		for var, editor in self.auto_editor.iteritems():
			if self.has(var):
				try:
					editor.edit.setPlainText(self.unistr(self.get(var, \
						_eval=False)))
				except Exception as e:
					self.experiment.notify(_("Failed to set control '%s': %s") \
						% (var, e))

	def sanitize_check(self, s, strict=False, allow_vars=True, notify=True):

		"""
		Checks whether a string is sane (i.e. unchanged by sanitize()) and
		optionally presents a warning if it's notably

		Arguments:
		s -- the string to check

		Keyword arguments:
		strict -- see sanitize()
		allow_vars -- see sanitize()
		notify -- indicates whether a notification should be presented if the
				  string is not sane.

		Returns:
		True if s is sane, False otherwise
		"""

		sane = s == self.sanitize(s, strict=strict, allow_vars=allow_vars)
		if not sane and notify:
			if strict:
				self.experiment.notify(
					_('All non-alphanumeric characters except underscores have been stripped'))
			else:
				self.experiment.notify(
					_('The following characters are not allowed and have been stripped: double-quote ("), backslash (\), and newline'))
		return sane

	def sanity_check(self):

		"""
		Checks whether all variables match prespecified criteria and fall back
		to the script editor otherwise. This is usefull to check that certain
		variables are numeric, etc.
		"""

		debug.msg()
		errors = []
		for var_name, criteria in self.sanity_criteria.items():
			msg = _("Invalid or missing value for variable '%s' (edit script to fix this)") \
				% var_name
			if 'msg' in criteria:
				msg += ': ' + criteria['msg']
			if not self.has(var_name) and 'required' in criteria and \
				criteria['required']:
				self.experiment.notify(msg)
				return False
			else:
				var = self.get(var_name, _eval=False)
				if 'type' in criteria:
					_type = criteria['type']
					if type(_type) != list:
						_type = [_type]
				 	if type(var) not in _type:
						self.experiment.notify(msg)
						return False
				if 'func' in criteria:
					if not criteria['func'](var):
						self.experiment.notify(msg)
						return False
		return True

	def auto_apply_edit_changes(self, rebuild=True):

		"""
		Apply the auto-widget controls

		Keyword arguments:
		rebuild -- deprecated (does nothing) (default=True)
		"""

		debug.msg()
		for var, edit in self.auto_line_edit.iteritems():
			if type(var) == str:
				val = unicode(edit.text()).strip()
				if val != "":
					self.set(var, val)

				# If the variable has no value, we assign a default value if it
				# has been specified, and unset it otherwise.
				elif hasattr(edit, "default"):
					self.set(var, edit.default)
				else:
					self.unset(var)

		for var, combobox in self.auto_combobox.iteritems():
			if type(var) == str:
				self.set(var, unicode(combobox.currentText()))

		for var, spinbox in self.auto_spinbox.iteritems():
			if type(var) == str:
				self.set(var, spinbox.value())

		for var, slider in self.auto_slider.iteritems():
			if type(var) == str:
				self.set(var, slider.value())

		for var, checkbox in self.auto_checkbox.iteritems():
			if type(var) == str:
				if checkbox.isChecked():
					val = "yes"
				else:
					val = "no"
				self.set(var, val)

		for var, editor in self.auto_editor.iteritems():
			if type(var) == str:
				self.set(var, editor.edit.toPlainText())
				editor.setModified(False)

		return True

	def auto_add_widget(self, widget, var=None):

		"""
		Add a widget to the list of auto-widgets

		Arguments:
		widget -- a QWidget

		Keyword arguments:
		var -- the variable to be linked to the widget (default=None)
		"""

		# Use the object id as a fallback name
		if var == None:
			var = id(widget)
		debug.msg(var)

		if isinstance(widget, QtGui.QSpinBox) or isinstance(widget, \
			QtGui.QDoubleSpinBox):
			widget.editingFinished.connect(self.apply_edit_changes)
			self.auto_spinbox[var] = widget

		elif isinstance(widget, QtGui.QComboBox):
			widget.currentIndexChanged.connect(self.apply_edit_changes)
			self.auto_combobox[var] = widget

		elif isinstance(widget, QtGui.QSlider):
			widget.editingFinished.connect(self.apply_edit_changes)
			self.auto_slider[var] = widget

		elif isinstance(widget, QtGui.QLineEdit):
			widget.editingFinished.connect(self.apply_edit_changes)
			self.auto_line_edit[var] = widget

		elif isinstance(widget, QtGui.QCheckBox):
			widget.toggled.connect(self.apply_edit_changes)
			self.auto_checkbox[var] = widget

		else:
			raise Exception("Cannot auto-add widget of type %s" % widget)


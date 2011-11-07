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
import os.path
import sip
import libopensesame.exceptions
import libqtopensesame.inline_editor
import libqtopensesame.help_browser
import libqtopensesame.syntax_highlighter


class header_widget(QtGui.QWidget):

	"""Provides clickable and editable labels for the item's name and description"""

	def __init__(self, item):

		"""
		Constructor

		Arguments:
		item -- the item to provide a header for
		"""

		QtGui.QWidget.__init__(self)
		self.setCursor(QtCore.Qt.IBeamCursor)
		self.setToolTip("Click to edit")
		self.item = item
		self.label_name = QtGui.QLabel()
		self.label_name.id = "name"
		self.edit_name = QtGui.QLineEdit()
		self.edit_name.editingFinished.connect(self.restore_name)
		self.edit_name.hide()
		self.label_desc = QtGui.QLabel()
		self.label_desc.id = "desc"
		self.edit_desc = QtGui.QLineEdit()
		self.edit_desc.editingFinished.connect(self.restore_desc)
		self.edit_desc.hide()
		vbox = QtGui.QVBoxLayout()
		vbox.setContentsMargins(8, 0, 0, 0)
		vbox.setSpacing(0)
		vbox.addWidget(self.label_name)
		vbox.addWidget(self.edit_name)
		vbox.addWidget(self.label_desc)
		vbox.addWidget(self.edit_desc)
		self.refresh()
		self.setLayout(vbox)

	def refresh(self):

		"""Update the header"""

		self.edit_name.setText(self.item.name)
		self.label_name.setText("<font size='5'><b>%s</b> - %s</font>&nbsp;&nbsp;&nbsp;<font color='gray'><i>Click to edit</i></font>" \
			% (self.item.name, self.item.item_type.replace("_", " ").title()))
		self.edit_desc.setText(self.item.description)
		self.label_desc.setText(self.item.description)

	def restore_name(self, apply_name_change = True):

		"""
		Apply the name change and revert the edit control back to the static label

		Keywords arguments:
		apply_name_change -- indicates of the name change should be applied (default = True)
		"""

		if apply_name_change:
			self.item.apply_name_change()
		self.label_name.show()
		self.edit_name.hide()

	def restore_desc(self):

		"""Apply the description change and revert the edit	back to the label"""

		self.item.apply_edit_changes()
		self.label_desc.show()
		self.edit_desc.hide()

	def mousePressEvent(self, event):

		"""
		Change the label into an edit for the name or
		the description, depending on where has been
		clicked

		Arguments:
		event -- the mouseClickEvent
		"""

		target = self.childAt(event.pos())

		if target != None and hasattr(target, "id"):
			if target.id == "name":
				self.restore_desc()
				self.label_name.hide()
				self.edit_name.show()
				self.edit_name.selectAll()
				self.edit_name.setFocus()
			else:
				self.restore_name()
				self.label_desc.hide()
				self.edit_desc.show()
				self.edit_desc.selectAll()
				self.edit_desc.setFocus()

class qtitem(object):

	"""
	The qtitem provides a base class for all
	other items
	"""

	def __init__(self):

		"""Constructor"""

		self.init_edit_widget()
		self.init_script_widget()
		self.script_tab = None
		self.lock = False
		self.edit_mode = "edit"
		
		if self.experiment.debug:
			print "qtitem.__init__(): created %s" % self.name

	def open_help_tab(self):

		"""Open the help tab"""

		i = self.experiment.main_window.get_tab_index("__help__%s__" % self.item_type)
		if i != None:
			self.experiment.main_window.switch_tab(i)
		else:
			path = self.experiment.help(self.item_type + ".html")
			text = libqtopensesame.help_browser.help_browser(path, self.item_type)
			text.help_item = self.name
			index = self.experiment.ui.tabwidget.addTab(text, self.experiment.icon("help"), self.name)
			self.experiment.ui.tabwidget.setCurrentIndex(index)
			
	def open_tab(self):
	
		"""Opens the correct tab based on the current edit mode"""
	
		if self.edit_mode == "edit":
			self.open_edit_tab()
		else:
			self.open_script_tab()
			
	def init_edit_widget(self, stretch=True):

		"""Build the GUI controls"""

		self.header = header_widget(self)

		self.header_hbox = QtGui.QHBoxLayout()
		self.header_hbox.addWidget(self.experiment.label_image("%s_large" % self.item_type))
		self.header_hbox.addWidget(self.header)
		self.header_hbox.addStretch()
		self.header_hbox.setContentsMargins(0, 0, 0, 16)

		button = QtGui.QPushButton(self.experiment.icon("script"), "")
		button.setToolTip("Edit script")
		button.setIconSize(QtCore.QSize(16, 16))
		QtCore.QObject.connect(button, QtCore.SIGNAL("clicked()"), self.open_script_tab)
		self.header_hbox.addWidget(button)

		button = QtGui.QPushButton(self.experiment.icon("help"), "")
		button.setToolTip("Tell me more about the %s item" % self.item_type)
		button.setIconSize(QtCore.QSize(16, 16))
		QtCore.QObject.connect(button, QtCore.SIGNAL("clicked()"), self.open_help_tab)
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
		self._edit_widget.edit_item = self.name

		return self._edit_widget

	def edit_widget(self, stretch=True):

		"""
		A dummy edit widget, to be overridden
		
		Keywords arguments:
		stretch -- a deprecated argument (default=True)
		"""

		if self.experiment.debug and not stretch:
			print "*** qtitem.edit_widget(): passing the stretch argument is deprecated"
		self.header.restore_name(False)
		self.header.refresh()
		self._edit_widget.edit_item = self.name
		return self._edit_widget

	def apply_name_change(self, rebuild=True):

		"""
		Apply an item name change
		
		Keywords arguments:
		rebuild -- a deprecated argument (default=True)
		"""

		new_name = self.experiment.sanitize(self.header.edit_name.text(), \
			strict=True, allow_vars=False)
		# Do nothing is the name stays the same
		if new_name == self.name:
			self.header.edit_name.setText(self.name)
			return
		valid = self.experiment.check_name(new_name)
		if valid != True:
			self.experiment.notify(valid)
			self.header.edit_name.setText(self.name)
		else:
			# Pass on the word
			self.experiment.main_window.set_unsaved()
			self.experiment.rename(self.name, new_name)		

	def apply_edit_changes(self, rebuild=True):

		"""
		Apply the GUI controls
		
		Keywords arguments:
		rebuild -- specifies whether the overview area (item list) should be
				   rebuild (default=True)
		"""

		if self.experiment.debug:
			print "qtitem.apply_edit_changes():", self.name

		if self.experiment.main_window.lock_refresh:
			if self.experiment.debug:
				print "qtitem.apply_edit_changes(): skipping, because refresh in progress"
			return False

		self.set("description", \
			self.experiment.sanitize(str(self.header.edit_desc.text()).strip()))
		if self.description == "":
			self.description = "No description"
		self.header.label_desc.setText(self.description)

		if rebuild:
			self.experiment.main_window.build_item_list()
		self.experiment.main_window.set_unsaved()
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
		
		if self.experiment.debug:
			print "qtitem.open_edit_tab(): %s (#%s)" % (self.name, hash(self))		
			
		self.edit_mode = "edit"
				
		# Close the script tab
		for i in range(self.experiment.ui.tabwidget.count()):
			w = self.experiment.ui.tabwidget.widget(i)
			if hasattr(w, "script_item") and w.script_item == self.name:
				self.experiment.ui.tabwidget.removeTab(i)
				if index == None:
					index = i
				break

		for i in range(self.experiment.ui.tabwidget.count()):
			w = self.experiment.ui.tabwidget.widget(i)
			if hasattr(w, "edit_item") and w.edit_item == self.name:
				index = i

		try:
			widget = self.edit_widget()
		except Exception as e:
			self.experiment.notify("%s (Edit the script to fix this)" % e)
			self.open_script_tab()
			return
			
		if index == None:
			self.edit_tab_index = self.experiment.ui.tabwidget.addTab(widget, self.experiment.icon(self.item_type), "%s" % self.name)
		else:
			self.experiment.ui.tabwidget.insertTab(index, widget, self.experiment.icon(self.item_type), "%s" % self.name)
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
			resp = QtGui.QMessageBox.question(self.experiment.main_window.ui.centralwidget, "Forget changes?",\
				"Are you sure you want to forget all changes to the script?", QtGui.QMessageBox.Yes, QtGui.QMessageBox.No)
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

		if self.experiment.debug:
			print "qtitem.apply_script_changes():", self.name
		script = self.experiment.usanitize(self.edit_script.edit.toPlainText())
		
		# Create a new item and make it a clone of the current item
		item = self.experiment.main_window.add_item(self.item_type, False, name=self.name)
		if catch:
			try:
				self.experiment.items[item].from_string(script)
			except Exception as e:
				self.experiment.notify(str(e))
				return
		else:
			self.experiment.items[item].from_string(script)
		self.edit_script.setModified(False)
		self.experiment.items[item].name = self.name
		
		# Replace the current item
		self.experiment.items[self.name] = self.experiment.items[item]
		del self.experiment.items[item]
		self.experiment.items[self.name].init_script_widget()
		
		# Refresh the experiment
		self.experiment.main_window.hard_refresh(self.name)
		self.experiment.main_window.refresh(self.name)

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

		self.edit_script = libqtopensesame.inline_editor.inline_editor(self.experiment, syntax="opensesame")
		script = ""
		for s in self.to_string().split("\n")[1:]:
			script += self.strip_script_line(s)
		self.edit_script.edit.setPlainText(script)
		self.edit_script.apply.clicked.connect(self.apply_script_changes)		
		
		button = QtGui.QPushButton(self.experiment.icon("apply"), "Apply and close")
		button.setToolTip("Apply changes and resume normal editing")
		button.setIconSize(QtCore.QSize(16, 16))
		button.clicked.connect(self.apply_script_and_close)
		self.edit_script.toolbar_hbox.addWidget(button)		
		
		button = QtGui.QPushButton(self.experiment.icon("close"), "Forget changes and close")
		button.setToolTip("Ignore changes and resume normal editing")
		button.setIconSize(QtCore.QSize(16, 16))
		button.clicked.connect(self.ignore_script_and_close)
		self.edit_script.toolbar_hbox.addWidget(button)				
		
		hbox = QtGui.QHBoxLayout()		
		hbox.addWidget(self.experiment.label_image("%s" % self.item_type))
		hbox.addWidget(QtGui.QLabel("Editing script for <b>%s</b> - %s" % (self.name, self.item_type)))
		hbox.addStretch()
		hbox.setContentsMargins(0,0,0,0)
		hwidget = QtGui.QWidget()
		hwidget.setLayout(hbox)
		
		vbox = QtGui.QVBoxLayout()
		vbox.addWidget(hwidget)
		vbox.addWidget(self.edit_script)
		self._script_widget = QtGui.QWidget()
		self._script_widget.setLayout(vbox)
		self._script_widget.script_item = self.name

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
		self._script_widget.script_item = self.name		
		return self._script_widget

	def open_script_tab(self, index=None, focus=True):

		"""
		Open/ show the script tab
				
		Keywords arguments:
		index -- the index of the tab (if it is already open) (default=None)
		focus -- indicates whether the tab should receive focus (default=True)		
		"""
		
		if self.experiment.debug:
			print "qtitem.open_script_tab(): %s (#%s)" % (self.name, hash(self))		
			
		self.edit_mode = "script"			

		# Close the edit tab
		for i in range(self.experiment.ui.tabwidget.count()):
			w = self.experiment.ui.tabwidget.widget(i)
			if hasattr(w, "edit_item") and w.edit_item == self.name:
				self.experiment.ui.tabwidget.removeTab(i)
				if index == None:
					index = i
				break
				
		for i in range(self.experiment.ui.tabwidget.count()):
			w = self.experiment.ui.tabwidget.widget(i)
			if hasattr(w, "script_item") and w.script_item == self.name:
				index = i
		if index == None:
			self.script_tab_index = self.experiment.ui.tabwidget.addTab(self.script_widget(), self.experiment.icon("script"), "%s" % self.name)
		else:
			self.script_tab_index = index
			self.experiment.ui.tabwidget.insertTab(index, self.script_widget(), self.experiment.icon("script"), "%s" % self.name)
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

	def item_tree_info(self):

		"""
		Returns an info string for the item tree widget

		Returns:
		An info string
		"""

		return ""

	def item_tree_widget(self, toplevel, icon = None, name = None, tooltip = None, info = None):

		"""
		Create a single item tree widget

		Arguments:
		toplevel -- the toplevel item

		Keyword arguments:
		icon -- an icon name or None for default (default = None)
		name -- the name of the item or None for default (default = None)
		info -- info for the second column or None for default (default = None)
		tooltip -- the tooltip or None for default (default = None)

		Returns:
		A QTreeWidgetItem
		"""

		if name == None:
			name = self.name
		if icon == None:
			icon = self.item_type
		if tooltip == None:
			tooltip = "Type: %s\nDescription: %s" % (self.item_type, self.description)
		if info == None:
			info = self.item_tree_info()
		font = QtGui.QFont()
		font.setPointSize(8)
		font.setItalic(True)
		widget = QtGui.QTreeWidgetItem(toplevel)
		widget.setText(0, name)
		widget.setIcon(0, self.experiment.icon(icon))
		widget.setText(1, info)
		widget.setFont(1, font)
		widget.name = name
		widget.setToolTip(0, tooltip)
		widget.setToolTip(1, tooltip)
		return widget

	def build_item_tree(self, toplevel = None, items = []):

		"""
		Construct an item tree

		Keyword arguments:
		toplevel -- the toplevel widget (default = None)
		items -- a list of items that have been added, to prevent recursion (default = [])
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
			if var not in exclude and str(self.variables[var]).find("[") >= 0:
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
			if self.experiment.debug:
				print "inline_script.finalize(): applying pending OpenSesame script changes"
			self.apply_script_changes(catch=False)
			return True
		return False


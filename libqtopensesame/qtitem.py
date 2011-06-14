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
		self.label_name.setText("<font size='5'><b>%s</b> - %s</font>&nbsp;&nbsp;&nbsp;<font color='gray'><i>Click to edit</i></font>" % (self.item.name, self.item.item_type.replace("_", " ").title()))
		self.label_name.id = "name"

		self.edit_name = QtGui.QLineEdit(self.item.name)
		self.edit_name.editingFinished.connect(self.restore_name)
		self.edit_name.hide()

		self.label_desc = QtGui.QLabel(self.item.description)
		self.label_desc.id = "desc"

		self.edit_desc = QtGui.QLineEdit(self.item.description)
		self.edit_desc.editingFinished.connect(self.restore_desc)
		self.edit_desc.hide()

		vbox = QtGui.QVBoxLayout()
		vbox.setContentsMargins(8, 0, 0, 0)
		vbox.setSpacing(0)
		vbox.addWidget(self.label_name)
		vbox.addWidget(self.edit_name)
		vbox.addWidget(self.label_desc)
		vbox.addWidget(self.edit_desc)

		self.setLayout(vbox)

	def restore_name(self, apply_name_change = True):

		"""
		Apply the name change and revert the edit control back to the static label

		Keywords arguments:
		apply_name_change -- indicates of the name change should be applied (default = True)
		"""

		if apply_name_change:
			self.item.apply_name_change()

		self.label_name.setText("<font size='5'><b>%s</b> - %s</font>&nbsp;&nbsp;&nbsp;<font color='gray'><i>Click to edit</i></font>" % (self.item.name, self.item.item_type.replace("_", " ").title()))
		self.label_name.show()
		self.edit_name.setText(self.item.name)
		self.edit_name.hide()

	def restore_desc(self):

		"""Apply the description change and revert the edit	back to the label"""

		self.item.apply_edit_changes()
		self.label_desc.setText(self.item.description)
		self.label_desc.show()
		self.edit_desc.setText(self.item.description)
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

		"""
		Initialize the qtitem
		"""

		self.init_edit_widget()
		self.init_script_widget()
		self.script_tab = None
		self.lock = False

		if self.experiment.debug:
			print "qtitem.__init__(): created %s" % self.name

	def open_help_tab(self):

		"""
		Open the help tab
		"""

		i = self.experiment.main_window.get_tab_index("__help__%s__" % self.item_type)
		if i != None:
			self.experiment.main_window.switch_tab(i)
		else:
			path = self.experiment.help(self.item_type + ".html")
			text = libqtopensesame.help_browser.help_browser(path, self.item_type)
			text.help_item = self.name
			index = self.experiment.ui.tabwidget.addTab(text, self.experiment.icon("help"), self.name)
			self.experiment.ui.tabwidget.setCurrentIndex(index)

	def init_edit_widget(self, stretch = True):

		"""
		Build the init widget
		"""

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

	def edit_widget(self, stretch = True):

		"""
		A dummy edit widget
		"""

		if self.experiment.debug and not stretch:
			print "*** qtitem.edit_widget(): passing the stretch argument is deprecated"

		if self.experiment.debug:
			print "qtitem.edit_widget(): %s" % self.name

		self.header.restore_name(False)
		#self.header.edit_name.setText(self.name)
		#self.header.edit_desc.setText(self.description)

		return self._edit_widget

	def apply_name_change(self, rebuild = True):

		"""
		Is called when the name of an item needs to be changed
		"""

		new_name = self.experiment.sanitize(str(self.header.edit_name.text()).strip(), True)

		# Do nothing is the name stays the same
		if new_name == self.name:
			self.header.edit_name.setText(self.name)
			return

		# Make sure the name is not empty
		if new_name == "":
			self.experiment.notify("An item must have a (non-empty) name")
			self.header.edit_name.setText(self.name)
			return

		# Make sure the name is not taken
		if new_name in self.experiment.items:
			self.experiment.notify("An item named '%s' already exists" % new_name)
			self.header.edit_name.setText(self.name)
			return

		# Pass on the word
		self.experiment.main_window.set_unsaved()
		self.experiment.rename(self.name, new_name)

	def apply_edit_changes(self, rebuild = True):

		"""
		Is called when changes are made to the item
		"""

		if self.experiment.debug:
			print "qtitem.apply_edit_changes():", self.name

		if self.experiment.main_window.lock_refresh:
			if self.experiment.debug:
				print "qtitem.apply_edit_changes(): skipping, because refresh in progress"
			return False

		self.set("description", self.experiment.sanitize(str(self.header.edit_desc.text()).strip()))
		if self.description == "":
			self.description = "No description"

		if rebuild:
			self.experiment.main_window.build_item_list()
		self.experiment.main_window.set_unsaved()
		return True

	def close_edit_tab(self, index = None):

		"""
		Closes the edit tab
		"""

		pass

	def open_edit_tab(self, index = None, focus = True):

		"""
		Opens a tab containing the edit widget
		"""

		if self.experiment.debug:
			print "qtitem.open_edit_tab():", self.name

		for i in range(self.experiment.ui.tabwidget.count()):
			w = self.experiment.ui.tabwidget.widget(i)
			if hasattr(w, "edit_item") and w.edit_item == self.name:
				index = i

		widget = self.edit_widget()

		if index == None:
			self.edit_tab_index = self.experiment.ui.tabwidget.addTab(widget, self.experiment.icon(self.item_type), "%s" % self.name)
		else:
			self.experiment.ui.tabwidget.insertTab(index, widget, self.experiment.icon(self.item_type), "%s" % self.name)
			self.edit_tab_index = index

		if focus:
			self.experiment.ui.tabwidget.setCurrentIndex(self.edit_tab_index)

	def apply_script_changes(self, rebuild = True, catch = True):

		"""
		Reloads the item based on the new script
		"""

		if self.experiment.debug:
			print "qtitem.apply_script_changes():", self.name

		script = self.experiment.usanitize(self.edit_script.edit.toPlainText())

		# Create a new item and make it a clone of the current item
		item = self.experiment.main_window.add_item(self.item_type, False)

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

		# Refresh the experiment
		self.experiment.main_window.hard_refresh(self.name)
		self.experiment.main_window.refresh(self.name)

	def strip_script_line(self, s):

		"""
		Strips the unwanted characters from the script line
		"""

		if len(s) > 0 and s[0] == "\t":
			return s[1:] + "\n"
		return s + "\n"

	def init_script_widget(self):

		"""
		Build the script widget
		"""

		self.edit_script = libqtopensesame.inline_editor.inline_editor(self.experiment)
		libqtopensesame.syntax_highlighter.syntax_highlighter(self.edit_script.edit.document(), libqtopensesame.syntax_highlighter.opensesame_keywords)

		script = ""
		for s in self.to_string().split("\n")[1:]:
			script += self.strip_script_line(s)

		self.edit_script.edit.setPlainText(script)
		self.edit_script.apply.clicked.connect(self.apply_script_changes)

		vbox = QtGui.QVBoxLayout()
		vbox.addWidget(self.edit_script)

		self._script_widget = QtGui.QWidget()
		self._script_widget.setLayout(vbox)
		self._script_widget.script_item = self.name

	def script_widget(self):

		"""
		Creates the script widget
		"""

		if self.experiment.debug:
			print "qtitem.script_widget(): %s" % self.name

		script = ""
		for s in self.to_string().split("\n")[1:]:
			script += self.strip_script_line(s)
		self.edit_script.edit.setPlainText(script)

		return self._script_widget

	def open_script_tab(self, index = None, focus = True):

		"""
		Opens a tab containing the script widget
		"""

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

	def close_script_tab(self, index = None):

		"""
		Closes the script tab
		"""

		pass

	def rename(self, from_name, to_name):

		"""
		Renames an item
		"""

		if self.name == from_name:
			self.name = to_name

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
		Checks if the item is offspring
		of the current item
		"""

		return False

	def parents(self):

		"""
		Gives a list of all the items
		that the current sequences is connected
		with upstream
		"""

		l = [self.name]
		for item in self.experiment.items:
			if self.experiment.items[item].is_offspring(self.name):
				l.append(item)
		return l

	def variable_vars(self, exclude = []):

		"""
		Returns True if one of the variables is defined in terms
		of another variable, e.g., 'set duration [soa]'
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
		"""

		if self.edit_script.isModified():
			if self.experiment.debug:
				print "inline_script.finalize(): applying pending OpenSesame script changes"
			self.apply_script_changes(catch = False)
			return True
		return False


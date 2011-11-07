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

import libopensesame.experiment
import libopensesame.plugins
from PyQt4 import QtCore, QtGui
import os.path

class experiment(libopensesame.experiment.experiment):

	"""Contains various GUI controls for the experiment"""

	def __init__(self, main_window, name, string = None, pool_folder = None):

		"""
		Constructor

		Arguments:
		main_window -- the GUI main window
		name -- the name of the experiment

		Keyword arguments:
		string -- a definition string for the experiment (default = None)
		pool_folder -- a path to be used for the file pool (default = None)
		"""

		self.main_window = main_window
		self.ui = self.main_window.ui
		self.unused_items = []
		self.core_items = "loop", "sequence", "sketchpad", "feedback", "sampler", "synth", "keyboard_response", "mouse_response", "logger", "inline_script"
		libopensesame.experiment.experiment.__init__(self, name, string, pool_folder)

	def help(self, name):

		"""
		Return the full path to a help file

		Arguments:
		name -- the name of the help file (e.g., "sequence.html")

		Returns:
		The full path to the help file or an empty string if the
		help file was not found
		"""

		# Check in the subfolder of the current path, which is
		# where the helpfile will be on Windows
		path = os.path.join("help", name)
		if os.path.exists(path):
			return path

		# Check in the shared folders
		if os.name == "posix":
			path = "/usr/share/opensesame/help/%s" % name
			if os.path.exists(path):
				return path

		# Fall back to the resource folder if the help
		# file is not found
		try:
			return self.resource(name)
		except:
			pass

		# Return an empty string if not found
		return ""

	def module_container(self):

		"""Specifies the module that is used to get items from"""

		return "libqtopensesame"

	def item_prefix(self):

		"""A prefix that should be added to classes for plugins"""

		return "qt"

	def build_item_tree(self, toplevel = None, items = []):

		"""
		Construct an item tree

		Keyword arguments:
		toplevel -- the toplevel widget (default = None)
		items -- a list of items that have been added, to prevent recursion (default = [])

		Returns:
		An updated list of items that have been added
		"""

		self.ui.itemtree.clear()

		items = []

		# First build the tree of the experiment
		widget = QtGui.QTreeWidgetItem(self.ui.itemtree)
		widget.setText(0, self.title)
		widget.setIcon(0, self.icon("experiment"))
		widget.setToolTip(0, "General options")
		widget.name = "__general__"
		self.ui.itemtree.insertTopLevelItem(0, widget)

		if self.start in self.items:
			items.append(self.items[self.start])
			self.items[self.start].build_item_tree(widget, items)
		widget.setExpanded(True)

		# Next build a tree with left over items

		self.unused_widget = QtGui.QTreeWidgetItem(self.ui.itemtree)
		self.unused_widget.setText(0, "Unused items")
		self.unused_widget.setIcon(0, self.icon("unused"))
		self.unused_widget.name = "__unused__"
		self.unused_widget.setToolTip(0, "Unused items")
		self.unused_widget.setToolTip(1, "Unused items")

		self.ui.itemtree.insertTopLevelItem(1, widget)

		self.unused_items = []
		c = 0
		for i in self.items:
			if self.items[i] not in items:
				self.unused_items.append(i)
				self.items[i].build_item_tree(self.unused_widget, items)
				c += 1
		self.unused_widget.setExpanded(False)

		font = QtGui.QFont()
		font.setPointSize(8)
		font.setItalic(True)

		if c > 0:
			self.unused_widget.setText(1, "contains items")
		else:
			self.unused_widget.setText(1, "empty")
		self.unused_widget.setFont(1, font)

		return items

	def rename(self, from_name, to_name):

		"""
		Rename an item

		Arguments:
		from_name -- the original name
		to_name -- the new name
		"""

		to_name = self.sanitize(to_name, True)

		if self.debug:
			print "experiment.rename(): from '%s' to '%s'" % (from_name, to_name)

		if self.get("start") == from_name:
			self.set("start", to_name)

		for item in self.items:
			self.items[item].rename(from_name, to_name)

		new_items = {}
		for item in self.items:
			if item == from_name:
				new_items[to_name] = self.items[item]
			else:
				new_items[item] = self.items[item]
		self.items = new_items

		for i in range(self.experiment.ui.tabwidget.count()):
			w = self.experiment.ui.tabwidget.widget(i)
			if hasattr(w, "edit_item") and w.edit_item == from_name:
				self.experiment.ui.tabwidget.setTabText(i, to_name)
				self.items[to_name].header.restore_name(False)
				w.edit_item = to_name
			if hasattr(w, "script_item") and w.script_item == from_name:
				w.script_item = to_name
				self.experiment.ui.tabwidget.setTabText(i, to_name)

		self.main_window.refresh()
		
	def check_name(self, name):
	
		"""
		Checks whether a given name is allowed. Reasons for not being allowed
		are invalid characters or match with an existing name.
		
		Arguments:
		name -- the name to check
		
		Returns:
		True if the name is allowed, False otherwise
		"""
		
		if name.strip() == "":
			return "Empty names are not allowed"
		if name.lower() in [item.lower() for item in self.items.keys()]:
			return "An item with that name already exists"	
		if name != self.sanitize(name, strict=True, allow_vars=False):
			return "Name contains special characters. Only alphanumeric characters and underscores are allowed."
		return True
		
	def delete(self, item_name, item_parent=None, index=None):
	
		"""
		Delete an item
		
		Arguments:
		item_name -- the name of the item to be deleted
		
		Keywords arguments:
		item_parent -- the parent item (default=None)
		index -- the index of the item in the parent (default=None)
		"""
		
		if self.start == item_name:
			self.notify("You cannot delete the entry point of the experiment. In order to change the entry point item, please open the General Tab and select a different item.")
			return		
		for item in self.items:
			self.items[item].delete(item_name, item_parent, index)
		self.main_window.refresh()
		self.main_window.close_item_tab(item_name)				

	def unique_name(self, name):

		"""
		Return a unique name that resembles the desired name

		Arguments:
		name -- the desired name

		Returns:
		The unique name
		"""

		for item in self.items:
			if item == name:
				name = "_" + name
				return self.unique_name(name)
		return name

	def icon(self, name):

		"""
		Return a QIcon for the given name

		Arguments:
		name -- the name (e.g., "sequence")

		Returns:
		A QIcon
		"""

		return QtGui.QIcon(self.resource("%s.png" % name))

	def label_image(self, name):

		"""
		Return a QLabel with a pixmap for the given name

		Arguments:
		name -- the name (e.g., "sequence")

		Returns:
		A QLabel
		"""

		label = QtGui.QLabel()
		label.setPixmap(QtGui.QPixmap(self.resource("%s.png" % name)))

		return label

	def item_combobox(self, select=None, exclude = [], c = None):

		"""
		Returns a combobox with all the items of the experiment

		Keyword arguments:
		select -- the item to be selected initially	or None to select nothing
				  (default=None)
		exclude -- a list of items that should not be included in the list
				   (default=[])
		c -- a QComboBox that should be cleared and re-filled (default = None)

		Returns:
		A QComboBox
		"""

		if c == None:
			index = 0
			c = QtGui.QComboBox(self.ui.centralwidget)
		else:
			index = max(0, c.currentIndex())
			c.clear()

		item_dict = {}
		i = 0
		
		if select != None and select not in self.experiment.items:
			c.addItem("[Please select an item]")
			c.setCurrentIndex(0)
			c.setItemIcon(i, self.icon("down"))
			i += 1

		for item in self.experiment.items:
			if item not in exclude:
				item_type = self.experiment.items[item].item_type
				if item_type not in item_dict:
					item_dict[item_type] = []
				item_dict[item_type].append(item)

		for item_type in item_dict:
			for item in sorted(item_dict[item_type]):
				c.addItem(item)
				c.setItemIcon(i, self.icon(self.experiment.items[item].item_type))
				if self.experiment.items[item].name == select:
					index = i
				i += 1
				
		c.setCurrentIndex(index)
		return c

	def item_type_combobox(self, core_items = True, plugins = True, c = None, select = None):

		"""
		Returns a combobox with all the item types and plug-ins

		Keyword arguments:
		core_items -- a boolean indicating if core items should be included (default = True)
		plugins -- a boolean indicating if plug-ins should be inculuded (default = True)
		c -- a QComboBox that should be cleared and re-filled (default = None)
		select -- the item that should be selected initially (default = None)

		Returns:
		A QComboBox
		"""

		if c == None:
			c = QtGui.QComboBox(self.ui.centralwidget)
		else:
			c.clear()

		i = 0

		for item in ["loop", "sequence", "sketchpad", "feedback", "sampler", "synth", "keyboard_response", "mouse_response", "logger", "inline_script"]:
			c.addItem(item)
			c.setItemIcon(i, self.icon(item))
			if item == select:
				c.setCurrentIndex(i)
			i += 1

		if core_items and plugins:
			c.addItem("")
			i += 1

		for plugin in libopensesame.plugins.list_plugins():
			c.addItem(plugin)
			c.setItemIcon(i, QtGui.QIcon(libopensesame.plugins.plugin_icon_small(plugin)))
			if plugin == select:
				c.setCurrentIndex(i)
			i += 1
		return c

	def combobox_text_select(self, combobox, text):

		"""
		Find a text in a combobox and select the corresponding item

		Arguments:
		combobox -- a QComboBox
		text -- a text string to select
		"""

		combobox.setCurrentIndex(0)
		for i in range(combobox.count()):
			if str(combobox.itemText(i)) == text:
				combobox.setCurrentIndex(i)
				break

	def notify(self, message):

		"""
		Present a default notification dialog

		Arguments:
		message -- the message to be shown
		"""
		
		from libqtopensesame import notification_dialog_ui
		
		a = QtGui.QDialog(self.main_window)
		a.ui = notification_dialog_ui.Ui_Dialog()
		a.ui.setupUi(a)
		a.ui.textedit_notification.setHtml(message)
		a.adjustSize()
		a.show()
		
	def text_input(self, title, message=None, content=""):
	
		"""
		Pops up a text input dialog
		
		Arguments:
		title -- the title for the dialog
		
		Keywords arguments:
		message -- a text message (default=None)
		contents -- the initial contents (default="")
		
		Returns:
		A string of text or None if cancel was pressed
		"""
		
		from libqtopensesame import text_input_dialog_ui		
		
		a = QtGui.QDialog(self.main_window)
		a.ui = text_input_dialog_ui.Ui_Dialog()
		a.ui.setupUi(a)
		if message != None:
			a.ui.label_message.setText(message)
		a.ui.textedit_input.setText(content)
		a.ui.textedit_input.setFont(self.monospace())
		a.adjustSize()
		if a.exec_() == QtGui.QDialog.Accepted:
			return self.usanitize(a.ui.textedit_input.toPlainText())					
		return None
		
	def colorpicker(self, title="Pick a color", initial_color=None):
	
		"""
		Pops up a colorpicker dialog and returns a color in hexadecimal RGB
		notation
				
		Keywords arguments:
		title -- title of the dialog (default='Pick a color')
		initial_color -- the color to start with (default=None)
		
		Returns:
		A color string or None if the dialog was cancelled
		"""
		
		try:
			self.color_check(initial_color)
		except:
			initial_color = "white"
		color = QtGui.QColorDialog.getColor(QtGui.QColor(initial_color), \
			self.main_window, title)
		if color.isValid():
			return self.sanitize(color.name())
		return None
		
	def monospace(self):
	
		"""
		Determines the OS specific monospace font
		
		Returns:
		A QFont
		"""
		
		if os.name == "posix":
			font_family = "mono"
		else:
			font_family = "courier"
		font = QtGui.QFont(font_family)				
		font.setFixedPitch(True)
		return font

	def clear_widget(self, widget):

		"""
		Explicitly clears the layout in a widget. This is necessary
		in some weird cases.

		Arguments:
		widget -- the QWidget to be cleared
		"""

		if widget != None:
			layout = widget.layout()
			if layout != None:
				while layout.count() > 0:
					item = layout.takeAt(0)
					if not item:
						continue
					w = item.widget()
					self.clear_widget(w)
					if w:
						w.deleteLater()
						QtCore.QCoreApplication.sendPostedEvents(w, QtCore.QEvent.DeferredDelete)


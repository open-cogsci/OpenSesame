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
from libqtopensesame import notification_dialog_ui
from PyQt4 import QtCore, QtGui
import os.path

class experiment(libopensesame.experiment.experiment):

	def __init__(self, main_window, name, string = None, pool_folder = None):
	
		"""
		Initialize the experiment		
		"""
		
		self.main_window = main_window
		self.ui = self.main_window.ui
		self.unused_items = []
		self.core_items = "loop", "sequence", "sketchpad", "feedback", "sampler", "synth", "keyboard_response", "mouse_response", "logger", "inline_script"
		libopensesame.experiment.experiment.__init__(self, name, string, pool_folder)
				
	def help(self, name):
	
		"""
		Get a file from the help folder
		"""
		
		path = os.path.join("help", name)
		
		if os.path.exists(path):
			return path
		
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
			
		return ""				
		
	def module_container(self):
	
		"""
		Specifies where the experiment looks for modules
		"""
	
		return "libqtopensesame"
		
	def item_prefix(self):
	
		"""
		Specifies which class from the plugin should be loaded
		"""
		
		return "qt"		
		
	def build_item_tree(self, toplevel = None, items = []):
	
		"""
		Construct an item tree
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
		self.ui.itemtree.insertTopLevelItem(1, widget)		

		self.unused_items = []
		for i in self.items:
			if self.items[i] not in items:
				self.unused_items.append(i)
				self.items[i].build_item_tree(self.unused_widget, items)
		self.unused_widget.setExpanded(False)		
		
		return items							
		
	def rename(self, from_name, to_name):
	
		"""
		Renames an item
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
		
	def unique_name(self, name):
	
		"""
		Create a unique name resembling the
		preferred name
		"""
		
		for item in self.items:
			if item == name:
				name = "_" + name
				return self.unique_name(name)
		return name
		
	def icon(self, name):
	
		"""
		Find and return an icon belonging to
		the name
		"""
		
		return QtGui.QIcon(self.resource("%s.png" % name))
		
	def label_image(self, name):
	
		"""
		Find and return a pixmap belonging to
		the name
		"""
				
		label = QtGui.QLabel()
		label.setPixmap(QtGui.QPixmap(self.resource("%s.png" % name)))
		
		return label
		
	def item_combobox(self, select, exclude = [], c = None):
	
		"""
		Returns a combobox with all the items of the experiment
		"""
		
		if c == None:
			c = QtGui.QComboBox(self.ui.centralwidget)
		else:
			c.clear()
			
		item_dict = {}
			
		i = 0
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
					c.setCurrentIndex(i)
				i += 1
		return c
		
	def item_type_combobox(self, core_items = True, plugins = True, c = None, select = None):
	
		"""
		Returns a combobox with all plugins
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
		Select and item from the combobox based on text
		"""
		
		combobox.setCurrentIndex(0)
		for i in range(combobox.count()):
			if str(combobox.itemText(i)) == text:
				combobox.setCurrentIndex(i)
				break		
		
	def notify(self, message):
	
		"""
		Presents a notification dialog
		"""
		
		a = QtGui.QDialog(self.main_window)	
		a.ui = notification_dialog_ui.Ui_Dialog()
		a.ui.setupUi(a)	
		a.ui.textedit_notification.setHtml(message)
		a.adjustSize()
		a.show()
		
	def clear_widget(self, widget):
	
		"""
		Clears the layout in a widget
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
						


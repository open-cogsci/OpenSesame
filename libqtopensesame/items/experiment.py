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
import libopensesame.experiment
import libopensesame.plugins
from libqtopensesame.misc.qtitem_store import qtitem_store
from PyQt4 import QtCore, QtGui
import os.path

class experiment(libopensesame.experiment.experiment):

	"""Contains various GUI controls for the experiment"""

	def __init__(self, main_window, name, string=None, pool_folder=None):

		"""
		Constructor.

		Arguments:
		main_window	--	The main window object.
		name		--	The name of the experiment.

		Keyword arguments:
		string		--	A definition string for the experiment or None to
						start with an empty experiment. (default=None)
		pool_folder	--	A path to be used for the file pool or None to use a
						system-specific temporary folder. (default=None)
		"""

		self.main_window = main_window
		self.ui = self.main_window.ui
		self.unused_items = []
		self.core_items = [u"loop", u"sequence", u"sketchpad", u"feedback",
			u"sampler", u"synth", u"keyboard_response", u"mouse_response",
			u"logger", u"inline_script"]
		items = qtitem_store(self)
		libopensesame.experiment.experiment.__init__(self, name, string,
			pool_folder, items=items)

	def help(self, name):

		"""
		Returns the full path to a help file.

		Arguments:
		name	--	The name of the help file. (e.g., "sequence.html")

		Returns:
		The full path to the help file or an empty string if the help file was
		not found.
		"""

		# Check in the subfolder of the current path, which is
		# where the helpfile will be on Windows
		path = os.path.join(u'help', name)
		if os.path.exists(path):
			return path
		# Check in the shared folders
		if os.name == u'posix':
			path = u'/usr/share/opensesame/help/%s' % name
			if os.path.exists(path):
				return path
		# Fall back to the resource folder if the help
		# file is not found
		try:
			return self.resource(name)
		except:
			pass
		# Return an empty string if not found
		return u''

	def module_container(self):

		"""
		Specifies the module that is used to get items from.

		Returns:
		u'libqtopensesame.items'
		"""

		return u'libqtopensesame.items'

	def item_prefix(self):

		"""
		Specifies a prefix that should be added to classes for plugins.

		Returns:
		u'qt'
		"""

		return u'qt'

	def build_item_tree(self, toplevel=None, items=[], max_depth=-1):

		"""
		Constructs an item tree.

		Keyword arguments:
		toplevel	--	The toplevel widget. (default=None)
		items		--	A list of items that have already been added, to
						prevent recursion. (default=[])

		Returns:
		An updated list of items that have been added.
		"""

		from libqtopensesame.widgets.tree_unused_items_item import \
			tree_unused_items_item
		from libqtopensesame.widgets.tree_general_item import tree_general_item
		self.ui.itemtree.clear()
		self.treeitem_general = tree_general_item(self)
		self.treeitem_unused = tree_unused_items_item(self.main_window)
		self.ui.itemtree.insertTopLevelItem(0, self.treeitem_general)
		self.ui.itemtree.insertTopLevelItem(1, self.treeitem_unused)
		self.treeitem_general.expand()
		self.treeitem_unused.collapse()

	def rename(self, from_name, to_name):

		"""
		Renames an item.

		Arguments:
		from_name	--	The old name.
		to_name		--	The new name.
		"""

		if self.get("start") == from_name:
			self.set("start", to_name)

	def check_name(self, name):

		"""
		Checks whether a given name is valid. Reasons for not being valid
		are invalid characters or a conflict with an existing name..

		Arguments:
		name	--	The name to check.

		Returns:
		True if the name is allowed, False otherwise.
		"""

		if name.strip() == u'':
			return u'Empty names are not allowed.'
		if name.lower() in [item.lower() for item in self.items.keys()]:
			return u'An item with that name already exists.'
		if name != self.sanitize(name, strict=True, allow_vars=False):
			return u'Name contains special characters. Only alphanumeric characters and underscores are allowed.'
		return True

	def delete(self, item_name, item_parent=None, index=None):

		"""
		Deletes an item.

		Arguments:
		item_name		--	The name of the item to be deleted.

		Keywords arguments:
		item_parent		--	The parent item. (default=None)
		index			--	The index of the item in the parent sequence, if
							applicable. (default=None)
		"""

		if self.start == item_name:
			self.notify( \
				u'You cannot delete the entry point of the experiment!')
			return
		for item in self.items:
			self.items[item].delete(item_name, item_parent, index)
		self.main_window.close_item_tab(item_name)

	def icon(self, name):

		"""
		Returns a QIcon for a given name (such as an item type).

		Arguments:
		name	--	A name. (e.g., u'sequence')

		Returns:
		A QIcon.
		"""


		# TODO This hack is necessary to avoid breaking compatibility with the
		# old resources system, but plug-ins should not do this anymore!
		if (name+u'.png') in self.resources:
			return QtGui.QIcon(self.resource(name+u'.png'))
		return self.main_window.theme.qicon(name)

	def label_image(self, name):

		"""
		Returns a QLabel for a given name (such as an item type).

		Arguments:
		name	--	A name. (e.g., u'sequence')

		Returns:
		A QLabel.
		"""

		# TODO This hack is necessary to avoid breaking compatibility with the
		# old resources system, but plug-ins should not do this anymore!
		if (name+u'_large.png') in self.resources:
			l = QtGui.QLabel()
			l.setPixmap(QtGui.QPixmap(self.resource(name+u'_large.png')))
			return l
		return self.main_window.theme.qlabel(name)

	def item_combobox(self, select=None, exclude=[], c=None):

		"""
		Returns a QComboBox that contains all the items of the experiment.

		Keyword arguments:
		select	--	The item to be selected initially or None to select
					nothing. (default=None)
		exclude	--	A list of items that should not be included in the list.
					(default=[])
		c		--	A QComboBox that should be cleared and re-filled.
					(default=None)

		Returns:
		A QComboBox.
		"""

		if c == None:
			index = 0
			c = QtGui.QComboBox(self.ui.centralwidget)
		else:
			index = max(0, c.currentIndex())
			c.clear()
		i = 0
		# If we are trying to select a non-existing item, add a dummy entry to
		# the combobox
		if select != None and select not in self.experiment.items:
			c.addItem(u'')
			c.setCurrentIndex(0)
			c.setItemIcon(i, self.icon(u'go-down'))
			i += 1
		# Add all existing items (except excluded) in alphabetical order
		for item in sorted(self.experiment.items):
			if item not in exclude:
				item_type = self.experiment.items[item].item_type
				c.addItem(item)
				c.setItemIcon(i, self.icon(self.experiment.items[item].item_type))
				if self.experiment.items[item].name == select:
					index = i
				i += 1
		c.setCurrentIndex(index)
		return c

	def item_type_combobox(self, core_items=True, plugins=True, c=None, \
		select=None):

		"""
		Returns a combobox with all the item types and plug-ins.

		Keyword arguments:
		core_items	--	A boolean indicating whether core items should be
						included. (default=True)
		plugins		--	A boolean indicating whether plug-ins should be
						inculuded. (default=True)
		c			--	A QComboBox that should be cleared and re-filled.
						(default=None)
		select		--	The item type that should be selected initially.
						(default=None)

		Returns:
		A QComboBox
		"""

		if c == None:
			c = QtGui.QComboBox(self.ui.centralwidget)
		else:
			c.clear()
		i = 0
		# Add all core items in alphabetical order.
		for item in sorted(self.core_items):
			c.addItem(item)
			c.setItemIcon(i, self.icon(item))
			if item == select:
				c.setCurrentIndex(i)
			i += 1
		if core_items and plugins:
			c.addItem(u'')
			i += 1
		# Add all plug-ins in alphabetical order. We need to sort the list here
		# because `list_plugins()` sorts by priority.
		for plugin in sorted(libopensesame.plugins.list_plugins()):
			c.addItem(plugin)
			c.setItemIcon(i, QtGui.QIcon( \
				libopensesame.plugins.plugin_icon_small(plugin)))
			if plugin == select:
				c.setCurrentIndex(i)
			i += 1
		return c

	def combobox_text_select(self, combobox, text):

		"""
		Finds a text in a combobox and selects the corresponding item.

		Arguments:
		combobox	--	A QComboBox.
		text		--	A text string to select, if a match is found.
		"""

		combobox.setCurrentIndex(0)
		for i in range(combobox.count()):
			if unicode(combobox.itemText(i)) == text:
				combobox.setCurrentIndex(i)
				break

	def notify(self, msg, title=None, icon=None):

		"""
		Presents a default notification dialog.

		Arguments:
		msg		--	The message to be shown.

		Keyword arguments:
		title	--	A title message or None for default title. (default=None)
		icon	--	A custom icon or None for default icon. (default=None)
		"""

		from libqtopensesame.dialogs.notification import notification
		nd = notification(self.main_window, msg=self.unistr(msg), title=title,
			icon=icon)
		nd.show()

	def text_input(self, title, message=None, content=u''):

		"""
		Pops up a text input dialog.

		Arguments:
		title		--	The title for the dialog.

		Keywords arguments:
		message		--	A text message. (default=None)
		contents	--	The initial contents. (default=u'')

		Returns:
		A string of text or None if cancel was pressed.
		"""

		from libqtopensesame.dialogs.text_input import text_input
		tid = text_input(self.main_window, msg=message, content=content)
		return tid.get_input()

	def colorpicker(self, title=u'Pick a color', initial_color=None):

		"""
		Pops up a colorpicker dialog and returns a color in hexadecimal RGB
		notation.

		Keywords arguments:
		title			--	Title of the dialog. (default=u'Pick a color')
		initial_color	--	The color to start with. (default=None)

		Returns:
		A color string or None if the dialog was canceled.
		"""

		try:
			self.color_check(initial_color)
		except:
			initial_color = u'white'
		color = QtGui.QColorDialog.getColor(QtGui.QColor(initial_color), \
			self.main_window, title)
		if color.isValid():
			return self.sanitize(color.name())
		return None

	def monospace(self):

		"""
		Returns the system-specific default monospace font.

		Returns:
		A QFont.
		"""

		if os.name == u'posix':
			font_family = u'mono'
		else:
			font_family = u'courier'
		font = QtGui.QFont(font_family)
		font.setFixedPitch(True)
		return font

	def clear_widget(self, widget):

		"""
		Explicitly clears the layout in a widget. This is necessary in some
		weird cases.

		Arguments:
		widget	--	The QWidget to be cleared.
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

	def varref(self, val):

		"""
		desc:
			Checks whether a value contains a variable reference, for example:

				'This is [width] px'

		arguments:
			val:
				desc:	The value to check. This can be any type, but only
						str and unicode can contain variable references.

		returns:
			desc:		True if a variable reference was found, False otherwise.
			type:		bool
		"""

		if not isinstance(val, basestring):
			return False
		# TODO: Improve with regular expression
		return u'[' in val

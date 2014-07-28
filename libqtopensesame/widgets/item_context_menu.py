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

from PyQt4 import QtCore, QtGui
from libqtopensesame.misc import _

class item_context_menu(QtGui.QMenu):

	"""Provides a basic context menu for an item"""

	def __init__(self, title, treeitem, item, parent_item=None, index=None):

		"""
		Constructor

		Arguments:
		title -- menu title
		parent -- parent widget
		item -- the item to which this context menu belongs

		Keyword arguments:
		parent_item -- the parent of the item (default=None)
		index -- the index of the item in the parent item (if applicable)
				 (default=None)
		"""

		QtGui.QMenu.__init__(self, title, treeitem.treeWidget())
		self.treeitem = treeitem
		self.item = item
		self.parent_item = parent_item
		self.index = index

		# The menu text
		self.open_text = _("Open %s") % item.name
		self.edit_text = _("Edit script")
		self.rename_text = _("Rename")
		self.delete_text = _("Delete")
		self.help_text = _("%s help") % item.item_type.capitalize()

		self.addAction(item.experiment.icon(item.item_type), self.open_text)
		self.addAction(item.experiment.icon("script"), self.edit_text)
		self.addSeparator()
		self.addAction(item.experiment.icon("rename"), self.rename_text)
		if parent_item != None:
			self.addAction(item.experiment.icon("delete"), self.delete_text)
		self.addSeparator()
		self.addAction(item.experiment.icon("help"), self.help_text)

	def popup(self, pos):

		"""
		Show the menu and execute the chosen action

		Arguments:
		pos -- the position to popup
		"""

		action = self.exec_(pos)
		if action == None:
			return
		action = unicode(action.text())
		if action == self.open_text:
			self.item.open_edit_tab()
		elif action == self.edit_text:
			self.item.open_script_tab()
		elif action == self.rename_text:
			self.rename()
		elif action == self.help_text:
			self.item.open_help_tab()
		elif action == self.delete_text:
			self.item.experiment.delete(self.item.name, self.parent_item, \
				self.index)

	def rename(self):

		"""Rename an item"""

		self.treeitem.start_edit(0)

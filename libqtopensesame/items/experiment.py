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

from libopensesame.py3compat import *
import libopensesame.experiment
import libopensesame.plugins
from libqtopensesame.misc.qtitem_store import qtitem_store
from libqtopensesame.misc.qtsyntax import qtsyntax
from qtpy import QtCore, QtWidgets, QtGui
import os
from libqtopensesame.misc.translate import translation_context
_ = translation_context(u'experiment', category=u'item')

class experiment(libopensesame.experiment.experiment):

	"""Contains various GUI controls for the experiment"""

	def __init__(self, main_window, name, string=None, pool_folder=None,
		experiment_path=None, resources={}):

		"""
		desc:
			Constructor. The experiment is created automatically be OpenSesame
			and you will generally not need to create it yourself.

		arguments:
			main_window:
				desc:	The main-window object.
				type:	qtopensesame
			name:
				desc:	The name of the experiment.
				type:	[str, unicode]

		keywords:
			string:
				desc:	A string containing the experiment definition, the
						name of an OpenSesame experiment file, or `None` to
						create a blank experiment.
				type:	[str, unicode, NoneType]
			pool_folder:
				desc:	A specific folder to be used for the file pool, or
						`None` to use a new temporary folder.
				type:	[str, unicode, NoneType]
			experiment_path:
				desc:	The path of the experiment file. This will need to
						be specified even if a filename was passed using the
						`string` keyword.
				type:	[str, unicode, NoneType]
			resources:
				desc:	A dictionary with names as keys and paths as values.
						This serves as a look-up table for resources.
				type:	dict
		"""

		self.main_window = main_window
		self.ui = self.main_window.ui
		self.unused_items = []
		self.core_items = [u"loop", u"sequence", u"sketchpad", u"feedback",
			u"sampler", u"synth", u"keyboard_response", u"mouse_response",
			u"logger", u"inline_script"]
		self.items = qtitem_store(self)
		self._syntax = qtsyntax(self)
		libopensesame.experiment.experiment.__init__(self, name, string,
			pool_folder, experiment_path=experiment_path, resources=resources,
			fullscreen=None)

	@property
	def overview_area(self):
		return self.main_window.ui.itemtree

	@property
	def default_title(self):
		return _(u'New experiment')

	@property
	def default_description(self):
		return _(u'Default description')

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

	def build_item_tree(self, toplevel=None, items=[], max_depth=-1,
		select=None):

		"""
		desc:
			Builds the overview area for the full experiment.

		keywords:
			toplevel:	The toplevel widget.
			items:		A list of items that have already been added, to
						prevent recursion.
			max_depth:	The maximum depth of the tree.
			select:		The selected item.
		"""

		if self.overview_area.locked:
			return
		from libqtopensesame.widgets.tree_unused_items_item import \
			tree_unused_items_item
		from libqtopensesame.widgets.tree_general_item import tree_general_item
		self.treeitem_general = tree_general_item(self)
		self.treeitem_unused = tree_unused_items_item(self.main_window)
		fold_state = self.overview_area.get_fold_state()
		self.overview_area.clear()
		self.overview_area.insertTopLevelItem(0, self.treeitem_general)
		self.overview_area.insertTopLevelItem(1, self.treeitem_unused)
		self.overview_area.set_fold_state(fold_state)
		if select is not None:
			self.ui.itemtree.select_item(select)

	def rename(self, from_name, to_name):

		"""
		Renames an item.

		Arguments:
		from_name	--	The old name.
		to_name		--	The new name.
		"""

		if self.var.start == from_name:
			self.var.start = to_name

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
		if name != self.syntax.sanitize(name, strict=True, allow_vars=False):
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

		if self.var.start == item_name:
			self.notify( \
				u'You cannot delete the entry point of the experiment!')
			return
		for item in self.items:
			self.items[item].delete(item_name, item_parent, index)
		self.main_window.close_item_tab(item_name)

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
		nd = notification(self.main_window, msg=safe_decode(msg), title=title,
			icon=icon)
		nd.show()

	def text_input(self, title, message=None, content=u'', parent=None):

		"""
		dexc:
			Pops up a text input dialog.

		arguments:
			title:		The title for the dialog.

		keywords:
			message:	A text message.
			contents:	The initial contents.
			parent:		A parent QWidget or None to use the main window as
						parent.

		returns:
			A string of text or None if cancel was pressed.
		"""

		from libqtopensesame.dialogs.text_input import text_input
		if parent is None:
			parent = self.main_window
		tid = text_input(parent, msg=message, content=content)
		return tid.get_input()

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

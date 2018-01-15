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
from qtpy import QtWidgets
from libqtopensesame.misc.base_subcomponent import base_subcomponent
from libqtopensesame.misc.translate import translation_context
_ = translation_context(u'unused_widget', category=u'core')


class unused_items_context_menu(base_subcomponent, QtWidgets.QMenu):

	"""
	desc:
		Provides a context menu for the unused items bin.
	"""

	def __init__(self, main_window, treeitem):

		"""
		desc:
			Constructor.

		arguments:
			main_window:
				desc:	The main-window object.
				type:	qtopensesame
			treeitem:
				desc:	The tree item.
				type:	tree_item_item
		"""

		super(unused_items_context_menu, self).__init__(main_window)
		self.setup(main_window)
		a = self.addAction(
			self.theme.qicon(u'purge'),
			_(u'Permanently delete unused items'),
			self.purge_unused
		)
		a.setDisabled(not self.experiment.items.unused())

	def purge_unused(self):

		"""
		desc:
			Purges unused items.
		"""

		self.tabwidget.open_unused()
		w = self.tabwidget.get_widget(u'__unused__')
		w.purge_unused()
		w.on_activate()

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
import libopensesame.plugins
from libopensesame import debug
from libqtopensesame.misc import _
from libqtopensesame.misc.base_subcomponent import base_subcomponent
from libqtopensesame.misc.config import cfg
from libqtopensesame.widgets.toolbar_items_label import toolbar_items_label
from libqtopensesame.widgets.toolbar_items_item import toolbar_items_item

class toolbar_items(base_subcomponent, QtGui.QToolBar):

	"""
	desc:
		The item toolbar, which allows you to insert items into the experiment
		through drag and drop.
	"""

	def __init__(self, parent):

		"""
		desc:
			Constructor.

		arguments:
			parent:
				desc:	The parent.
				type:	QWidget
		"""

		super(toolbar_items, self).__init__(parent)
		self.setup(parent)
		self.orientationChanged.connect(self.build)

	def add_content(self, content):

		"""
		desc:
			Add double rows of content to the toolbar.

		arguments:
			content:
				desc:	A list of content widgets.
				type:	list
		"""

		if self.orientation() == QtCore.Qt.Horizontal:
			for c in content:
				self.addWidget(c)
		else:
			i = 0
			for c in content:
				if i % 2 == 0:
					if i > 0:
						self.addWidget(w)
					l = QtGui.QHBoxLayout()
					l.setSpacing(16)
					w = QtGui.QWidget()
					w.setLayout(l)
				c.setMargin(0)
				l.addWidget(c)
				i += 1
			if i % 2 == 1:
				l.addStretch()
			self.addWidget(w)

	def build(self):

		"""
		desc:
			Populates the toolbar with items.
		"""

		# This function is called first when no experiment has been loaded yet.
		try:
			self.experiment
		except:
			return

		# Remove old items
		self.clear()

		if self.orientation() == QtCore.Qt.Vertical:
			self.addWidget(toolbar_items_label(self, u'Commonly used'))

		# Add the core items
		content = []
		for item in self.experiment.core_items:
			w = toolbar_items_item(self, item, self.theme.qpixmap(item,
				size=cfg.toolbar_size))
			content.append(w)
		self.add_content(content)

		# Create a dictionary of plugins by category. We also maintain a list
		# to preserve the order of the categories.
		cat_list = []
		cat_dict = {}
		for plugin in libopensesame.plugins.list_plugins():
			cat = libopensesame.plugins.plugin_category(plugin)
			if cat not in cat_dict:
				cat_dict[cat] = []
				cat_list.append(cat)
			cat_dict[cat].append(plugin)

		# Add the plugins
		for cat in cat_list:
			self.addSeparator()
			if self.orientation() == QtCore.Qt.Vertical:
				self.addWidget(toolbar_items_label(self, cat))
			content = []
			for plugin in cat_dict[cat]:
				debug.msg(u"adding plugin '%s'" % plugin)
				if cfg.toolbar_size == 16:
					pixmap = QtGui.QPixmap(
						libopensesame.plugins.plugin_icon_small(plugin))
				else:
					pixmap = QtGui.QPixmap(
						libopensesame.plugins.plugin_icon_large(plugin))
				w = toolbar_items_item(self, plugin, pixmap)
				content.append(w)
			self.add_content(content)

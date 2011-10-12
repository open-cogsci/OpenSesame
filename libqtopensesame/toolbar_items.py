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

class widget_item(QtGui.QLabel):

	"""A draggable toolbar icon"""

	def __init__(self, icon, item, main_window):
	
		"""
		Constructor
		
		Arguments:
		icon -- a QIcon
		item -- the item name
		main_window -- the main window
		"""
	
		self.main_window = main_window
		self.item = item
		self.pixmap = QtGui.QPixmap(icon)

		QtGui.QLabel.__init__(self)
		self.setMargin(6)
		self.setToolTip("Drag this <b>%s</b> item into the experiment overview" % self.item)
		self.setCursor(QtGui.QCursor(QtCore.Qt.OpenHandCursor))
		self.setPixmap(self.pixmap)
		
	def mouseMoveEvent(self, e):
	
		"""
		Start a drag operation and drop it if it was accepted by item overview		
		
		Arguments:
		e -- a mouse event
		"""
	
		if e.buttons() != QtCore.Qt.LeftButton:
			return
			
		mimedata = QtCore.QMimeData()
		mimedata.setText("__osnew__ %s" % self.item)
		
		drag = QtGui.QDrag(self)
		drag.setMimeData(mimedata)
		drag.setHotSpot(e.pos() - self.rect().topLeft())
		drag.setPixmap(self.pixmap)
		
		if drag.start(QtCore.Qt.CopyAction) == QtCore.Qt.CopyAction:
			if self.item == "loop":
				self.main_window.drop_item(self.main_window.add_loop)
			elif self.item == "sequence":
				self.main_window.drop_item(self.main_window.add_sequence)				
			else:
				self.main_window.drop_item(self.item)
		else:
			if self.main_window.experiment.debug:
				print "widget_item.mouseMoveEvent(): drop cancelled"
				
class toolbar_label(QtGui.QFrame):

	"""A toolbar label"""

	def __init__(self, label):
	
		"""
		Constructor
		
		Arguments:
		label -- the text for the label
		"""
	
		QtGui.QWidget.__init__(self)
		
		l = QtGui.QLabel(label)
		l.setMaximumWidth(90)
		l.setIndent(5)
		l.setWordWrap(True)
		
		hbox = QtGui.QHBoxLayout()
		hbox.addWidget(l)
		hbox.setMargin(0)
		
		self.setLayout(hbox)

class toolbar_items(QtGui.QToolBar):

	"""This class implements the drag-and-droppable item toolbar"""

	def __init__(self, parent=None):
	
		"""
		Constructor

		Keywords arguments:
		parent -- parent widget		
		"""
	
		QtGui.QToolBar.__init__(self, parent)		
		self.main_window = None		
		self.orientationChanged.connect(self.build)
		
	def add_content(self, content):
	
		"""
		Add double rows of content to the toolbar
		
		Arguments:
		content -- a list of content widgets
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

	def build(self, dummy=None):
	
		"""
		Populate the toolbar with items (core and plugins)
		
		Keywords arguments:
		dummy -- a dummy argument
		"""
		
		# Only do something if the main_window has been attached
		if self.main_window == None:
			return
				
		# Remove old items
		self.clear()
		
		if self.orientation() == QtCore.Qt.Vertical:		
			self.addWidget(toolbar_label("<small>Commonly used</small>"))

		# Add the core items
		content = []
		for item in self.main_window.experiment.core_items:
			content.append(widget_item(self.main_window.experiment.resource("%s_large.png" % item), item, self.main_window))
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
				self.addWidget(toolbar_label("<small>%s</small>" % cat))			
			content = []
			for plugin in cat_dict[cat]:
				if self.main_window.experiment.debug:
					print "toolbar_items.build(): adding plugin '%s'" % plugin
				
				content.append(widget_item(libopensesame.plugins.plugin_icon_large(plugin), plugin, self.main_window))
			self.add_content(content)
							


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
from libqtopensesame.misc import config, _
from PyQt4 import QtGui, QtCore

class tab_widget(QtGui.QTabWidget):

	"""A custom tab widget with some extra functionality"""

	def __init__(self, parent=None):
	
		"""
		Constructor

		Keywords arguments:
		parent -- the parent QWidget
		"""	
	
		QtGui.QTabWidget.__init__(self, parent)		
		self.tabCloseRequested.connect(self.removeTab)				
		self.currentChanged.connect(self.index_changed)
		self.setSizePolicy(QtGui.QSizePolicy.MinimumExpanding, \
			QtGui.QSizePolicy.MinimumExpanding)
		
	def add(self, widget, icon, name):
	
		"""
		Open a tab and switch to it
		
		Arguments:
		widget -- a QWidget for the tab
		icon -- the name of an icon or a QIcon
		name -- a name for the tab		
		"""

		self.setCurrentIndex(self.addTab(widget, \
			self.main_window.experiment.icon(icon), _(name)))
			
	def close_all(self):
	
		"""Close all tabs"""
		
		while self.count() > 0:
			self.removeTab(0)		
			
	def close_current(self):
		
		"""Close the current tab"""
		
		self.removeTab(self.currentIndex())
			
	def close_other(self):
	
		"""Close all tabs except for the currently opened one"""
		
		while self.count() > 0 and \
			self.currentIndex() != 0:
			self.removeTab(0)
		while self.count() > 1:
			self.removeTab(1)	

	def get_index(self, tab_name):

		"""
		Return the index of a specific tab

		Arguments:
		tab_name -- the tab_name of the widget

		Returns:
		The index of the tab or None if the tab wasn't found
		"""

		for i in range(self.count()):
			w = self.widget(i)
			if (hasattr(w, "tab_name") and w.tab_name == tab_name) or \
				(hasattr(w, tab_name)):
				return i
		return None			
		
	def get_item(self, item):
	
		"""
		Return the index of a specific item tab

		Arguments:
		item -- the name of the item

		Returns:
		The index of the tab or None if the tab wasn't found
		"""
			
		for i in range(self.count()):
			w = self.widget(i)
			if (hasattr(w, "__edit_item__") and w.__edit_item__ == item):
				return i
		return None
					
		
	def get_widget(self, tab_name):
	
		"""
		Return a specific tab

		Arguments:
		tab_name -- the tab_name of the widget

		Returns:
		A QWidget or None if the tab wasn't found
		"""	
		
		i = self.get_index(tab_name)
		if i == None:
			return None
		return self.widget(i)
		
	def open_about(self):

		"""Open the about help tab"""

		self.open_help("About", "about")				
		
	def open_browser(self, url):
	
		"""
		Open a browser tab to browse local or remote HTML files
		
		Argument:
		url -- a url
		"""
	
		from libqtopensesame.widgets import webbrowser		
		browser = webbrowser.webbrowser(self.main_window)
		browser.load(url)
		self.add(browser, "web-browser", 'Help')
			
	def open_help(self, title, item):

		"""
		Open a help tab for the specified item. Looks for a file
		called [item].html in the resources folder.

		Arguments:
		title -- the tab title
		item -- the item for which help should be displayed
		"""

		self.open_browser(self.main_window.experiment.help("%s.html" % item))
		
	def open_backend_settings(self):
	
		"""Opens the backend settings"""
				
		if self.switch('__backend_settings__'):
			return
		from libqtopensesame.widgets.backend_settings import backend_settings
		self.add(backend_settings(self.main_window), 'backend', \
			'Back-end settings')	
			
	def open_forum(self):
	
		"""Open osdoc.cogsci.nl"""
	
		self.open_browser('http://forum.cogsci.nl')								
		
	def open_general(self):

		"""Opens the general tab"""

		if self.switch('__general_properties__'):
			return			
		from libqtopensesame.widgets.general_properties import general_properties
		w = general_properties(self.main_window)		
		self.add(w, 'experiment', 'General properties')

	def open_general_help(self):

		"""Open the general help tab"""

		self.open_help("Help: General", "general")
		
	def open_general_script(self):
	
		"""Opens the general script editor"""
				
		if self.switch('__general_script__'):
			return
		from libqtopensesame.widgets.general_script_editor import \
			general_script_editor
		self.add(general_script_editor(self.main_window), 'terminal', \
			'General script editor')	
			
	def open_osdoc(self):
	
		"""Open osdoc.cogsci.nl"""
	
		self.open_browser('http://osdoc.cogsci.nl')			

	def open_stdout_help(self):

		"""Open the debug window help tab"""

		self.open_help("Help: Debug window", "stdout")
		
	def open_unused(self):

		"""Opens the unused tab"""

		if self.switch('__general__'):
			return			
		from libqtopensesame.widgets.unused_widget import unused_widget
		w = unused_widget(self.main_window)		
		self.add(w, 'unused', 'Unused items')		

	def open_variables_help(self):

		"""Open the variable inspector help tab"""

		self.open_help("Help: Variable inspector", "variables")

	def open_preferences(self):

		"""Open the preferences tab"""

		from libqtopensesame.widgets import preferences_widget
		if not self.switch("__preferences__"):
			self.add(preferences_widget.preferences_widget(self.main_window), \
				"options", "Preferences")	
				
	def open_start_new(self, start=False):

		"""
		Opens the start new tab
		
		Keyword arguments:
		start -- indicates whether the widget is opened because OpenSesame has
				 started (True) or because the new button has been clicked
				 (False) (default=True)
		"""

		if start:
			if self.switch('__start_wizar__'):
				return			
		else:
			if self.switch('__new_wizard__'):
				return			 
		from libqtopensesame.widgets.start_new_widget import start_new_widget
		w = start_new_widget(self.main_window, start=start)		
		self.add(w, 'os-experiment', 'Get started')
		
	def switch(self, tab_name):
	
		"""
		Switch to a specific tab
		
		Returns:
		True if the tab exists, False otherwise
		"""
		
		i = self.get_index(tab_name)
		if i == None:
			return False
		self.setCurrentIndex(i)
		return True
		
	def toggle_onetabmode(self):

		"""Toggles onetabmode"""

		config.set_config("onetabmode", \
			self.main_window.ui.action_onetabmode.isChecked())
		if config.get_config("onetabmode"):
			self.close_other()
		self.setTabsClosable(not config.get_config("onetabmode"))
		self.main_window.ui.action_close_other_tabs.setEnabled(not \
			config.get_config("onetabmode"))
			
	def index_changed(self, index):

		"""
		Monitors tab index changes, closing other tabs if onetabmode is enabled

		Arguments:
		index -- the index of the new tab
		"""

		if config.get_config("onetabmode"):
			self.close_other()
		w = self.currentWidget()
		if hasattr(w, 'on_activate'):
			w.on_activate()
	

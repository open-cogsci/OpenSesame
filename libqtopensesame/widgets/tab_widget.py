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
		try:
			self.tabCloseRequested.connect(self.removeTab)
		except:
			# Catch what appears to be a bug in earlier versions of PyQt4.
			self.tabCloseRequested.connect(self._removeTab)
		self.currentChanged.connect(self.index_changed)
		self.setSizePolicy(QtGui.QSizePolicy.MinimumExpanding, \
			QtGui.QSizePolicy.MinimumExpanding)

	def _removeTab(self, i):

		"""
		This is simply a wrapper around QTabWidget.removeTab(). For some reason,
		connecting this function to tabCloseRequested causes an exception on
		older versions of PyQt4. This functions is a workaround.

		Arguments:
		i		--	The index of the tab to close.
		"""

		self.removeTab(i)

	def add(self, widget, icon, name):

		"""
		Open a tab and switch to it

		Arguments:
		widget -- a QWidget for the tab
		icon -- the name of an icon or a QIcon
		name -- a name for the tab
		"""


		index = self.indexOf(widget)
		if index < 0:
			index = self.addTab(widget, self.main_window.experiment.icon(icon),
			   _(name))
		self.setCurrentIndex(index)

	def remove(self, widget):

		"""
		desc:
			Removes the tab with a given widget in it.

		arguments:
			widget:
				desc:	The widget in the tab.
				type:	QWidget
		"""

		index = self.indexOf(widget)
		if index >= 0:
			self.removeTab(index)

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
			if (hasattr(w, u"tab_name") and w.tab_name == tab_name) or \
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
			if (hasattr(w, u"__edit_item__") and w.__edit_item__ == item):
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

		self.open_browser(u'http://osdoc.cogsci.nl/about/')

	def open_browser(self, url):

		"""
		Open a browser tab to browse local or remote HTML files

		Argument:
		url -- a url
		"""

		from libqtopensesame.widgets import webbrowser
		browser = webbrowser.webbrowser(self.main_window)
		browser.load(url)
		self.add(browser, u"web-browser", u'Help')

	def open_help(self, item):

		"""
		Open a help tab for the specified item. Looks for a file called
		[item].html or [item.md] in the resources folder.

		Arguments:
		item -- the item for which help should be displayed
		"""

		import os
		md_path = self.main_window.experiment.help(item + u'.md')
		html_path = self.main_window.experiment.help(item + u'.html')
		if os.path.exists(md_path):
			path = md_path
		elif os.path.exists(html_path):
			path = html_path
		else:
			path = self.main_window.experiment.help(u'missing.md')
		self.open_browser(path)

	def open_backend_settings(self):

		"""Opens the backend settings"""

		if self.switch(u'__backend_settings__'):
			return
		from libqtopensesame.widgets.backend_settings import backend_settings
		self.add(backend_settings(self.main_window), u'backend', \
			u'Back-end settings')

	def open_forum(self):

		"""Open osdoc.cogsci.nl"""

		self.open_browser(u'http://forum.cogsci.nl')

	def open_general(self):

		"""Opens the general tab"""

		if self.switch(u'__general_properties__'):
			return
		from libqtopensesame.widgets.general_properties import general_properties
		w = general_properties(self.main_window)
		self.add(w, u'experiment', u'General properties')

	def open_general_help(self):

		"""Open the general help tab"""

		self.open_help(u'general')

	def open_general_script(self):

		"""Opens the general script editor"""

		if self.switch(u'__general_script__'):
			return
		from libqtopensesame.widgets.general_script_editor import \
			general_script_editor
		self.add(general_script_editor(self.main_window), u'terminal', \
			u'General script editor')

	def open_osdoc(self):

		"""Open osdoc.cogsci.nl"""

		self.open_browser(u'http://osdoc.cogsci.nl')

	def open_stdout_help(self):

		"""Open the debug window help tab"""

		self.open_help(u'stdout')

	def open_unused(self):

		"""Opens the unused tab"""

		if self.switch(u'__unused__'):
			return
		from libqtopensesame.widgets.unused_widget import unused_widget
		w = unused_widget(self.main_window)
		self.add(w, u'unused', u'Unused items')

	def open_variables_help(self):

		"""Open the variable inspector help tab"""

		self.open_help(u'variables')

	def open_preferences(self):

		"""Open the preferences tab"""

		from libqtopensesame.widgets import preferences_widget
		if not self.switch(u"__preferences__"):
			self.add(preferences_widget.preferences_widget(self.main_window), \
				u"options", u"Preferences")

	def open_start_new(self, start=False):

		"""
		Opens the start new tab

		Keyword arguments:
		start -- indicates whether the widget is opened because OpenSesame has
				 started (True) or because the new button has been clicked
				 (False) (default=True)
		"""

		if start:
			if self.switch(u'__start_wizard__'):
				return
		else:
			if self.switch(u'__new_wizard__'):
				return
		from libqtopensesame.widgets.start_new_widget import start_new_widget
		w = start_new_widget(self.main_window, start=start)
		self.add(w, u'os-experiment', u'Get started')

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

		config.set_config(u"onetabmode", \
			self.main_window.ui.action_onetabmode.isChecked())
		if config.get_config(u"onetabmode"):
			self.close_other()
		self.setTabsClosable(not config.get_config(u"onetabmode"))
		self.main_window.ui.action_close_other_tabs.setEnabled(not \
			config.get_config(u"onetabmode"))

	def index_changed(self, index):

		"""
		Monitors tab index changes, closing other tabs if onetabmode is enabled

		Arguments:
		index -- the index of the new tab
		"""

		if config.get_config(u"onetabmode"):
			self.close_other()
		w = self.currentWidget()
		if hasattr(w, u'on_activate'):
			w.on_activate()

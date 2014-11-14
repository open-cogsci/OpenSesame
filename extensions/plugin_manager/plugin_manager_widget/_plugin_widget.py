 
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

from libopensesame import plugins
from libqtopensesame.misc.config import cfg
from libqtopensesame.widgets.base_widget import base_widget

class plugin_widget(base_widget):

	"""
	desc:
		A widget for a single plugin.
	"""

	def __init__(self, plugin, main_window):

		"""
		desc:
			Constructor.

		arguments:
			plugin:			The name of the plugin.
			main_window:	The main-window object.
		"""

		super(plugin_widget, self).__init__(main_window,
			ui=u'extensions.plugin_manager.plugin')
		self.plugin = plugin
		self.info = plugins.plugin_properties(plugin)
		self.ui.label_name.setText(plugin)
		self.ui.label_folder.setText(self.info[u'plugin_folder'])
		if u'description' in self.info:
			self.ui.label_description.setText(self.unistr(
				self.info[u'description']))
		if u'author' in self.info:
			self.ui.label_author.setText(self.unistr(self.info[u'author']))
		if u'version' in self.info:
			self.ui.label_version.setText(self.unistr(self.info[u'version']))
		if u'url' in self.info:
			self.ui.label_url.setText(self.unistr(self.info[u'url']))
		self.ui.checkbox_enable.setChecked(self.is_enabled())
		self.ui.checkbox_enable.clicked.connect(self.toggle)

	def is_enabled(self):

		"""
		returns:
			True if the plug-in is enabled, False otherwise.
		"""

		cfg_var = u'disabled_%s' % self.info[u'type']
		return self.plugin not in cfg[cfg_var]

	def toggle(self):

		"""
		desc:
			Toggles the enabled status of the plugin.
		"""

		cfg_var = u'disabled_%s' % self.info[u'type']
		disabled_plugins = cfg[cfg_var].split(u';')
		if self.ui.checkbox_enable.isChecked():
			if self.plugin in disabled_plugins:
				disabled_plugins.remove(self.plugin)
		else:
			if self.plugin not in disabled_plugins:
				disabled_plugins.append(self.plugin)
		cfg[cfg_var] = u';'.join(disabled_plugins)

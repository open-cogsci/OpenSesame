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

import os
import os.path
import imp

# Caching variables
_list = None
_folders = {}
_categories = {}
		
def plugin_folders():

	"""
	Returns a list of plugin folders
	"""
	
	l = []
	
	path = "plugins"
	if os.path.exists(path):
		l.append(path)
				
	if os.name == "posix":
	
		path = os.path.join(os.environ["HOME"], ".opensesame", "plugins")
		if os.path.exists(path):
			l.append(path)	
	
		path = "/usr/share/opensesame/plugins"
		if os.path.exists(path):
			l.append(path)
									
	elif os.name == "nt":
		path = os.path.join(os.environ["USERPROFILE"], ".opensesame", "plugins")
		if os.path.exists(path):
			l.append(path)		
			
	return l

def is_plugin(item_type):

	"""
	Checks if a given item type corresponds to a plugin
	"""

	return plugin_folder(item_type) != None
	
def plugin_category(plugin):

	"""
	Returns the category of a plugin
	"""
	
	global _categories
	
	if plugin in _categories:
		return _categories[plugin]
	
	for l in open(os.path.join(plugin_folder(plugin), "info.txt"), "r"):
		a = l.split(":")
		if len(a) == 2 and a[0] == "category":
			cat = a[1].strip()
			_categories[plugin] = cat
			return cat

	cat = "Uncategorized"	
	_categories[plugin] = cat			
	return cat
	
def list_plugins():

	"""
	Returns a list of plugins
	"""
	
	global _list
	
	if _list != None:
		return _list
	
	plugins = []
	for folder in plugin_folders():
		for plugin in os.listdir(folder):
			if is_plugin(plugin) and plugin not in plugins:
				plugins.append(plugin)
	_list = plugins				
	return plugins
	
def plugin_folder(plugin):
	
	"""
	Return the folder of a plugin
	"""
	
	global _folders
	
	if plugin in _folders:
		return _folders[plugin]	
	
	for folder in plugin_folders():
		if os.path.exists(os.path.join(folder, plugin, "%s.py" % plugin)):
			f = os.path.join(folder, plugin)
			_folders[plugin] = f
			return f
			
	return None
	
def plugin_icon_large(plugin):

	"""
	Return the large icon for a plugin
	"""
	
	return os.path.join(plugin_folder(plugin), "%s_large.png" % plugin)
	
def plugin_icon_small(plugin):

	"""
	Return the large icon for a plugin
	"""
	
	return os.path.join(plugin_folder(plugin), "%s.png" % plugin)	
	
def import_plugin(plugin):

	"""
	Import plugin module
	"""
	
	path = os.path.join(plugin_folder(plugin), "%s.py" % plugin)
	return imp.load_source(plugin, path)
	
def load_plugin(plugin, item_name, experiment, string, prefix = ""):

	"""
	Returns an instance of the plugin
	"""

	mod = import_plugin(plugin)
	cmd = "mod.%(prefix)s%(plugin)s(item_name, experiment, string)" % {"plugin" : plugin, "prefix" : prefix}
	item = eval(cmd)
	return item
	

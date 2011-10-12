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

# Caching variables
_list = None
_folders = {}
_properties = {}
	
def plugin_folders(only_existing=True):

	"""
	Returns a list of plugin folders
	
	Keywords arguments:
	only_existing -- specifies if only existing folders should be returned
					 (default=True)
	
	Returns:
	A list of folders
	"""
	
	l = []
	
	path = os.path.join(os.getcwd(), "plugins")
	if not only_existing or os.path.exists(path):
		l.append(path)
				
	if os.name == "posix":
	
		path = os.path.join(os.environ["HOME"], ".opensesame", "plugins")
		if not only_existing or os.path.exists(path):
			l.append(path)	
	
		path = "/usr/share/opensesame/plugins"
		if not only_existing or os.path.exists(path):
			l.append(path)
									
	elif os.name == "nt":
		path = os.path.join(os.environ["USERPROFILE"], ".opensesame", "plugins")
		if not only_existing or os.path.exists(path):
			l.append(path)		
			
	return l

def is_plugin(item_type):

	"""
	Checks if a given item type corresponds to a plugin
	
	Returns:
	True if the item_type is a plugin, False otherwise
	"""

	return plugin_folder(item_type) != None
	
def plugin_disabled(plugin):
	
	"""
	Checks if a plugin has been disabled. If the config module cannot be loaded
	the return value is False.
	
	Arguments:
	plugin -- the plugin to check
	
	Returns:
	True if the plugin has been disabled, False otherwise
	"""

	try:
		from libqtopensesame import config
		return plugin in config.get_config("disabled_plugins").split(";")
	except:
		return False
	
def plugin_property(plugin, _property, default=0):

	"""
	Returns the property of a plug-in
	
	Arguments:
	plugin -- name of the plugin
	_property -- name of the property
	
	Keywords arguments:
	default -- a default property value (default=0)
	
	Returns:
	The property value
	"""
	
	global _properties	
	if plugin in _properties and _property in _properties[plugin]:
		return _properties[plugin][_property]
	if plugin not in _properties:
		_properties[plugin] = {}	
	for l in open(os.path.join(plugin_folder(plugin), "info.txt"), "r"):
		a = l.split(":")
		if len(a) == 2 and a[0] == _property:
			val = a[1].strip()			
			try:
				val = int(val)
			finally:
				_properties[plugin][_property] = val
				return val
	_properties[plugin][_property] = default				
	return default
	
def plugin_category(plugin):

	"""
	Returns the category of a plugin
	
	Returns:
	A category
	"""
	
	return plugin_property(plugin, "category", default="Miscellaneous")
	
def list_plugins(filter_disabled=True):

	"""
	Returns a list of plugins
	
	Returns:
	A list of plugins (item_types)
	"""
	
	global _list	
	if _list != None:
		return [plugin for plugin in _list if not (filter_disabled and plugin_disabled(plugin))]
	
	plugins = []
	for folder in plugin_folders():
		for plugin in os.listdir(folder):			
			if is_plugin(plugin):
				_plugin = plugin, plugin_property(plugin, "priority")			
				if _plugin not in plugins:
					plugins.append(_plugin)
				
	# Sort (inversely) by priority
	plugins.sort(key=lambda p: -p[1])
	_list = [plugin[0] for plugin in plugins]
	return [plugin for plugin in _list if not (filter_disabled and plugin_disabled(plugin))]
	
def plugin_folder(plugin):
	
	"""
	Returns the folder of a plugin
	
	Arguments:
	plugin -- the name of the plugin
	
	Returns:
	The folder of the plugin
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
	
	Arguments:
	plugin -- the name of the plugin	
	
	Returns:
	The full path to an icon
	"""
	
	return os.path.join(plugin_folder(plugin), "%s_large.png" % plugin)
	
def plugin_icon_small(plugin):

	"""
	Return the small icon for a plugin
	
	Arguments:
	plugin -- the name of the plugin
		
	Returns:
	The full path to an icon	
	"""
	
	return os.path.join(plugin_folder(plugin), "%s.png" % plugin)	
	
def import_plugin(plugin):

	"""
	Imports plugin module
	
	Arguments:
	plugin -- the name of the plugin
	"""
	
	import imp
	path = os.path.join(plugin_folder(plugin), "%s.py" % plugin)
	return imp.load_source(plugin, path)
	
def load_plugin(plugin, item_name, experiment, string, prefix = ""):

	"""
	Returns an instance of the plugin
	
	Arguments:
	plugin -- the name of the plugin
	item_name -- the name of the item (plugin instance)
	experiment -- the experiment
	string -- a definitions tring
	
	Keywords arguments:
	prefix -- a class prefix to allow switching between [plugin] and qt[plugin]
	
	Returns:
	An item (plugin instance)
	"""

	mod = import_plugin(plugin)
	cmd = "mod.%(prefix)s%(plugin)s(item_name, experiment, string)" % {"plugin" : plugin, "prefix" : prefix}
	item = eval(cmd)
	return item
	

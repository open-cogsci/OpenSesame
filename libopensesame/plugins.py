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

import os
import os.path
import json
from libopensesame import debug

# Caching variables
_list = None
_folders = {}
_properties = {}

# The plug-ins can be either source or bytecode. Usually they will be source,
# but some distributions (notably the runtime for Android) will automatically
# compile everything to bytecode.
src_templates = [u'%s.py']
bytecode_templates = [u'%s.pyo', u'%s.pyc']
	
def plugin_folders(only_existing=True):

	"""
	Returns a list of plugin folders.
	
	Keywords arguments:
	only_existing	--	Specifies if only existing folders should be returned.
						(default=True)
	
	Returns:
	A list of folders.
	"""
	
	l = []
	
	# For all platforms, the plugins folder relative to the working directory
	# should be searched
	path = os.path.join(os.getcwdu(), u'plugins')
	if not only_existing or os.path.exists(path):
		l.append(path)				
		
	if os.name == u'posix' and u'HOME' in os.environ:
		# Regular Linux distributions. TODO: How well does this apply to Mac OS?
		path = os.path.join(os.environ[u'HOME'], u'.opensesame', u'plugins')
		if not only_existing or os.path.exists(path):
			l.append(path)		
		path = u'/usr/share/opensesame/plugins'
		if not only_existing or os.path.exists(path):
			l.append(path)			
			
	elif os.name == u'posix' and u'HOME' not in os.environ:
		# Android can be recognized by the fact that the HOME variable is not
		# available. We can simply use the relative path `plugins`, which will
		# (always?) point to `/data/data/nl.cogsci.nl/opensesame/files/plugins`
		path = u'plugins'
		if not only_existing or os.path.exists(path):
			l.append(path)
		
	elif os.name == u'nt':
		# Windows
		path = os.path.join(os.environ[u'APPDATA'], u'.opensesame', u'plugins')
		if not only_existing or os.path.exists(path):
			l.append(path)		
			
	return l

def is_plugin(item_type):

	"""
	Checks if a given item type corresponds to a plugin.
	
	Returns:
	True if the item_type is a plugin, False otherwise.
	"""

	return plugin_folder(item_type) != None
	
def plugin_disabled(plugin):
	
	"""
	Checks if a plugin has been disabled. If the config module cannot be loaded
	the return value is False.
	
	Arguments:
	plugin	--	The plugin to check.
	
	Returns:
	True if the plugin has been disabled, False otherwise.
	"""

	from libqtopensesame.misc import config
	return plugin in config.get_config(u'disabled_plugins').split(u';')
	
def plugin_property(plugin, _property, default=0):

	"""
	Returns a property of a plug-in.
	
	Arguments:
	plugin		--	The name of the plugin.
	_property	--	The name of the property.
	
	Keywords arguments:
	default		--	A default property value. (default=0)
	
	Returns:
	The property value.
	"""
	
	global _properties	
	if plugin in _properties and _property in _properties[plugin]:
		return _properties[plugin][_property]
	if plugin not in _properties:
		_properties[plugin] = {}		
	info_txt = os.path.join(plugin_folder(plugin), u'info.txt')
	info_json = os.path.join(plugin_folder(plugin), u'info.json')	
	# New-style plug-ins, using info.json
	if os.path.exists(info_json):
		try:
			_json = json.load(open(info_json))
		except:
			debug.msg(u'Failed to parse %s' % info_json)
			_json = {}
		if _property in _json:
			return _json[_property]
	# Old-style plug-ins, using info.txt
	else:
		for l in open(info_txt, u'r'):
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
	Returns the category of a plugin.
	
	Returns:
	A category.
	"""
	
	return plugin_property(plugin, u'category', default=u'Miscellaneous')
	
def list_plugins(filter_disabled=True):

	"""
	Returns a list of plugins.
	
	Returns:
	A list of plugins (item_types).
	"""
	
	global _list	
	if _list != None:
		return [plugin for plugin in _list if not (filter_disabled and \
			plugin_disabled(plugin))]
	
	plugins = []
	for folder in plugin_folders():
		for plugin in os.listdir(folder):			
			if is_plugin(plugin):
				_plugin = plugin, plugin_property(plugin, u'priority')
				if _plugin not in plugins:
					plugins.append(_plugin)
				
	# Sort (inversely) by priority
	plugins.sort(key=lambda p: -p[1])
	_list = [plugin[0] for plugin in plugins]
	return [plugin for plugin in _list if not (filter_disabled and \
		plugin_disabled(plugin))]
	
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
		plugin = str(plugin)
		for tmpl in src_templates + bytecode_templates:		
			if os.path.exists(os.path.join(folder, plugin, tmpl % plugin)):
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
	
	return os.path.join(plugin_folder(plugin), u'%s_large.png' % plugin)
	
def plugin_icon_small(plugin):

	"""
	Return the small icon for a plugin
	
	Arguments:
	plugin -- the name of the plugin
		
	Returns:
	The full path to an icon	
	"""
	
	return os.path.join(plugin_folder(plugin), u'%s.png' % plugin)
	
def import_plugin(plugin):

	"""
	Imports plugin module
	
	Arguments:
	plugin -- the name of the plugin
	"""
	
	import imp
	plugin = str(plugin)
	for tmpl in src_templates:
		if os.path.exists(os.path.join(plugin_folder(plugin), tmpl % plugin)):
			path = os.path.join(plugin_folder(plugin), tmpl % plugin).encode( \
				u'utf-8')
			return imp.load_source(plugin, path)
	for tmpl in bytecode_templates:
		if os.path.exists(os.path.join(plugin_folder(plugin), tmpl % plugin)):
			path = os.path.join(plugin_folder(plugin), tmpl % plugin).encode( \
				u'utf-8')
			return imp.load_compiled(plugin, path)
	
def load_plugin(plugin, item_name, experiment, string, prefix=u''):

	"""
	Returns an instance of the plugin.
	
	Arguments:
	plugin		--	The name of the plugin.
	item_name	--	Yhe name of the item (plugin instance).
	experiment	--	The experiment object.
	string		--	A definition string.
	
	Keywords arguments:
	prefix		--	A class prefix to allow switching between [plugin] and
					qt[plugin]. (default=u'')
	
	Returns:
	An item (plugin instance).
	"""

	item_module = import_plugin(plugin)
	item_class = getattr(item_module, prefix+plugin)
	item = item_class(item_name, experiment, string)
	return item
	

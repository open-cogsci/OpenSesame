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

# About

This module is used to maintain configuration settings. When this module is
first loaded, a single instance of the `config` class is instantiated, whicn is
subsequently used for all configuration getting and setting (i.e. a singleton
design pattern).

	from libqtopensesame.misc.config import cfg
	cfg.my_setting = 'my_value' # set
	print(cfg.my_setting) # get
"""

from libopensesame.py3compat import *
from libopensesame.exceptions import osexception
from qtpy import QtCore
import libopensesame.misc
from libopensesame.oslogging import oslogger
import platform
import sys


DEFAULT_CONFIG = {
	u"cfg_ver" : 0,
	u"_initial_window_geometry" : QtCore.QByteArray(),
	u"_initial_window_state" : QtCore.QByteArray(),
	u"auto_update_check" : True,
	u"auto_response" : False,
	u"default_logfile_folder" : libopensesame.misc.home_folder(),
	u"default_pool_folder" : libopensesame.misc.home_folder(),
	u"disabled_plugins" : "",
	u"disabled_extensions" : "",
	u"file_dialog_path" : "",
	u"file_pool_size_warning" : 104857600,
	u"loop_wizard" : None,
	u"onetabmode" : False,
	u"quick_run_logfile": u"quickrun.csv",
	u"recent_files" : u"",
	u"reset_console_on_experiment_start" : True,
	u"shortcut_itemtree" : u"Ctrl+1",
	u"shortcut_tabwidget" : u"Ctrl+2",
	u"shortcut_stdout" : u"Ctrl+3",
	u"shortcut_pool" : u"Ctrl+4",
	u"shortcut_copy_clipboard_unlinked" : u"Ctrl+C",
	u"shortcut_copy_clipboard_linked" : u"Ctrl+Shift+C",
	u"shortcut_paste_clipboard" : u"Ctrl+V",
	u"shortcut_delete" : u"Del",
	u"shortcut_permanently_delete" : u"Shift+Del",
	u"shortcut_context_menu" : u"+",
	u"shortcut_rename" : u"F2",
	u"shortcut_edit_runif" : u"F3",
	u"style" : u"",
	u"theme" : u"default",
	u"toolbar_size" : 32,
	u"toolbar_text" : False,
	u"runner" : u"multiprocess",
	u"opensesamerun_exec" : u"",
	u"start_drag_delay" : 300,
	u"pos" : QtCore.QPoint(200, 200),
	u"size" : QtCore.QSize(1000, 600),
	u"url_website" : u"http://www.cogsci.nl/opensesame",
	u"url_facebook" : u"http://www.facebook.com/cognitivescience",
	u"url_twitter" : u"http://www.twitter.com/cogscinl",
	u'sketchpad_placeholder_color' : u'#00FF00',
	u'sketchpad_grid_color' : u'#00FF00',
	u'sketchpad_grid_thickness_thin' : 2,
	u'sketchpad_grid_thickness_thick' : 4,
	u'sketchpad_grid_opacity' : 32,
	u'sketchpad_preview_color' : u'#00FF00',
	u'sketchpad_preview_penwidth' : 2,
	u'mode': u'default',
	u'locale' : u'',
	}
DEFAULT_CONFIG_LINUX = {
	u"theme" : u"gnome"
	}
DEFAULT_CONFIG_MAC = {}
DEFAULT_CONFIG_WINDOWS = {}


class config(object):

	def __init__(self):

		"""
		desc:
			Constructor.
		"""

		self.reset()

	def __str__(self):

		return self.__unicode__() if py3 else safe_encode(self.__unicode__())

	def __unicode__(self):

		s = u''
		for key, val in self.config.items():
			if not isinstance(val, basestring) and not isinstance(val, int) \
				and not isinstance(val, float):
				val = type(val)
			s += u'%s: %s\n' % (key, val)
		return s

	def __getattr__(self, setting):

		"""
		desc:
			A getter for settings, to allow for easy access

		arguments:
			setting:	The setting to get
		"""

		if setting not in self.config:
			raise osexception(u'The setting "%s" does not exist' \
				% setting)
		return self.config[setting]

	def __setattr__(self, setting, value):

		"""
		desc:
			A setter for settings, to allow for easy access

		argumentsL
			setting: 	The setting to set
			value:		The value to set
		"""

		if setting not in self.config:
			raise osexception(u'The setting "%s" does not exist' \
				% setting)
		self.config[setting] = value
		self.config[u'cfg_ver'] += 1

	def __setitem__(self, setting, value):

		"""
		desc:
			Emulate dict API.
		"""

		self.__setattr__(setting, value)

	def __getitem__(self, setting):

		"""
		desc:
			Emulate dict API.
		"""

		return self.__getattr__(setting)

	def __contains__(self, setting):

		"""
		returns:
			True if setting exists, False otherwise.
		"""

		return setting in self.config

	def register(self, setting, default):

		"""
		desc:
			Registers a new setting, if it doesn't already exist.

		arguments:
			setting:	The setting name.
			default:	A default value, which is used if the setting doesn't
						already exist.
		"""

		qsettings = QtCore.QSettings(u"cogscinl", self.mode)
		qsettings.beginGroup(u"MainWindow")
		if '--start-clean' in sys.argv:
			self.config[setting] = default
		elif setting not in self.config:
			value = qsettings.value(setting, default)
			value = self.type_qvariant(value, default)
			self.config[setting] = value
		qsettings.endGroup()

	def parse_cmdline_args(self, args):

		"""
		desc:
			Apply settings that were specified on the command line. The expected
			format is as follows: [name]=[val];[name]=[val];...

		arguments:
			args:	The string of command line arguments
		"""

		if args is None:
			return
		for arg in args.split(u";"):
			a = arg.split(u"=")
			if len(a) == 2:
				# Automagically determine the data type
				if a[1] == u"True":
					val = True
				elif a[1] == u"False":
					val = False
				else:
					try:
						val = int(a[1])
					except:
						try:
							val = float(a[1])
						except:
							val = a[1]
				# Apply the argument
				try:
					self.__setattr__(a[0], val)
					oslogger.debug(u"%s = %s" % (a[0], val))
				except:
					oslogger.error(u"Failed to parse argument: %s" % arg)

	def type_qvariant(self, value, default):

		"""
		desc:
			Typecasts a value to a normal type that matches the type of a
			default value. This is necessary, because under some combinations
			of Python 2/3 and PyQt 4/5 settings are returned as QVariant
			objects, whereas on other combinations the type casting occurs
			automatically.

		arguments:
			value:		A value.
			default:	A default value.

		returns:
			A value.
		"""

		if hasattr(QtCore, u'QPyNullVariant') and \
				isinstance(value, QtCore.QPyNullVariant):
			return default
		if isinstance(default, bool):
			if isinstance(value, basestring):
				return value == u'true'
			try:
				return bool(value)
			except:
				oslogger.error('Failed to convert %s' % value)
				return default
		if isinstance(default, int):
			try:
				return int(value)
			except:
				oslogger.error('Failed to convert %s' % value)
				return default
		if isinstance(default, float):
			try:
				return float(value)
			except:
				oslogger.error('Failed to convert %s' % value)
				return default
		return value

	def restore(self, mode):

		"""
		desc:
			Restore settings from a QSettings.
		"""

		self.mode = mode
		qsettings = QtCore.QSettings(u"cogscinl", mode)
		qsettings.beginGroup(u'MainWindow')
		for setting, default in self.config.items():
			try:
				value = qsettings.value(setting, default)
			except TypeError:
				continue
			value = self.type_qvariant(value, default)
			self.config[setting] = value
		qsettings.endGroup()

	def save(self):

		"""
		desc:
			Save settings to a QSettings.
		"""

		qsettings = QtCore.QSettings(u"cogscinl", self.mode)
		qsettings.beginGroup(u'MainWindow')
		for setting, value in self.config.items():
			if setting != u"cfg_ver":
				qsettings.setValue(setting, value)
		qsettings.endGroup()

	def clear(self):

		"""
		desc:
			Clears all settings.
		"""

		qsettings = QtCore.QSettings(u"cogscinl", self.mode)
		qsettings.beginGroup(u'MainWindow')
		qsettings.clear()
		qsettings.endGroup()

	def version(self):

		"""
		desc:
			Gets the current version of the config.

		Returns:
			The config version.
		"""

		return self.cfg_ver

	def reset(self):

		"""
		desc:
			Resets the configution back to default.
		"""

		object.__setattr__(self, u'config', {})
		self.config.update(DEFAULT_CONFIG)
		if platform.system() == u"Windows":
			self.config.update(DEFAULT_CONFIG_WINDOWS)
		elif platform.system() == u"Darwin":
			self.config.update(DEFAULT_CONFIG_MAC)
		elif platform.system() == u"Linux":
			self.config.update(DEFAULT_CONFIG_LINUX)

	def nuke(self):

		"""
		desc:
			Clears the config.
		"""

		self.reset()
		self.clear()
		self.save()


# Create a singleton config instance
cfg = config()

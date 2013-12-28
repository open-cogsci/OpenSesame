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

<DOC>
This module is used to maintain configuration settings. There is a old and a new
style API. The new one is obviously preferred for new code. When this module is
first loaded, a single instance of the `config` class is instantiated, whicn is
subsequently used for all configuration getting and setting (i.e. a singleton
design pattern).

Old style:

	from libqtopensesame.misc import config
	config.set_config('my_setting', 'my_value')
	print config.get_config('my_setting')

New style:

	from libqtopensesame.misc.config import cfg
	cfg.my_setting = 'my_value' # set
	print cfg.my_setting # get
</DOC>
"""

from libopensesame.exceptions import osexception
from PyQt4 import QtCore
import libopensesame.misc
from libopensesame import debug
import platform
import sip
if sip.getapi(u'QString') == 2:
	QtCore.QStringList = list

class config(object):

	config = {
		u"cfg_ver" : 0,
		u"_initial_window_geometry" : QtCore.QByteArray(),
		u"_initial_window_state" : QtCore.QByteArray(),
		u"auto_update_check" : True,
		u"auto_response" : False,
		u"autosave_interval" : 10 * 60 * 1000,
		u"autosave_max_age" : 7,
		u"default_logfile_folder" : libopensesame.misc.home_folder(),
		u"default_pool_folder" : libopensesame.misc.home_folder(),
		u"disabled_plugins" : "",
		u"file_dialog_path" : "",
		u"immediate_rename" : False,
		u"locale" : u"default",
		u"loop_wizard" : QtCore.QStringList(),
		u"onetabmode" : False,
		u"qProgEditCommentShortcut" : u'Ctrl+M',
		u"qProgEditUncommentShortcut" : u'Ctrl+Shift+M',
		u'qProgEditFontFamily' : u'Monospace',
		u'qProgEditFontSize' : 10,
		u'qProgEditLineNumbers' : True,
		u'qProgEditHighlightCurrentLine' : False,
		u'qProgEditHighlightMatchingBrackets' : True,
		u'qProgEditWordWrapMarker' : 80,
		u'qProgEditWordWrap' : True,
		u'qProgEditTabWidth' : 4,
		u'qProgEditAutoIndent' : True,
		u'qProgEditShowEol' : False,
		u'qProgEditShowWhitespace' : False,
		u'qProgEditShowIndent' : False,
		u'qProgEditShowFolding' : True,
		u'qProgEditAutoComplete' : True,
		u'qProgEditColorScheme' : u'Default',
		u'qProgEditValidate' : True,
		u"quick_run_logfile": u"quickrun.csv",
		u"recent_files" : u"",
		u"shortcut_itemtree" : u"Ctrl+1",
		u"shortcut_tabwidget" : u"Ctrl+2",
		u"shortcut_stdout" : u"Ctrl+3",
		u"shortcut_pool" : u"Ctrl+4",
		u"shortcut_variables" : u"Ctrl+5",
		u"style" : u"",
		u"theme" : u"default",
		u"toolbar_size" : 32,
		u"toolbar_text" : False,
		u"runner" : u"inprocess",
		u"opensesamerun_exec" : u"",
		u"pos" : QtCore.QPoint(200, 200),
		u"size" : QtCore.QSize(1000, 600),
		u"url_website" : u"http://www.cogsci.nl/opensesame",
		u"url_facebook" : u"http://www.facebook.com/cognitivescience",
		u"url_twitter" : u"http://www.twitter.com/cogscinl",
		u"version_check_url" : \
			u"http://files.cogsci.nl/software/opensesame/MOST_RECENT_VERSION.TXT"
		}

	# OS specific override settings
	config_linux = {
		u"theme" : u"gnome"
		}
	config_mac = {}
	config_windows = {
		u'qProgEditFontFamily' : u'Courier New'
		}

	def __init__(self):

		"""Constructor"""

		# Determine the sip api that is used, because this depends on whether
		# or not IPython is loaded
		object.__setattr__(self, u'api', sip.getapi(u'QString'))
		if self.api not in (1,2):
			raise Exception(u'config: unknown api %s' % self.api)

		# Apply OS specific override settings
		if platform.system() == u"Windows":
			for key, value in self.config_windows.iteritems():
				self.config[key] = value
		elif platform.system() == u"Darwin":
			for key, value in self.config_mac.iteritems():
				self.config[key] = value
		elif platform.system() == u"Linux":
			for key, value in self.config_linux.iteritems():
				self.config[key] = value

	def __getattr__(self, setting):

		"""
		A getter for settings, to allow for easy access

		Argument:
		setting -- the setting to get
		"""

		if setting not in self.config:
			raise osexception(u'The setting "%s" does not exist' \
				% setting)
		return self.config[setting]

	def __setattr__(self, setting, value):

		"""
		A setter for settings, to allow for easy access

		Argument:
		setting -- the setting to set
		value -- the value to set
		"""
		if setting not in self.config:
			raise osexception(u'The setting "%s" does not exist' \
				% setting)
		self.config[setting] = value
		self.config[u'cfg_ver'] += 1

	def parse_cmdline_args(self, args):

		"""
		Apply settings that were specified on the command line. The expected
		format is as follows: [name]=[val];[name]=[val];...

		Arguments:
		args -- the string of command line arguments
		"""

		if args == None:
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
					debug.msg(u"%s = %s" % (a[0], val))
				except:
					debug.msg(u"Failed to parse argument: %s" % arg)

	def restore(self, qsettings):

		"""
		Restore settings from a QSettings

		Arguments:
		qsettings -- a QSettings instance
		"""

		for setting, default in self.config.items():
			value = qsettings.value(setting, default)

			# The older (default) api requires an explicit type conversion
			if self.api == 1:
				if type(default) == bool:
					value = value.toBool()
				elif type(default) == str:
					try:
						value = unicode(value.toString())
					except:
						value = default
				elif type(default) == int:
					value = value.toInt()[0]
				elif type(default) == QtCore.QPoint:
					value = value.toPoint()
				elif type(default) == QtCore.QSize:
					value = value.toSize()
				elif type(default) == QtCore.QByteArray:
					value = value.toByteArray()
				elif type(default) == QtCore.QString:
					value = value.toString()
				elif type(default) == QtCore.QStringList:
					value = value.toStringList()
				elif type(default) == unicode:
					value = unicode(value.toString())

			# The newer api returns some things as strings, so we still have to
			# do some type conversion
			else:
				if type(default) == bool:
					if value == u'false':
						value = False
					else:
						value = True
				elif type(default) == int:
					value = int(value)

			self.__setattr__(setting, value)

	def save(self, qsettings):

		"""
		Save settings to a QSettings

		Arguments:
		qsettings -- a QSettings instance
		"""

		for setting, value in self.config.items():
			if setting != u"cfg_ver":
				qsettings.setValue(setting, value)
				
	def version(self):
		
		"""
		Gets the current version of the config.
		
		Returns:
		The config version.
		"""

		return self.cfg_ver

# Old style API. See explanation above
def get_config(setting):
	return cfg.__getattr__(setting)

def set_config(setting, value):
	cfg.__setattr__(setting, value)

def restore_config(settings):
	cfg.restore(settings)

def save_config(settings):
	cfg.save(settings)

def parse_cmdline_args(args):
	cfg.parse_cmdline_args(args)

# Create a singleton config instance
global cfg
cfg = config()

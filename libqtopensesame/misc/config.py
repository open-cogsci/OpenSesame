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

USAGE
=====
This module is used to maintain configuration settings. There is a old and a new
style API. The new one is obviously preferred for new code.

OLD STYLE
=========
>>> from libqtopensesame.misc import config 
>>> config.set_config('my_setting', 'my_value')
>>> print config.get_config('my_setting')

NEW STYLE
=========
>>> from libqtopensesame.misc.config import cfg
>>> cfg.my_setting = 'my_value' # set
>>> print cfg.my_setting # get
"""

from PyQt4 import QtCore
import libopensesame.misc
from libopensesame import debug, exceptions
import platform
import sip
if sip.getapi('QString') == 2:
	QtCore.QStringList = list

class config(object):

	config = {
		"cfg_ver" : 0,
		"_initial_window_geometry" : QtCore.QByteArray(),
		"_initial_window_state" : QtCore.QByteArray(),
		"auto_update_check" : True,
		"auto_response" : False,
		"autosave_interval" : 10 * 60 * 1000,
		"autosave_max_age" : 7,
		"default_logfile_folder" : libopensesame.misc.home_folder(),
		"default_pool_folder" : libopensesame.misc.home_folder(),
		"disabled_plugins" : "",
		"file_dialog_path" : "",
		"immediate_rename" : False,
		"locale" : "default",
		"loop_wizard" : QtCore.QStringList(),
		"onetabmode" : False,
		"quick_run_logfile": u"quickrun.csv",
		"recent_files" : "",
		"scintilla_line_numbers" : True,
		"scintilla_right_margin" : False,
		"scintilla_eol_visible" : False,
		"scintilla_whitespace_visible" : False,
		"scintilla_indentation_guides" : True,
		"scintilla_auto_indent" : True,
		"scintilla_folding" : True,
		"scintilla_brace_match" : True,
		"scintilla_syntax_highlighting" : True,
		"scintilla_custom_font" : False,
		"scintilla_font_family" : "courier",
		"scintilla_font_size" : 10,
		"shortcut_itemtree" : "Ctrl+1",
		"shortcut_tabwidget" : "Ctrl+2",
		"shortcut_stdout" : "Ctrl+3",
		"shortcut_pool" : "Ctrl+4",
		"shortcut_variables" : "Ctrl+5",
		"style" : "",
		"theme" : "default",
		"toolbar_size" : 32,
		"toolbar_text" : False,
		"opensesamerun" : False,
		"opensesamerun_exec" : "",
		"pos" : QtCore.QPoint(200, 200),
		"size" : QtCore.QSize(1000, 600),
		"url_website" : "http://www.cogsci.nl/opensesame",
		"url_facebook" : "http://www.facebook.com/cognitivescience",
		"url_twitter" : "http://www.twitter.com/cogscinl",
		"version_check_url" : \
			"http://files.cogsci.nl/software/opensesame/MOST_RECENT_VERSION.TXT"
		}
		
	# OS specific override settings
	config_linux = {
		"theme" : "gnome"
		}		
	config_mac = {}
	config_windows = {}
		
	def __init__(self):
		
		"""Constructor"""
		
		# Determine the sip api that is used, because this depends on whether
		# or not IPython is loaded
		object.__setattr__(self, 'api', sip.getapi('QString'))
		if self.api not in (1,2):
			raise Exception('config: unknown api %s' % self.api)	
		
		# Apply OS specific override settings
		if platform.system() == "Windows":
			for key, value in self.config_windows.iteritems():
				self.config[key] = value
		elif platform.system() == "Darwin":
			for key, value in self.config_mac.iteritems():
				self.config[key] = value
		elif platform.system() == "Linux":			
			for key, value in self.config_linux.iteritems():
				self.config[key] = value
		
	def __getattr__(self, setting):
		
		"""
		A getter for settings, to allow for easy access
		
		Argument:
		setting -- the setting to get
		"""
		
		if setting not in self.config:
			raise exceptions.runtime_error('The setting "%s" does not exist' \
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
			raise exceptions.runtime_error('The setting "%s" does not exist' \
				% setting)		
		self.config[setting] = value
		self.config['cfg_ver'] += 1
		
	def parse_cmdline_args(self, args):

		"""
		Apply settings that were specified on the command line. The expected
		format is as follows: [name]=[val];[name]=[val];...
		
		Arguments:
		args -- the string of command line arguments
		"""
		
		if args == None:		
			return
			
		for arg in args.split(";"):
			a = arg.split("=")
			if len(a) == 2:
			
				# Automagically determine the data type
				if a[1] == "True":
					val = True
				elif a[1] == "False":
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
					debug.msg("%s = %s" % (a[0], val))
				except:
					debug.msg("Failed to parse argument: %s" % arg)				
		
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
					if value == 'false':
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
			if setting != "cfg_ver":
				qsettings.setValue(setting, value)		
	

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

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

from PyQt4 import QtCore
import libopensesame.misc
from libopensesame import debug

# Determine the sip api that is used, because this depends on whether or not
# IPython is loaded
import sip
api = sip.getapi('QString')
if api not in (1,2):
	raise Exception('config: unknown api %s' % api)

config = {
	"cfg_ver" : 0,
	"_initial_window_state" : QtCore.QByteArray(),
	"auto_update_check" : True,
	"auto_response" : False,
	"autosave_interval" : 10 * 60 * 1000,
	"autosave_max_age" : 7,
	"default_logfile_folder" : libopensesame.misc.home_folder(),
	"disabled_plugins" : "",
	"immediate_rename" : False,
	"onetabmode" : False,
	"overview_info" : False,
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
	"show_startup_tip" : True,
	"style" : "",
	"theme" : "gnome",
	"toolbar_size" : 32,
	"toolbar_text" : False,
	"new_experiment_dialog" : True,
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
	
def get_config(setting):

	"""
	Retrieve a setting

	Returns:
	A setting or False if the setting does not exist
	"""

	return config[setting]

def set_config(setting, value):

	"""
	Set a setting

	Arguments:
	setting -- the setting name
	value -- the setting value
	"""

	config[setting] = value
	config["cfg_ver"] += 1

def restore_config(settings):

	"""
	Restore settings from a QSetting

	Arguments:
	settings -- a QSetting
	"""

	global api
	for setting, default in config.items():
		value = settings.value(setting, default)

		# The older (default) api requires an explicit type conversion
		if api == 1:
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

		# The newer api returns some things as strings, so we still have to do
		# some type conversion
		else:
			if type(default) == bool:
				if value == 'false':
					value = False
				else:
					value = True
			elif type(default) == int:
				value = int(value)

		set_config(setting, value)
		
def save_config(settings):

	"""
	Save settings to a QSetting

	Arguments:
	setting -- a QSetting
	"""

	for setting, value in config.items():
		if setting != "cfg_ver":
			settings.setValue(setting, value)

def parse_cmdline_args(args):

	"""
	Apply settings that were specified on the command line. The expected format
	is as follows: [name]=[val];[name]=[val];...
	
	Arguments:
	args -- the string of arguments
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
				set_config(a[0], val)
				debug.msg("%s = %s" % (a[0], val))
			except:
				debug.msg("Failed to parse argument: %s" % arg)
				

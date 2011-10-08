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

config = {
	"cfg_ver" : 0,
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
	"new_experiment_dialog" : True,
	"disabled_plugins" : "",
	"version_check_url" : "http://files.cogsci.nl/software/opensesame/MOST_RECENT_VERSION.TXT"
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

	for setting, default in config.items():
		if type(default) == bool:
			value = settings.value(setting, default).toBool()
		elif type(default) == str:
			try:
				value = str(settings.value(setting, default).toString())
			except:
				value = default
		elif type(default) == int:
			value = settings.value(setting, default).toInt()[0]	
		set_config(setting, value)
	
def save_config(settings):

	"""
	Save settings to a QSetting
	
	Arguments:
	setting -- a QSetting
	"""
	
	for setting, value in config.items():
		settings.setValue(setting, value)


# -*- coding:utf-8 -*-

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
    "cfg_ver": 0,
    "_initial_window_geometry": QtCore.QByteArray(),
    "_initial_window_state": QtCore.QByteArray(),
    "auto_update_check": True,
    "default_logfile_folder": libopensesame.misc.home_folder(),
    "default_pool_folder": libopensesame.misc.home_folder(),
    "disabled_plugins": "",
    "disabled_extensions": "",
    "file_dialog_path": "",
    "file_pool_size_warning": 104857600,
    "loop_wizard": None,
    "onetabmode": False,
    "quick_run_logfile": u"quickrun.csv",
    "recent_files": u"",
    "reset_console_on_experiment_start": True,
    "shortcut_itemtree": u"Ctrl+1",
    "shortcut_tabwidget": u"Ctrl+2",
    "shortcut_stdout": u"Ctrl+3",
    "shortcut_pool": u"Ctrl+4",
    "shortcut_copy_clipboard_unlinked": u"Ctrl+C",
    "shortcut_copy_clipboard_linked": u"Ctrl+Shift+C",
    "shortcut_paste_clipboard": u"Ctrl+V",
    "shortcut_delete": u"Del",
    "shortcut_permanently_delete": u"Shift+Del",
    "shortcut_context_menu": u"+",
    "shortcut_rename": u"F2",
    "shortcut_edit_runif": u"F3",
    "style": u"",
    "theme": u"default",
    "toolbar_size": 32,
    "toolbar_text": False,
    "runner": u"multiprocess",
    "opensesamerun_exec": u"",
    "start_drag_delay": 300,
    "pos": QtCore.QPoint(200, 200),
    "size": QtCore.QSize(1000, 600),
    "url_website": u"http://www.cogsci.nl/opensesame",
    "url_facebook": u"http://www.facebook.com/cognitivescience",
    "url_twitter": u"http://www.twitter.com/cogscinl",
    'sketchpad_placeholder_color': u'#00FF00',
    'sketchpad_grid_color': u'#00FF00',
    'sketchpad_grid_thickness_thin': 2,
    'sketchpad_grid_thickness_thick': 4,
    'sketchpad_grid_opacity': 32,
    'sketchpad_preview_color': u'#00FF00',
    'sketchpad_preview_penwidth': 2,
    'mode': u'default',
    'locale': u'',
}
DEFAULT_CONFIG_LINUX = {}
DEFAULT_CONFIG_MAC = {}
DEFAULT_CONFIG_WINDOWS = {}


class Config:

    def __init__(self):
        self.reset()

    def __str__(self):
        s = u''
        for key, val in self.config.items():
            if not isinstance(val, str) and not isinstance(val, int) \
                    and not isinstance(val, float):
                val = type(val)
            s += u'%s: %s\n' % (key, val)
        return s

    def __getattr__(self, setting):
        r"""A getter for settings, to allow for easy access

        Parameters
        ----------
        setting
            The setting to get
        """
        if setting not in self.config:
            raise osexception(u'The setting "%s" does not exist'
                              % setting)
        return self.config[setting]

    def __setattr__(self, setting, value):
        """A setter for settings, to allow for easy access"""
        if setting not in self.config:
            raise osexception(u'The setting "%s" does not exist'
                              % setting)
        self.config[setting] = value
        self.config[u'cfg_ver'] += 1

    def __setitem__(self, setting, value):
        r"""Emulate dict API."""
        self.__setattr__(setting, value)

    def __getitem__(self, setting):
        r"""Emulate dict API."""
        return self.__getattr__(setting)

    def __contains__(self, setting):
        """
        returns:
                True if setting exists, False otherwise.
        """
        return setting in self.config

    def register(self, setting, default):
        r"""Registers a new setting, if it doesn't already exist.

        Parameters
        ----------
        setting
            The setting name.
        default
            A default value, which is used if the setting doesn't already
            exist.
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
        """Apply settings that were specified on the command line. The expected
        format is as follows: [name]=[val];[name]=[val];...

        Parameters
        ----------
        args: str
            The string of command line arguments
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

    def type_qvariant(self, value, default=None):
        r"""Typecasts a value to a normal type that matches the type of a
        default value, because QSettings returns str objects.

        Parameters
        ----------
        value
            A value.
        default
            A default value.

        Returns
        -------
        A value.
        """
        if not isinstance(value, str):
            return value
        if (default is None or isinstance(default, bool)):
            if value == 'true':
                return True
            if value == 'false':
                return False
        if (default is None or isinstance(default, int)):
            try:
                return int(value)
            except (TypeError, ValueError):
                pass
        if (default is None or isinstance(default, float)):
            try:
                return float(value)
            except (TypeError, ValueError):
                pass
        return value

    def restore(self, mode):
        r"""Restore settings from a QSettings."""
        oslogger.debug('restoring config profile {}'.format(mode))
        qsettings = QtCore.QSettings(u"cogscinl", mode)
        qsettings.beginGroup('OpenSesame4')
        for setting, default in self.config.items():
            try:
                value = qsettings.value(setting, default)
            except TypeError:
                continue
            value = self.type_qvariant(value, default)
            self.config[setting] = value
        for setting in qsettings.allKeys():
            if setting in self.config:
                continue
            oslogger.info(f'unregistered setting {setting}')
            value = qsettings.value(setting)
            value = self.type_qvariant(value, None)
            self.config[setting] = value
        self.mode = mode
        qsettings.endGroup()

    def save(self):
        r"""Save settings to a QSettings."""
        oslogger.debug('saving config profile {}'.format(self.mode))
        qsettings = QtCore.QSettings(u"cogscinl", self.mode)
        qsettings.beginGroup('OpenSesame4')
        for setting, value in self.config.items():
            if setting != u"cfg_ver":
                qsettings.setValue(setting, value)
        qsettings.endGroup()

    def clear(self):
        r"""Clears all settings."""
        qsettings = QtCore.QSettings(u"cogscinl", self.mode)
        qsettings.beginGroup('OpenSesame4')
        qsettings.clear()
        qsettings.endGroup()

    def version(self):
        r"""Gets the current version of the config."""
        return self.cfg_ver

    def reset(self):
        r"""Resets the configution back to default."""
        object.__setattr__(self, u'config', {})
        self.config.update(DEFAULT_CONFIG)
        if platform.system() == u"Windows":
            self.config.update(DEFAULT_CONFIG_WINDOWS)
        elif platform.system() == u"Darwin":
            self.config.update(DEFAULT_CONFIG_MAC)
        elif platform.system() == u"Linux":
            self.config.update(DEFAULT_CONFIG_LINUX)

    def nuke(self):
        r"""Clears the config."""
        self.reset()
        self.clear()
        self.save()


# Create a singleton config instance
cfg = Config()

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
"""
from libopensesame.py3compat import *
from pathlib import Path
from importlib import import_module
from libopensesame.misc import camel_case
from libopensesame import plugins  # deprecated
from libopensesame.plugin_manager import OldStylePlugin, Plugin, PluginManager
from libopensesame.oslogging import oslogger
from libqtopensesame.items.qtautoplugin import QtAutoPlugin


class QtPlugin(Plugin):
    """An extenion of the Plugin class that loads the Qt interface of a
    plugin or extension.
    """
    
    def build(self, *args, **kwargs):
        if self._runtime_cls is None:
            oslogger.debug(f'finding plugin gui class for {self.name}')
            mod = import_module(
                f'{self._mod.__package__}.{self.name}')
            cls_name = f'Qt{camel_case(self.name)}'
            if hasattr(mod, cls_name):
                self._runtime_cls = getattr(mod, cls_name)
            else:
                oslogger.info(
                    f'dynamically creating plugin gui class for {self.name}')
                Runtime = getattr(mod, camel_case(self.name))
                
                def cls_init(self, name, experiment, script=None):
                    Runtime.__init__(self, name, experiment, script)
                    QtAutoPlugin.__init__(self, __file__)
                    
                self._runtime_cls = type(cls_name, (Runtime, QtAutoPlugin),
                                         {'__init__': cls_init})
            if not hasattr(self._runtime_cls, 'description'):
                self._runtime_cls.description = self._mod.__doc__
        oslogger.info(f'building plugin gui for {self.name}')
        return self._runtime_cls(*args, **kwargs)
        

class QtOldStylePlugin(OldStylePlugin):
    """An extenion of the OldStylePlugin class that loads the Qt interface of a
    plugin or extension. This is deprecated and will be removed.
    """
    
    def build(self, *args, **kwargs):
        oslogger.debug(f'building old-style plugin gui for {self.name}')
        if self.type_ == 'plugins':
            return plugins.load_plugin(self.name, *args, prefix='qt', **kwargs)
        return plugins.load_extension(self.name, *args, **kwargs)


class QtPluginManager(PluginManager):
    """An etxenion of the PluginManager that provdes access to the Qt
    interfaces of plugins and extensions.
    """

    def _discover_plugin(self, name):
        plugin = QtPlugin(import_module(name))
        self._plugins[plugin.name] = plugin

    def _discover_oldstyle(self):
        type_ = 'plugins' if self._pkg.__name__ == 'opensesame_plugins' \
            else 'extensions'
        for plugin_name in plugins.list_plugins(_type=type_):
            oslogger.warning(f'found deprecated old-style plugin {plugin_name}')
            if plugin_name in self._plugins:
                oslogger.warning(f'plugin {plugin_name} already found')
                continue
            self._plugins[plugin_name] = QtOldStylePlugin(plugin_name, type_)

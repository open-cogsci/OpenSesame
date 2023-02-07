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
from libopensesame import plugins  # deprecated
from libopensesame.plugin_manager import OldStylePlugin, Plugin, PluginManager
from libopensesame.oslogging import oslogger


class QtPlugin(Plugin):

    def build(self, *args, **kwargs):
        if self._runtime_cls is None:
            oslogger.info(f'finding plugin gui class for {self.name}')
            mod = import_module(
                f'{self._mod.__package__}.Qt{self.name}')
            self._runtime_cls = getattr(mod, f'Qt{camel_case(self.name)}')
        oslogger.info(f'building plugin gui for {self.name}')
        return self._runtime_cls(*args, **kwargs)
        

class QtOldStylePlugin(OldStylePlugin):
    
    def build(self, *args, **kwargs):
        oslogger.info(f'building old-style plugin gui for {self.name}')
        if self.type_ == 'plugins':
            return plugins.load_plugin(self.name, *args, prefix='qt', **kwargs)
        return plugins.load_extension(self.name, *args, **kwargs)


class QtPluginManager(PluginManager):

    def _discover_plugin(self, name):
        plugin = QtPlugin(import_module(name))
        self._plugins[plugin.name] = plugin

    def _discover_oldstyle(self):
        type_ = 'plugins' if self._pkg.__name__ == 'opensesame_plugins' \
            else 'extensions'
        for plugin_name in plugins.list_plugins(_type=type_):
            oslogger.warning(f'found deprecated old-style plugin {plugin_name}')
            self._plugins[plugin_name] = QtOldStylePlugin(plugin_name, type_)

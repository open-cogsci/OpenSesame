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
import pkgutil
import pathlib
from importlib import import_module
from libopensesame import plugins  # deprecated
from libopensesame.misc import camel_case
from libopensesame.oslogging import oslogger


class Plugin:
    
    def __init__(self, mod):
        self.name = mod.__package__.split('.')[-1]
        self._mod = mod
        self._runtime_cls = None
        self.folder = Path(mod.__file__)
        self.icon =  self.folder / f'{self.name}.png'
        self.icon_large = self.folder / f'{self.name}_large.png'
    
    def __getitem__(self, attr):
        return getattr(self._mod, attr)
        
    def attribute(self, attr, default=None):
        return self._mod.__dict__.get(attr, default)
    
    def build(self, *args, **kwargs):
        if self._runtime_cls is None:
            oslogger.info(f'finding plugin runtime for {self.name}')
            mod = import_module(
                f'{self._mod.__package__}.{self.name}')
            if hasattr(mod, camel_case(self.name)):
                self._runtime_cls = getattr(mod, camel_case(self.name))
            else:
                self._runtime_cls = getattr(mod, self.name)
        oslogger.info(f'building plugin gui for {self.name}')
        return self._runtime_cls(*args, **kwargs)


class OldStylePlugin:
    
    def __init__(self, name, type_):
        self.name = name
        self.type_ = type_
        self.folder = plugins.plugin_folder(name, _type=self.type_)
        self.icon = plugins.plugin_icon_small(name, _type=self.type_)
        self.icon_large = plugins.plugin_icon_large(name, _type=self.type_)
        
    def __getitem__(self, attr):
        return self.attribute(attr,
                              default='default' if attr == 'modes' else None)
        
    def attribute(self, attr, default=None):
        return plugins.plugin_property(self.name, attr, default=default, 
                                       _type=self.type_)
        
    def build(self, *args, **kwargs):
        oslogger.info(f'building old-style plugin for {self.name}')
        if self.type_ == 'plugins':
            return plugins.load_plugin(self.name, *args, **kwargs)
        return plugins.load_extension(self.name, *args, **kwargs)


class PluginManager:
    
    def __init__(self, pkg):
        self._plugins = {}
        self._pkg = pkg
        for importer, name, ispkg in pkgutil.iter_modules(
                pkg.__path__, prefix=pkg.__name__ + '.'):
            if not ispkg:
                continue
            oslogger.info(f'found plugin package {name} in {importer.path}')
            self._discover_subpkg(name)
        self._discover_oldstyle()
                
    def _discover_subpkg(self, name):
        pkg = import_module(name)
        for importer, plugin_name, ispkg in pkgutil.iter_modules(
                pkg.__path__, prefix=name + '.'):
            if not ispkg:
                continue
            oslogger.info(f'found plugin {plugin_name} in {importer.path}')
            self._discover_plugin(plugin_name)
            
    def _discover_plugin(self, name):
        plugin = Plugin(import_module(name))
        self._plugins[plugin.name] = plugin
        
    def _discover_oldstyle(self):
        type_ = 'plugins' if self._pkg.__name__ == 'opensesame_plugins' \
            else 'extensions'
        for plugin_name in plugins.list_plugins(_type=type_):
            oslogger.warning(f'found deprecated old-style plugin {plugin_name}')
            self._plugins[plugin_name] = OldStylePlugin(plugin_name, type_)
        
    def filter(self, **kwargs):
        for plugin in self:
            for key, value in kwargs.items():
                if isinstance(plugin[key], (list, tuple, set, dict)):
                    if value in plugin[key]:
                        yield plugin
                elif plugin[key] == value:
                    yield plugin
        
    def __contains__(self, name):
        return name in self._plugins
    
    def __getitem__(self, name):
        return self._plugins[name]
        
    def __iter__(self):
        for plugin in self._plugins.values():
            yield plugin

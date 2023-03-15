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
import os
from openexp import resources
from importlib import import_module
from libopensesame.misc import camel_case
from libopensesame import plugins  # deprecated
from libopensesame.plugin_manager import OldStylePlugin, Plugin, PluginManager
from libopensesame.oslogging import oslogger
from libqtopensesame.items.qtautoplugin import QtAutoPlugin
from libqtopensesame.misc.translate import translation_context


class QtPlugin(Plugin):
    """An extenion of the Plugin class that loads the Qt interface of a
    plugin or extension.
    """
    
    def __init__(self, mod):
        super().__init__(mod)
        # The main icon is set to the icon plugin attribute if available, and
        # otherwise to a [plugin_name].png file in the plugin folder
        self.icon = self._mod.icon if hasattr(self._mod, 'icon') \
            else os.path.join(self.folder, f'{self.name}.png')
        # The large icon is set to the large_icon plugin attribute if
        # available, and otherwise to the main icon if specified through an
        # attribute and otherwise to a [plugin_name]_large.png file.
        if hasattr(self._mod, 'icon_large'):
            self.icon_large = self._mod.icon_large
        elif hasattr(self._mod, 'icon'):
            self.icon_large = self._mod.icon
        else:
            self.icon_large = os.path.join(self.folder,
                                           f'{self.name}_large.png')

    @property
    def description(self):
        # We translate the description
        _ = translation_context(self.name, category=self._type)
        return _(super().description)
    
    def _get_cls(self, mod):
        # If there is a class named Qt[PluginName], then is assumed to be
        # the GUI class
        cls_name = f'Qt{camel_case(self.name)}'
        if hasattr(mod, cls_name):
            return getattr(mod, cls_name)
        # Otherwise, we dynamically create a class that inherits from the
        # plugin runtime class and QtAutoPlugin. We also specify a custom
        # __init__() function that calls the parent constructors correclty.
        oslogger.info(
            f'dynamically creating plugin gui class for {self.name}')
        Runtime = getattr(mod, camel_case(self.name))
        
        def cls_init(self, name, experiment, script=None):
            Runtime.__init__(self, name, experiment, script)
            QtAutoPlugin.__init__(self, __file__)
            
        return type(cls_name, (Runtime, QtAutoPlugin), {'__init__': cls_init})
        
    def supports(self, experiment):
        fnc = self.attribute('supports', None)
        if callable(fnc):
            return fnc(experiment)
        return True


class QtOldStylePlugin(OldStylePlugin):
    """An extenion of the OldStylePlugin class that loads the Qt interface of a
    plugin or extension. This is deprecated and will be removed.
    """
    
    def __init__(self, name, type_):
        super().__init__(name, type_)
        self.icon = plugins.plugin_icon_small(name, _type=self.type_)
        self.icon_large = plugins.plugin_icon_large(name, _type=self.type_)
    
    def build(self, *args, **kwargs):
        oslogger.debug(f'building old-style plugin gui for {self.name}')
        if self.type_ == 'plugins':
            return plugins.load_plugin(self.name, *args, prefix='qt', **kwargs)
        return plugins.load_extension(self.name, *args, **kwargs)

    def supports(self, experiment):
        return True


class QtPluginManager(PluginManager):
    """An extension of the PluginManager that provdes access to the Qt
    interfaces of plugins and extensions.
    """
    
    plugin_cls = QtPlugin
    oldstyle_plugin_cls = QtOldStylePlugin

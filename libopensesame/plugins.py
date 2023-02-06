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
import os
import sys
import json
import time
from libopensesame import misc
from libopensesame.oslogging import oslogger
from libopensesame.exceptions import osexception
from libopensesame.py3compat import *

# Caching variables
_plugin_dict = {}
_folders = {}
_properties = {}

# The plug-ins can be either source or bytecode. Usually they will be source,
# but some distributions (notably the runtime for Android) will automatically
# compile everything to bytecode.
src_templates = [u'%s.py']
bytecode_templates = [u'%s.pyo', u'%s.pyc']


def plugin_folders(only_existing=True, _type=u'plugins'):
    r"""Returns a list of plugin folders.

    Parameters
    ----------
    only_existing : bool, optional
        Specifies if only existing folders should be returned.
    _type : str, unicode, optional
        Indicates whether runtime plugins ('plugins') or GUI extensions
        ('extensions') should be listed.

    Returns
    -------
    list
        A list of folders.
    """
    l = []
    # Build a list of default plugin/ extension folders
    for folder in misc.base_folders:
        path = os.path.join(folder, u'opensesame_%s' % _type)
        if os.path.exists(path):
            l.append(path)
    # Get the environment variables
    if _type == u'plugins':
        key = u'OPENSESAME_PLUGIN_PATH'
    else:
        key = u'OPENSESAME_EXTENSION_PATH'
    if key in os.environ:
        for path in os.environ[key].split(';'):
            path = safe_decode(path, enc=misc.filesystem_encoding())
            if os.path.exists(path):
                l.insert(0, path)
    if os.name == u'posix' and u'HOME' in os.environ:
        # Regular Linux distributions. TODO: How well does this apply to Mac OS?
        path = os.path.join(os.environ[u'HOME'], u'.opensesame', _type)
        if not only_existing or os.path.exists(path):
            l.append(path)
        path = u'/usr/share/opensesame/%s' % _type
        if not only_existing or os.path.exists(path):
            l.append(path)
    elif os.name == u'posix' and u'HOME' not in os.environ:
        # Android can be recognized by the fact that the HOME variable is not
        # available. We can simply use the relative path `plugins`, which will
        # (always?) point to `/data/data/nl.cogsci.nl/opensesame/files/plugins`
        path = _type
        if not only_existing or os.path.exists(path):
            l.append(path)
    elif os.name == u'nt':
        # Windows
        path = os.path.join(safe_decode(os.environ[u'APPDATA'],
                                        enc=misc.filesystem_encoding()), u'.opensesame', _type)
        if not only_existing or os.path.exists(path):
            l.append(path)
    return l


def is_plugin(item_type, _type=u'plugins'):
    r"""Checks if a given item type corresponds to a plugin.

    Returns
    -------
    True if the item_type is a plugin, False otherwise.
    """
    return plugin_folder(item_type, _type=_type) is not None


def plugin_disabled(plugin, _type=u'plugins'):
    r"""Checks if a plugin has been disabled. If the config module cannot be
    loaded the return value is False.

    Parameters
    ----------
    plugin
        The plugin to check.
    _type, optional
        plugins/ extensions

    Returns
    -------
    True if the plugin has been disabled, False otherwise.
    """
    from libqtopensesame.misc.config import cfg

    if plugin_property(plugin, u'disabled', _type=_type):
        return True
    # Check if disabled_plugins is not empty in which case it is a
    # QPyNullVariant which does not have split() method
    disabled_plugins = cfg[u'disabled_%s' % _type]
    if hasattr(disabled_plugins, u"split") and plugin in disabled_plugins.split(u';'):
        return True
    return False


def plugin_property(plugin, _property, default=0, _type=u'plugins'):
    r"""Returns a property of a plug-in.

    Parameters
    ----------
    plugin
        The name of the plugin.
    _property
        The name of the property.
    default, optional
        A default property value.

    Returns
    -------
    The property value.
    """
    return plugin_properties(plugin, _type=_type).get(_property, default)


def set_plugin_property(plugin, property, value):
    r"""Sets a property in the info dictionary for a plugin.

    Parameters
    ----------
    plugin
        The plugin name.
    property
        The property name.
    value
        The property value.
    """
    plugin_properties(plugin)
    _properties[plugin][property] = value


def plugin_properties(plugin, _type=u'plugins'):
    r"""Gets the info dictionary for a plugin.

    Parameters
    ----------
    plugin
        The plugin name.
    _type
        The plugin type (i.e. 'plugins' or 'extensions').

    Returns
    -------
    An info dictionary.
    """
    if plugin in _properties:
        return _properties[plugin]
    folder = plugin_folder(plugin, _type=_type)
    info_txt = os.path.join(folder, u'info.txt')
    info_json = os.path.join(folder, u'info.json')
    info_yaml = os.path.join(folder, u'info.yaml')
    # First try to read json. This is used by the plugins bundled with
    # OpenSesame because it is faster (even if it's less readable)
    if os.path.exists(info_json):
        with safe_open(info_json) as fd:
            s = fd.read()
        try:
            _properties[plugin] = json.loads(s)
        except:
            oslogger.error(u'Failed to parse %s' % info_json)
            _properties[plugin] = {}
    # New-style plug-ins, using info.yaml
    elif os.path.exists(info_yaml):
        # Read the yaml file and replace all tabs by spaces. This is necessary,
        # because yaml doesn't accept tab-based indentation, whereas json does.
        with safe_open(info_yaml) as fd:
            s = fd.read()
        s = s.replace(u'\t', u'    ')
        try:
            _properties[plugin] = safe_yaml_load(s)
        except:
            oslogger.error(u'Failed to parse %s' % info_yaml)
            _properties[plugin] = {}
    # Old-style plug-ins, using info.txt
    elif os.path.exists(info_txt):
        _properties[plugin] = {}
        with safe_open(info_txt) as fd:
            for l in fd:
                a = l.split(":")
                if len(a) == 2:
                    val = a[1].strip()
                    var = a[0].strip()
                    try:
                        val = int(val)
                    except:
                        pass
                    _properties[plugin][var] = val
    else:
        _properties[plugin] = {}
        oslogger.error(
            u'Failed to read plug-in information (%s) from info.[txt|yaml|json]'
            % plugin
        )
    _properties[plugin][u'plugin_folder'] = folder
    _properties[plugin][u'type'] = _type
    return _properties[plugin]


def plugin_category(plugin, _type=u'plugins'):
    r"""Returns the category of a plugin.

    Parameters
    ----------
    plugin
        The plugin name.
    _type, optional
        plugins/ extensions

    Returns
    -------
    A category
    """
    return plugin_property(
        plugin,
        u'category',
        default=u'Miscellaneous',
        _type=_type
    )


def list_plugins(filter_disabled=True, _type=u'plugins', mode=u'default'):
    r"""Returns a list of plugins.

    Parameters
    ----------
    filter_disabled, optional
        Indicates whether disabled plugins should be included in the list.
    _type, optional
        plugins/ extensions
    mode, optional
        A mode as specified on the command line

    Returns
    -------
    A list of plugins (item_types).
    """
    if _type not in _plugin_dict:
        plugins = []
        for folder in plugin_folders(_type=_type):
            for plugin in os.listdir(folder):
                if is_plugin(plugin, _type=_type):
                    if mode not in plugin_property(
                            plugin,
                            u'modes',
                            default=[u'default'],
                            _type=_type
                    ):
                        oslogger.debug(
                            '{} does not support mode {}'.format(plugin, mode)
                        )
                        continue
                    _plugin = plugin, plugin_property(
                        plugin, u'priority',
                        _type=_type
                    )
                    if _plugin not in plugins:
                        plugins.append(_plugin)
        # Sort (inversely) by priority
        plugins.sort(key=lambda p: -p[1])
        _plugin_dict[_type] = [plugin[0] for plugin in plugins]
    return [
        plugin
        for plugin in _plugin_dict[_type]
        if not (filter_disabled and plugin_disabled(plugin, _type=_type))
    ]


def plugin_folder(plugin, _type=u'plugins'):
    r"""Returns the folder of a plugin

    Parameters
    ----------
    plugin
        The name of the plugin

    Returns
    -------
    The folder of the plugin.
    """
    global _folders

    if plugin in _folders:
        return _folders[plugin]
    for folder in plugin_folders(_type=_type):
        plugin = str(plugin)
        for tmpl in src_templates + bytecode_templates:
            if os.path.exists(os.path.join(folder, plugin, tmpl % plugin)):
                f = os.path.join(folder, plugin)
                _folders[plugin] = f
                return f
    return None


def plugin_icon_large(plugin, _type=u'plugins'):
    r"""Return the large icon for a plugin

    Parameters
    ----------
    plugin
        The name of the plugin
    _type, optional
        plugins/ extensions

    Returns
    -------
    The full path to an icon
    """
    icon = plugin_property(plugin, u'icon', default=None)
    if icon is not None:
        return icon
    return os.path.join(plugin_folder(plugin, _type=_type),
                        u'%s_large.png' % plugin)


def plugin_icon_small(plugin, _type=u'plugins'):
    r"""Return the small icon for a plugin

    Parameters
    ----------
    plugin
        The name of the plugin.
    _type, optional
        plugins/ extensions

    Returns
    -------
    The full path to an icon
    """
    icon = plugin_property(plugin, u'icon', default=None)
    if icon is not None:
        return icon
    return os.path.join(plugin_folder(plugin, _type=_type), u'%s.png' % plugin)


def import_plugin(plugin, _type=u'plugins'):
    r"""Imports plugin module.

    Parameters
    ----------
    plugin
        The name of the plugin.
    _type, optional
        plugins/ extensions

    Returns
    -------
    The imported module.
    """
    import imp
    plugin = str(plugin)
    folder = plugin_folder(plugin, _type=_type)
    for tmpl in src_templates:
        if os.path.exists(os.path.join(folder, tmpl % plugin)):
            path = os.path.join(folder, tmpl % plugin)
            if not py3:
                path = safe_encode(path, enc=misc.filesystem_encoding())
            return imp.load_source(plugin, path)
    for tmpl in bytecode_templates:
        if os.path.exists(os.path.join(folder, tmpl % plugin)):
            path = os.path.join(folder, tmpl % plugin)
            if not py3:
                path = safe_encode(path, enc=misc.filesystem_encoding())
            return imp.load_compiled(plugin, path)


def load_plugin(
        plugin, item_name, experiment, string, prefix=u'', _type=u'plugins'
):
    r"""Returns an instance of the plugin.

    Parameters
    ----------
    plugin
        The name of the plugin.
    item_name
        The name of the item (plugin instance).
    experiment
        The experiment object.
    string
        A definition string.
    prefix, optional
        A class prefix to allow switching between [plugin] and qt[plugin].

    Returns
    -------
    An item (plugin instance).
    """
    t0 = time.time()
    if plugin_folder(plugin, _type=_type) not in sys.path:
        sys.path.append(plugin_folder(plugin, _type=_type))
    item_module = import_plugin(plugin, _type=_type)
    item_class = getattr(item_module, prefix + plugin)
    item = item_class(item_name, experiment, string)
    set_plugin_property(plugin, u'startup_time', time.time() - t0)
    return item


def load_extension(ext_name, main_window):
    r"""Creates an instance of an extension.

    Parameters
    ----------
    ext_name
        The extension name.
    main_window
        The main window object.

    Returns
    -------
    An extension object.
    """
    t0 = time.time()
    sys.path.append(plugin_folder(ext_name, _type=u'extensions'))
    mod = import_plugin(ext_name, _type=u'extensions')
    cls = getattr(mod, ext_name)
    ext = cls(
        main_window,
        info=plugin_properties(ext_name, _type=u'extensions')
    )
    set_plugin_property(ext_name, u'startup_time', time.time() - t0)
    return ext


def load_cls(path, cls, mod, pkg=None):
    r"""Dynamically loads a module from a path and return a class from the
    module.

    Parameters
    ----------
    path
        A folder or file name. If a filename is specified, the file's directory
        will be used as path.
    cls
        The class name.
    mod
        The name of a module, which corresponds to the name of the source file
        without the `.py` extension.
    pkg
        The module's package. This is effectively a subfolder that is added to
        the path.

    Returns
    -------
    A class.
    """
    mod = load_mod(path, mod, pkg)
    return getattr(mod, cls)


def load_mod(path, mod, pkg=None):
    r"""Dynamically loads a module from a path.

    Parameters
    ----------
    path
        A folder or file name. If a filename is specified, the file's directory
        will be used as path.
    mod
        The name of a module, which corresponds to the name of the source file
        without the `.py` extension.
    pkg
        The module's package. This is effectively a subfolder that is added to
        the path.

    Returns
    -------
    A module.
    """
    import imp
    path = safe_decode(path, enc=sys.getfilesystemencoding())
    if not os.path.isdir(path):
        path = os.path.dirname(path)
    if pkg is not None:
        path = os.path.join(path, pkg)
    path = os.path.join(path, mod+u'.py')
    if not os.path.exists(path):
        raise osexception(u'%s does not exist' % path)
    oslogger.debug(u'loading module from %s' % path)
    if not py3:
        mod = safe_encode(mod, enc=sys.getfilesystemencoding())
        path = safe_encode(path, enc=sys.getfilesystemencoding())
    return imp.load_source(mod, path)

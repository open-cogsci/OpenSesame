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
from libopensesame.misc import snake_case
from libopensesame.cistr import CIStr
from libopensesame.oslogging import oslogger
from libopensesame.exceptions import osexception
from libopensesame.item_stack import item_stack_singleton


# A list of names that cannot be used, because they cause trouble for one reason
# or another
INVALID_NAMES = [
    'response'  # causes conflict with correct_response variable
]


class ItemStore:

    r"""The `items` object provides dict-like access to the items. It's mainly
    useful for programatically executing items.

    An `items` object is created
    automatically when the experiment starts.

    In addition to the functions
    listed below, the following semantics are
    supported:

    __Example__:

    ~~~
    .python
    # Programmatically prepare and run a sketchpad item.
    items.execute(u'my_sketchpad')
    # Check if an item exists
    if u'my_sketchpad'
    in items:
            print(u'my_sketchpad exists')
    # Delete an item
    del
    items[u'my_sketchpad']
    # Walk through all item names
    for item_name in
    items:
            print(item_name)
    ~~~

    [TOC]
    """
    built_in_types = [u'sequence', u'loop', u'sketchpad', u'feedback',
                      u'keyboard_response', u'mouse_response', u'sampler',
                      u'synth', u'inline_script', u'logger']

    def __init__(self, experiment):
        r"""Constructor.

        Parameters
        ----------
        experiment : experiment.
            The experiment object.
        """
        self.__items__ = {}
        self.experiment = experiment

    def execute(self, name):
        r"""Executes the run and prepare phases of an item, and updates the
        item stack.

        Parameters
        ----------
        name : str
            An item name.

        Examples
        --------
        >>> items.execute(u'target_sketchpad')
        """
        self.prepare(name)
        self.run(name)

    def run(self, name):
        r"""Executes the run phase of an item, and updates the item stack.

        Parameters
        ----------
        name : str
            An item name.

        Examples
        --------
        >>> items.prepare('target_sketchpad')
        >>> items.run('target_sketchpad')
        """
        item_stack_singleton.push(name, u'run')
        self[name].run()
        item_stack_singleton.pop()

    def prepare(self, name):
        r"""Executes the prepare phase of an item, and updates the item stack.

        Parameters
        ----------
        name : str
            An item name.

        Examples
        --------
        >>> items.prepare('target_sketchpad')
        >>> items.run('target_sketchpad')
        """
        item_stack_singleton.push(name, u'prepare')
        self[name].prepare()
        item_stack_singleton.pop()

    def new(self, _type, name=None, script=None, allow_rename=True):
        r"""Creates a new item.

        Parameters
        ----------
        _type : unicode
            The item type.
        name : unicode, NoneType, optional
            The item name, or None to choose a unique name based on the item
            type.
        script : unicode, NoneType, optional
            A definition script, or None to start with a blank item.
        allow_rename : bool, optional
            Indicates whether OpenSesame can use a different name from the one
            that is provided as `name` to avoid duplicate names etc.

        Returns
        -------
        item
            The newly generated item.

        Examples
        --------
        >>> items.new('sketchpad', name='my_sketchpad')
        >>> items['my_sketchpad'].prepare()
        >>> items['my_sketchpad'].run()
        """
        oslogger.debug('creating %s' % _type)
        if allow_rename:
            name = self.valid_name(_type, suggestion=name)
        else:
            name = CIStr(name)
        if _type in self.experiment.plugin_manager:
            # Load a plug-in
            try:
                item = self.experiment.plugin_manager[_type].build(
                    name, self.experiment, script)
            except Exception as e:
                raise osexception(u"Failed to load plugin '%s'" % _type,
                                  exception=e)
            self.__items__[name] = item
            return item
        # Load one of the core items
        oslogger.debug(u"loading core item '%s' from '%s'" % (
            _type, self.experiment.module_container()))
        item_module = __import__(self.item_module(_type), fromlist=[u'dummy'])
        item_class = getattr(item_module, _type)
        item = item_class(name, self.experiment, script)
        self.__items__[name] = item
        return item

    def valid_name(self, item_type, suggestion=None):
        r"""Generates a unique name that is valid and resembles the desired
        name.

        Parameters
        ----------
        item_type : unicode
            The type of the item to suggest a name for.
        suggestion : unicode, NoneType, optional
            The desired name, or None to choose a name based on the item's
            type.

        Returns
        -------
        unicode
            A unique name.

        Examples
        --------
        >>> valid_name = items.valid_name(u'sketchpad', u'an invalid name')
        """
        if suggestion is None:
            name = u'new_%s' % item_type
        else:
            name = self.experiment.syntax.sanitize(suggestion, strict=True,
                                                   allow_vars=False)
            # Empty names are not allowed, and we fall back to the item type
            if not name:
                name = item_type
            # Names cannot start with a number, and are therefore prefixed by
            # an underscore.
            elif name[0].isnumeric():
                name = u'_' + name
        _name = name
        invalid_names = list(self) + INVALID_NAMES
        i = 1
        while _name in invalid_names:
            _name = u'%s_%d' % (name, i)
            i += 1
        return CIStr(_name)

    def _type(self, name):
        r"""Gets the type of an item.

        Parameters
        ----------
        name : unicode
            The name of an item.

        Returns
        -------
        unicode, NoneType
            The type of an item, or `None` if the item doesn't exist.

        Examples
        --------
        >>> print(items._type('target_sketchpad'))
        """
        if name not in self:
            return None
        return self[name].item_type
    
    def item_module(self, item_type):
        
        return f'{self.experiment.module_container()}.{snake_case(item_type)}'
        
    # The properties below emulate a dict interface.

    @property
    def __setitem__(self):
        return self.__items__.__setitem__

    @property
    def __delitem__(self):
        return self.__items__.__delitem__

    @property
    def __len__(self):
        return self.__items__.__len__

    @property
    def __iter__(self):
        return self.__items__.__iter__

    @property
    def items(self):
        return self.__items__.items

    @property
    def keys(self):
        return self.__items__.keys

    @property
    def values(self):
        return self.__items__.values

    @property
    def copy(self):
        return self.__items__.copy

    # The functions below are overridden to implement case insensitivity.

    def __contains__(self, name):

        if not isinstance(name, CIStr):
            try:
                name = CIStr(name)
            except AttributeError:
                return False
        return name in self.__items__

    def __getitem__(self, name):

        if not isinstance(name, CIStr):
            name = CIStr(name)
        try:
            return self.__items__[name]
        except KeyError:
            raise osexception(u'No item named "%s"' % name)


# Alias for backwards compatibility
item_store = ItemStore

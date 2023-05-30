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
from libopensesame.var_store import var_store
import warnings
from libopensesame.misc import snake_case
from libopensesame.exceptions import InvalidOpenSesameScript, InvalidValue, \
    IncompatibilityError
from libopensesame.oslogging import oslogger


class Item:
    """Abstract class that serves as the basis for all OpenSesame items.
    
    Parameters
    ----------
    name: str
        The name of the item
    experiment: Experiment
    string: str or None, optional
        A definition string
    """
    
    encoding = u'utf-8'
    var = None

    def __init__(self, name, experiment, string=None):
        if self.var is None:
            self.var = var_store(self, parent=experiment.var)
        self.name = name
        self.experiment = experiment
        self.debug = oslogger.debug_mode
        self.count = 0
        self._get_lock = None
        # Deduce item_type from class name. This takes into account that the
        # class name can be CamelCase and may prefixed by Qt (QtCamelCase),
        # whereas the item_type should always be snake_case without the qt 
        # prefix.
        prefix = self.experiment.item_prefix()
        self.item_type = self.__class__.__name__
        if self.item_type.lower().startswith(prefix.lower()):
            self.item_type = self.item_type[len(prefix):]
        self.item_type = snake_case(self.item_type)
        if not hasattr(self, u'description'):
            self.var.description = self.default_description
        else:
            self.var.description = self.description
        self.from_string(string)

    def __deepcopy__(self, memo):
        """Disable deep-copying of items"""
        return None

    @property
    def clock(self):
        return self.experiment._clock

    @property
    def log(self):
        return self.experiment._log

    @property
    def syntax(self):
        return self.experiment._syntax

    @property
    def python_workspace(self):
        return self.experiment._python_workspace

    @property
    def responses(self):
        return self.experiment._responses
    
    @property
    def plugin_manager(self):
        return self.experiment._plugin_manager

    @property
    def default_description(self):
        return u'Default description'

    def reset(self):
        r"""Resets all item variables to their default value."""
        pass

    def prepare(self):
        """Implements the prepare phase of the item."""
        self.experiment.var.set(u'count_%s' % self.name, self.count)
        self.count += 1

    def run(self):
        """Implements the run phase of the item."""
        pass

    def parse_variable(self, line):
        """Reads a single variable from a single definition line.

        Parameters
        ----------
        line
            A single definition line.

        Returns
        -------
        bool
            True on succes, False on failure.
        """
        # It is a little ugly to call parse_comment() here, but otherwise
        # all from_string() derivatives need to be modified
        if self.parse_comment(line):
            return True
        l = self.syntax.split(line.strip())
        if len(l) == 0 or l[0] != u'set':
            return False
        if len(l) != 3:
            raise InvalidOpenSesameScript(
                'Error parsing variable definition', line=line)
        self.var.set(l[1], l[2])
        return True

    def parse_line(self, line):
        """Allows for arbitrary line parsing, for item-specific requirements.

        Parameters
        ----------
        line
            A single definition line.
        """
        pass

    def parse_comment(self, line):
        """Parses comments from a single definition line, indicated by 
        # // or '.

        Parameters
        ----------
        line
            A single definition line.

        Returns
        -------
        bool
            True on succes, False on failure.
        """
        line = line.strip()
        if len(line) > 0 and line[0] == u'#':
            self.comments.append(line[1:])
            return True
        elif len(line) > 1 and line[0:2] == u'//':
            self.comments.append(line[2:])
            return True
        return False

    def variable_to_string(self, var):
        r"""Encodes a variable into a definition string.

        Parameters
        ----------
        var : str
            The name of the variable to encode.

        Returns
        -------
        str
            A definition string.
        """
        val = safe_decode(self.var.get(var, _eval=False))
        # Multiline variables are stored as a block
        if u'\n' in val or u'"' in val:
            s = u'__%s__\n' % var
            val = val.replace(u'__end__', u'\\__end__')
            for l in val.split(u'\n'):
                s += '\t%s\n' % l
            while s[-1] in (u'\t', u'\n'):
                s = s[:-1]
            s += u'\n\t__end__\n'
            return s
        # Regular variables
        return self.syntax.create_cmd(u'set', arglist=[var, val]) + u'\n'

    def from_string(self, string):
        r"""Parses the item from a definition string.

        Parameters
        ----------
        string : str, NoneType
            A definition string, or None to reset the item.
        """
        self._script = string
        textblock_var = None
        self.var.clear()
        self.reset()
        self.comments = []
        if string is None:
            return
        for line in string.split(u'\n'):
            line_stripped = line.strip()
            # The end of a textblock
            if line_stripped == u'__end__':
                if textblock_var is None:
                    raise InvalidOpenSesameScript(
                        'It appears that a textblock has been closed without '
                        'being opened')
                self.var.set(textblock_var,
                             textblock_val.replace(u'\\__end__', u'__end__'))
                textblock_var = None
            # The beginning of a textblock. A new textblock is only started when
            # a textblock is not already ongoing, and only if the textblock
            # start is of the format __VARNAME__
            elif line_stripped[:2] == u'__' and line_stripped[-2:] == u'__' \
                    and textblock_var is None:
                textblock_var = line_stripped[2:-2]
                if textblock_var != u'':
                    textblock_val = u''
                else:
                    textblock_var = None
                # We cannot just strip the multiline code, because that may mess
                # up indentation. So we have to detect if the string is indented
                # based on the opening __varname__ line.
                strip_tab = line[0] == u'\t'
            # Collect the contents of a textblock
            elif textblock_var is not None:
                if strip_tab:
                    textblock_val += line[1:] + u'\n'
                else:
                    textblock_val += line + u'\n'
            # Parse regular variables
            elif not self.parse_variable(line):
                self.parse_line(line)
        if textblock_var is not None:
            raise InvalidOpenSesameScript(
                'Missing __end__ block for multiline variable {textblock_var}')

    def to_string(self, item_type=None):
        """
        Encodes the item into an OpenSesame definition string.

        Keyword arguments:
        item_type	--	The type of the item or None for autodetect.
                                        (default=None)

        Returns:
        The unicode definition string
        """
        if item_type is None:
            item_type = self.item_type
        s = u'define %s %s\n' % (item_type, self.name)
        for comment in self.comments:
            s += u'\t# %s\n' % comment.strip()
        for var in self.var:
            s += u'\t' + self.variable_to_string(var)
        return s

    def resolution(self):
        r"""Returns the display resolution and checks whether the resolution is
        valid.

        __Important note:__

        The meaning of 'resolution' depends on the
        back-end. For example,
        the legacy back-end changes the actual
        resolution of the display,
        whereas the other back-ends do not alter the
        actual display
        resolution, but create a 'virtual display' with the
        requested
        resolution that is presented in the center of the display.

        Returns
        -------
        tuple
            A (width, height) tuple
        """
        w = self.var.get(u'width')
        h = self.var.get(u'height')
        if type(w) != int or type(h) != int:
            raise InvalidValue(f'({w}, {h}) is not a valid resolution')
        return w, h

    def set_item_onset(self, time=None):
        r"""Set a timestamp for the onset time of the item's execution.

        Parameters
        ----------
        time, optional
            A timestamp or None to use the current time.

        Returns
        -------
        """
        if time is None:
            time = self.clock.time()
        self.experiment.var.set(u'time_%s' % self.name, time)
        return time

    def var_info(self):
        """Give a list of dictionaries with variable descriptions.

        Returns
        -------
        list
            A list of (variable, description) tuples
        """
        return [(u"time_%s" % self.name, u"[Timestamp of last item call]"),
                (u"count_%s" % self.name, u"[Number of item calls]")]
        
    def get(self, *args, **kwargs):
        raise IncompatibilityError(
            'Item.get() has been removed in OpenSesame 4. Please see '
            'the section in the documentation on using variables.')

    def set(self, *args, **kwargs):
        raise IncompatibilityError(
            'Item.set() has been removed in OpenSesame 4. Please see '
            'the section in the documentation on using variables.')


# alias for backwards compatibility
item = Item

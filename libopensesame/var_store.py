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
import warnings
from numbers import Number
from types import NoneType
from libopensesame.py3compat import *
from libopensesame.exceptions import InvalidOpenSesameScript, OSException, \
    VariableDoesNotExist, InvalidValue


class VarStore:

    r"""As of OpenSesame 4.0, all experimental variables are also available
    in the Python workspace. This means that you therefore generally don't need
    to interact with the `var` object anymore.
    
    
    The `var` object provides access to experimental variables.
    Experimental variables are the variables that live in the GUI, and are
    commonly set as independent variables in the LOOP item, referred
    to using
    the square-bracket (`[my_variable]`) notation, and logged by
    the LOGGER
    item.

    A `var` object is created automatically when the experiment starts.
    In addition to the functions listed below, the following semantics are
    supported:

    __Example__:

    ~~~ .python
    # Set an experimental variable
    var.my_variable = u'my_value'
    # Get an experimental variable
    print(u'Subject nr = %d' % var.subject_nr)
    # Delete (unset) an experimental
    variable
    del var.my_variable
    # Check if an experimental variable exists
    if
    u'my_variable' in var:
        print(u'my_variable exists!')
    # Loop through all
    experimental variables
    for var_name in var:
            print(u'variable found:
    %s' % var_name)
    ~~~

    [TOC]
    """
    def __init__(self, item, parent=None):
        r"""Constructor.

        Parameters
        ----------
        item : item
            The associated item.
        parent : var_store, NoneType, optional
            The parent var_store (i.e. for the experiment) or `None` for no
            parent.
        """
        object.__setattr__(self, u'__item__', item)
        object.__setattr__(self, u'__parent__', parent)
        object.__setattr__(self, u'__vars__', {})
        object.__setattr__(self, u'__lock__', None)
        self._copy_class_description()

    def _copy_class_description(self):
        r"""Item descriptions can be class properties. In that case, copy theme
        into the var store to avoid warnings.
        """
        if hasattr(self.__item__.__class__, u'description'):
            self.__vars__[u'description'] = self.__item__.__class__.description

    def _check_var_name(self, var):
        r"""Checks whether a variable name is valid, and raises an
        Exception if it isn't.

        Parameters
        ----------
        var
            The variable name to check.
        """
        try:
            self.__item__.experiment
        except:
            return
        if isinstance(var, str) and \
                self.__item__.experiment.syntax.valid_var_name(var):
            return
        raise InvalidOpenSesameScript(f'"{var}" is not a valid variable name')

    def __contains__(self, var):
        r"""Implements the `in` operator to check if a variable exists."""
        self._check_var_name(var)
        if var in self.__vars__:
            return True
        if hasattr(self.__item__, var):
            warnings.warn(u'var %s is stored as attribute of item %s'
                          % (var, self.__item__.name))
            return True
        if self.__parent__ is not None:
            return self.__parent__.__contains__(var)
        return False

    def __delattr__(self, var):
        r"""Implements the `del` statement to delete a variable."""
        if var in self.__vars__:
            del self.__vars__[var]
        if hasattr(self.__item__, var):
            warnings.warn(u'var %s is stored as attribute of item %s'
                          % (var, self.__item__.name))
            delattr(self.__item__, var)

    def __getattr__(self, var):
        r"""Implements property retrieval to allow direct access to variables."""
        return self.get(var)

    def __setattr__(self, var, val):
        r"""Implements property assignment."""
        self.__vars__[var] = val

    def clear(self, preserve=[]):
        r"""*New in 3.1.2*

        Clears all experimentals variables.

        Parameters
        ----------
        preserve : list, optional
            A list of variable names that shouldn't be cleared.

        Examples
        --------
        >>> var.clear()
        """
        for var in list(self.__vars__.keys()):
            if var not in preserve:
                del self.__vars__[var]
        self._copy_class_description()

    def get(self, var, default=None, _eval=True, valid=None):
        r"""Gets an experimental variable.

        Parameters
        ----------
        var : str, unicode
            The variable to retrieve.
        default : any, optional
            A default value in case the variable doesn't exist, or `None` for
            no default value.
        _eval : bool, optional
            Determines whether the returned should be evaluated for variable
            references.
        valid : NoneType, list, optional
            A list of valid values, or `None` to allow all values.

        Examples
        --------
        >>> print('my_variable = %s' % var.get(u'my_variable'))
        >>> # Equivalent to:
        >>> print('my_variable = %s' % var.my_variable)
        >>> # But if you want to pass keyword arguments you need to use `get()`:
        >>> var.get(u'my_variable', default=u'a_default_value')
        """
        self._check_var_name(var)
        if self.__lock__ == var:
            raise OSException(f"Recursion detected! Is variable {var} defined "
                              f"in terms of itself (e.g., 'var = [var]')")
        if var in self.__vars__:
            val = self.__vars__[var]
        elif hasattr(self.__item__, var):
            warnings.warn(
                u'var %s is stored as attribute of item %s'
                % (var, self.__item__.name)
            )
            val = getattr(self.__item__, var)
        elif self.__parent__ is not None:
            val = self.__parent__.get(
                var,
                default=default,
                _eval=_eval,
                valid=valid
            )
        elif default is not None:
            val = default
        else:
            raise VariableDoesNotExist(var)
        if valid is not None and val not in valid:
            raise InvalidValue(
                f'Variable {var} should be in {valid}, not {val}')
        if _eval:
            object.__setattr__(self, u'__lock__', var)
            val = self.__item__.syntax.eval_text(val)
            object.__setattr__(self, u'__lock__', None)
        if isinstance(val, bool):
            return u'yes' if val else u'no'
        return val

    def has(self, var):
        r"""Checks if an experimental variable exists.

        Parameters
        ----------
        var : str, unicode
            The variable to check.

        Examples
        --------
        >>> if var.has(u'my_variable'):
        >>>         print(u'my_variable has been defined!')
        >>> # Equivalent to:
        >>> if u'my_variable' in var:
        >>>         print(u'my_variable has been defined!')
        """
        return self.__contains__(var)

    def set(self, var, val):
        r"""Sets and experimental variable.

        Parameters
        ----------
        var : str, unicode
            The variable to assign.
        val : any
            The value to assign.

        Examples
        --------
        >>> var.set(u'my_variable', u'my_value')
        >>> # Equivalent to
        >>> var.my_variable = u'my_value'
        """
        self._check_var_name(var)
        # The logic here is that we first try to convert to float, and if this
        # is not successful, return the orignal type. If this is succesful we
        # turn the float into an int if this doesn't result in data loss, and
        # otherwise return the float.
        try:
            val = float(val)
        except (TypeError, ValueError):
            pass
        try:
            ival = int(val)
        except (ValueError, ArithmeticError):
            # A float can always be converted to an int, except nan values,
            # which result in ValueError, or inf values, which result in an
            # OverFlowError (which is a subclass of ArithmeticError).
            pass
        else:
            if ival == val:
                val = ival
        self.__setattr__(var, val)

    def unset(self, var):
        r"""Deletes a variable.

        Parameters
        ----------
        var : str, unicode
            The variable to delete.

        Examples
        --------
        >>> var.unset(u'my_variable')
        >>> # Equivalent to:
        >>> del var.my_variable
        """
        self._check_var_name(var)
        self.__delattr__(var)

    def __iter__(self):
        r"""Implements the iterator."""
        return var_store_iterator(self)

    def __len__(self):
        r"""Returns the number of experimental variables that are stored in the
        `var_store` object.

        Returns
        -------
        int
            The number of experimental variables.
        """
        return len(self.__vars__)

    def vars(self):
        r"""Returns a list of experimental variables. Because experimental
        variables can be stored in multiple places, this list may not be
        exhaustive. That is, `u'my_var' in var` may return `True`, while
        u'my_var' is not in the list of variables as returned by this function.

        Returns
        -------
        list
            A list of variable names.

        Examples
        --------
        >>> for varname in var.vars():
        >>>         print(varname)
        """
        return sorted(list(self.__vars__.keys()))

    def items(self):
        r"""Returns a list of (variable_name, value) tuples. See `var.vars()`
        for a note about the non-exhaustiveness of this function.

        Returns
        -------
        list
            A list of (variable_name, value) tuples.

        Examples
        --------
        >>> for varname, value in var.items():
        >>>         print(varname, value)
        """
        return list(self.__vars__.items())
        
    def is_default_loggable(self, var, val):
        """Checks whether a value is loggable by default. This includes int,
        str, byes, float, bool, and None values, as well as any type that is 
        derived from numbers.Number. Variable names that start with '_' are
        not logged by default.

        Parameters
        ----------
        var : str
        val

        Returns
        -------
        bool
        """
        return not var.startswith('_') and \
            isinstance(val, (str, bytes, NoneType, Number))

    def inspect(self):
        r"""Generates a description of all experimental variables, both alive
        and hypothetical.

        Returns
        -------
        dict
            A dict where variable names are keys, and values are dicts with
            source, value, and alive keys.
        """
        d = {}
        for item_name, item in list(self.__item__.items.items()) \
                + [(u'global', self.__item__)]:
            for var, desc in item.var_info():
                if var not in d:
                    d[var] = {u'source': []}
                d[var][u'source'].append(item_name)
                d[var][u'value'] = None
                d[var][u'alive'] = False
        for var in self:
            val = self.get(var, _eval=False)
            if var not in d:
                # If a variable is not explicitly defined through var_info()
                # functions, and it's not a default-loggable type, then we
                # ignore it. This will for example ignore numpy arrays that
                # are defined in a script.
                if not self.is_default_loggable(var, val):
                    continue
                d[var] = {u'source': [u'?']}
            d[var][u'value'] = val
            d[var][u'alive'] = True
        return d

    def __reduce__(self):
        r"""Implements custom pickling. See var_store_pickle."""
        try:
            # If the parent var store is specified and is not None, then this
            # is a var store of an item, and we don't pickle it.
            if self.__parent__ is not None:
                return None
        except AttributeError:
            pass
        return (var_store_pickle, (self.inspect(), ))


class VarStorePickle(VarStore):

    r"""A read-only view of the var_store, which is used to inspect the Python
    workspace in the debug window and variable inspector. The real var_store is
    pickled using the `__reduce__()` method, transferred through the
    experiment's output_channel, and then unpickled into a `var_store_pickle`
    object.
    """
    def __init__(self, inspect):

        object.__setattr__(self, u'__inspect__', inspect)
        _vars = {}
        for var, info in inspect.items():
            if info[u'alive']:
                _vars[var] = info[u'value']
        object.__setattr__(self, u'__vars__', _vars)

    def __contains__(self, var):

        if var in self.__vars__:
            return True
        return False

    def __setattr__(self, var, val):

        raise RuntimeError('This var object is read-only')

    def get(self, var, default=None, _eval=True, valid=None):

        if var not in self:
            raise AttributeError(u'The variable %s does not exist' % var)
        return self.__vars__[var]

    def inspect(self):

        return self.__inspect__


class VarStoreIterator:

    r"""Implements an iterator over all variables in a var_store."""
    def __init__(self, var):

        self.var = var
        self.vars = var.vars()

    def __iter__(self):

        return self

    def __next__(self):

        # For Python 3
        return self.next()

    def next(self):

        if len(self.vars) == 0:
            raise StopIteration
        return self.vars.pop()


# Alias for backwards compatibility
var_store = VarStore
var_store_pickle = VarStorePickle
var_store_iterator = VarStoreIterator

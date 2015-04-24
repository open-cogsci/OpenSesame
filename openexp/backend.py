#-*- coding:utf-8 -*-

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
from libopensesame.exceptions import osexception
from functools import partial
import inspect
try:
	from yamldoc._functiondoc import FunctionDoc
	from yamldoc import inherit as docinherit
except:
	FunctionDoc = None
	docinherit = type

def configurable(fnc):

	"""
	desc:
		A decorator that makes a function configurable.

	arguments:
		fnc:	The function to make configurable.

	returns:
		A decorated configurable function.
	"""

	def inner(self, *arglist, **kwdict):

		cfg = {}
		for key, val in list(kwdict.items()):
			if key in self.configurables:
				cfg[key] = val
				del kwdict[key]
		if len(cfg) > 0:
			old_cfg = self.get_config()
			self.set_config(**cfg)
		retval = fnc(self, *arglist, **kwdict)
		if len(cfg) > 0:
			self.set_config(**old_cfg)
		return retval
	# We need to copy the docstring and argument specification, otherwise using
	# this decorator will break the documentation functions.
	if FunctionDoc is not None:
		inner.__doc__ = fnc.__doc__
		inner.__argspec__ = inspect.getargspec(fnc)
		inner._dict = FunctionDoc(fnc)._dict()
		inner.__name__ = fnc.__name__
	return inner

def getter(key, self):

	"""
	desc:
		A getter function for configurable properties.
	"""

	return self.__cfg__[key]

def setter(key, self, val):

	"""
	desc:
		A setter function for configurable properties.
	"""

	self.set_config(**{key : val})

def deller():

	"""
	desc:
		A dummy delete function for configurable properties.
	"""

	pass

def docstring(key):

	"""
	returns:
		A docstring for configurable properties.
	"""

	return """
	name:
		%(key)s
	desc:
		This is a read-and-write property. Changing the `%(key)s` property will
		affect subsequent operations.
	""" % {u'key' : key}

class backend(object):

	"""
	desc:
		A base backend that provides the configurable framework.
	"""

	docinherit = type

	def __init__(self, configurables={}, **cfg):

		"""
		desc:
			Constructor.

		keywords:
			configurables:
				desc:	A dict of configurable properties with the name of the
						property as a key, and a validation function (which can
						be None) as value.
				type:	dict

		keyword-dict:
			cfg:	The initial values for all the configurable properties.
		"""

		self.configurables = configurables
		for key in configurables:
			if hasattr(backend, key):
				continue
			fnc = property(
				partial(getter, key),
				partial(setter, key),
				deller,
				docstring(key))
			setattr(self.__class__, key, fnc)
		self.__cfg__ = {}
		_cfg = self.default_config().copy()
		_cfg.update(cfg)
		self.set_config(**_cfg)

	def assert_list_or_None(self, key, val):

		"""
		visible:	False

		desc:
			Asserts that a value is a list or None.

		arguments:
			key:	The name of the configurable.
			val:	The value of the configurable.
		"""

		if not val is None and not isinstance(val, list):
			raise osexception(
				u'%s should be a list or None, not %s' % (key, val))

	def assert_bool(self, key, val):

		"""
		visible:	False

		desc:
			Asserts that a value is bool.

		arguments:
			key:	The name of the configurable.
			val:	The value of the configurable.
		"""

		if not isinstance(val, bool) and not isinstance(val, int):
			raise osexception(
				u'%s should be True or False, not %s' % (key, val))

	def assert_numeric_or_None(self, key, val):

		"""
		visible:	False

		desc:
			Asserts that a value is float, int, or None.

		arguments:
			key:	The name of the configurable.
			val:	The value of the configurable.
		"""

		if not val is None and not isinstance(val, int) and \
			not isinstance(val, float):
			raise osexception(
				u'%s should be numeric (float or int) or None, not %s' \
				% (key, val))

	def assert_numeric(self, key, val):

		"""
		visible:	False

		desc:
			Asserts that a value is float or int.

		arguments:
			key:	The name of the configurable.
			val:	The value of the configurable.
		"""

		if not isinstance(val, int) and not isinstance(val, float):
			raise osexception(
				u'%s should be numeric (float or int), not %s' % (key, val))

	def assert_string(self, key, val):

		"""
		visible:	False

		desc:
			Asserts that a value is string or unicode.

		arguments:
			key:	The name of the configurable.
			val:	The value of the configurable.
		"""

		if not isinstance(val, basestring):
			raise osexception(
				u'%s should be string (str or unicode), not %s' % (key, val))

	def get_config(self):

		"""
		visible:	False

		returns:
			desc:	A dict that contains all configurables with names as keys
					and values as values.
			type:	dict
		"""

		return self.__cfg__.copy()

	def set_config(self, **cfg):

		"""
		visible:	False

		desc:
			Updates the configurables.

		keyword-dict:
			cfg:	The to-be-updated configurables.
		"""

		for key in cfg:
			if key not in self.configurables:
				raise osexception(u'Unknown argument: %s' % key)
			assert_fnc = self.configurables[key]
			if assert_fnc is not None:
				assert_fnc(key, cfg[key])
		self.__cfg__.update(cfg)
		# Check whether the config is valid
		for key in self.configurables:
			if key not in self.__cfg__:
				raise osexception(u'Invalid config: %s' % str(self.__cfg__))

	def default_config(self):

		"""
		visible:	False

		returns:
			desc:	The default configurable values, with names as keys and
					values as values.
			type:	dict
		"""

		return {}

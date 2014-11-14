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

from libopensesame import plugins
from libopensesame.misc import debug
from libopensesame.exceptions import osexception

class item_store(object):

	"""
	desc:
		A collection of items. It can be used as a dictionary, or as property.
	"""

	def __init__(self, experiment):

		"""
		desc:
			Constructor.

		arguments:
			experiment:
				desc:	The experiment object.
				type:	experiment.
		"""

		self.__items__ = {}
		self.experiment = experiment

	def new(self, _type, name=None, script=None):

		"""
		desc:
			Creates a new item.

		arguments:
			_type:
				desc:	The item type.
				type:	unicode

		keywords:
			name:
				desc:	The item name, or None to choose a unique name based
						on the item type.
				type:	[unicode, NoneType]
			script:
				desc:	A definition script, or None to start with a blank item.
				type:	[unicode, NoneType]

		returns:
			desc:	The newly generated item.
			type:	item
		"""

		debug.msg(u'creating %s' % _type)
		name = self.valid_name(_type, suggestion=name)
		if plugins.is_plugin(_type):
			# Load a plug-in
			try:
				item = plugins.load_plugin(_type, name,
					self.experiment, script, self.experiment.item_prefix())
			except Exception as e:
				raise osexception(
					u"Failed to load plugin '%s'" % _type, exception=e)
			self.__items__[name] = item
		else:
			# Load one of the core items
			debug.msg(u"loading core item '%s' from '%s'" % (_type,
				self.experiment.module_container()))
			item_module = __import__(u'%s.%s' % (
				self.experiment.module_container(), _type),
				fromlist=[u'dummy'])
			item_class = getattr(item_module, _type)
			item = item_class(name, self.experiment, script)
			self.__items__[name] = item
		return item

	def valid_name(self, item_type, suggestion=None):

		"""
		desc:
			Generates a unique name that is valid and resembles the desired
			name.

		arguments:
			item_type:
				desc:	The type of the item to suggest a name for.
				type:	unicode

		keywords:
			suggestion:
				desc:	The desired name, or None to choose a name based on the
						item's type.
				type:	[unicode, NoneType]

		returns:
			desc:	A unique name.
			type:	unicode
		"""

		if suggestion == None:
			name = item_type
		else:
			name = self.experiment.sanitize(suggestion, strict=True,
				allow_vars=False)
			if len(name) == 0:
				name = item_type
		while name in self:
			name = u'_' + name
		return name

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

		if not isinstance(name, basestring):
			return False
		for item in self.__items__:
			if item.lower() == name.lower():
				return True
		return False

	def __getitem__(self, name):

		for item in self.__items__:
			if item.lower() == name.lower():
				return self.__items__[item]
		raise osexception(u'No item named "%s"' % name)

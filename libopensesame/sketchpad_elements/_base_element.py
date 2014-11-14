#-*- coding:utf-8 -*-

"""
This file is part of openexp.

openexp is free software: you can redistribute it and/or modify
it under the terms of the GNU General Public License as published by
the Free Software Foundation, either version 3 of the License, or
(at your option) any later version.

openexp is distributed in the hope that it will be useful,
but WITHOUT ANY WARRANTY; without even the implied warranty of
MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
GNU General Public License for more details.

You should have received a copy of the GNU General Public License
along with openexp.  If not, see <http://www.gnu.org/licenses/>.
"""

from libopensesame import debug
from libopensesame.exceptions import osexception

class base_element(object):

	"""
	desc:
		A base class from which all sketchpad elements are derived.
	"""


	def __init__(self, sketchpad, string, defaults=[]):

		"""
		desc:
			Constructor.

		arguments:
			sketchpad:		A sketchpad object.
			string:			A definition string.

		keywords:
			defaults:		A list with (name, default_value) tuples for all
							keywords.
		"""

		self._type = self.__class__.__name__
		# These keywords provide compatibility with older versions of
		# OpenSesame. `only_keywords` specifies whether all parameters should be
		# written as keywords, which will prevent < 2.9.0 from reading the
		# sketchpad elements. If not, keywords with a None default will be
		# written value-only style. `fix_coordinates` specifies whether
		# coordinates should be translated to top-left = 0,0.
		self.only_keywords = False
		self.fix_coordinates = True
		debug.msg(self._type)
		self.defaults = defaults + [
			(u'z_index', 0),
			(u'show_if', u'always')
			]
		self.sketchpad = sketchpad
		self.from_string(string)

	@property
	def canvas(self): return self.sketchpad.canvas

	@property
	def get(self): return self.sketchpad.get

	@property
	def get_file(self): return self.sketchpad.experiment.get_file

	@property
	def name(self): return self.sketchpad.name

	@property
	def split(self): return self.sketchpad.split

	@property
	def experiment(self): return self.sketchpad.experiment

	@property
	def z_index(self):

		"""
		desc:
			Determines the drawing order of the elements. Elements with a
			higher z-index are drawn first, so they are at the bottom of the
			stack.
		returns:
			A z-index.
		"""

		return self.properties[u'z_index']

	def draw(self):

		"""
		desc:
			Draws the element to the canvas of the sketchpad.
		"""

		pass

	def from_string(self, string):

		"""
		desc:
			Parse a definition string for the element.

		arguments:
			string:		A definition string.
		"""

		l  = self.split(string)
		if len(l) < 2 or l[0] != u'draw' or l[1] != self._type:
			raise osexception(u'Invalid sketchpad-element definition: \'%s\'' \
				% string)
		# First load the default values
		self.properties = {}
		for var, val in self.defaults:
			self.properties[var] = val
		# Parse the specified values
		keyword_nr = 0
		vars_parsed = []
		for keyword in l[2:]:
			i = keyword.find(u'=')
			if i >= 0:
				var = keyword[:i]
				# If the keyword is not known, we assumed that it's not a
				# keyword at all, but part of the value. This is mostly a hack
				# necessary to maintain backwards compatibility for the texline
				# element, which may have strings of text that look like keyword
				# -value specifications, but are really just text, like:
				# "Accuracy = [acc] ms"
				if self.valid_keyword(var):
					val = keyword[i+1:]
				else:
					debug.msg(
						u'Invalid keyword "%s", assuming "%s"' \
						% (var, self.defaults[keyword_nr][0]))
					var = self.defaults[keyword_nr][0]
					val = keyword
			else:
				var = self.defaults[keyword_nr][0]
				val = keyword
			if var in vars_parsed:
				raise osexception(
					(u'The keyword \'%s\' has been specified multiple times in '
					u'sketchpad element \'%s\' in item \'%s\'') % (var,
					self._type, self.name))
			vars_parsed.append(var)
			self.properties[var] = self.sketchpad.auto_type(val)
			keyword_nr += 1
		# Check if all values that need to be specified have indeed been
		# specified.
		for var, val in self.properties.items():
			if val == None:
				raise osexception(
					(u'Required keyword \'%s\' has not been specified in '
					u'sketchpad element \'%s\' in item \'%s\'') % (var,
					self._type, self.name))
		# Check if no non-existing keywords have been specified
		for var in self.properties.keys():
			valid = False
			for _var, _val in self.defaults:
				if _var == var:
					valid = True
					break
			if not valid:
				raise osexception(
					(u'The keyword \'%s\' is not applicable to '
					u'sketchpad element \'%s\' in item \'%s\'') % (var,
					self._type, self.name))

	def valid_keyword(self, keyword):

		"""
		desc:
			Checks whether a particular keyword is valid for this element.

		arguments:
			keyword:	A keyword.
			type:		unicode

		returns:
			desc:		True if keyword is valid.
			type:		bool
		"""

		for var, val in self.defaults:
			if var == keyword:
				return True
		return False

	def escape(self, val, quote=True):

		"""
		desc:
			Escapes and optionally quotes a value so that it can be safely
			inserted into a definition string. Everything except unicode is
			returned as is.

		arguments:
			val:
				desc:	The value to escape.
				type:	[unicode, float, int]
			quote:
				desc:	Indicates whether unicode strings should be quoted
						with double quotes.
				type:	bool

		returns:
			desc:		A value that can be safely inserted into a definiton
						string.
			type:		[unicode, int, float]
		"""

		if not isinstance(val, unicode):
			return val
		val = val.replace(u'\\', u'\\\\')
		val = val.replace(u'"', u'\\"')
		if quote:
			val = u'"%s"' % val
		return val

	def to_string(self):

		"""
		desc:
			Generates a string representation of the element.

		returns:
			desc:	A string representation.
			type:	unicode
		"""

		s = u'draw %s' % self._type
		for var, default in self.defaults:
			val = self.properties[var]
			val = self.escape(val)
			if default == None and not self.only_keywords:
				s += u' %s' % val
			else:
				s += u' %s=%s' % (var, val)
		return s

	def eval_properties(self):

		"""
		desc:
			Evaluates all properties.

		returns:
			A new property dictionary.
		"""

		properties = {}
		xc = self.get(u'width')/2
		yc = self.get(u'height')/2
		for var, val in self.properties.items():
			if var == u'text':
				round_float = True
			else:
				round_float = False
			val = self.sketchpad.eval_text(val, round_float=round_float)
			if self.fix_coordinates and type(val) in (int, float):
				if var in [u'x', u'x1', u'x2']:
					val += xc
				if var in [u'y', u'y1', u'y2']:
					val += yc
			properties[var] = val
		return properties

	def is_shown(self):

		"""
		desc:
			Determines whether the element should be shown, based on the
			show-if statement.

		returns:
			desc:	A bool indicating whether the element should be shown.
			type:	bool
		"""

		return eval(self.sketchpad.compile_cond(self.properties[u'show_if']))


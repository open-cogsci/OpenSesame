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

import re
from libopensesame import item
from openexp import canvas
from libopensesame.exceptions import osexception

_globals = {}

class inline_script(item.item):

	"""Allows users to use Python code in their experiments"""

	description = u'Executes Python code'

	def reset(self):

		"""See item."""

		self._prepare = u''
		self._run = u''
		self._var_info = None

	def copy_sketchpad(self, sketchpad_name):

		"""<DOC>
		Creates a canvas that is a copy from the canvas of a sketchpad item.

		Arguments:
		sketchpad_name	--	The name of the sketchpad.

		Returns:
		An openexp canvas.

		Example:
		>>> my_canvas = self.copy_sketchpad('my_sketchpad')
		</DOC>"""

		c = self.offline_canvas()
		c.copy(self.experiment.items[sketchpad_name].canvas)
		return c

	def offline_canvas(self, auto_prepare=True):

		"""<DOC>
		Creates an empty canvas.

		Keyword arguments:
		auto_prepare 	--	See canvas documentation. (default=True)

		Returns:
		An openexp canvas.

		Example:
		>>> my_canvas = self.offline_canvas()
		</DOC>"""

		return canvas.canvas(self.experiment, self.get(u'background'), \
			self.get(u'foreground'), auto_prepare=auto_prepare)

	def prepare(self):

		"""<DOC>
		Executes the prepare script. The code that you enter in the 'prepare' #
		tab of an inline_script item in the GUI is used as a body for this #
		function.
		</DOC>"""

		global _globals, _locals

		item.item.prepare(self)
		if self.experiment.transparent_variables == u'yes':
			self.start_transparency()
		# Convenience variables need to be registered as globals. By specifying
		# a __name__, the script will function as a module, so that e.g. import
		# statements do not suffer from locality.
		if u'exp' not in _globals:
			_globals[u'exp'] = self.experiment
			_globals[u'win'] = self.experiment.window
			_globals[u'__name__'] = u'myname'
		# 'self' must always be registered, otherwise we get confusions between
		# the various inline_script items.
		_globals[u'self'] = self
		# Prepend source encoding (PEP 0263) and encode scripts. This is
		# necessary, because the exec statement doesn't take kindly to Unicode.
		_prepare = (u'#-*- coding:%s -*-\n' % self.encoding + self._prepare) \
			.encode(self.encoding)
		_run = (u'#-*- coding:%s -*-\n' % self.encoding + self._run) \
			.encode(self.encoding)
		# Compile prepare script
		try:
			self.cprepare = compile(_prepare, u'<string>', u'exec')
		except Exception as e:
			raise osexception(u'Failed to compile inline script', item= \
				self.name, phase=u'prepare', exception=e)
		# Compile run script
		try:
			self.crun = compile(_run, u'<string>', u'exec')
		except Exception as e:
			raise osexception(u'Failed to compile inline script', item= \
				self.name, phase=u'run', exception=e)
		# Run prepare script
		try:
			exec(self.cprepare, _globals)
		except Exception as e:
			raise osexception(u'Error while executing inline script', item= \
				self.name, phase=u'prepare', exception=e)
		if self.experiment.transparent_variables == u'yes':
			self.end_transparency()

	def run(self):

		"""<DOC>
		Executes the run script. The code that you enter in the 'run' tab of #
		an inline_script item in the GUI is used as a body for this function.
		</DOC>"""

		global _globals, _locals
		self.set_item_onset()
		# 'self' must always be registered, otherwise we get confusions between
		# the various inline_script items.
		_globals[u'self'] = self
		if self.experiment.transparent_variables == u'yes':
			self.start_transparency()
		try:
			exec(self.crun, _globals)
		except Exception as e:
			raise osexception(u'Error while executing inline script', item= \
				self.name, phase=u'run', exception=e)
		if self.experiment.transparent_variables == u'yes':
			self.end_transparency()

	def var_info(self):

		"""
		Gives a list of dictionaries with variable descriptions.

		Returns:
		A list of (variable, description) tuples.
		"""

		# Don't parse the script if it isn't necessary, since
		# regular expressions are a bit slow
		if self._var_info != None:
			return self._var_info

		l = item.item.var_info(self)

		m = re.findall( \
			u"self.experiment.set\(\"(\w+)\"(\s*),(\s*)(\"*)([^\"\)]*)(\"*)", \
			self._prepare + self._run) \
			+ re.findall( \
			u"self.experiment.set\('(\w+)'(\s*),(\s*)('*)([^'\)]*)('*)", \
			self._prepare + self._run) \
			+ re.findall( \
			u"exp.set\(\"(\w+)\"(\s*),(\s*)(\"*)([^\"\)]*)(\"*)", \
			self._prepare + self._run) \
			+ re.findall( \
			u"exp.set\('(\w+)'(\s*),(\s*)('*)([^'\)]*)('*)", \
			self._prepare + self._run)

		for var, s1, s2, q1, val, q2 in m:
			if q1 != u'"':
				val = u'[Set to \'%s\']' % val
			l.append( (var, val) )
		self._var_info = l

		return l

	def start_transparency(self):

		"""
		Registers all experiment variables in the locals dictionary. This allows
		the user to interact with the experimental variables without needing
		to call `exp.set()`.
		"""

		global _globals
		for var, val in self.experiment.var_info():
			_globals[var] = val

	def end_transparency(self):

		"""
		Sets all local variables, so that the user doesn't have explicitly have
		to call `exp.set()`.
		"""

		global _globals
		for var, val in _globals.items():
			if isinstance(val, basestring) or isinstance(val, float) or \
				isinstance(val, int):
				self.experiment.set(var, val)

def restore_state():

	"""Restores the system state."""

	global _globals
	_globals = {}

def save_state():

	"""Saves the system state."""

	# Currently does nothing.
	pass

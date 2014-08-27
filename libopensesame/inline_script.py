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

class inline_script(item.item):

	"""
	desc: |
		Allows users to use Python code in their experiments.

		When you are using the inline_script item, you are essentially writing
		the body of two functions (`prepare` and `run`) of an `inline_script`
		object. The `inline_script` object has many more functions which you can
		use, and these are listed below. To use these functions, you use the
		`self.[function_name]` notation.

		__Important note:__

		All inline_script items share the same workspace. This means that
		variables that are created in one inline_script are available in
		another inline_script. Similarly, modules that are imported in one
		inline_script are available in all other inline_scripts.

		__Example:__

		~~~ {.python}
		subject_nr = self.get("subject_nr")
		~~~

		__Example:__

		{% highlight python %}
		self.sleep(1000)
		{% endhighlight %}

		__Function list:__

		%--
		toc:
			mindepth: 2
			maxdepth: 2
		--%
	"""

	description = u'Executes Python code'

	def reset(self):

		"""See item."""

		self._prepare = u''
		self._run = u''
		self._var_info = None

	def copy_sketchpad(self, sketchpad_name):

		"""
		desc:
			Creates a canvas that is a copy from the canvas of a sketchpad item.

		arguments:
			sketchpad_name:
				desc:	The name of the sketchpad.
				type:	[str, unicode]

		returns:
			desc:	A canvas.
			type:	canvas

		example: |
			my_canvas = self.copy_sketchpad('my_sketchpad')
		"""

		c = self.offline_canvas()
		c.copy(self.experiment.items[sketchpad_name].canvas)
		return c

	def offline_canvas(self, auto_prepare=True):

		"""
		desc:
			Creates an empty canvas.

		keywords:
			auto_prepare:
				desc:	See `openexp.canvas.__init__`.
				type:	bool

		returns:
			desc:	A canvas.
			type:	canvas

		example: |
			my_canvas = self.offline_canvas()
		"""

		return canvas.canvas(self.experiment, self.get(u'background'), \
			self.get(u'foreground'), auto_prepare=auto_prepare)

	def prepare(self):

		"""
		desc:
			Executes the prepare script. The code that you enter in the
			'prepare' tab of an inline_script item in the GUI is used as a body
			for this function.
		"""

		item.item.prepare(self)
		if self.experiment.transparent_variables == u'yes':
			self.start_transparency()
		# 'self' must always be registered, otherwise we get confusions between
		# the various inline_script items.
		self.experiment.python_workspace[u'self'] = self
		# Compile prepare script
		try:
			self.cprepare = self.experiment.python_workspace._compile(
				self._prepare)
		except Exception as e:
			raise osexception(u'Failed to compile inline script',
				item=self.name, phase=u'prepare', exception=e)
		# Compile run script
		try:
			self.crun = self.experiment.python_workspace._compile(self._run)
		except Exception as e:
			raise osexception(u'Failed to compile inline script',
				item=self.name, phase=u'run', exception=e)
		# Run prepare script
		try:
			self.experiment.python_workspace._exec(self.cprepare)
		except Exception as e:
			raise osexception(u'Error while executing inline script',
				item=self.name, phase=u'prepare', exception=e)
		if self.experiment.transparent_variables == u'yes':
			self.end_transparency()

	def run(self):

		"""
		desc:
			Executes the run script. The code that you enter in the 'run' tab of
			an inline_script item in the GUI is used as a body for this
			function.
		"""

		self.set_item_onset()
		# 'self' must always be registered, otherwise we get confusions between
		# the various inline_script items.
		self.experiment.python_workspace[u'self'] = self
		if self.experiment.transparent_variables == u'yes':
			self.start_transparency()
		try:
			self.experiment.python_workspace._exec(self.crun)
		except Exception as e:
			raise osexception(u'Error while executing inline script',
				item=self.name, phase=u'run', exception=e)
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
		Registers all experimental variables. This allows
		the user to interact with the experimental variables without needing
		to call `exp.set()`.
		"""

		for var, val in self.experiment.var_info():
			self.experiment.python_workspace[var] = val

	def end_transparency(self):

		"""
		Sets all global variables, so that the user doesn't have explicitly have
		to call `exp.set()`.
		"""

		for var, val in self.experiment.python_workspace.items():
			if isinstance(val, basestring) or isinstance(val, float) or \
				isinstance(val, int):
				self.experiment.set(var, val)

def restore_state():

	"""Restores the system state."""

	# Currently does nothing.
	pass

def save_state():

	"""Saves the system state."""

	# Currently does nothing.
	pass

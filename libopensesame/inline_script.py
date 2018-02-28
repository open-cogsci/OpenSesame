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
import warnings
import re
from libopensesame import item
from openexp import canvas
from libopensesame.exceptions import osexception, AbortCoroutines

extract_old_style = re.compile(
	r'(self.experiment.set|exp.set|var.set)\(u?[\'"]([_a-zA-Z]+[_a-zA-Z0-9]*)[\'"]')
extract_new_style = re.compile(r'var.([_a-zA-Z]+[_a-zA-Z0-9]*)\s*=')

class inline_script(item.item):

	"""
	desc: |
		Allows users to use Python code in their experiments.
	"""

	description = u'Executes Python code'

	def reset(self):

		"""See item."""

		self.var._prepare = u''
		self.var._run = u''
		self._var_info = None

	def prepare(self):

		"""
		desc:
			Executes the prepare script. The code that you enter in the
			'prepare' tab of an inline_script item in the GUI is used as a body
			for this function.
		"""

		item.item.prepare(self)
		# 'self' must always be registered, otherwise we get confusions between
		# the various inline_script items.
		self.experiment.python_workspace[u'self'] = self
		# Compile prepare script
		try:
			self.cprepare = self.experiment.python_workspace._compile(
				self.var.get(u'_prepare', _eval=False))
		except Exception as e:
			raise osexception(u'Failed to compile inline script',
				line_offset=-1, item=self.name, phase=u'prepare', exception=e)
		# Compile run script
		try:
			self.crun = self.experiment.python_workspace._compile(
				self.var.get(u'_run', _eval=False))
		except Exception as e:
			raise osexception(u'Failed to compile inline script',
				line_offset=-1, item=self.name, phase=u'run', exception=e)
		# Run prepare script
		try:
			self.experiment.python_workspace._exec(self.cprepare)
		except Exception as e:
			raise osexception(u'Error while executing inline script',
				line_offset=-1, item=self.name, phase=u'prepare', exception=e)

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
		try:
			self.experiment.python_workspace._exec(self.crun)
		except Exception as e:
			raise osexception(
				u'Error while executing inline script',
				line_offset=-1, item=self.name, phase=u'run', exception=e
			)

	def coroutine(self, coroutines):

		"""See coroutines plug-in"""

		yield
		self.set_item_onset()
		while True:
			self.experiment.python_workspace[u'self'] = self
			try:
				self.experiment.python_workspace._exec(self.crun)
			except AbortCoroutines as e:
				# If the inline_script is part of a coroutines, this signals
				# that the coroutines should be aborted, so we don't wrap it
				# into an osexception.
				raise
			except Exception as e:
				raise osexception(
					u'Error while executing inline script',
					line_offset=-1, item=self.name, phase=u'run', exception=e
				)
			yield

	def var_info(self):

		"""
		desc:
			Gives a list of dictionaries with variable descriptions.

		returns:
			A list of (variable, description) tuples.
		"""

		l = item.item.var_info(self)
		script = (
			self.var.get(u'_prepare', _eval=False, default=u'')
			+ self.var.get(u'_run', _eval=False, default=u'')
		)
		for dummy, var in re.findall(extract_old_style, script):
			l.append( (var, None) )
		for var in re.findall(extract_new_style, script):
			l.append( (var, None) )
		return l

	def copy_sketchpad(self, sketchpad_name):

		"""
		desc:
			Deprecated function.
		"""

		warnings.warn(u'self.copy_sketchpad() is deprecated. '
			'Use copy_sketchpad() instead.',
			DeprecationWarning)
		c = self.offline_canvas()
		c.copy(self.experiment.items[sketchpad_name].canvas)
		return c

	def offline_canvas(self, auto_prepare=True):

		"""
		desc:
			Deprecated function.
		"""

		warnings.warn(u'self.offline_canvas() is deprecated. '
			'Use canvas() instead.', DeprecationWarning)
		return canvas.canvas(self.experiment, auto_prepare=auto_prepare,
			background_color=self.var.background, color=self.var.foreground)

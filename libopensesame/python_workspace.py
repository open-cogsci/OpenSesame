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
import libopensesame.python_workspace_api as api
from libopensesame.exceptions import AbortCoroutines
import types
from openexp.canvas_elements import ElementFactory
from libopensesame.widgets.widget_factory import WidgetFactory
from libopensesame.base_python_workspace import base_python_workspace


class python_workspace(base_python_workspace):

	"""
	desc:
		Provides a worspace in which Python scripts can be executed. Generally,
		each experiment has one python_workspace object, which is used for all
		inline_script items, and other items that make allow users to execute
		Python code.

		The python_workspace object is dictionary-like, and allows you to get
		and set global variables in a dictionary way, e.g.:

			self.experiment.python_workspace[u'my_var'] = 10
	"""

	def __init__(self, experiment):

		"""
		desc:
			Constructor.

		arguments:
			experiment:
				desc:	The experiment object.
				type:	experiment
		"""

		base_python_workspace.__init__(self, experiment)
		api.experiment = experiment

	def init_globals(self):

		"""
		desc:
			Initialize the global workspace.
		"""

		# By setting the __name__ global, the workspace will operate as a
		# module, so that e.g. import statements don't suffer from locality.
		self._globals.update({
			u'__name__'			: u'python_workspace',
			u'exp'				: self.experiment,
			u'var'				: self.experiment.var,
			u'pool'				: self.experiment.pool,
			u'items'			: self.experiment.items,
			u'clock'			: self.experiment._clock,
			u'log'				: self.experiment._log,
			u'responses'		: self.experiment._responses,
			u'data_files'		: self.experiment.data_files,
			u'AbortCoroutines'	: AbortCoroutines,
		})
		# All functions from the api modules are also loaded into the globals.
		# This way they can be called directly by name.
		api.set_aliases()
		for name, obj in api.__dict__.items():
			if self._is_api_object(obj):
				self._globals[name] = obj

	def _is_api_object(self, obj):

		if isinstance(obj, types.FunctionType):
			return True
		if isinstance(obj, type) and issubclass(
			obj, (WidgetFactory, ElementFactory)):
				return True
		return False

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
import fnmatch
import subprocess
from libopensesame.oslogging import oslogger
from libqtopensesame.misc.config import cfg
from libqtopensesame.extensions import BaseExtension


class FileHandler(BaseExtension):

	"""
	desc:
		Opens files in external applications.
	"""

	def event_startup(self):

		# First make sure that the bindings config evaluates to a dict
		try:
			self._bindings = safe_yaml_load(cfg.external_bindings)
			if not isinstance(self._bindings, dict):
				raise TypeError('YAML is not a dict')
		except Exception as e:
			oslogger.error('invalid YAML in {}'.format(cfg.external_bindings))
			self._bindings = {}
		# And then take only those entries where both the pattern and the
		# command are strings
		self._bindings = {
			pattern: cmd
			for pattern, cmd in self._bindings.items()
			if isinstance(pattern, basestring) and isinstance(cmd, basestring)
		}

	def _is_experiment(self, path):

		path = path.lower()
		return (
			path.endswith(u'.osexp') or
			path.endswith(u'.opensesame') or
			path.endswith(u'.opensesame.tar.gz')
		)

	def provide_file_handler(self, path):

		if not isinstance(path, basestring) or self._is_experiment(path):
			return
		for pattern, cmd in self._bindings.items():
			if fnmatch.fnmatch(path, pattern):
				oslogger.debug('providing file handler for {}'.format(path))
				return self._file_handler
		oslogger.debug('not providing file handler for {}'.format(path))

	def _file_handler(self, path):

		for pattern, cmd in self._bindings.items():
			if fnmatch.fnmatch(path, pattern):
				try:
					subprocess.Popen([cmd, path])
				except Exception as e:
					self.notify(_(
						u'Failed to open file. '
						u'See debug window for error message.'
					))
					self.console.write(e)


# PEP8 alias
file_handler = FileHandler

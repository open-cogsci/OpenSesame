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
from openexp._clock.clock import Clock
from psychopy import core


class Psycho(Clock):

	"""
	desc:
		For docstrings, see openexp._clock.clock.
	"""

	def time(self):

		return 1000.*core.getTime()

	def sleep(self, ms):

		core.wait(.001*ms)


# Non PEP-8 alias for backwards compatibility
psycho = Psycho

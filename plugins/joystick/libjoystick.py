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
from libopensesame import plugins

def libjoystick(experiment, **kwargs):

	"""
	A factory that returns a back-end specific joystick module.

	Arguments:
	experiment		--	The experiment object.

	Keyword arguments:
	**kwargs		--	A keyword-argument dictionary.
	"""

	if experiment.var.get(u'canvas_backend') == u'psycho':
		raise osexception(
			u'The joystick plug-in does not yet support the psycho back-end')
	backend = u'legacy'
	cls = plugins.load_cls(__file__, cls=backend, mod=backend,
		pkg=u'_libjoystick')
	return cls(experiment, **kwargs)

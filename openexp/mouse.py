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

class mouse:

	"""
	Based on the mouse_backend variable in the experiment, this class
	morphs into the appropriate keyboard backend class.
	"""

	def __init__(self, experiment, buttonlist=None, timeout=None, visible=False):
	
		backend = experiment.mouse_backend		
		debug.msg('morphing into %s' % backend)
		mod = __import__('openexp._mouse.%s' % backend, fromlist=['dummy'])			
		cls = getattr(mod, backend)
		self.__class__ = cls
		cls.__init__(self, experiment, buttonlist, timeout, visible)
		

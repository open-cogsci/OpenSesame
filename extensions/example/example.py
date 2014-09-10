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

from libopensesame import debug
from libqtopensesame.extensions import base_extension

class example(base_extension):

	"""
	desc:
		An example extension.
	"""
	
	def activate(self):

		"""
		desc:
			Is called when the extension is activated through the menu/ toolbar
			action.
		"""

		debug.msg(u'Example extension activated')
		int('x') # Triggers exception, which we be caught by OpenSesame

	# Below is a list of event handlers, which you can implement to have your
	# extension react to specific events.

	def event_startup(self):

		debug.msg(u'Event fired: startup')

	def event_run_experiment(self, fullscreen):

		debug.msg(u'Event fired: run_experiment(fullscreen=%s)' % fullscreen)

	def event_end_experiment(self):

		debug.msg(u'Event fired: end_experiment')

	def event_save_experiment(self, path):
		
		debug.msg(u'Event fired: save_experiment(path=%s)' % path)

	def event_open_experiment(self, path):

		debug.msg(u'Event fired: open_experiment(path=%s)' % path)

	def event_close(self):

		debug.msg(u'Event fired: close')

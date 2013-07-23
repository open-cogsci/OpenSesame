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

class base_runner(object):
	
	"""
	A runner implements a specific way to execute an OpenSesame experiment from
	within the GUI. The base_runner is an abstract runner that is inherited by
	actual runners.
	"""
	
	def __init__(self, main_window, experiment):
		
		"""
		Constructor.
		
		Arguments:
		main_window		--	An QtGui.QMainWindow object. Typically this will be
							the qtopensesame object.
		experiment		--	An experiment object.
		"""		
		
		self.experiment = experiment
		self.main_window = main_window

	def execute(self):
		
		"""
		Executes the experiments. This function should be transparent and leave
		no mess to clean up for the GUI.
		
		Returns:
		None if the experiment finished cleanly, or an Exception (any kind) if
		an exception occurred.
		"""
		
		pass

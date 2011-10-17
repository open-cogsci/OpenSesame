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

from libopensesame import item
from libqtopensesame import qtplugin
from PyQt4 import QtGui, QtCore

class reset_feedback(item.item):

	"""A very simple plug-in to reset feedback variables"""

	def __init__(self, name, experiment, string=None):

		"""
		Constructor
		
		Arguments:
		name -- item name
		experiment -- experiment instance
		
		Keywords arguments:
		string -- definition string (default=None)
		"""

		# The item_typeshould match the name of the module
		self.item_type = "reset_feedback"

		# Provide a short accurate description of the items functionality
		self.description = "Resets the feedback variables, such as 'avg_rt' and 'acc'"

		# The parent handles the rest of the contruction
		item.item.__init__(self, name, experiment, string)

	def prepare(self):

		"""Empty prepare phase"""

		item.item.prepare(self)
		return True

	def run(self):

		"""Reset the feedback variables"""
		
		self.experiment.reset_feedback()
		return True

class qtreset_feedback(reset_feedback, qtplugin.qtplugin):

	"""GUI part of the plug-in"""

	def __init__(self, name, experiment, string = None):

		"""
		Constructor
		
		Arguments:
		name -- item name
		experiment -- experiment instance
		
		Keywords arguments:
		string -- definition string (default=None)
		"""
		
		# Pass the word on to the parents
		reset_feedback.__init__(self, name, experiment, string)
		qtplugin.qtplugin.__init__(self, __file__)

	def init_edit_widget(self):

		"""Initialize controls"""

		# Lock the widget until we're doing creating it
		self.lock = True

		# Pass the word on to the parent
		qtplugin.qtplugin.init_edit_widget(self, False)

		self.add_text("This plug-in has no settings")
		self.edit_vbox.addStretch()

		# Unlock
		self.lock = True

	def apply_edit_changes(self):

		"""Apply controls"""

		# Abort if the parent reports failure of if the controls are locked
		if not qtplugin.qtplugin.apply_edit_changes(self, False) or self.lock:
			return False

		# Refresh the main window, so that changes become visible everywhere
		self.experiment.main_window.refresh(self.name)

		# Report success
		return True

	def edit_widget(self):

		"""Update controls"""

		# Lock the controls, otherwise a recursive loop might aris
		# in which updating the controls causes the variables to be
		# updated, which causes the controls to be updated, etc...
		self.lock = True

		# Let the parent handle everything
		qtplugin.qtplugin.edit_widget(self)

		# Unlock
		self.lock = False

		# Return the _edit_widget
		return self._edit_widget


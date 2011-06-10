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

from libopensesame import item, exceptions
from libqtopensesame import qtplugin
import openexp.canvas
import os.path
import imp
from PyQt4 import QtGui, QtCore

class eyelink_drift_correct(item.item):

	"""
	This class (the class with the same name as the module)
	handles the basic functionality of the item. It does
	not deal with GUI stuff.
	"""

	def __init__(self, name, experiment, string = None):

		"""
		Constructor
		"""

		# The item_typeshould match the name of the module
		self.item_type = "eyelink_drift_correct"

		self._mode_manual = "Manual (spacebar triggered)"
		self._mode_auto = "Automatic (fixation triggered)"
		self.mode = self._mode_manual

		self.xpos = 0
		self.ypos = 0

		# Provide a short accurate description of the items functionality
		self.description = "Drift correction plugin for the Eyelink series of eye trackers (SR-Research)"

		# The parent handles the rest of the contruction
		item.item.__init__(self, name, experiment, string)

	def prepare(self):

		"""
		Prepare the item. In this case this means drawing a fixation
		dot to an offline canvas.
		"""

		# Pass the word on to the parent
		item.item.prepare(self)

		# Create an eyelink instance if it doesn't exist yet. Libeyelink is
		# dynamically loaded
		if not hasattr(self.experiment, "eyelink"):
			raise exceptions.runtime_error("Please connect to the eyelink using the the eyelink_calibrate plugin before using any other eyelink plugins")

		# Report success
		return True

	def run(self):

		"""
		Run the item. In this case this means putting the offline canvas
		to the display and waiting for the specified duration.
		"""

		self.set_item_onset()

		try:
			x = int(self.get("xpos"))
			y = int(self.get("ypos"))
		except:
			raise exceptions.runtime_error("Please use numeric values for the coordinates in eyelink_drift_correct item '%s'" % self.name)

		if not self.has("coordinates") or self.get("coordinates") == "relative":
			x += self.get("width") / 2
			y += self.get("height") / 2

		# Draw a fixation dot
		c = openexp.canvas.canvas(self.experiment, self.get("background"), self.get("foreground"))
		c.set_penwidth(3)
		c.line(x - 5, y, x + 5, y)
		c.line(x, y - 5, x, y + 5)
		c.show()
		# Do drift correction
		while not self.experiment.eyelink.drift_correction( (x, y), self.get("mode") == self._mode_auto):
			self.experiment.eyelink.calibrate()
			c.show()

		# Report success
		return True

class qteyelink_drift_correct(eyelink_drift_correct, qtplugin.qtplugin):

	"""
	This class (the class named qt[name of module] handles
	the GUI part of the plugin. For more information about
	GUI programming using PyQt4, see:
	<http://www.riverbankcomputing.co.uk/static/Docs/PyQt4/html/classes.html>
	"""

	def __init__(self, name, experiment, string = None):

		"""
		Constructor
		"""

		# Pass the word on to the parents
		eyelink_drift_correct.__init__(self, name, experiment, string)
		qtplugin.qtplugin.__init__(self, __file__)

	def init_edit_widget(self):

		"""
		This function creates the controls for the edit
		widget.
		"""

		# Lock the widget until we're doing creating it
		self.lock = True

		# Pass the word on to the parent
		qtplugin.qtplugin.init_edit_widget(self, False)
		self.add_combobox_control("mode", "Mode", [self._mode_manual, self._mode_auto], tooltip = "Indicates if drift correction should be manual or automatic")

		if self.has("coordinates") and self.get("coordinates") == "absolute":
			self.add_line_edit_control("xpos", "X coordinate", self.get("width") / 2)
			self.add_line_edit_control("ypos", "Y coordinate", self.get("height") / 2)
		else:
			self.add_line_edit_control("xpos", "X coordinate", 0)
			self.add_line_edit_control("ypos", "Y coordinate", 0)

		# Add a stretch to the edit_vbox, so that the controls do not
		# stretch to the bottom of the window.
		self.edit_vbox.addStretch()

		# Unlock
		self.lock = True

	def apply_edit_changes(self):

		"""
		Set the variables based on the controls
		"""

		# Abort if the parent reports failure of if the controls are locked
		if not qtplugin.qtplugin.apply_edit_changes(self, False) or self.lock:
			return False

		# Refresh the main window, so that changes become visible everywhere
		self.experiment.main_window.refresh(self.name)

		# Report success
		return True

	def edit_widget(self):

		"""
		Set the controls based on the variables
		"""

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


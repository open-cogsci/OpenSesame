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

from libopensesame import item, generic_response
from libqtopensesame import qtplugin
import openexp.canvas
import os.path
from PyQt4 import QtGui, QtCore

class fixation_dot(item.item, generic_response.generic_response):

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
		self.item_type = "fixation_dot"

		# Provide a short accurate description of the items functionality
		self.description = "Presents a central fixation dot with a choice of various styles"

		# Set some item-specific variables
		self.style = "default"
		self.duration = 1000
		self.penwidth = 3
		self.x = 0
		self.y = 0

		# The parent handles the rest of the contruction
		item.item.__init__(self, name, experiment, string)

	def prepare(self):

		"""
		Prepare the item. In this case this means drawing a fixation
		dot to an offline canvas.
		"""

		# Pass the word on to the parent
		item.item.prepare(self)

		# Create an offline canvas
		self.c = openexp.canvas.canvas(self.experiment, self.get("background"), self.get("foreground"))

		# Set the coordinates
		self._x = self.get("x")
		self._y = self.get("y")
		if self.get("coordinates") == "relative":
			self._x += self.c.xcenter()
			self._y += self.c.ycenter()

		# Draw the fixation dot
		self.c.set_penwidth(self.get("penwidth"))
		if self.style == "default":
			self.c.fixdot(self._x, self._y)
		elif self.style == "filled":
			self.c.ellipse(self._x - 10, self._y - 10, 20, 20, True)
		elif self.style == "filled-small":
			self.c.ellipse(self._x - 5, self._y - 5, 10, 10, True)
		elif self.style == "empty":
			self.c.ellipse(self._x - 10, self._y - 10, 20, 20, False)
		elif self.style == "empty-small":
			self.c.ellipse(self._x - 5, self._y - 5, 10, 10, False)
		elif self.style == "cross":
			self.c.line(self._x - 10, self._y, self._x + 10, self._y)
			self.c.line(self._x, self._y - 10, self._x, self._y + 10)
		elif self.style == "cross-small":
			self.c.line(self._x - 5, self._y, self._x + 5, self._y)
			self.c.line(self._x, self._y - 5, self._x, self._y + 5)

		generic_response.generic_response.prepare(self)		

		# Report success
		return True

	def run(self):

		"""
		Run the item. In this case this means putting the offline canvas
		to the display and waiting for the specified duration.
		"""

		self.set_item_onset(self.c.show())
		self.set_sri()
		self.process_response()
		return True

class qtfixation_dot(fixation_dot, qtplugin.qtplugin):

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
		fixation_dot.__init__(self, name, experiment, string)
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

		# Create the controls
		#
		# A number of convenience functions are available which
		# automatically create controls, which are also automatically
		# updated and applied. If you set the varname to None, the
		# controls will be created, but not automatically updated
		# and applied.
		#
		# qtplugin.add_combobox_control(varname, label, list_of_options)
		# - creates a QComboBox
		# qtplugin.add_line_edit_control(varname, label)
		# - creates a QLineEdit
		# qtplugin.add_spinbox_control(varname, label, min, max, suffix = suffix, prefix = prefix)

		self.add_combobox_control("style", "Style", ["default", "filled", "filled-small", "empty", "empty-small", "cross", "cross-small"], tooltip = "Style of the fixation dot")
		self.add_spinbox_control("penwidth", "Pen width", 1, 100, suffix = "px", tooltip = "Pen width")
		self.add_line_edit_control("duration", "Duration", tooltip = "Expecting a value in milliseconds, 'keypress' or 'mouseclick'")
		self.add_line_edit_control("foreground", "Foreground", tooltip = "Expecting a colorname (e.g., 'blue') or an HTML color (e.g., '#0000FF')")
		self.add_line_edit_control("background", "Background", tooltip = "Expecting a colorname (e.g., 'blue') or an HTML color (e.g., '#0000FF')")
		self.add_line_edit_control("x", "X-coordinate", tooltip = "X-coordinate of the dot (e.g., 0)")
		self.add_line_edit_control("y", "Y-coordinate", tooltip = "Y-coordinate of the dot (e.g., 0)")

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


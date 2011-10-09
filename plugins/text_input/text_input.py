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

from libopensesame import item, exceptions, generic_response
from libqtopensesame import qtplugin
import openexp.canvas
import openexp.keyboard
import os.path
from PyQt4 import QtGui, QtCore

class text_input(item.item, generic_response.generic_response):

	"""A text input display"""

	def __init__(self, name, experiment, string = None):

		"""
		Constructor

		Arguments:
		name -- the name of the item
		experiment -- the experiment instance

		Keyword arguments:
		string -- a definition string
		"""

		# The item_typeshould match the name of the module
		self.item_type = "text_input"
		self._question = "Your question goes here..."
		self.linewidth = 600
		self.frame = "yes"
		self.frame_width = 3
		self.font_family = "sans"
		self.font_size = 24
		self.duration = "dummy"
		self.accept_on = "return press"
		self.timeout = 1000

		# Provide a short accurate description of the items functionality
		self.description = "Provides a simple text input"

		# The parent handles the rest of the contruction
		item.item.__init__(self, name, experiment, string)

	def run(self):

		"""
		Run the item

		Returns:
		True on success, False on failure
		"""

		self.set_item_onset(self.time())

		# If no start response interval has been set, set it to the onset of
		# the current response item
		if self.experiment.start_response_interval == None:
			self.experiment.start_response_interval = self.get("time_%s" % self.name)		

		self._keyboard = openexp.keyboard.keyboard(self.experiment)

		# Create a canvas
		c = openexp.canvas.canvas(self.experiment, self.get("background"), self.get("foreground"))
		c.set_font(self.get("font_family"), self.get("font_size"))
		c.set_penwidth(self.get("frame_width"))

		# Determine the character size and the maximum number of
		# characters per line (assuming a mono font)
		w, h = c.text_size("0")
		maxchar = self.get("linewidth") / w

		if maxchar < 2:
			raise exceptions.runtime_error("The maximum line width is too small (or the font is too large) in text_input '%s'" % self.name)

		margin = 32

		question = self.experiment.unsanitize(self.eval_text(self.get("_question")))

		resp = ""
		response = ""
		response_time = None
		while True:
		
			if self._check_return and resp == "return":
				break
		
			if self._check_timeout and self.time() - self.experiment.start_response_interval > self.timeout:
				break

			# Fill the canvas and put it to the screen
			c.clear()

			_s = question + "\n" + response + "_"
			l = 0
			for s in _s.split("\n"):
				while len(s) > 0:
					c.text(s[:maxchar], False, c.xcenter() - self.get("linewidth") / 2, c.ycenter() + h * l - self.get("linewidth") / 2)
					s = s[maxchar:]
					l += 1
				l += 1

			if self.get("frame") == "yes":
				c.rect(c.xcenter() - self.get("linewidth") / 2 - margin, \
					c.ycenter() - self.get("linewidth") / 2 - margin, \
					self.get("linewidth") + 2 * margin, \
					h * l + 2 * margin, \
					False)

			c.show()

			# Get the response and the moderators (shift etc.)
			key, time = self._keyboard.get_key()
			resp = self._keyboard.to_chr(key)
			mods = self._keyboard.get_mods()

			if response_time == None:
				response_time = time

			# Process the response
			if resp == "backspace":
				if len(response) > 0:
					response = response[:-1]
			elif resp == "space":
				response += " "
			elif len(resp) == 1:
				response += self._keyboard.shift(key, mods)

		self.experiment.set("response", self.experiment.usanitize(self.experiment.sanitize(response)))
		self.experiment.end_response_interval = response_time		
		self.response_bookkeeping()

		# Report success
		return True
		
	def prepare(self):
	
		"""Prepare for the run phase"""
		
		if self.get("accept_on") != "return press":
			self._check_timeout = True
		else:
			self._check_timeout = False
			
		if self.get("accept_on") != "timeout":
			self._check_return = True
		else:
			self._check_return = False			
	
		return True

	def var_info(self):

		return generic_response.generic_response.var_info(self)

class qttext_input(text_input, qtplugin.qtplugin):

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
		text_input.__init__(self, name, experiment, string)
		qtplugin.qtplugin.__init__(self, __file__)

	def init_edit_widget(self):

		"""
		This function creates the controls for the edit
		widget.
		"""

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

		self.add_editor_control("_question", "Question", default = "Your question?", tooltip = "The question to be displayed above the input field")
		self.add_spinbox_control("linewidth", "Maximum line width", 100, 2000, suffix = "px", tooltip = "The maximum width of the input field in pixels")
		self.add_combobox_control("frame", "Draw frame", ["yes", "no"], tooltip = "If 'yes', a rectangular frame will be drawn around the input field")
		self.add_spinbox_control("frame_width", "Frame width", 1, 512, suffix = "px", tooltip = "The width of the frame (if enabled)")
		self.add_color_edit_control("foreground", "Foreground", tooltip = "Expecting a colorname (e.g., 'blue') or an HTML color (e.g., '#0000FF')")
		self.add_color_edit_control("background", "Background", tooltip = "Expecting a colorname (e.g., 'blue') or an HTML color (e.g., '#0000FF')")
		self.add_combobox_control("font_family", "Font family", ["mono", "sans", "serif"], tooltip = "The font style")
		self.add_spinbox_control("font_size", "Font size", 1, 512, suffix = "pt", tooltip = "The font size")
		self.add_combobox_control("accept_on", "Accept on", ["return press", "timeout", "return press or timeout"], tooltip = "Indicates when the input text should be accepted")
		self.add_spinbox_control("timeout", "Timeout (if applicable)", 1, 100000, suffix = "ms", tooltip = "Timeout value")		

		# Add a stretch to the edit_vbox, so that the controls do not
		# stretch to the bottom of the window.
		self.edit_vbox.addStretch()

		self.lock = False

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


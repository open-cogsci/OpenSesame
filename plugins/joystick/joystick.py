"""
30-05-2012
Author: Edwin Dalmaijer

This file is part of OpenSesame.

OpenSesame is free software: you can redistribute it and/or modify
it under the terms of the GNU General Public License as published by
the Free Software Foundation, either version 3 of the License, or
(at your option) any later version.

OpenSesame is distributed in the hope that it will be useful,
but WITHOUT ANY WARRANTY; without even the implied warranty of
MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE. See the
GNU General Public License for more details.

You should have received a copy of the GNU General Public License
along with OpenSesame. If not, see <http://www.gnu.org/licenses/>.
"""

from libopensesame import item, generic_response, exceptions, debug
from libqtopensesame.items.qtautoplugin import qtautoplugin
import openexp.keyboard
import imp
import os
import os.path
from PyQt4 import QtGui, QtCore

class joystick(item.item, generic_response.generic_response):

	"""A plug-in for using a joystick/gamepad"""
	
	description = u'Collects input from a joystick or gamepad'

	def __init__(self, name, experiment, string=None):

		"""
		Constructor

		Arguments:
		name		--	The item name.
		experiment	--	The OpenSesame experiment.

		Keyword arguments:
		string		--	A definition string. (default=None)
		"""

		self.timeout = u'infinite'
		self.allowed_responses = u'1;2'
		self._dummy = u'no'
		item.item.__init__(self, name, experiment, string)
		self.process_feedback = True

	def prepare(self):

		"""Prepares the item."""

		# Pass the word on to the parent
		item.item.prepare(self)

		# Prepare the allowed responses
		if self.has("allowed_responses"):
			self._allowed_responses = []
			for r in self.unistr(self.get("allowed_responses")).split(";"):
				if r.strip() != "":
					try:
						r = int(r)
					except:
						raise exceptions.runtime_error( \
							"'%s' is not a valid response on your joystick/gamepad. Expecting a number in the range of 1 to the amount of buttons." \
							% (r,self.name))
					if r < 0 or r > 255:
						raise exceptions.runtime_error( \
							"'%s' is not a valid response on your joystick/gamepad. Expecting a number in the range of 1 to the amount of buttons." \
							% (r, self.name))
					self._allowed_responses.append(r)
			if len(self._allowed_responses) == 0:
				self._allowed_responses = None
		else:
			self._allowed_responses = None

		debug.msg("allowed responses has been set to %s" % self._allowed_responses)

		# In case of dummy-mode:
		self._keyboard = openexp.keyboard.keyboard(self.experiment)
		if self.has("_dummy") and self.get("_dummy") == "yes":
			self._resp_func = self._keyboard.get_key

		# Not in dummy-mode:
		else:

			# Prepare joybuttonlist and timeout
			joybuttonlist = self.get("_allowed_responses")
			timeout = self.get("timeout")

			# Dynamically load a joystick instance
			if not hasattr(self.experiment, "joystick"):
				path = os.path.join(os.path.dirname(__file__), "libjoystick.py")
				_joystick = imp.load_source("libjoystick", path)
				self.experiment.joystick = _joystick.libjoystick(self.experiment, [joybuttonlist, timeout])
				#self.experiment.cleanup_functions.append(self.close)

			# Prepare auto response
			if self.experiment.auto_response:
				self._resp_func = self.auto_responder
			else:
				self._resp_func = self.experiment.joystick.get_joybutton

		self.prepare_timeout()

	def run(self):

		"""Runs the item."""

		# Set the onset time
		self.set_item_onset()

		# Flush keyboard, so the escape key can be used
		self._keyboard.flush()

		# If no start response interval has been set, set it to the onset of
		# the current response item
		if self.experiment.start_response_interval == None:
			self.experiment.start_response_interval = self.get("time_%s" \
																% self.name)
		if self.has("_dummy") and self.get("_dummy") == "yes":

			# In dummy mode, no one can hear you scream! Oh, and we simply
			# take input from the keyboard
			resp, self.experiment.end_response_interval = self._resp_func( \
				None, self._timeout)
			try:
				resp = self._keyboard.to_chr(resp)
				if resp != "timeout":
					resp = int(resp)
			except:
				raise exceptions.runtime_error( \
					"An error occured in joystick '%s': Only number keys are accepted in dummy mode" \
					% self.name)

		else:
			# Get the response
			try:
				resp, self.experiment.end_response_interval = \
						self._resp_func(self._allowed_responses, self._timeout)
			except Exception as e:
				raise exceptions.runtime_error( \
					"An error occured in joystick '%s': '%s." % (self.name, e))

		debug.msg(u'received %s' % resp)
		self.experiment.response = resp
		generic_response.generic_response.response_bookkeeping(self)

	def var_info(self):
		
		"""
		Gives a list of dictionaries with variable descriptions.

		Returns:
		A list of (name, description) tuples
		"""		

		return item.item.var_info(self) + \
			generic_response.generic_response.var_info(self)

class qtjoystick(joystick, qtautoplugin):

	def __init__(self, name, experiment, script=None):

		# Call parent constructors.
		joystick.__init__(self, name, experiment, script)
		qtautoplugin.__init__(self, __file__)

#-*- coding:utf-8 -*-

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

from libopensesame.py3compat import *
from libopensesame import plugins
from libopensesame.exceptions import osexception
from libopensesame import item, generic_response, debug
from libqtopensesame.items.qtautoplugin import qtautoplugin
import openexp.keyboard

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

		item.item.__init__(self, name, experiment, string)
		self.process_feedback = True

	def reset(self):

		"""
		desc:
			Initialize the plug-in.
		"""

		self.var.timeout = u'infinite'
		self.var.allowed_responses = u''
		self.var._dummy = u'no'
		self.var._device = 0

	def prepare(self):

		"""
		desc:
			Prepares the item.
		"""

		item.item.prepare(self)
		self._allowed_responses = []
		for r in safe_decode(self.var.allowed_responses).split(u";"):
			if r.strip() != "":
				try:
					r = int(r)
				except:
					raise osexception(
						u"'%s' is not a valid response on your joystick/gamepad. Expecting a number in the range of 1 to the amount of buttons." \
						% (r,self.name))
				if r < 0 or r > 255:
					raise osexception(
						u"'%s' is not a valid response on your joystick/gamepad. Expecting a number in the range of 1 to the amount of buttons." \
						% (r, self.name))
				self._allowed_responses.append(r)
		if len(self._allowed_responses) == 0:
			self._allowed_responses = None
		debug.msg(
			u"allowed responses has been set to %s" % self._allowed_responses)
		# In case of dummy-mode:
		self._keyboard = openexp.keyboard.keyboard(self.experiment)
		if self.var._dummy == u"yes":
			self._resp_func = self._keyboard.get_key
		# Not in dummy-mode:
		else:
			timeout = self.var.timeout
			# Dynamically load a joystick instance
			if not hasattr(self.experiment, u"joystick"):
				_joystick = plugins.load_mod(__file__, u'libjoystick')
				self.experiment.joystick = _joystick.libjoystick(
					self.experiment, device=self._device)
			# Prepare auto response
			if self.experiment.auto_response:
				self._resp_func = self.auto_responder
			else:
				self._resp_func = self.experiment.joystick.get_joybutton
		self.prepare_timeout()

	def run(self):

		"""
		desc:
			Runs the item.
		"""

		# Set the onset time
		self.set_item_onset()
		# Flush keyboard, so the escape key can be used
		self._keyboard.flush()
		# If no start response interval has been set, set it to the onset of
		# the current response item
		if self.experiment._start_response_interval is None:
			self.experiment._start_response_interval = self.var.get(
				u'time_%s' % self.name)
		if self.var._dummy == u'yes':
			# In dummy mode, no one can hear you scream! Oh, and we simply
			# take input from the keyboard
			resp, self.experiment.end_response_interval = self._resp_func(
				keylist=None, timeout=self._timeout)
		else:
			# Get the response
			resp, self.experiment.end_response_interval = self._resp_func(
				self._allowed_responses, self._timeout)
		debug.msg(u'received %s' % resp)
		self.experiment.var.response = resp
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

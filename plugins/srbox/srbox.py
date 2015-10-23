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

from libopensesame.exceptions import osexception
from libopensesame import item, generic_response, debug
from libqtopensesame.items.qtautoplugin import qtautoplugin
import openexp.keyboard
import imp
import os
import os.path
from PyQt4 import QtGui, QtCore
import libsrbox
from libopensesame.py3compat import *

class srbox(item.item, generic_response.generic_response):

	"""
	desc:
		A plug-in for using the serial response box.
	"""

	def reset(self):

		"""
		desc:
			Reset item and experimental variables.
		"""

		self.var.timeout = u'infinite'
		self.var.lights = u''
		self.var.dev = u'autodetect'
		self.var._dummy = u'no'
		self.var.require_state_change = u'no'
		self.process_feedback = True

	def prepare(self):

		"""
		desc:
			Prepare the item.
		"""

		item.item.prepare(self)
		self.prepare_timeout()
		self._require_state_change = self.require_state_change == u'yes'
		# Prepare the allowed responses
		self._allowed_responses = None
		if u'allowed_responses' in self.var:
			self._allowed_responses = []
			for r in safe_decode(self.var.allowed_responses).split(u';'):
				if r.strip() != u'':
					try:
						r = int(r)
					except:
						raise osexception(
							u"'%s' is not a valid response in srbox '%s'. Expecting a number in the range 0 .. 5." \
							% (r, self.name))
					if r < 0 or r > 255:
						raise osexception(
							u"'%s' is not a valid response in srbox '%s'. Expecting a number in the range 0 .. 5." \
							% (r, self.name))
					self._allowed_responses.append(r)
			if not self._allowed_responses:
				self._allowed_responses = None
		debug.msg(u"allowed responses set to %s" % self._allowed_responses)
		# Prepare keyboard for dummy-mode and flushing
		self._keyboard = openexp.keyboard.keyboard(self.experiment)
		if self.var._dummy == u'yes':
			self._resp_func = self._keyboard.get_key
			return
		# Prepare the device string
		dev = self.var.dev
		if dev == u"autodetect":
			dev = None
		# Dynamically create an srbox instance
		if not hasattr(self.experiment, "srbox"):
			self.experiment.srbox = libsrbox.libsrbox(self.experiment, dev)
			self.experiment.cleanup_functions.append(self.close)
			self.python_workspace[u'srbox'] = self.experiment.srbox
		# Prepare the light byte
		s = "010" # Control string
		for i in range(5):
			if str(5 - i) in str(self.var.lights):
				s += "1"
			else:
				s += "0"
		self._lights = chr(int(s, 2))
		debug.msg(u"lights string set to %s (%s)" % (s, self.var.lights))
		# Prepare auto response
		if self.experiment.auto_response:
			self._resp_func = self.auto_responder
		else:
			self._resp_func = self.experiment.srbox.get_button_press

	def run(self):

		"""
		desc:
			Runs the item.
		"""

		self.set_item_onset()
		self._keyboard.flush()
		self.set_sri(reset=True)
		if self.var._dummy == 'yes':
			# In dummy mode, we simply take the numeric keys from the keyboard
			if self._allowed_responses is None:
				self._allowed_responses = list(range(0,10))
			resp, self.experiment.end_response_interval = self._resp_func(
				keylist=self._allowed_responses, timeout=self._timeout)
			if resp is not None:
				resp = int(resp)
		else:
			# Get the response
			try:
				self.experiment.srbox.send(self._lights)
				self.experiment.srbox.start()
				resp, self.experiment.end_response_interval = \
					self._resp_func(allowed_buttons=self._allowed_responses,
						timeout=self._timeout,
						require_state_change=self._require_state_change)
				self.experiment.srbox.stop()
			except Exception as e:
				raise osexception(
					"An error occured in srbox '%s': %s." % (self.name, e))
			if isinstance(resp, list):
				resp = resp[0]
		debug.msg("received %s" % resp)
		self.experiment.var.response = resp
		generic_response.generic_response.response_bookkeeping(self)

	def close(self):

		"""
		desc:
			Neatly close the connection to the srbox.
		"""

		if not hasattr(self.experiment, "srbox") or \
			self.experiment.srbox is None:
				debug.msg("no active srbox")
				return
		try:
			self.experiment.srbox.close()
			self.experiment.srbox = None
			debug.msg("srbox closed")
		except:
			debug.msg("failed to close srbox")

	def var_info(self):

		"""
		returns:
			A list of (name, description) tuples with variable descriptions.
		"""

		return item.item.var_info(self) + \
			generic_response.generic_response.var_info(self)

class qtsrbox(srbox, qtautoplugin):

	def __init__(self, name, experiment, script=None):

		srbox.__init__(self, name, experiment, script)
		qtautoplugin.__init__(self, __file__)

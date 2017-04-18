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
from libopensesame.item import item
from libqtopensesame.items.qtautoplugin import qtautoplugin
from openexp.canvas import canvas
from time import gmtime, strftime
from datetime import datetime
from datetime import timedelta
from libopensesame.exceptions import osexception

import time
import socket
import sys

class LabScribe_send_message(item):
	"""Plugin to send messages to Labscribe"""
	description = u'Plugin to send messages to Labscribe.'

	def __init__(self, name, experiment, script=None):
	
		"""
		Constructor
		
		Arguments:
		name -- item name
		experiment -- experiment instance
		
		Keyword arguments:
		script -- definition string (default=None)
		"""
		
		
		self._checkbox = u'no' # yes = checked, no = unchecked
		self._color = u'blue'
		self._option = u'Start Connection'
		self._file = u''
		self._text = u'Insert message here.'
		self._script = u'print 10'	

		global s
		global host
		global port
		global data
		global startTime
		global timeDiff
		global socketCreated

		item.__init__(self, name, experiment, script)

	def prepare(self):
		item.prepare(self)

	def run(self):
		"""Process the request to send message.  Record the time stamp and send the message."""
		self.set_item_onset() # Record the timestamp of the plug-in execution.
		global s
		global host
		global port
		global data
		global startTime
		global timeDiff
		global socketCreated

		def millis():
			global startTime

			dt = datetime.now() - startTime
			ms = (dt.days * 24 * 60 * 60 + dt.seconds) * 1000 + dt.microseconds / 1000.0
			return ms
		
		if self._option == u'Start Connection':
			host = '127.0.0.1'
			port = 3000
			socketCreated = 0
			
			try:
				s = socket.create_connection((host, port))
				socketCreated = 1
			except:
				raise osexception( u'Error Creating socket connection. Make sure that LabScribe is recordng data and the Experiment Server port is set to 3000.')
			
			startTime = datetime.now()
			msg = startTime.strftime("cmdstart^%H:%M:%S^%f^")
			
			try:
				s.sendall(data)
				socketCreated = 1
			except:
				raise osexception( u'Error sending Start Connection')
			
				
		elif self._option == u'Send Message':
			if socketCreated == 1:
				msg = u'mark^' +  str(millis()) + u'^' + self._text + u'^'

				try :
					s.sendall(msg)
				except:
					raise osexception( u'Error Sending Message')
			else:
				print u'error'
				
		elif self._option == u'End Connection':
			if socketCreated == 1:
				msg = u'cmdstop^' + str(millis()) + u'^'

				try :
					s.sendall(msg)

				except :
					raise osexception( u'Error Ending Connection')
				
				s.close()
			else:
				print u'error'

		self.set_item_onset() # Record the timestamp of the plug-in execution.

class qtLabScribe_send_message(LabScribe_send_message, qtautoplugin):
	"""GUI controls for LabScribe_send_message plug-in"""
	def __init__(self, name, experiment, script=None):
		LabScribe_send_message.__init__(self, name, experiment, script)
		qtautoplugin.__init__(self, __file__)

	def init_edit_widget(self):
		qtautoplugin.init_edit_widget(self)
	
	def IndexChanged(index):
		if index == 0:
			self.line_edit_widget.setEnabled(true)
		else:
			self.line_edit_widget.setEnabled(false)

	def edit_widget(self):
		qtautoplugin.edit_widget(self)      
		if self.combobox_widget.currentText() == u'Send Message':
			self.line_edit_widget.show()
		else:
			self.line_edit_widget.hide()
		return self._edit_widget
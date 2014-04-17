from libopensesame import debug
from libopensesame.item import item
from libqtopensesame.items.qtautoplugin import qtautoplugin
from openexp.canvas import canvas
from libopensesame.item import item
from time import gmtime, strftime
from datetime import datetime
from datetime import timedelta


import time
import socket
import sys

class send_message(item):

	description = u'Plugin to send messages to Labscribe.'

	def __init__(self, name, experiment, script=None):
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

			except socket.error, msg:
				print 'Error Code : ' + str(msg[0]) + ' Message ' + msg[1]

			if socketCreated == 1:
				startTime = datetime.now()
				msg = "cmdstart^" + startTime.strftime("%H:%M:%S^%f") + "^"
				data = msg.encode('utf8')

				try:
					s.sendall(data)
				except socket.error, msg:
					print 'Error Code : ' + str(msg[0]) + ' Message ' + msg[1]
			else:
				print 'error'
				
		elif self._option == u'Send Message':
			if socketCreated == 1:
				msg = "mark^" +  str(millis()) + "^" + self._text + "^"
				data = msg.encode('utf8')

				try :
					s.sendall(data)

				except socket.error, msg:
					print 'Error Code : ' + str(msg[0]) + ' Message ' + msg[1]
			else:
				print 'error'
				
		elif self._option == u'End Connection':
			if socketCreated == 1:
				msg = "cmdstop^" + str(millis()) + "^"
				data = msg.encode('utf8')

				try :
					s.sendall(data)

				except socket.error, msg:
					print 'Error Code : ' + str(msg[0]) + ' Message ' + msg[1]
				
				s.close()
			else:
				print 'error'

		self.set_item_onset() # Record the timestamp of the plug-in execution.

class qtsend_message(send_message, qtautoplugin):

	def __init__(self, name, experiment, script=None):
		send_message.__init__(self, name, experiment, script)
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
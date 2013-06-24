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

from libopensesame.item import item
from libqtopensesame.items.qtautoplugin import qtautoplugin
from openexp.canvas import canvas

class mobile_start(item):

	"""
	This class (the class with the same name as the module) handles the basic
	functionality of the item. It does not deal with GUI stuff.
	"""

	# Provide an informative description for your plug-in.
	description = u'An example new-style plug-in'

	def __init__(self, name, experiment, script=None):

		"""
		Constructor.
		
		Arguments:
		name		--	The name of the plug-in.
		experiment	--	The experiment object.
		
		Keyword arguments:
		script		--	A definition script. (default=None)
		"""

		# Here we provide default values for the variables that are specified
		# in info.json. If you do not provide default values, the plug-in will
		# work, but the variables will be undefined when they are not explicitly
		# set in the GUI.
		
		# I'm not sure what the end user will need to control here yet.
		# Leaving the examples defaults here as placeholders.
		self._checkbox = u'yes' # yes = checked, no = unchecked
		self._color = u'white'
		self._option = u'Option 1'
		self._file = u''
		self._text = u'Default text'
		self._spinbox_value = 1
		self._slider_value = 1
		self._script = u'print 10'
		# Then call the parent constructor
		item.__init__(self, name, experiment, script)

	def prepare(self):

		"""The preparation phase of the plug-in goes here."""

		# Call the parent constructor.
		item.prepare(self)
		# Specific code
		# Use this to define global functions
		def send_data(data, delete):
			self.c.clear()
			self.c.text('Connecting to server...')
			self.c.show()
	
			# Try to open the connection
			address = 'http://cogsci.nl/etravers/androidsql.php'
	
			try:
				page = urllib.urlopen(address, 'position=openingconnection')
				page.close()
				# Connection works. Send data.
				print 'Connected'
				t = 0
				for trial in data:
					progress = int(float(t)/len(data)*680)
					#print t, len(data), progress
					self.c.clear()
					self.c.text('Sending...')
					self.c.rect(300, 600, 680, 72, False, 'white')
					# Update progress bar
					self.c.rect(303, 601, progress, 70, True, 'red')
					self.c.show()
					encode_data = urllib.urlencode(trial)
					print encode_data
					for i in range(5):
						try:
							page = urllib.urlopen(address, encode_data)
							page.close()
							print 'Sent!', t
						except IOError as e:
								print str(e)
						else:
							break
					t += 1
				result = 'Data sent!'
				#Delete sent datafile
				if delete:
					if os.path.isfile(data_path):
						os.remove(data_path)
			except IOError as e:
				result = 'Unable to connect.\nPlease try again when connected to the internet.'
				save_data()
				print str(e)
			self.c.clear()
			self.c.text(result)
			self.c.show()
			my_mouse.get_click()
		
		def save_data():
			sdcard_folders = ['/sdcard/', '/mnt/sdcard/']
			for path in sdcard_folders:
				if os.path.isdir(path):
					break
			try:
				f = open(os.path.join(path, 'datafile.txt'), 'w')
			except:
				print 'Failed to create %s' % path
				f = open('datafile.txt', 'w')
			f.truncate()
			f.write( 'data_log = ' + repr(data_log)+'\n' + 'global data_log')
			f.close()
	

		global send_data, save_data




	def run(self):

		"""The run phase of the plug-in goes here."""

		# self.set_item_onset() sets the time_[item name] variable. Optionally,
		# you can pass a timestamp, such as returned by canvas.show().
		#self.set_item_onset(self.c.show())			
		
		# The following is the opening screen of the experiment
		# Needs a good bit of work
		exp = self.experiment
		from openexp.mouse import mouse
		from openexp.canvas import canvas
		from openexp.keyboard import keyboard
		import urllib
		#import socket
		#import errno
		import os
		import time
		#Using more than one timing method?
		from pygame.mouse import get_pressed
		from random import randint
		subject_number = randint(1,99999)
		
		try:
		    import android
		except ImportError:
		    android = None
		
		#Define global variables/methods
		my_mouse = mouse(exp, visible = True)
		self.c = canvas(exp, auto_prepare=False)
		self.c = canvas(self.experiment, self.get(u'background'), \
			self.get(u'foreground'))
		my_keyboard = keyboard(exp)
		exp.set('run_experiment', 1)
		
		global my_mouse, my_canvas, my_keyboard, urllib, event
		global pickle, os, android, time, get_pressed, subject_number
		#print 'Path = '+str(os.path.curdir)
		
		sdcard_folders = ['/sdcard/', '/mnt/sdcard/']
		for path in sdcard_folders:
			if os.path.isdir(path):
				print path
				break
		if os.path.exists(os.path.join(path, 'datafile.txt')):
			data_path = os.path.join(path, 'datafile.txt')
		elif os.path.exists('datafile.txt'):
			data_path = 'datafile.txt'
		else:
			data_path = None
		global data_path
		if data_path:
			print 'Unsent data detected'
			my_canvas.clear()
			self.c.text('Unsent data detected. Send now?')
			self.c.text('Yes', x=150, y=125)
			self.c.text('No', x=1050, y=125)
			self.c.show()
			while 1:
				button, position, timestamp = my_mouse.get_click()	
				x, y = position
				if x < 350 and y < 200:
				#Yes
					try:
						print 'Opening data...'
						execfile(data_path)
						global data_log
						print 'Opened'
						# Try to send it
						send_data(data_log, True)
					except IOError as e:
						self.c.clear()
						self.c.text('No data found.\nTap to continue.')
						# Hopefully, this doesn't happen!
						self.c.show()
						my_mouse.get_click()
					break
				if x > 930 and y < 200:
					#No
					#This overwrites old data.
					#Add a warning about this.
					break
			self.c.clear()
			self.c.text('Continue to experiment?')
			self.c.text('Yes', x=150, y=125)
			self.c.text('No', x=1050, y=125)
			self.c.show()
			waiting = True
			while waiting:
				button, position, timestamp = my_mouse.get_click()	
				x, y = position
				if x < 350 and y < 200:
					exp.set('run_experiment', 1)
					break
				if x > 930 and y < 200:
					exp.set('run_experiment', 0)
					break
		
		data_log = []
		trial_id = 0
		global data_log, trial_id


class qtmobile_start(mobile_start, qtautoplugin):
	
	"""
	This class handles the GUI aspect of the plug-in. By using qtautoplugin, we
	usually need to do hardly anything, because the GUI is defined in info.json.
	"""

	def __init__(self, name, experiment, script=None):

		"""
		Constructor.
		
		Arguments:
		name		--	The name of the plug-in.
		experiment	--	The experiment object.
		
		Keyword arguments:
		script		--	A definition script. (default=None)
		"""

		# We don't need to do anything here, except call the parent
		# constructors.
		mobile_start.__init__(self, name, experiment, script)
		qtautoplugin.__init__(self, __file__)

	def init_edit_widget(self):

		"""
		Constructs the GUI controls. Usually, you can omit this function
		altogether, but if you want to implement more advanced functionality,
		such as controls that are grayed out under certain conditions, you need
		to implement this here.
		"""

		# First, call the parent constructor, which constructs the GUI controls
		# based on info.json.
		qtautoplugin.init_edit_widget(self)
		# If you specify a 'name' for a control in info.json, this control will
		# be available self.[name]. The type of the object depends on the
		# control. A checkbox will be a QCheckBox, a line_edit will be a
		# QLineEdit. Here we connect the stateChanged signal of the QCheckBox,
		# to the setEnabled() slot of the QLineEdit. This has the effect of
		# disabling the QLineEdit when the QCheckBox is uncheckhed.
		self.checkbox_widget.stateChanged.connect( \
			self.line_edit_widget.setEnabled)



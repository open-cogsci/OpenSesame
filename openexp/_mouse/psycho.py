"""
This file is part of openexp.

openexp is free software: you can redistribute it and/or modify
it under the terms of the GNU General Public License as published by
the Free Software Foundation, either version 3 of the License, or
(at your option) any later version.

openexp is distributed in the hope that it will be useful,
but WITHOUT ANY WARRANTY; without even the implied warranty of
MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
GNU General Public License for more details.

You should have received a copy of the GNU General Public License
along with openexp.  If not, see <http://www.gnu.org/licenses/>.
"""

import openexp.mouse
import openexp.exceptions
import openexp._mouse.legacy
from psychopy import event

class psycho(openexp._mouse.legacy.legacy):

	"""
	This is a mouse backend which uses PsychoPy
	"""

	def __init__(self, experiment, buttonlist = None, timeout = None, visible = False):
	
		"""
		Intializes the mouse object
		
		Arguments:
		experiment -- an instance of libopensesame.experiment.experiment
		
		Keyword arguments:
		buttonlist -- a list of buttons that are accepted or None to accept
					  all input (default = None)
		timeout -- an integer value specifying a timeout in milliseconds or
				   None for no timeout (default = None)
		visible -- a boolean indicating the visibility of the cursor (default = False)
		"""
		
		if experiment.canvas_backend != "psycho":
			raise openexp.exceptions.response_error("The psycho mouse backend must be used in combination with the psycho canvas backend!")
	
		self.experiment = experiment						
		self.set_buttonlist(buttonlist)
		self.set_timeout(timeout)
		self.mouse = event.Mouse(visible = False, win = self.experiment.window)
		self.set_visible(visible)
		event.mouseButtons = [0, 0, 0]	
				
	def set_buttonlist(self, buttonlist = None):
	
		"""
		Sets a list of accepted buttons

		Keyword arguments:
		buttonlist -- a list of buttons that are accepted or None to accept
					  all input (default = None)
		"""	
	
		if buttonlist == None:
			self.buttonlist = None
		else:
			self.buttonlist = []
			try:
				for b in buttonlist:
					self.buttonlist.append(int(b))
			except:
				raise openexp.exceptions.response_error("The list of mousebuttons must be a list of numeric values")
		
	def set_timeout(self, timeout = None):	
	
		"""
		Sets a timeout
		
		Keyword arguments:
		timeout -- an integer value specifying a timeout in milliseconds or
				   None for no timeout (default = None)		
		"""
			
		self.timeout = timeout
				
	def set_visible(self, visible = True):
	
		"""
		Sets the visibility of the cursor
		
		Keyword arguments:
		visible -- A boolean indicating the visibility of the cursor (default = True)
		"""	
	
		self.visible = visible
		self.mouse.setVisible(visible)		
		
	def get_click(self, buttonlist = None, timeout = None, visible = None):
	
		"""
		Waits for mouse input
		
		Keyword arguments:
		buttonlist -- a list of buttons that are accepted or None
					  to use the default. This parameter does not change 
					  default keylist. (default = None)
		timeout -- an integer value specifying a timeout in milliseconds or
				   None to use the default. This parameter does not change the
				   default timeout. (default = None)		
		visible -- a boolean indicating the visibility of the target or None
				   to use the default. This parameter does not change the default 
				   visibility (default = False)
				   
		Returns:
		A (button, position, timestamp) tuple. The button and position are None if
		a timeout occurs. Position is an (x, y) tuple in screen coordinates.
		"""		
	
		if buttonlist == None:
			buttonlist = self.buttonlist
		if timeout == None:
			timeout = self.timeout	
		if visible == None:
			visible = self.visible			
		self.mouse.setVisible(visible)	
		
		start_time = 1000.0 * self.experiment.clock.getTime()
		time = start_time			
		button = None
		pos = None
		self.mouse.clickReset()
		while timeout == None or time - start_time < timeout:
			time = 1000.0 * self.experiment.clock.getTime()			
			buttons, times = self.mouse.getPressed(getTime=True)
			if buttons[0] and (buttonlist == None or 1 in buttonlist):
				button = 1
				pos = self.mouse.getPos()
				break
			if buttons[1] and (buttonlist == None or 2 in buttonlist):
				button = 2
				pos = self.mouse.getPos()
				break
			if buttons[2] and (buttonlist == None or 1 in buttonlist):
				button = 3
				pos = self.mouse.getPos()
				break
		if pos != None:
			pos = pos[0]+self.experiment.width/2, \
				self.experiment.height/2-pos[1]
		self.mouse.setVisible(self.visible)					
		return button, pos, time					
		
	def get_pos(self):
	
		"""
		Returns the current location of the cursor
		
		Returns:
		A (position, timestamp) tuple.
		"""	
	
		x, y = self.mouse.getPos()
		t = self.experiment.time()
		x = x + self.experiment.width/2
		y = self.experiment.height/2 - y
		return (x, y), t
		
	def flush(self):
	
		"""
		Clears all pending input, not limited to the mouse
		
		Returns:
		True if a button had been clicked (i.e., if there was something
		to flush) and False otherwise
		"""	
	
		event.mouseButtons = [0,0,0]
		event.clearEvents()
		return False

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
import pygame
from pygame.locals import *

class legacy:

	"""
	The legacy backend is the default backend which uses PyGame to handle all
	mouse input.

	This class serves as a template for creating OpenSesame mouse input
	backends. The new backend can be activated by adding "set mouse_backend dummy"
				
	A few guidelines:
	-- Buttons are numbered as follows: 1 = left, 2 = middle, 3 = right, 4 = scroll up, 5 = scroll down
	-- Catch exceptions wherever possible and raise an openexp.exceptions.canvas_error
	   with a clear and descriptive error message.
	-- Do not deviate from the guidelines. All back-ends should be interchangeable and 
	   transparent to OpenSesame. You are free to add functionality to this class, to be 
	   used in inline scripts, but this should not break the basic functionality.
	-- Print debugging output only if experiment.debug == True and preferrably in the
	   following format: "template.__init__(): Debug message here".	
	"""

	def __init__(self, experiment, buttonlist = None, timeout = None, visible = False):
	
		"""<DOC>
		Intializes the mouse object
		
		Arguments:
		experiment -- an instance of libopensesame.experiment.experiment
		
		Keyword arguments:
		buttonlist -- a list of buttons that are accepted or None to accept
					  all input (default = None)
		timeout -- an integer value specifying a timeout in milliseconds or
				   None for no timeout (default = None)
		visible -- a boolean indicating the visibility of the cursor (default = False)
		</DOC>"""	
	
		self.experiment = experiment
		self.set_buttonlist(buttonlist)
		self.set_timeout(timeout)
		self.set_visible(visible)
				
	def set_buttonlist(self, buttonlist = None):
	
		"""<DOC>
		Sets a list of accepted buttons

		Keyword arguments:
		buttonlist -- a list of buttons that are accepted or None to accept
					  all input (default = None)
		</DOC>"""	
	
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
	
		"""<DOC>
		Sets a timeout
		
		Keyword arguments:
		timeout -- an integer value specifying a timeout in milliseconds or
				   None for no timeout (default = None)		
		</DOC>"""
			
		self.timeout = timeout
				
	def set_visible(self, visible = True):
	
		"""<DOC>
		Sets the visibility of the cursor
		
		Keyword arguments:
		visible -- A boolean indicating the visibility of the cursor (default = True)
		</DOC>"""	
	
		self.visible = visible
		pygame.mouse.set_visible(visible)				
		
	def get_click(self, buttonlist = None, timeout = None, visible = None):
	
		"""<DOC>
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
		</DOC>"""		
	
		if buttonlist == None:
			buttonlist = self.buttonlist
		if timeout == None:
			timeout = self.timeout	
		if visible == None:
			visible = self.visible			
		pygame.mouse.set_visible(visible)	
		
		start_time = pygame.time.get_ticks()
		time = start_time	
	
		while timeout == None or time - start_time < timeout:
			time = pygame.time.get_ticks()
			for event in pygame.event.get():			
				if event.type == KEYDOWN and event.key == pygame.K_ESCAPE:
					raise openexp.exceptions.response_error("The escape key was pressed.")										
				if event.type == MOUSEBUTTONDOWN:
					if buttonlist == None or event.button in buttonlist:
						pygame.mouse.set_visible(self.visible)
						return event.button, event.pos, time
					
		pygame.mouse.set_visible(self.visible)					
		return None, None, time					
		
	def get_pos(self):
	
		"""<DOC>
		Returns the current location of the cursor
		
		Returns:
		A (position, timestamp) tuple.
		</DOC>"""	
	
		return pygame.mouse.get_pos(), self.experiment.time()
		
	def flush(self):
	
		"""<DOC>
		Clears all pending input, not limited to the mouse
		
		Returns:
		True if a button had been clicked (i.e., if there was something
		to flush) and False otherwise
		</DOC>"""	
	
		buttonclicked = False
		for event in pygame.event.get():
			if event.type == KEYDOWN and event.key == pygame.K_ESCAPE:
				raise openexp.exceptions.response_error("The escape key was pressed.")
			if event.type == MOUSEBUTTONDOWN:
				buttonclicked = True
		return buttonclicked

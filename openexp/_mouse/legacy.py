#-*- coding:utf-8 -*-

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
	backends. The new backend can be activated by adding
	"set mouse_backend dummy"
				
	A few guidelines:
	-- Buttons are numbered as follows:
		1 = left
		2 = middle
		3 = right
		4 = scroll up
		5 = scroll down
	-- Catch exceptions wherever possible and raise an
	   openexp.exceptions.canvas_error with a clear and descriptive error
	   message.
	-- Do not deviate from the guidelines. All back-ends should be
	   interchangeable and transparent to OpenSesame. You are free to add
	   functionality to this class, to be used in inline scripts, but this
	   should not break the basic functionality.
	"""
	
	settings = {
		"custom_cursor" : {
			"name" : "Custom cursor",
			"description" : "Bypass the system mouse cursor",
			"default" : "yes"
			},
		"enable_escape" : {
			"name" : "Enable escape",
			"description" : "Abort the experiment when the upper left and right corners are clicked",
			"default" : "no",
			}
		}

	def __init__(self, experiment, buttonlist=None, timeout=None, visible=False):
	
		"""<DOC>
		Intializes the mouse object.
		
		Arguments:
		experiment -- An instance of libopensesame.experiment.experiment.
		
		Keyword arguments:
		buttonlist -- A list of buttons that are accepted or None to accept all #
					  input (default = None).
		timeout -- An integer value specifying a timeout in milliseconds or None #
				   for no timeout (default = None).
		visible -- A Boolean indicating the visibility of the cursor #
				   (default=False).
		   
		Example:
		>>> from openexp.mouse import mouse
		>>> my_mouse = mouse(exp)
		</DOC>"""	
	
		self.experiment = experiment
		self.set_buttonlist(buttonlist)
		self.set_timeout(timeout)
		self.set_visible(visible)		
		if self.experiment.get_check('custom_cursor', 'yes') == 'yes':
			self.cursor = pygame.image.load(self.experiment.resource( \
				'cursor.png'))		
		else:
			self.cursor = None
				
	def set_buttonlist(self, buttonlist = None):
	
		"""<DOC>
		Sets a list of accepted buttons.

		Keyword arguments:
		buttonlist -- A list of buttons that are accepted or None to accept all #
					  input (default=None).
		  
		Example:
		>>> from openexp.mouse import mouse
		>>> my_mouse = mouse(exp)
		>>> my_mouse.set_buttonlist( [1,2] )
		</DOC>"""	
	
		if buttonlist == None:
			self.buttonlist = None
		else:
			self.buttonlist = []
			try:
				for b in buttonlist:
					self.buttonlist.append(int(b))
			except:
				raise openexp.exceptions.response_error( \
					"The list of mousebuttons must be a list of numeric values")
		
	def set_timeout(self, timeout=None):	
	
		"""<DOC>
		Sets a timeout.
		
		Keyword arguments:
		timeout -- An integer value specifying a timeout in milliseconds or None #
				   for no timeout (default=None).
		
		Example:
		>>> from openexp.mouse import mouse
		>>> my_mouse = mouse(exp)
		>>> my_mouse.set_timeout(2000)
		</DOC>"""
			
		self.timeout = timeout
				
	def set_visible(self, visible=True):
	
		"""<DOC>
		Sets the visibility of the cursor.
		
		Keyword arguments:
		visible -- A Boolean indicating the visibility of the cursor #
				   (default=True).

		Example:
		>>> from openexp.mouse import mouse
		>>> my_mouse = mouse(exp)
		>>> my_mouse.set_visible()
		</DOC>"""	
	
		self.visible = visible
		pygame.mouse.set_visible(visible)

	def set_pos(self, pos=(0,0)):

		"""<DOC>
		Sets the mouse position.
		
		Keyword arguments:
		pos -- A (x,y) tuple for the new mouse coordinates (default = (0,0))

		Example:
		>>> from openexp.mouse import mouse
		>>> my_mouse = mouse(exp)
		>>> my_mouse.set_pos(pos=(0,0))
		</DOC>"""	
	
		pygame.mouse.set_pos(pos)						
		
	def get_click(self, buttonlist=None, timeout=None, visible=None):
	
		"""<DOC>
		Waits for mouse input.
		
		Keyword arguments:
		buttonlist -- A list of buttons that are accepted or None to use the #
					  default. This parameter does not change the default keylist #
					  (default=None).
		timeout -- An integer value specifying a timeout in milliseconds or None #
				   to use the default. This parameter does not change the #
				   default timeout (default=None).		
		visible -- A Boolean indicating the visibility of the target or None to #
				   use the default. This parameter does not change the default #
				   visibility (default=False).
				   
		Returns:
		A (button, position, timestamp) tuple. The button and position are None #
		if a timeout occurs. Position is an (x, y) tuple in screen coordinates.
		
		Example:
		>>> from openexp.mouse import mouse
		>>> my_mouse = mouse(exp)
		>>> button, position, timestamp = my_mouse.get_click()
		>>> if button == None:
		>>> 	print 'A timeout occurred!'
		</DOC>"""		
	
		if buttonlist == None:
			buttonlist = self.buttonlist
		if timeout == None:
			timeout = self.timeout	
		if visible == None:
			visible = self.visible			
		enable_escape = self.experiment.get_check('enable_escape', 'no', \
			['yes', 'no']) == 'yes'		
		if self.cursor == None:
			pygame.mouse.set_visible(visible)
		elif visible:
			pygame.mouse.set_visible(False)
		
		start_time = pygame.time.get_ticks()
		time = start_time
		
		while True:
			time = pygame.time.get_ticks()						
			
			# Draw a cusom cursor if necessary
			if self.cursor != None and visible:
				surface = self.experiment.lastShownCanvas.copy()
				surface.blit(self.cursor, pygame.mouse.get_pos())
				self.experiment.surface.blit(surface, (0,0))		
				pygame.display.flip()
			
			# Process the input
			for event in pygame.event.get():								
				if event.type == KEYDOWN and event.key == pygame.K_ESCAPE:
					raise openexp.exceptions.response_error( \
						"The escape key was pressed.")										
				if event.type == MOUSEBUTTONDOWN:					
				
					# Check escape sequence. If the top-left and top-right
					# corner are clicked successively within 2000ms, the
					# experiment is aborted
					if enable_escape and event.pos[0] < 64 and event.pos[1] \
						< 64:
						_time = pygame.time.get_ticks()
						while pygame.time.get_ticks() - _time < 2000:
							for event in pygame.event.get():
								if event.type == MOUSEBUTTONDOWN:
									if event.pos[0] > self.experiment.get( \
										'width')-64 and event.pos[1] < 64:
										raise openexp.exceptions.response_error( \
											"The escape sequence was clicked/ tapped")
						
					if (buttonlist == None or event.button in buttonlist):
						if self.cursor is None:						
							pygame.mouse.set_visible(self.visible)
						return event.button, event.pos, time
			if timeout != None and time-start_time >= timeout:
				break
											
		if self.cursor == None:
			pygame.mouse.set_visible(self.visible)					
		return None, None, time		
		
	def get_pos(self):
	
		"""<DOC>
		Returns the current location of the cursor.
		
		Returns:
		A (position, timestamp) tuple.
		
		Example:
		>>> from openexp.mouse import mouse
		>>> my_mouse = mouse(exp)
		>>> position, timestamp = my_mouse.get_pos()
		>>> x, y = position
		>>> print 'The cursor was at (%d, %d)' % (x, y)
		</DOC>"""	
	
		pygame.event.get()
		return pygame.mouse.get_pos(), self.experiment.time()

	def get_pressed(self):
	
		"""<DOC>
		Returns the current state of the mouse buttons. A True value means #
		the button is currently being pressed.
		
		Returns:
		A (button1, button2, button3) tuple.
		
		Example:
		>>> from openexp.mouse import mouse
		>>> my_mouse = mouse(exp)
		>>> buttons = my_mouse.get_pressed()
		>>> b1, b2, b3 = buttons
		>>> print 'Currently pressed mouse buttons: (%d, %d, %d)' % (b1, b2, b3)
		</DOC>"""

		return pygame.mouse.get_pressed()
		
	def flush(self):
	
		"""<DOC>
		Clears all pending input, not limited to the mouse.
		
		Returns:
		True if a button had been clicked (i.e., if there was something #
		to flush) and False otherwise.
		
		Example:
		>>> from openexp.mouse import mouse
		>>> my_mouse = mouse(exp)
		>>> my_mouse.flush()
		>>> button, position, timestamp = my_mouse.get_click()
		</DOC>"""	
	
		buttonclicked = False
		for event in pygame.event.get():
			if event.type == KEYDOWN and event.key == pygame.K_ESCAPE:
				raise openexp.exceptions.response_error( \
					"The escape key was pressed.")
			if event.type == MOUSEBUTTONDOWN:
				buttonclicked = True
		return buttonclicked
		
	def synonyms(self, button):
	
		"""
		Gives a list of synonyms for a mouse button. For example, 1 and #
		'left_click' are synonyms.
		
		Arguments:
		button -- A button value.
		
		Returns:
		A list of synonyms.
		"""
				
		button_map = [ (1, "left_button"), (2, "middle_button"), (3, \
			"right_button"), (4, "scroll_up"), (5, "scroll_down") ]
		for bm in button_map:
			if button in bm:
				return bm
		return []


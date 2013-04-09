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
import openexp._mouse.legacy
from psychopy import event
import psychopy.visual

class psycho(openexp._mouse.legacy.legacy):

	"""This is a mouse backend built on top of PsychoPy"""

	def __init__(self, experiment, buttonlist=None, timeout=None, \
		visible=False):
	
		"""See openexp._mouse.legacy"""
		
		if experiment.canvas_backend != "psycho":
			raise openexp.exceptions.response_error( \
				"The psycho mouse backend must be used in combination with the psycho canvas backend!")
	
		self.experiment = experiment						
		self.set_buttonlist(buttonlist)
		self.set_timeout(timeout)
		self.mouse = event.Mouse(visible=False, win=self.experiment.window)
		self.set_visible(visible)
		event.mouseButtons = [0, 0, 0]	
				
	def set_buttonlist(self, buttonlist=None):
	
		"""See openexp._mouse.legacy"""
	
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
	
		"""See openexp._mouse.legacy"""
			
		self.timeout = timeout
				
	def set_visible(self, visible=True):
	
		"""See openexp._mouse.legacy"""
	
		self.visible = visible
		self.mouse.setVisible(visible)

	def set_pos(self, pos=(0,0)):

		"""See openexp._mouse.legacy"""	

		if psychopy.visual.openWindows[0].winType == 'pyglet':
			raise openexp.exceptions.response_error( \
				"Method set_pos not supported in pyglet environment (default for psycho back-end)")

		self.mouse.setPos(newPos=pos)
		
	def get_click(self, buttonlist=None, timeout=None, visible=None):
	
		"""See openexp._mouse.legacy"""
		
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
		while True:
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
			if buttons[2] and (buttonlist == None or 3 in buttonlist):
				button = 3
				pos = self.mouse.getPos()
				break
			if timeout != None and time-start_time >= timeout:
				break
		if pos != None:
			pos = pos[0]+self.experiment.width/2, \
				self.experiment.height/2-pos[1]
		self.mouse.setVisible(self.visible)					
		return button, pos, time					
		
	def get_pos(self):
	
		"""See openexp._mouse.legacy"""
	
		x, y = self.mouse.getPos()
		t = self.experiment.time()
		x = x + self.experiment.width/2
		y = self.experiment.height/2 - y
		return (x, y), t

	def get_pressed(self):
	
		"""See openexp._mouse.legacy"""

		return tuple(self.mouse.getPressed(getTime=False))
		
	def flush(self):
	
		"""See openexp._mouse.legacy"""
	
		event.mouseButtons = [0,0,0]
		event.clearEvents()
		return False
		
	def synonyms(self, button):
	
		"""See openexp._mouse.legacy"""
				
		button_map = [ (1, "left_button"), (2, "middle_button"), (3, \
			"right_button"), (4, "scroll_up"), (5, "scroll_down") ]
		for bm in button_map:
			if button in bm:
				return bm
		return []		

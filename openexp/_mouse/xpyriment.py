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

import openexp._mouse.legacy
import pygame
from pygame.locals import *
from expyriment import stimuli
from expyriment.misc.geometry import coordinates2position as c2p

class xpyriment(openexp._mouse.legacy.legacy):

	"""
	Mouse backend built on top of Expyriment. Contains only minor differences
	from the legacy backend to re-implement the custom mouse cursor.
	"""

	def __init__(self, experiment, buttonlist=None, timeout=None, \
		visible=False):
	
		"""See openexp._mouse.legacy"""		
	
		self.experiment = experiment
		self.set_buttonlist(buttonlist)
		self.set_timeout(timeout)
		self.set_visible(visible)		
		if self.experiment.get_check('custom_cursor', 'yes') == 'yes':
			self.cursor = stimuli.Picture(self.experiment.resource( \
				'cursor.png'))
		else:
			self.cursor = None				
		
	def get_click(self, buttonlist=None, timeout=None, visible=None):
	
		"""See openexp._mouse.legacy"""		
	
		if buttonlist == None:
			buttonlist = self.buttonlist
		if timeout == None:
			timeout = self.timeout	
		if visible == None:
			visible = self.visible			
		
		if self.cursor == None:
			pygame.mouse.set_visible(visible)
		elif visible:
			pygame.mouse.set_visible(False)
			bg_surface = self.experiment.window.copy()
			dx, dy = self.cursor.surface_size
			dx /= 2
			dy /= 2
		
		start_time = pygame.time.get_ticks()
		time = start_time		
		
		while timeout == None or time - start_time < timeout:
			time = pygame.time.get_ticks()						
			
			# Draw a cusom cursor if necessary
			if self.cursor != None and visible:
				self.experiment.window.blit(bg_surface, (0,0))		
				x, y = pygame.mouse.get_pos()
				self.cursor.position = c2p((x+dx, y+dy))
				self.cursor.present(clear=False)
			
			# Process the input
			for event in pygame.event.get():								
				if event.type == KEYDOWN and event.key == pygame.K_ESCAPE:
					raise openexp.exceptions.response_error( \
						"The escape key was pressed.")										
				if event.type == MOUSEBUTTONDOWN:
					if buttonlist == None or event.button in buttonlist:
						pygame.mouse.set_visible(self.visible)
						return event.button, event.pos, time
											
		if self.cursor == None:
			pygame.mouse.set_visible(self.visible)					
		return None, None, time		
		

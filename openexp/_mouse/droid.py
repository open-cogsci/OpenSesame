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

import sys
import pygame
from pygame.locals import *
import openexp._mouse.legacy
try:
	import android
except ImportError:
	android = None

class droid(openexp._mouse.legacy.legacy):

	"""
	Mouse back-end for Android devices. Only changes the legacy back-end by
	allowing Android-specific interrupts and not providing a custom mouse
	cursor.
	"""	
	
	def __init__(self, experiment, buttonlist=None, timeout=None, visible=False):
	
		"""See openexp._mouse.legacy"""		
	
		self.experiment = experiment
		self.set_buttonlist(buttonlist)
		self.set_timeout(timeout)
		self.set_visible(visible)		
		
	def get_click(self, buttonlist=None, timeout=None, visible=None):
	
		"""See openexp._mouse.legacy"""		
	
		# clear() command added to prevent carry-over from previous screen-presses.
		pygame.event.clear()
		if android == None:
			pygame.mouse.set_visible(True)
		if buttonlist == None:
			buttonlist = self.buttonlist
		if timeout == None:
			timeout = self.timeout	
		if visible == None:
			visible = self.visible			
		enable_escape = self.experiment.get_check('enable_escape', 'no', \
			['yes', 'no']) == 'yes'		
		start_time = pygame.time.get_ticks()
		time = start_time		
		while timeout == None or time - start_time < timeout:
			time = pygame.time.get_ticks()						
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
					if buttonlist == None or event.button in buttonlist:
						return event.button, event.pos, time						
			# Allow Android interrupt
			if android != None and android.check_pause():
				android.wait_for_resume()				
		return None, None, time
		

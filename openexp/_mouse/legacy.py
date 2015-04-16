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

from libopensesame.py3compat import *

from openexp._mouse import mouse
from openexp._coordinates.legacy import legacy as legacy_coordinates
from libopensesame.exceptions import osexception
import pygame
from pygame.locals import *

class legacy(mouse.mouse, legacy_coordinates):

	"""
	desc:
		This is a mouse backend built on top of PyGame.
		For function specifications and docstrings, see
		`openexp._mouse.mouse`.
	"""

	settings = {
		u"custom_cursor" : {
			u"name" : u"Custom cursor",
			u"description" : u"Bypass the system mouse cursor",
			u"default" : u"no"
			},
		u"enable_escape" : {
			u"name" : u"Enable escape",
			u"description" : u"Abort the experiment when the upper left and right corners are clicked",
			u"default" : u"no",
			}
		}

	def __init__(self, experiment, buttonlist=None, timeout=None,
		visible=False):

		self.experiment = experiment
		self.xcenter = self.experiment.var.width/2
		self.ycenter = self.experiment.var.height/2
		self.set_buttonlist(buttonlist)
		self.set_timeout(timeout)
		self.set_visible(visible)
		self.uniform_coordinates = \
			self.experiment.var.uniform_coordinates==u'yes'
		if self.experiment.var.get('custom_cursor', 'no') == 'yes':
			self.cursor = pygame.image.load(
				self.experiment.resource('cursor.png'))
		else:
			self.cursor = None

	def set_visible(self, visible=True):

		self.visible = visible
		pygame.mouse.set_visible(visible)

	def set_pos(self, pos=(0,0)):

		pygame.mouse.set_pos(self.to_xy(pos))

	def get_click(self, buttonlist=None, timeout=None, visible=None):

		if buttonlist is None:
			buttonlist = self.buttonlist
		if timeout is None:
			timeout = self.timeout
		if visible is None:
			visible = self.visible
		enable_escape = self.experiment.var.get('enable_escape', 'no', \
			['yes', 'no']) == 'yes'
		if self.cursor is None:
			pygame.mouse.set_visible(visible)
		elif visible:
			pygame.mouse.set_visible(False)

		start_time = pygame.time.get_ticks()
		time = start_time

		while True:
			time = pygame.time.get_ticks()

			# Draw a cusom cursor if necessary
			if self.cursor is not None and visible:
				surface = self.experiment.last_shown_canvas.copy()
				surface.blit(self.cursor, pygame.mouse.get_pos())
				self.experiment.surface.blit(surface, (0,0))
				pygame.display.flip()

			# Process the input
			for event in pygame.event.get():
				if event.type == KEYDOWN and event.key == pygame.K_ESCAPE:
					raise osexception( \
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
									if event.pos[0] > self.experiment.var.get( \
										'width')-64 and event.pos[1] < 64:
										raise osexception( \
											"The escape sequence was clicked/ tapped")

					if (buttonlist is None or event.button in buttonlist):
						if self.cursor is None:
							pygame.mouse.set_visible(self.visible)
						return event.button, self.from_xy(event.pos), time
			if timeout is not None and time-start_time >= timeout:
				break

		if self.cursor is None:
			pygame.mouse.set_visible(self.visible)
		return None, None, time

	def get_pos(self):

		pygame.event.get()
		return self.from_xy(pygame.mouse.get_pos()), self.experiment.time()

	def get_pressed(self):

		return pygame.mouse.get_pressed()

	def flush(self):

		buttonclicked = False
		for event in pygame.event.get():
			if event.type == KEYDOWN and event.key == pygame.K_ESCAPE:
				raise osexception(
					"The escape key was pressed.")
			if event.type == MOUSEBUTTONDOWN:
				buttonclicked = True
		return buttonclicked

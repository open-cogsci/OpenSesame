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

from openexp._mouse import legacy
from libopensesame.exceptions import osexception
import pygame
from pygame.locals import *
from expyriment import stimuli
from expyriment.misc.geometry import coordinates2position as c2p

class xpyriment(legacy.legacy):

	"""
	desc:
		This is a mouse backend built on top of PyGame, adapted for Expyriment.
		For function specifications and docstrings, see
		`openexp._mouse.mouse`.
	"""

	settings = {
		u"custom_cursor" : {
			u"name" : u"Custom cursor",
			u"description" : u"Bypass the system mouse cursor",
			u"default" : u"no"
			}
		}

	def __init__(self, experiment, buttonlist=None, timeout=None,
		visible=False):

		self.experiment = experiment
		self.set_buttonlist(buttonlist)
		self.set_timeout(timeout)
		self.set_visible(visible)
		if self.experiment.get_check('custom_cursor', 'no') == 'yes':
			if self.experiment.expyriment.screen._fullscreen:
				raise osexception(
					'The xpyriment mouse back-end does not support custom cursors in fullscreen mode (you can change this in the back-end settings)')
			self.cursor = stimuli.Picture(self.experiment.resource(
				'cursor.png'))
		else:
			self.cursor = None

	def get_click(self, buttonlist=None, timeout=None, visible=None):

		if buttonlist is None:
			buttonlist = self.buttonlist
		if timeout is None:
			timeout = self.timeout
		if visible is None:
			visible = self.visible

		if self.cursor is None:
			pygame.mouse.set_visible(visible)
		elif visible:
			pygame.mouse.set_visible(False)
			bg_surface = self.experiment.last_shown_canvas._get_surface().copy()
			dx, dy = self.cursor.surface_size
			dx /= 2
			dy /= 2

		start_time = pygame.time.get_ticks()
		time = start_time

		while True:
			time = pygame.time.get_ticks()

			# Draw a cusom cursor if necessary
			if self.cursor is not None and visible:
				x, y = pygame.mouse.get_pos()
				self.experiment.window.blit(bg_surface, (0,0))
				self.cursor.position = c2p((x+dx, y+dy))
				self.cursor.present(clear=False)

			# Process the input
			for event in pygame.event.get([MOUSEBUTTONDOWN, KEYDOWN]):
				if event.type == KEYDOWN and event.key == pygame.K_ESCAPE:
					raise osexception( \
						"The escape key was pressed.")
				if event.type == MOUSEBUTTONDOWN:
					if buttonlist is None or event.button in buttonlist:
						pygame.mouse.set_visible(self.visible)

						# Compensate for the fact that the screen is padded
						x, y = event.pos
						x -= (self.experiment.expyriment.screen.window_size[0] \
							-self.experiment.width)/2
						y -= (self.experiment.expyriment.screen.window_size[1] \
							-self.experiment.height)/2

						return event.button, (x,y), time
			if timeout is not None and time-start_time >= timeout:
				break

		if self.cursor is None:
			pygame.mouse.set_visible(self.visible)
		return None, None, time

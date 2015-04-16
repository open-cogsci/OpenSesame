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

import sys
import pygame
from pygame.locals import *
from openexp._mouse import legacy
from libopensesame.exceptions import osexception
try:
	import android
except ImportError:
	android = None

class droid(legacy.legacy):

	"""
	desc:
		This is a mouse backend built on top of PyGame, adapted for android.
		For function specifications and docstrings, see
		`openexp._mouse.mouse`.
	"""

	def __init__(self, experiment, buttonlist=None, timeout=None, visible=False):

		self.experiment = experiment
		self.set_buttonlist(buttonlist)
		self.set_timeout(timeout)
		self.set_visible(visible)
		self.uniform_coordinates = \
			self.experiment.var.uniform_coordinates==u'yes'

	def get_click(self, buttonlist=None, timeout=None, visible=None):

		if android is None:
			pygame.mouse.set_visible(True)
		if buttonlist is None:
			buttonlist = self.buttonlist
		if timeout is None:
			timeout = self.timeout
		if visible is None:
			visible = self.visible
		enable_escape = self.experiment.var.get(u'enable_escape', u'no', \
			[u'yes', u'no']) == u'yes'
		start_time = pygame.time.get_ticks()
		time = start_time
		while timeout is None or time - start_time < timeout:
			time = pygame.time.get_ticks()
			# Process the input
			for event in pygame.event.get():
				if event.type == KEYDOWN and event.key == pygame.K_ESCAPE:
					raise osexception(u"The escape key was pressed.")
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
										u'width')-64 and event.pos[1] < 64:
										raise osexception( \
											u"The escape sequence was clicked/ tapped")
					if buttonlist is None or event.button in buttonlist:
						return event.button, self.from_xy(event.pos), time
			# Allow Android interrupt
			if android is not None and android.check_pause():
				android.wait_for_resume()
		return None, None, time

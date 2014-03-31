#-*- coding:utf-8 -*-

"""
Created on 25-05-2012

Author: Edwin Dalmaijer

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

import pygame
from pygame.locals import *
from pygame.joystick import Joystick
from libopensesame.exceptions import osexception

class legacy:

	def __init__(self, experiment, joybuttonlist=None, timeout=None):

		"""<DOC>
		Intializes the joystick object.

		Arguments:
		experiment		--	An instance of libopensesame.experiment.experiment.

		Keyword arguments:
		joybuttonlist	--	A list of buttons that are accepted or None to
							accept all buttons. (default=None)
		timeout			--	An integer value specifying a timeout in
							milliseconds or None for no timeout. (default=None)
		</DOC>"""


		global js
		pygame.init()
		js = pygame.joystick.Joystick(0)
		js.init()

		self.experiment = experiment
		self.set_joybuttonlist(joybuttonlist)
		self.set_timeout(timeout)

	def set_joybuttonlist(self, joybuttonlist=None):

		"""<DOC>
		Sets a list of accepted buttons.

		Keyword arguments:
		joybuttonlist	--	A list of button numbers that are accepted or None
							to accept all buttons. (default=None)
		</DOC>"""

		if joybuttonlist == None or joybuttonlist == []:
			self._joybuttonlist = None
		else:
			self._joybuttonlist = []
			for joybutton in joybuttonlist:
				self._joybuttonlist.append(joybutton)

	def set_timeout(self, timeout=None):

		"""<DOC>
		Sets a timeout.

		Keyword arguments:
		timeout		--	An integer value specifying a timeout in milliseconds or
						None for no timeout. (default=None)
		</DOC>"""

		self.timeout = timeout

	def get_joybutton(self, joybuttonlist=None, timeout=None):

		"""<DOC>
		Waits for joystick button input.

		Keyword arguments:
		joybuttonlist	--	A list of button numbers that are accepted or
							None to use the default. This parameter does not
							change the default joybuttonlist. (default = None)
		timeout			--	An integer value specifying a timeout in
							milliseconds or None to use the default. This
							parameter does not change the default timeout.
							(default=None)

		Returns:
		A (joybutton, timestamp) tuple. The joybutton is None if a timeout
		occurs.
		</DOC>"""

		if joybuttonlist == None or joybuttonlist == []:
			joybuttonlist = self._joybuttonlist
		if timeout == None:
			timeout = self.timeout

		start_time = pygame.time.get_ticks()
		time = start_time

		while timeout == None or time - start_time <= timeout:
			time = pygame.time.get_ticks()
			for event in pygame.event.get():
				if event.type == KEYDOWN:
					if event.key == pygame.K_ESCAPE:
						raise osexception(u"The escape key was pressed.")
				if event.type == JOYBUTTONDOWN:
					if joybuttonlist == None or event.button + 1 in \
						joybuttonlist:
						bpress = event.button + 1
						return bpress, time

		return None, time

	def get_joyaxes(self, timeout=None):

		"""<DOC>
		Waits for joystick axes movement.

		Keyword arguments:
		timeout		--	An integer value specifying a timeout in milliseconds
						or None to use the default. This parameter does not
						change the default timeout. (default=None)

		Returns:
		A (position, timestamp) tuple. The position is None if a timeout occurs.
		</DOC>"""

		if timeout == None:
			timeout = self.timeout

		pos = []
		start_time = pygame.time.get_ticks()
		time = start_time

		while timeout == None or time - start_time < timeout:
			time = pygame.time.get_ticks()
			for event in pygame.event.get():
				if event.type == KEYDOWN:
					if event.key == pygame.K_ESCAPE:
						raise osexception(u"The escape key was pressed.")
				if event.type == JOYAXISMOTION:
					for axis in range(js.get_numaxes()):
						pos.append(js.get_axis(axis))
					return pos, time

		return None, time

	def get_joyballs(self, timeout=None):

		"""<DOC>
		Waits for joystick trackball movement.

		Keyword arguments:
		timeout		--	An integer value specifying a timeout in milliseconds
						or None to use the default. This parameter does not
						change the default timeout. (default=None)

		Returns:
		A (position, timestamp) tuple. The position is None if a timeout occurs.
		</DOC>"""

		if timeout == None:
			timeout = self.timeout

		ballpos = []
		start_time = pygame.time.get_ticks()
		time = start_time

		while timeout == None or time - start_time < timeout:
			time = pygame.time.get_ticks()
			for event in pygame.event.get():
				if event.type == KEYDOWN:
					if event.key == pygame.K_ESCAPE:
						raise osexception(u"The escape key was pressed.")
				if event.type == JOYBALLMOTION:
					for ball in range(js.get_numballs()):
						ballpos.append(js.get_ball(ball))
					return ballpos, time

		return None, time

	def get_joyhats(self, timeout=None):

		"""<DOC>
		Waits for joystick hat movement.

		Keyword arguments:
		timeout		--	An integer value specifying a timeout in milliseconds
						or None to use the default. This parameter does not
						change the default timeout. (default=None)

		Returns:
		A (position, timestamp) tuple. The position is None if a timeout occurs.
		</DOC>"""

		if timeout == None:
			timeout = self.timeout

		hatpos = []
		start_time = pygame.time.get_ticks()
		time = start_time

		while timeout == None or time - start_time < timeout:
			time = pygame.time.get_ticks()
			for event in pygame.event.get():
				if event.type == KEYDOWN:
					if event.key == pygame.K_ESCAPE:
						raise osexception(u"The escape key was pressed.")
				if event.type == JOYHATMOTION:
					for hat in range(js.get_numhats()):
						hatpos.append(js.get_hat(hat))
					return hatpos, time

		return None, time

	def get_joyinput(self, joybuttonlist=None, timeout=None):

		"""<DOC>
		Waits for any joystick input (buttons, axes, hats or balls).

		Keyword arguments:
		joybuttonlist	--	A list of button numbers that are accepted or
							None to use the default. This parameter does not
							change the default joybuttonlist. (default=None)
		timeout			--	An integer value specifying a timeout in
							milliseconds or None to use the default. This
							parameter does not change the default timeout.
							(default=None)

		Returns:
		A (event, value, timestamp) tuple. The value is None if a timeout
		occurs.
		</DOC>"""

		if joybuttonlist == None or joybuttonlist == []:
			joybuttonlist = self._joybuttonlist
		if timeout == None:
			timeout = self.timeout

		pos = []
		ballpos = []
		hatpos = []
		eventtype = None
		start_time = pygame.time.get_ticks()
		time = start_time

		while timeout == None or time - start_time <= timeout:
			time = pygame.time.get_ticks()
			for event in pygame.event.get():
				if event.type == KEYDOWN:
					if event.key == pygame.K_ESCAPE:
						raise osexception(u"The escape key was pressed.")
				if event.type == JOYBUTTONDOWN:
					if joybuttonlist == None or event.button + 1 in \
						joybuttonlist:
						eventtype = u'joybuttonpress'
						bpress = event.button + 1
						return eventtype, bpress, time
				if event.type == JOYAXISMOTION:
					eventtype = u'joyaxismotion'
					for axis in range(js.get_numaxes()):
						pos.append(js.get_axis(axis))
					return eventtype, pos, time
				if event.type == JOYBALLMOTION:
					eventtype = u'joyballmotion'
					for ball in range(js.get_numballs()):
						ballpos.append(js.get_ball(ball))
					return eventtype, ballpos, time
				if event.type == JOYHATMOTION:
					eventtype = u'joyhatmotion'
					for hat in range(js.get_numhats()):
						hatpos.append(js.get_hat(hat))
					return eventtype, hatpos, time

		return eventtype, None, time

	def input_options(self):

		"""<DOC>
		Generates a list with amount of available buttons, axes, balls and hats.

		Returns:
		List with number of inputs as: [buttons, axes, balls, hats]
		</DOC>"""

		ninputs = [js.get_numbuttons(), js.get_numaxes(), js.get_numballs(), \
			js.get_numhats()]
		return ninputs

	def flush(self):

		"""<DOC>
		Clears all pending input, not limited to the joystick.

		Returns:
		True if a joyinput has been made (i.e., if there was something
		to flush) and False otherwise
		</DOC>"""

		joyinput = False
		for event in pygame.event.get():
			if event.type == KEYDOWN and event.key == pygame.K_ESCAPE:
				raise osexception(u"The escape key was pressed.")
			if event.type == JOYBUTTONDOWN or event.type == JOYAXISMOTION or \
				event.type == JOYBALLMOTION or event.type == JOYHATMOTION:
				joyinput = True
		return joyinput

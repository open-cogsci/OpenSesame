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

from math import hypot
import pygame
from openexp._canvas.legacy import legacy
from libopensesame.exceptions import osexception

try:
	import android
except ImportError:
	android = None

initialized = False
resolution = 1280, 800 # resolution is hardcoded for now

class droid(legacy):

	"""
	This is a canvas backend for Android devices. It is identical to the legacy
	backend, except for the display initialization.
	"""

	@staticmethod
	def init_display(experiment):

		if experiment.resolution() != resolution:
			raise osexception( \
			'The droid back-end requires a resolution of %d x %d. Your display will be scaled automatically to fit devices with different resolutions.' \
			% resolution)

		# Intialize PyGame
		if not pygame.display.get_init():
			pygame.init()
		experiment.window = pygame.display.set_mode(resolution)
		experiment.surface = pygame.display.get_surface()
		# Set the time functions to use pygame
		experiment._time_func = pygame.time.get_ticks
		experiment._sleep_func = pygame.time.delay
		experiment.time = experiment._time_func
		experiment.sleep = experiment._sleep_func
		# Initialze the Android device if necessary
		if android is not None:
			android.init()
			android.map_key(android.KEYCODE_BACK, pygame.K_ESCAPE)
			dpi = android.get_dpi()
		else:
			# A dummy dpi if we are not on Android
			dpi = 96
		# Log the device characteristics
		info = pygame.display.Info()
		diag = hypot(info.current_w, info.current_h) / dpi
		if diag < 6: # 6" is the minimum size to be considered a tablet
			is_tablet = 'yes'
		else:
			is_tablet = 'no'
		experiment.var.device_resolution_width = info.current_w
		experiment.var.device_resolution_height = info.current_h
		experiment.var.device_dpi = dpi
		experiment.var.device_screen_diag = diag
		experiment.var.device_is_tablet = is_tablet

		# Start with a splash screen
		splash = pygame.image.load(experiment.resource('android-splash.jpg'))
		x = resolution[0]/2 - splash.get_width()/2
		y = resolution[1]/2 - splash.get_height()/2
		experiment.surface.blit(splash, (x,y))
		for i in range(10):
			pygame.display.flip()
			pygame.time.delay(100)
		if android is not None and android.check_pause():
			android.wait_for_resume()

	@staticmethod
	def close_display(experiment):

		# On Android, we don't quit the display, as this appears to exit the
		# application altogether.
		if android is None:
			pygame.display.quit()

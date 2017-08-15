# coding=utf-8

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
import os
import pygame
from libopensesame.exceptions import osexception
from openexp._canvas._image.image import Image
from openexp._canvas._element.legacy import LegacyElement


class Legacy(LegacyElement, Image):

	def prepare(self):

		if not hasattr(self, '_image_surface') or self._dirty:
			self._dirty = False
			fname = safe_decode(self.fname)
			if not os.path.isfile(fname):
				raise osexception(u'"%s" does not exist' % fname)
			with open(fname, u'rb') as fd:
				try:
					self._image_surface = pygame.image.load(fd)
				except pygame.error:
					raise osexception(
						u"'%s' is not a supported image format" % fname)
			if self.scale is not None:
				try:
					self._image_surface = pygame.transform.smoothscale(
						self._image_surfacesurface,
						(int(self._image_surface.get_width()*self.scale),
						int(self._image_surface.get_height()*self.scale))
					)
				except:
					self._image_surface = pygame.transform.scale(
						self._image_surface,
						(int(self._image_surface.get_width()*self.scale),
						int(self._image_surface.get_height()*self.scale))
					)
		size = self._image_surface.get_size()
		x, y = self.to_xy(self.x, self.y)
		if self.center:
			x -= size[0] / 2
			y -= size[1] / 2
		self.surface.blit(self._image_surface, (x, y))

	@staticmethod
	def _setter(key, self, val):

		self._dirty = True
		Image._setter(key, self, val)

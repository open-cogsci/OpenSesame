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

		fname = safe_decode(self.fname)
		if not os.path.isfile(fname):
			raise osexception(u'"%s" does not exist' % fname)
		with open(fname, u'rb') as fd:
			try:
				surface = pygame.image.load(fd)
			except pygame.error:
				raise osexception(
					u"'%s' is not a supported image format" % fname)
		if self.scale is not None:
			try:
				surface = pygame.transform.smoothscale(surface,
					(int(surface.get_width()*self.scale),
					int(surface.get_height()*self.scale)))
			except:
				surface = pygame.transform.scale(surface,
					(int(surface.get_width()*self.scale),
					int(surface.get_height()*self.scale)))
		size = surface.get_size()
		x, y = self.to_xy(self.x, self.y)
		if self.center:
			x -= size[0] / 2
			y -= size[1] / 2
		self.surface.blit(surface, (x, y))

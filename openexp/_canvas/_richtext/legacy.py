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
from openexp._canvas._richtext.richtext import RichText
from openexp._canvas._element.legacy import LegacyElement
import pygame


class Legacy(LegacyElement, RichText):

	def prepare(self):

		if not hasattr(self, '_text_surface') or self._dirty:
			im = self._to_pil()
			self._text_surface = pygame.image.fromstring(
				im.tobytes(), im.size, im.mode)
			self._dirty = False
		x, y = self.to_xy(self.x, self.y)
		if self.center:
			x -= self._text_surface.get_width()//2
			y -= self._text_surface.get_height()//2
		self.surface.blit(self._text_surface, (x, y))

	@staticmethod
	def _setter(key, self, val):

		self._dirty = True
		RichText._setter(key, self, val)

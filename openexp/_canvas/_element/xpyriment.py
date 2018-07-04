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
import copy


class XpyrimentElement(object):

	"""
	desc:
		Together with Element, XpyrimentElement is the base object for all
		xpyriment sketchpad elements.
	"""

	ANTI_ALIAS = 1

	@property
	def win(self):
		return self._canvas.experiment.window

	def show(self, **kwargs):

		if self.visible:
			if not hasattr(self, u'_stim'):
				self.prepare()
			self._stim.present(**kwargs)

	def copy(self, canvas):

		e = copy.copy(self)
		e._stim = self._stim.copy()
		e._canvas = canvas
		return e

	def _on_attribute_change(self, **kwargs):

		if self._canvas.auto_prepare:
			self.prepare()

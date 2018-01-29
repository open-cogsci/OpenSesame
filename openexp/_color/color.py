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
import webcolors
import numbers
from libopensesame.exceptions import osexception


class Color(object):

	"""
	desc:
		Converts various color specifications to a back-end specific format.
		Valid color specificatons are described in more detail in
		openexp._canvas.canvas.canvas.
	"""

	def __init__(self, experiment, colorspec):

		"""
		desc:
			Constructor.

		arguments:
			experiment:
				desc:	The experiment object.
				type:	experiment
			colorspec:
				desc:	A color specification.
				type:	[str, unicode, tuple, int]
		"""

		self.experiment = experiment
		self.colorspec = colorspec
		self.hexcolor = self.to_hex(self.colorspec)
		self.backend_color = self.to_backend_color(self.hexcolor)

	def __repr__(self):

		"""
		returns:
			A representation of the color, which matches the color
			specification.
		"""

		return self.colorspec

	@staticmethod
	def to_hex(colorspec):

		"""
		desc:
			Converts a color specificaton to a seven-character lowercase
			hexadecimal color string, such as '#ff0000'.

		arguments:
			colorspec:
				desc:	A color specification.
				type:	[str, unicode, array-like, int]

		returns:
			desc:	A hexadecimal color specification.
			type:	unicode
		"""
		is_rgb = (
			lambda c: hasattr(c, '__len__')
			and len(c) == 3
			and all(isinstance(i, numbers.Integral) and 0 <= i <= 255 for i in c)
		)

		if isinstance(colorspec, int):
			return webcolors.rgb_to_hex((colorspec, colorspec, colorspec))
		if is_rgb(colorspec):
			return webcolors.rgb_to_hex(colorspec)
		if isinstance(colorspec, basestring):
			try:
				colorspec = int(colorspec)
				return webcolors.rgb_to_hex((colorspec, colorspec, colorspec))
			except:
				pass
			if colorspec.startswith(u'#'):
				try:
					return webcolors.rgb_to_hex(
						webcolors.hex_to_rgb(colorspec))
				except:
					raise osexception(
						u'Invalid color specification: %s'
						% safe_decode(colorspec)
					)
			if colorspec.startswith(u'rgb'):
				if u'%' in colorspec:
					l = colorspec[4:-1].split(u',')
					if len(l) != 3:
						raise osexception(
							u'Invalid color specification: %s'
							% safe_decode(colorspec)
						)
					for v in l:
						if u'%' not in v:
							raise osexception(
								u'Invalid color specification: %s'
								% safe_decode(colorspec)
							)
					try:
						l = tuple([v.strip() for v in l])
					except:
						raise osexception(
							u'Invalid color specification: %s'
							% safe_decode(colorspec)
						)
					return webcolors.rgb_percent_to_hex(l)
				l = colorspec[4:-1].split(u',')
				if len(l) != 3:
					raise osexception(
						u'Invalid color specification: %s'
						% safe_decode(colorspec)
					)
				try:
					l = tuple([int(v) for v in l])
				except:
					raise osexception(
						u'Invalid color specification: %s'
						% safe_decode(colorspec)
					)
				return webcolors.rgb_to_hex(l)
			try:
				return webcolors.name_to_hex(colorspec)
			except:
				raise osexception(
					u'Invalid color specification: %s'
					% safe_decode(colorspec)
				)
		raise osexception(
			u'Invalid color specification: %s' % safe_decode(colorspec))

	def to_backend_color(self, hexcolor):

		"""
		desc:
			Converts a hexadecimal color string to a backend-specific color
			object.

		arguments:
			hexcolor:
				desc:	A hexadecimal color specification.
				type:	[str, unicode]

		returns:
			A backend-specific color object.
		"""

		return hexcolor


# Non PEP-8 alias for backwards compatibility
color = Color

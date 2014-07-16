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

from libopensesame import debug
from libqtopensesame.dialogs import sketchpad_dialog
from libqtopensesame.items import qtitem
from libqtopensesame.misc import _

class feedpad:

	"""GUI controls that are common to the sketchpad and the feedback item"""

	def popout(self):

		"""Open a new window for the drawing tool"""

		a = sketchpad_dialog.sketchpad_dialog(
			self.experiment.main_window, self);
		a.exec_()
		self.apply_edit_changes()

	def static_items(self):

		"""
		Returns a list of items which are 'static' in the sense that they don't
		contain variables that make it hard to draw them onto a sketchpad.
		Variables in text and show_if properties are allowed.

		Returns:
		A list of static items
		"""

		l = []
		#for item in self.items:
			#static = True
			#for var in item:
				#if var != "text" and var != "show_if" and type(item[var]) == \
					#unicode and item[var].find("[") >= 0:
					#debug.msg("variable property: %s = %s" % (var, item[var]))
					#static = False
			#if static:
				#l.append(item)
		return l

	def items_out_of_bounds(self):

		"""
		Returns a count of items that are 'out of bounds' in the sense that the
		coordinates fall outside of the screen boundaries.

		Returns:
		The nr of items the are out of bounds
		"""

		xc = self.get("width")/2
		yc = self.get("height")/2
		return sum( ["x" in i and "y" in i
			and ( (type(i["x"]) not in (str, unicode) and abs(i["x"]) > xc)
			or (type(i["y"]) not in (str, unicode) and abs(i["y"]) > yc) )
			for i in self.items] )



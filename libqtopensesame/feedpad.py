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

import libqtopensesame.sketchpad_dialog
import libqtopensesame.qtitem

class feedpad:

	"""GUI controls that are common to the sketchpad and the feedback item"""

	def popout(self):

		"""Open a new window for the drawing tool"""

		a = libqtopensesame.sketchpad_dialog.sketchpad_dialog(self.experiment.ui.centralwidget, self);
		a.exec_()
		self.apply_edit_changes()

	def static_items(self):

		"""
		Returns a list of items which are 'static' in the sense that they don't contain variables
		that make it hard to draw them onto a sketchpad. Variables in text and show_if properties
		are allowed.

		Returns:
		A list of static items
		"""

		l = []
		for item in self.items:
			static = True
			for var in item:
				if var != "text" and var != "show_if" and type(item[var]) == str and item[var].find("[") >= 0:
					if self.experiment.debug:
						print "sketchpad.static_items(): variable property: %s = %s" % (var, item[var])
					static = False
			if static:
				l.append(item)
		return l

	def item_tree_info(self):

		"""
		Returns an info string for the item tree widget

		Returns:
		An info string
		"""

		if type(self.duration) == int:
			if self.duration <= 0:
				return "no delay"
			return "%s ms" % self.duration

		if "[" in self.duration:
			return "variable duration"

		return "until %s" % self.duration


#-*- coding:utf-8 -*-

"""
This file is part of openexp.

openexp is free software: you can redistribute it and/or modify
it under the terms of the GNU General Public License as published by
the Free Software Foundation, either version 3 of the License, or
(at your option) any later version.

openexp is distributed in the hope that it will be useful,
but WITHOUT ANY WARRANTY; without even the implied warranty of
MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
GNU General Public License for more details.

You should have received a copy of the GNU General Public License
along with openexp.  If not, see <http://www.gnu.org/licenses/>.
"""

from libopensesame.exceptions import osexception
from libqtopensesame.misc import _
from PyQt4 import QtGui, QtCore

class base_element(object):

	"""
	desc:
		A base class for the sketchpad-element GUIs.
	"""

	def __init__(self, sketchpad, string=None, properties=None):

		"""
		desc:
			Constructor.

		arguments:
			sketchpad:	A sketchpad object.
			type:		sketchpad

		keywords:
			string:
				desc:	An element-definition string.
				type:	[str, unicode, NoneType]
			properties:
				desc:	A dictionary with element properties. If a dictionary
						is provided, the string keyword is ignored, and a
						definition string is created from the properties dict.
				type:	[dict, NoneType]
		"""

		if properties != None:
			string = u'draw %s' % (self.__class__.__name__)
			for var, val in properties.items():
				string += u' %s="%s"' % (var, val)
		super(base_element, self).__init__(sketchpad, string)
		self.selected = False
		self.highlighted = False

	@property
	def main_window(self):
		return self.experiment.main_window

	@property
	def theme(self):
		return self.experiment.main_window.theme

	def draw(self):

		"""
		desc:
			Draw this element, without redrawing the entire sketchpad.
		"""

		self.graphics_item = super(base_element, self).draw()
		self.graphics_item.element = self
		self.graphics_item.setToolTip(self.to_string())
		self.update()

	def move(self, dx=0, dy=0):

		"""
		desc:
			Moves the element position.

		keywords:
			dx:		The horizontal movement.
			dy:		The vertical movement.
		"""

		for var, val in self.properties.items():
			if var in [u'x', u'x1', u'x2']:
				self.properties[var] += dx
			if var in [u'y', u'y1', u'y2']:
				self.properties[var] += dy

	def set_pos(self, x=0, y=0):

		"""
		desc:
			Sets the element position.

		keywords:
			x:		The horizontal position.
			y:		The vertical position.
		"""

		self.properties[u'x'] = x
		self.properties[u'y'] = y

	def get_pos(self):

		"""
		desc:
			Gets the element position.

		returns:
			desc:	An (x,y) tuple.
			type:	tuple
		"""

		if u'x' in self.properties:
			return self.properties[u'x'], self.properties[u'y']
		return self.properties[u'x1'], self.properties[u'y1']

	def update(self):

		"""
		desc:
			Redraws this element.
		"""

		if self.highlighted:
			self.graphics_item.setGraphicsEffect(self.highlighted_effect())
		elif self.selected:
			self.graphics_item.setGraphicsEffect(self.selected_effect())
		else:
			self.graphics_item.setGraphicsEffect(None)

	def highlight(self, highlighted=True):

		"""
		desc:
			Sets the highlight status of the element and redraws.

		arguments:
			highlighted:	A bool indicating the highlight status.
		"""

		self.highlighted = highlighted
		self.update()

	def select(self, selected=True):

		"""
		desc:
			Sets the selected status of the element and redraws.

		arguments:
			selected:	A bool indicating the selected status.
		"""

		self.selected = selected
		self.update()

	def selected_effect(self):

		"""
		desc:
			Creates the selected effect.

		returns:
			A QGraphicsEffect object.
		"""

		effect = QtGui.QGraphicsDropShadowEffect()
		effect.setColor(QtGui.QColor('#00FF00'))
		effect.setBlurRadius(32)
		effect.setOffset(8,8)
		return effect

	def highlighted_effect(self):

		"""
		desc:
			Creates the highlighted effect.

		returns:
			A QGraphicsEffect object.
		"""


		effect = QtGui.QGraphicsOpacityEffect()
		return effect

	def get_property(self, name, _type=unicode):

		"""
		desc:
			Gets an element property.

		arguments:
			name:	The property name.

		keywords:
			_type:	The property type.

		returns:
			The property in the specified type, or None if the property doesn't
			exist.
		"""

		properties = self.eval_properties()
		if name not in properties:
			return None
		val = properties[name]
		if _type == unicode:
			return unicode(val)
		if _type == int:
			return int(val)
		if _type == float:
			return float(val)
		if _type == bool:
			if val in (u'yes', u'1'):
				return True
			if val in (u'no', u'0'):
				return False
			return bool(val)
		raise osexception(u'Unknown type: %s' % _type)

	def set_property(self, name, val, yes_no=False):

		"""
		desc:
			Sets an element property.

		arguments:
			name:	The property name.
			val:	The property value.

		keywords:
			yes_no:	Indicates whether the value should be treated as a bool and
					recoded to yes/ no.
		"""

		if name not in self.properties:
			return None
		if yes_no:
			if val:
				val = u'yes'
			else:
				val = u'no'
		self.properties[name] = val

	def show_script_edit_dialog(self):

		"""
		desc:
			Shows the script-edit dialog.
		"""

		old_string = self.to_string()
		string = self.experiment.text_input(_(u'Edit element'),
			message=_(u'Element script'), content=self.to_string(),
			parent=self.sketchpad._edit_widget)
		if string == None:
			return
		try:
			self.from_string(string)
		except osexception as e:
			self.experiment.notify(e)
			self.main_window.print_debug_window(e)
			self.from_string(old_string)
			return
		self.sketchpad.draw()

	def show_edit_dialog(self):

		"""
		desc:
			Shows an edit dialog for the element, typically to edit the element
			script.
		"""

		self.show_script_edit_dialog()

	def show_context_menu(self, pos):

		"""
		desc:
			Shows a context menu for the element.

		arguments:
			pos:
				type:	QPoint
		"""

		from libqtopensesame._input.popup_menu import popup_menu
		pm = popup_menu(self.main_window, [
			(0, _(u'Edit script'), u'utilities-terminal'),
			(1, _(u'Raise to front'), u'go-top'),
			(2, _(u'Lower to bottom'), u'go-bottom'),
			(3, _(u'Delete'), u'edit-delete'),
			])
		resp = pm.show()
		if resp == None:
			return
		if resp == 0:
			self.show_script_edit_dialog()
		elif resp == 1:
			self.properties[u'z_index'] = self.sketchpad.min_z_index() - 1
		elif resp == 2:
			self.properties[u'z_index'] = self.sketchpad.max_z_index() + 1
		elif resp == 3:
			self.sketchpad.remove_elements([self])
		self.sketchpad.draw()

	@classmethod
	def mouse_press(cls, sketchpad, pos):

		"""
		desc:
			A static method that processes mouse clicks and returns an element
			object when one has been created.

		arguments:
			sketchpad:	A sketchpad object.
			pos:		An (x,y) tuple with mouse-click coordinates.

		returns:
			An element object, or None if no element was created.
		"""

		return None

	@classmethod
	def mouse_release(cls, sketchpad, pos):

		"""
		desc:
			A static method that processes mouse releases and returns an element
			object when one has been created.

		arguments:
			sketchpad:	A sketchpad object.
			pos:		An (x,y) tuple with mouse-release coordinates.

		returns:
			An element object, or None if no element was created.
		"""

		pass

	@classmethod
	def mouse_move(cls, sketchpad, pos):

		"""
		desc:
			A static method that processes mouse moves, and gives elements the
			opportunity to update their preview.

		arguments:
			sketchpad:	A sketchpad object.
			pos:		An (x,y) tuple with mousecoordinates.
		"""

		pass

	@classmethod
	def reset(cls, sketchpad):

		pass

	@staticmethod
	def requires_text():

		"""
		desc:
			Indicates whether the element requires text settings.

		returns:
			type:	bool
		"""

		return False

	@staticmethod
	def requires_penwidth():

		"""
		desc:
			Indicates whether the element requires penwidth settings.

		returns:
			type:	bool
		"""

		return False

	@staticmethod
	def requires_color():

		"""
		desc:
			Indicates whether the element requires color settings.

		returns:
			type:	bool
		"""

		return False

	@staticmethod
	def requires_arrow_size():

		"""
		desc:
			Indicates whether the element requires arrow-size settings.

		returns:
			type:	bool
		"""

		return False

	@staticmethod
	def requires_scale():

		"""
		desc:
			Indicates whether the element requires scale settings.

		returns:
			type:	bool
		"""

		return False

	@staticmethod
	def requires_fill():

		"""
		desc:
			Indicates whether the element requires fill settings.

		returns:
			type:	bool
		"""

		return False

	@staticmethod
	def requires_center():

		"""
		desc:
			Indicates whether the element requires center settings.

		returns:
			type:	bool
		"""

		return False

	@staticmethod
	def requires_show_if():

		"""
		desc:
			Indicates whether the element requires show-if settings.

		returns:
			type:	bool
		"""

		return True

	@staticmethod
	def cursor():

		"""
		desc:
			Indicates which cursor should be shown when the element tool is
			selected.

		returns:
			desc:	A Qt::CursorShape value
			type:	int
		"""

		return QtCore.Qt.CrossCursor

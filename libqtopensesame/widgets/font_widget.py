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

from PyQt4 import QtCore, QtGui
from libqtopensesame.widgets.base_widget import base_widget
from libqtopensesame.misc import _

class font_widget_base(base_widget):

	"""A font selection widget"""

	max_size = 64
	font_list = [u'mono', u'sans', u'serif', u'arabic', \
		u'chinese-japanese-korean', u'hebrew', u'hindi', _(u'other ...', \
		context=u'font_widget')]

	font_changed = QtCore.pyqtSignal(['QString', int, bool, bool])

	def _apply(self):

		"""Applies the controls."""

		self.family = self.ui.combobox_family.currentText()
		self.size = self.ui.spinbox_size.value()
		self.italic = self.ui.checkbox_italic.isChecked()
		self.bold = self.ui.checkbox_bold.isChecked()
		self.ui.label_example.setFont(self.get_font())
		self.emit(QtCore.SIGNAL(u"font_changed"))
		self.font_changed.emit(self.family, self.size, self.italic, self.bold)

	def apply_family(self):

		"""
		Applies the controls and optionally presents a full font selection
		dialog if the user has selected 'other ...'
		"""

		if self.ui.combobox_family.currentText() == _(u'other ...', context= \
			u'font_widget'):
			font, ok = QtGui.QFontDialog.getFont(self.get_font())
			if ok:
				self.family = unicode(font.family())
			else:
				self.family = self.experiment.get(u'font_family')
			self.update_family_combobox()
		self._apply()

	def get_font(self):

		"""
		Make a QFont based on the settings

		Returns:
		A QFont
		"""

		if self.bold:
			weight = QtGui.QFont.Bold
		else:
			weight = QtGui.QFont.Normal
		return QtGui.QFont(self.family, min(self.max_size, self.size), weight, \
			self.italic)

	def set_font(self, family=None, italic=None, bold=None, size=None):

		"""
		desc:
			Sets the widget to the specified font. For keywords, see
			initialize().
		"""


		self.ui.combobox_family.activated.disconnect()
		self.ui.checkbox_italic.clicked.disconnect()
		self.ui.checkbox_bold.clicked.disconnect()
		self.ui.spinbox_size.editingFinished.disconnect()
		self.initialize(family=family, italic=italic, bold=bold, size=size)

	def initialize(self, experiment=None, family=None, italic=None, bold=None,
		size=None):

		"""
		Initializes the widget.

		Arguments:
		experiment	--	The experiment.

		Keyword arguments:
		family		--	The font family or None to use experiment default.
						(default=None)
		italic		--	The font italic state or None to use experiment default.
						(default=None)
		bold		--	The font bold state or None to use experiment default.
						(default=None)
		size		--	The font size or None to use experiment default.
						(default=None)
		"""

		if experiment == None:
			experiment = self.experiment
		if family == None:
			self.family = experiment.get(u'font_family')
		else:
			self.family = family
		if italic == None:
			self.italic = experiment.get(u'font_italic') == u'yes'
		else:
			self.italic = italic
		if bold == None:
			self.bold = experiment.get(u'font_bold') == u'yes'
		else:
			self.bold = bold
		if size == None:
			self.size = experiment.get(u'font_size')
		else:
			self.size = size
		if self.ui.combobox_family.findText(self.family) < 0:
			self.ui.combobox_family.addItem(self.family)
		self.ui.combobox_family.setCurrentIndex(
			self.ui.combobox_family.findText(self.family))
		self.ui.checkbox_italic.setChecked(self.italic)
		self.ui.checkbox_bold.setChecked(self.bold)
		self.ui.spinbox_size.setValue(self.size)
		self._apply()
		self.ui.combobox_family.activated.connect(self.apply_family)
		self.ui.checkbox_italic.clicked.connect(self._apply)
		self.ui.checkbox_bold.clicked.connect(self._apply)
		self.ui.spinbox_size.editingFinished.connect(self._apply)

	def update_family_combobox(self):

		"""Updates the family combobox to include a custom font."""

		self.ui.combobox_family.activated.disconnect()
		self.ui.combobox_family.clear()
		l = self.font_list[:]
		if self.family not in l:
			l += [self.family]
		self.ui.combobox_family.insertItems(0, l)
		self.ui.combobox_family.setCurrentIndex(
			self.ui.combobox_family.findText(self.family))
		self.ui.combobox_family.activated.connect(self.apply_family)

class font_widget_horizontal(font_widget_base):

	def __init__(self, main_window):

		"""
		Constructor.

		Arguments:
		experiment	--	The experiment.

		Keywords arguments:
		parent		--	The parent QWidget. (default=None)
		"""

		super(font_widget_horizontal, self).__init__(main_window,
			ui=u'widgets.font_widget_horizontal')

class font_widget(font_widget_base):

	def __init__(self, main_window):

		"""
		Constructor.

		Arguments:
		experiment	--	The experiment.

		Keywords arguments:
		parent		--	The parent QWidget. (default=None)
		"""

		super(font_widget, self).__init__(main_window,
			ui=u'widgets.font_widget')

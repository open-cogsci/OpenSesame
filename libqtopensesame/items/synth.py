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

from libopensesame.synth import synth as synth_runtime
from libqtopensesame.misc import _
from libqtopensesame.items.qtplugin import qtplugin
from libqtopensesame.widgets.synth_widget import synth_widget
from libqtopensesame.validators import duration_validator
from PyQt4 import QtCore, QtGui

class synth(synth_runtime, qtplugin):

	"""
	desc:
		GUI controls for the synth item.
	"""

	def __init__(self, name, experiment, string=None):

		"""See item."""

		synth_runtime.__init__(self, name, experiment, string)
		qtplugin.__init__(self)

	def init_edit_widget(self):

		"""See qtitem."""

		super(synth, self).init_edit_widget(self)
		self.synth_widget = synth_widget(self.main_window)
		self.add_widget(self.synth_widget)
		self.add_stretch()
		self.auto_add_widget(self.synth_widget.ui.edit_freq, u'freq')
		self.auto_add_widget(self.synth_widget.ui.spin_attack, u'attack')
		self.auto_add_widget(self.synth_widget.ui.spin_decay, u'decay')
		self.auto_add_widget(self.synth_widget.ui.spin_volume, u'volume')
		self.auto_add_widget(self.synth_widget.ui.spin_pan, u'pan')
		self.auto_add_widget(self.synth_widget.ui.spin_length, u'length')
		self.auto_add_widget(self.synth_widget.ui.edit_duration, u'duration')
		self.synth_widget.ui.edit_duration.setValidator(
			duration_validator(self, default=u'sound'))
		self.synth_widget.ui.dial_attack.valueChanged.connect(self.apply_dials)
		self.synth_widget.ui.dial_decay.valueChanged.connect(self.apply_dials)
		self.synth_widget.ui.dial_pan.valueChanged.connect(self.apply_dials)
		self.synth_widget.ui.dial_volume.valueChanged.connect(self.apply_dials)
		self.synth_widget.ui.button_sine.clicked.connect(self.set_sine)
		self.synth_widget.ui.button_saw.clicked.connect(self.set_saw)
		self.synth_widget.ui.button_square.clicked.connect(self.set_square)
		self.synth_widget.ui.button_white_noise.clicked.connect(
			self.set_white_noise)

	def apply_edit_changes(self):

		"""See qtitem."""

		super(synth, self).apply_edit_changes()
		self.update_dials()

	def apply_script_changes(self):

		"""See qtitem."""

		super(synth, self).apply_script_changes()
		self.update_dials()

	def update_dials(self):

		"""
		desc:
			Updates the dials to match the corresponding spinboxes.
		"""

		self.synth_widget.ui.dial_pan.setDisabled(
			type(self.get(u'pan', _eval=False)) not in (int, float))
		self.synth_widget.ui.dial_decay.setDisabled(
			type(self.get(u'decay', _eval=False)) not in (int, float))
		self.synth_widget.ui.dial_attack.setDisabled(
			type(self.get(u'attack', _eval=False)) not in (int, float))
		self.synth_widget.ui.dial_volume.setDisabled(
			type(self.get(u'volume', _eval=False)) not in (int, float))
		self.synth_widget.ui.dial_pan.setValue(
			self.synth_widget.ui.spin_pan.value())
		self.synth_widget.ui.dial_decay.setValue(
			self.synth_widget.ui.spin_decay.value())
		self.synth_widget.ui.dial_attack.setValue(
			self.synth_widget.ui.spin_attack.value())
		self.synth_widget.ui.dial_volume.setValue(
			100*self.synth_widget.ui.spin_volume.value())

	def apply_dials(self):

		"""
		desc:
			Applies changes to the dials.
		"""

		if self.synth_widget.ui.dial_attack.isEnabled():
			self.set(u"attack", self.synth_widget.ui.dial_attack.value())
		if self.synth_widget.ui.dial_decay.isEnabled():
			self.set(u"decay", self.synth_widget.ui.dial_decay.value())
		if self.synth_widget.ui.dial_pan.isEnabled():
			self.set(u"pan", self.synth_widget.ui.dial_pan.value())
		if self.synth_widget.ui.dial_volume.isEnabled():
			self.set(u"volume", .01*self.synth_widget.ui.dial_volume.value())
		self.edit_widget()
		self.update_script()

	def edit_widget(self):

		"""See qtitem."""

		super(synth, self).edit_widget()
		osc = self.get(u'osc', _eval=False)
		self.synth_widget.ui.button_sine.setChecked(osc == u'sine')
		self.synth_widget.ui.button_saw.setChecked(osc == u'saw')
		self.synth_widget.ui.button_square.setChecked(osc == u'square')
		self.synth_widget.ui.button_white_noise.setChecked(osc == u'noise')

	def set_sine(self):

		"""
		desc:
			Selects the sine oscillator
		"""

		self.set(u"osc", u"sine")
		self.update()

	def set_saw(self):

		"""
		desc:
			Selects the saw oscillator
		"""

		self.set(u"osc", u"saw")
		self.update()

	def set_square(self):

		"""
		desc:
			Selects the square oscillator
		"""

		self.set(u"osc", u"square")
		self.update()

	def set_white_noise(self):

		"""
		desc:
			Selects the noise oscillator
		"""

		self.set(u"osc", u"white_noise")
		self.update()

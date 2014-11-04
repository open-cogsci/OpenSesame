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

from libopensesame.sampler import sampler as sampler_runtime
from libqtopensesame.misc import _
from libqtopensesame.items.qtplugin import qtplugin
from libqtopensesame.widgets.sampler_widget import sampler_widget
from libqtopensesame.widgets import pool_widget
from libqtopensesame.validators import duration_validator
from PyQt4 import QtCore, QtGui

class sampler(sampler_runtime, qtplugin):

	"""
	desc:
		GUI controls for the sampler item.
	"""

	def __init__(self, name, experiment, string=None):

		"""See item."""

		sampler_runtime.__init__(self, name, experiment, string)
		qtplugin.__init__(self)

	def init_edit_widget(self):

		"""See qtitem."""

		super(sampler, self).init_edit_widget()
		self.sampler_widget = sampler_widget(self.main_window)
		self.add_widget(self.sampler_widget)
		self.add_stretch()
		self.auto_add_widget(self.sampler_widget.ui.spin_pan, u'pan')
		self.auto_add_widget(self.sampler_widget.ui.spin_volume, u'volume')
		self.auto_add_widget(self.sampler_widget.ui.spin_pitch, u'pitch')
		self.auto_add_widget(self.sampler_widget.ui.spin_stop_after,
			u'stop_after')
		self.auto_add_widget(self.sampler_widget.ui.spin_fade_in, u'fade_in')
		self.auto_add_widget(self.sampler_widget.ui.edit_sample, u'sample')
		self.auto_add_widget(self.sampler_widget.ui.edit_duration, u'duration')
		self.auto_add_widget(self.sampler_widget.ui.spin_pan, u'pan')
		self.sampler_widget.ui.edit_duration.setValidator(
			duration_validator(self, default=u'sound'))
		self.sampler_widget.ui.button_browse_sample.clicked.connect(
			self.browse_sample)
		self.sampler_widget.ui.dial_pan.sliderMoved.connect(self.apply_dials)
		self.sampler_widget.ui.dial_volume.sliderMoved.connect(self.apply_dials)
		self.sampler_widget.ui.dial_pitch.sliderMoved.connect(self.apply_dials)
		self.set_focus_widget(self.sampler_widget.ui.edit_sample, override=True)
		self.update_dials()

	def browse_sample(self):

		"""
		desc:
			Presents a file dialog to browse for the sample.
		"""

		s = pool_widget.select_from_pool(self.main_window)
		if unicode(s) == u'':
			return
		self.sampler_widget.ui.edit_sample.setText(s)
		self.apply_edit_changes()

	def apply_edit_changes(self):

		"""See qtitem."""

		super(sampler, self).apply_edit_changes()
		self.update_dials()

	def apply_script_changes(self):

		"""See qtitem."""

		super(sampler, self).apply_script_changes()
		self.update_dials()

	def update_dials(self):

		"""
		desc:
			Updates the dials to match the corresponding spinboxes.
		"""

		self.sampler_widget.ui.dial_pan.setDisabled(
			type(self.get(u'pan', _eval=False)) not in (int, float))
		self.sampler_widget.ui.dial_pitch.setDisabled(
			type(self.get(u'pitch', _eval=False)) not in (int, float))
		self.sampler_widget.ui.dial_volume.setDisabled(
			type(self.get(u'volume', _eval=False)) not in (int, float))
		self.sampler_widget.ui.dial_pan.setValue(
			self.sampler_widget.ui.spin_pan.value())
		self.sampler_widget.ui.dial_pitch.setValue(
			100*self.sampler_widget.ui.spin_pitch.value())
		self.sampler_widget.ui.dial_volume.setValue(
			100*self.sampler_widget.ui.spin_volume.value())

	def apply_dials(self):

		"""
		desc:
			Applies changes to the dials.
		"""

		if self.sampler_widget.ui.dial_pan.isEnabled():
			self.set(u"pan", self.sampler_widget.ui.dial_pan.value())
		if self.sampler_widget.ui.dial_pitch.isEnabled():
			self.set(u"pitch", .01*self.sampler_widget.ui.dial_pitch.value())
		if self.sampler_widget.ui.dial_volume.isEnabled():
			self.set(u"volume", .01*self.sampler_widget.ui.dial_volume.value())
		self.edit_widget()
		self.update_script()

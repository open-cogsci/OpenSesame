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
from libopensesame.synth import synth as synth_runtime
from libqtopensesame.items.qtplugin import qtplugin
from libqtopensesame.validators import duration_validator
from libqtopensesame.misc.translate import translation_context
_ = translation_context(u'synth', category=u'item')

class synth(synth_runtime, qtplugin):

	"""
	desc:
		GUI controls for the synth item.
	"""

	description = _(u'A basic sound synthesizer')

	def __init__(self, name, experiment, string=None):

		"""See item."""

		synth_runtime.__init__(self, name, experiment, string)
		qtplugin.__init__(self)

	def init_edit_widget(self):

		"""See qtitem."""

		qtplugin.init_edit_widget(self)
		self.add_combobox_control(u'osc', _(u'Waveform'),
			[u'sine', u'saw', u'square', u'white_noise'],
			tooltip=_(u'The waveform for the sound'))
		self.add_line_edit_control(u'freq',
			_(u'Frequency (in Hz) or note (e.g. \'A1\')'),
			tooltip=_(u'A frequency (in Hz) or a note (e.g. \'A1\''))
		self.add_spinbox_control(u'attack', _(u'Attack'),
			min_val=0, max_val=10000000,
			tooltip=_(u'The attack (or fade-in) time'), suffix=_(u' ms'))
		self.add_spinbox_control(u'decay', _(u'Decay'),
			min_val=0, max_val=10000000,
			tooltip=_(u'The decay (or fade-out) time'), suffix=_(u' ms'))
		self.add_doublespinbox_control(u'volume', _(u'Volume'),
			min_val=0, max_val=1,
			tooltip=_(u'The sound volume'), suffix=_(u' x maximum'))
		self.add_doublespinbox_control(u'pan', _(u'Panning'),
			min_val=-20, max_val=20, suffix=_(u' toward right'),
			tooltip=_(u'The panning of the sound. Left is negative, right is positive.'))
		self.add_spinbox_control(u'length', _(u'Length'),
			min_val=0, max_val=10000000,
			tooltip=_(u'The sound length'), suffix=_(u' ms'))
		self.add_line_edit_control(u'duration', _(u'Duration'),
			tooltip=_(u"Expecting a duration in ms, 'sound' (to wait until the sound is finished playing), 'keypress', 'mouseclick', or a variable (e.g., '[synth_dur]')."),
			validator=duration_validator(self, default=u'sound'))

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
	help_url = u'manual/stimuli/sound'
	lazy_init = True

	def __init__(self, name, experiment, string=None):

		"""See item."""

		synth_runtime.__init__(self, name, experiment, string)
		qtplugin.__init__(self)

	def init_edit_widget(self):

		"""See qtitem."""

		qtplugin.init_edit_widget(self)
		self.add_combobox_control(u'osc', _(u'Waveform'),
			[u'sine', u'saw', u'square', u'white_noise'])
		self.add_line_edit_control(u'freq',
			_(u'Frequency'),
			info=_(u'In Hertz or as note, e.g. "A1"'))
		self.add_spinbox_control(u'attack', _(u'Attack'),
			min_val=0, max_val=10000000, suffix=_(u' ms'))
		self.add_spinbox_control(u'decay', _(u'Decay'),
			min_val=0, max_val=10000000, suffix=_(u' ms'))
		self.add_doublespinbox_control(u'volume', _(u'Volume'),
			min_val=0, max_val=1, suffix=_(u' x maximum'))
		self.add_line_edit_control(u'pan', _(u'Panning'),
			info=_(u'Positive values toward the right; "left" or "right" for full panning'))
		self.add_spinbox_control(u'length', _(u'Length'),
			min_val=0, max_val=10000000, suffix=_(u' ms'))
		self.add_line_edit_control(u'duration', _(u'Duration'),
			info=_(u'In milliseconds, "sound", "keypress", or "mouseclick"'),
			validator=duration_validator(self, default=u'sound'))

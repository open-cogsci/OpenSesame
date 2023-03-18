# -*- coding:utf-8 -*-

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
from libopensesame.synth import Synth as SynthRuntime
from libqtopensesame.items.qtplugin import QtPlugin
from libqtopensesame.validators import DurationValidator
from libqtopensesame.misc.translate import translation_context
_ = translation_context('synth', category='item')


class Synth(SynthRuntime, QtPlugin):
    """GUI controls for the synth item."""
    
    description = _('A basic sound synthesizer')
    help_url = 'manual/stimuli/sound'
    lazy_init = True

    def __init__(self, name, experiment, string=None):
        SynthRuntime.__init__(self, name, experiment, string)
        QtPlugin.__init__(self)

    def init_edit_widget(self):
        super().init_edit_widget()
        self.add_combobox_control(
            'osc', _('Waveform'),
            ['sine', 'saw', 'square', 'white_noise'])
        self.add_line_edit_control(
            'freq', _('Frequency'), info=_('In Hertz or as note, e.g. "A1"'))
        self.add_spinbox_control(
            'attack', _('Attack'), min_val=0, max_val=10000000,
            suffix=_(' ms'))
        self.add_spinbox_control(
            'decay', _('Decay'), min_val=0, max_val=10000000, suffix=_(' ms'))
        self.add_doublespinbox_control(
            'volume', _('Volume'), min_val=0, max_val=1,
            suffix=_(' x maximum'))
        self.add_line_edit_control(
            'pan', _('Panning'),
            info=_('Positive values toward the right; "left" or "right" for full panning'))
        self.add_spinbox_control(
            'length', _('Length'), min_val=0, max_val=10000000,
            suffix=_(' ms'))
        self.add_line_edit_control(
            'duration', _('Duration'),
            info=_('In milliseconds, "sound", "keypress", or "mouseclick"'),
            validator=DurationValidator(self, default='sound'))


# Alias for backwards compatibility
synth = Synth

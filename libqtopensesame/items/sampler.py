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
from libopensesame.sampler import Sampler as SamplerRuntime
from libqtopensesame.items.qtplugin import QtPlugin
from libqtopensesame.validators import DurationValidator
from libqtopensesame.misc.translate import translation_context
_ = translation_context(u'sampler', category=u'item')


class Sampler(SamplerRuntime, QtPlugin):

    r"""GUI controls for the sampler item."""
    description = _(u'Plays a sound file in .wav or .ogg format')
    help_url = u'manual/stimuli/sound'
    lazy_init = True

    def __init__(self, name, experiment, string=None):
        """See item."""
        SamplerRuntime.__init__(self, name, experiment, string)
        QtPlugin.__init__(self)

    def init_edit_widget(self):
        """See qtitem."""
        QtPlugin.init_edit_widget(self)
        self.add_filepool_control(u'sample', _(u'Sound file'),
                                  info=_(u'In .ogg or .wav format'))
        self.add_doublespinbox_control(u'volume', _(u'Volume'),
                                       min_val=0, max_val=1,
                                       suffix=_(u' x original'))
        self.add_line_edit_control(u'pan', _(u'Panning'),
                                   info=_(u'Positive values toward the right; "left" or "right" for full panning'))
        self.add_doublespinbox_control(u'pitch', _(u'Pitch'), min_val=0,
                                       max_val=1000, suffix=_(u' x original'))
        self.add_spinbox_control(u'stop_after', _(u'Stop after'),
                                 min_val=0, max_val=10000000, suffix=_(u' ms'))
        self.add_spinbox_control(u'fade_in', _(u'Fade in'),
                                 min_val=0, max_val=10000000, suffix=_(u' ms'))
        self.add_line_edit_control(u'duration', _(u'Duration'),
                                   info=_(u'In milliseconds, "sound", "keypress", or "mouseclick"'),
                                   validator=DurationValidator(self, default=u'sound'))


# Alias for backwards compatibilit
sampler = Sampler

# coding=utf-8

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
from libqtopensesame.extensions import BaseExtension
from libqtopensesame.misc import display
from libqtopensesame.misc.translate import translation_context
_ = translation_context(u'system_check', category=u'extension')


class SystemCheck(BaseExtension):

    def event_startup(self):
        r"""Performs several checks when OpenSesame is started. For now, it
        only checks whether the display is scaled or not, and if so, provides a
        warning because this may affect how stimuli look during the experiment.
        """
        if display.display_scaling != 1:
            self.extension_manager.fire(
                u'notify',
                message=_(
                    u'Display scaling is set to %d%% by the operating system. '
                    u'This may affect the appearance of your experiment.'
                ) % (100*display.display_scaling),
                category=u'warning',
                timeout=5000
            )

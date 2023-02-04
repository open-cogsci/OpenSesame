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
from libopensesame import sketchpad


class feedback(sketchpad.sketchpad):

    description = u'Provides feedback to the participant'

    def reset(self):
        """See item."""

        super(feedback, self).reset()
        self.var.reset_variables = u'yes'

    def prepare(self):
        """Prepares the item."""

        pass

    def run(self):
        """Runs the item."""

        sketchpad.sketchpad.prepare(self)
        sketchpad.sketchpad.run(self)
        if self.var.reset_variables == u'yes':
            self.experiment.reset_feedback()

    def coroutine(self):
        """See coroutines plug-in."""

        sketchpad.sketchpad.prepare(self)
        yield
        self.set_item_onset(self.canvas.show())

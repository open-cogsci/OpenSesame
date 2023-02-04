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
import os
from libopensesame.widgets.themes.gray import Gray
from libopensesame.widgets.themes.plain import Plain


class GrayLarge(gray):

    def __init__(self, form):

        Plain.__init__(self, form)
        self.box_checked_image = self.form.experiment.resource(os.path.join(
            'widgets', 'gray', 'box-checked-large.png'))
        self.box_unchecked_image = self.form.experiment.resource(os.path.join(
            'widgets', 'gray', 'box-unchecked-large.png'))

    def box_size(self):

        return 32


# Alias for backwards compatibility
gray_large = GrayLarge

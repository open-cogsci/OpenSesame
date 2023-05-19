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
from ..form_base.form_base import FormBase

default_script = u"""
set form_text 'Your message'
set form_title 'Title'
set ok_text 'Ok'
set rows 1;4;1
set cols 1;1;1
widget 0 0 3 1 label text={form_title}
widget 0 1 3 1 label text={form_text} center=no
widget 1 2 1 1 button text={ok_text}
"""


class FormTextDisplay(FormBase):

    initial_view = u'controls'

    def __init__(self, name, experiment, string=None):
        if string is None or string.strip() == u'':
            string = default_script
        super().__init__(name, experiment, string)

    def from_string(self, script):
        self._widgets = []
        super().from_string(script)

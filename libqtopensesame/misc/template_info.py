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
from libqtopensesame.misc.translate import translation_context
_ = translation_context('template', category='core')

templates = [
    ('templates/default.osexp', _('Default template')),
    ('templates/online.osexp', _('OSWeb (online) template')),
    ('templates/extended_template.osexp', _('Extended template')),
    ('templates/form_template.osexp', _('Questionnaire template')),
    ('templates/pygaze_template.osexp', _('Eye-tracking template')),
]

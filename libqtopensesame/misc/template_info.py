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
from libqtopensesame.misc.translate import translation_context
_ = translation_context(u'template', category=u'core')

if py3:
	templates = [
		(u'templates/default-py3.osexp', _(u'Default template')),
		(u'templates/extended_template-py3.osexp', _(u'Extended template')),
		(u'templates/form_template.osexp',
			_(u'Questionnaire template')),
	]
else:
	templates = [
		(u'templates/default.osexp', _(u'Default template')),
		(u'templates/extended_template.osexp', _(u'Extended template')),
		(u'templates/form_template.osexp',
			_(u'Questionnaire template')),
		(u'templates/pygaze_template.osexp', _(u'Eye-tracking template')),
	]

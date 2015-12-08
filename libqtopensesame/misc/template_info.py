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

if py3:
	templates = [
		('templates/default.osexp', 'Default template (legacy backend)')
		]
else:
	templates = [
		('templates/default.osexp', 'Default template'),
		('templates/extended_template.osexp', 'Extended template'),
		('templates/form_template.osexp', 'Form template (questionnaires)'),
		('templates/android_template.osexp', 'Runtime for Android template'),
		('templates/pygaze_template.osexp', 'PyGaze eye-tracking template'),
		('templates/eco_alt_template.osexp',
				'Stimulus set: an ecological alternative to Snodgrass & Vanderwart'),
		]

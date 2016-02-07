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

class Translatables(object):

	def __init__(self):

		self._translatables = {}

	def add(self, context, translatable):

		if context not in self._translatables:
			self._translatables[context] = []
		self._translatables[context].append(translatable)

	def __str__(self):

		l = []
		for context, translatables in self._translatables.items():
			l.append(u'class %s:\n\tdef _():' % context)
			for s in translatables:
				s = s.replace(u"'", u"\\'")
				s = s.replace(u'\n', u'\\n')
				l.append(u'\t\tself.tr(\'%s\')' % s)
		return u'\n'.join(l) + u'\n'

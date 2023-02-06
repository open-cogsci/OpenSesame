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
import unittest
from opensesame_unittest import backends, compilable, color, syntax, response, \
	headless, translations, readandwrite

for mod in (backends, compilable, color, syntax, response, headless, \
	translations, readandwrite):
	res = unittest.main(mod, exit=False)
	if len(res.result.errors) > 0 or len(res.result.failures) > 0:
		exit(1)

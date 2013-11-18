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

import sys
from libopensesame import debug

# The UI files expect the widgets to be in the same package. This redirect
# allows the UI files to use widgets from the libqtopensesame.widgets package.
for redirect in [u"pyterm",  u"statusbar", u"tree_overview", u"toolbar_items", \
	u"variable_inspector", u"good_looking_table"]:
	debug.msg(u"redirect '%s' module to libqtopensesame.widgets" % redirect)
	item_module = __import__(u'libqtopensesame.widgets.%s' % redirect, \
		fromlist=[u'dummy'])
	sys.modules[redirect] = item_module
	

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
from libopensesame import plugins
from libqtopensesame.items.qtautoplugin import qtautoplugin
form_base = plugins.import_plugin(u'form_base')

default_script = u"""
set form_text 'Your message'
set form_title 'Title'
set ok_text 'Ok'
set rows 1;4;1
set cols 1;1;1
widget 0 0 3 1 label text=[form_title]
widget 0 1 3 1 label text=[form_text] center=no
widget 1 2 1 1 button text=[ok_text]
"""


class form_text_display(form_base.form_base):

	initial_view = u'controls'

	def __init__(self, name, experiment, string=None):

		"""
		Constructor.

		Arguments:
		name		--	The name of the item.
		experiment	--	The experiment instance.

		Keyword arguments:
		string		--	A definition string. (default=None)
		"""

		if string is None or string.strip() == u'':
			string = default_script
		# Due to dynamic loading, we need to implement this super() hack. See
		# <http://thingspython.wordpress.com/2010/09/27/another-super-wrinkle-raising-typeerror/>
		self.super_form_text_display = super(form_text_display, self)
		self.super_form_text_display.__init__(name, experiment, string,
			item_type=u'form_text_display',
			description=u'A simple text display form')

	def from_string(self, script):

		"""
		Re-generates the form from a definition script.

		Arguments:
		script		--	The definition script.
		"""

		self._widgets = []
		self.super_form_text_display.from_string(script)

class qtform_text_display(form_text_display, qtautoplugin):

	def __init__(self, name, experiment, script=None):

		form_text_display.__init__(self, name, experiment, script)
		qtautoplugin.__init__(self, __file__)

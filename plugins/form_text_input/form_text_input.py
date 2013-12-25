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

from libopensesame import item, exceptions, generic_response, widgets, plugins
from libqtopensesame.items.qtautoplugin import qtautoplugin
from openexp.canvas import canvas
import openexp.keyboard
import os.path
from PyQt4 import QtGui, QtCore

form_base = plugins.import_plugin(u'form_base')

default_script = u"""
set form_question 'Your question'
set form_title Title
set form_var response
set rows 1;1;6
set cols 1
widget 0 0 1 1 label text=[form_title]
widget 0 1 1 1 label text=[form_question] center=no
widget 0 2 1 1 text_input return_accepts=yes focus=yes var=[form_var] stub=""
"""

class form_text_input(form_base.form_base):

	def __init__(self, name, experiment, string=None):

		"""
		Constructor.

		Arguments:
		name		--	The name of the item.
		experiment	--	The experiment instance.

		Keyword arguments:
		string		--	A definition string. (default=None)
		"""

		if string == None:
			string = default_script
			
		# Due to dynamic loading, we need to implement this super() hack. See
		# <http://thingspython.wordpress.com/2010/09/27/another-super-wrinkle-raising-typeerror/>
		self.super_form_text_input = super(form_text_input, self)		
		self.super_form_text_input.__init__(name, experiment, string, \
			item_type=u'form_text_input', description= \
			u'A simple text input form')

	def from_string(self, script):

		"""
		Re-generates the form from a definition script.

		Arguments:
		script		--	The definition script.
		"""

		self._widgets = []
		self.super_form_text_input.from_string(script)

	def var_info(self):

		"""
		Returns a list of dictionaries with variable descriptions.

		Returns:
		A list of (name, description) tuples.
		"""

		return self.super_form_text_input.var_info() + \
			[(self.get(u'form_var'), u'[Depends on response]')]
		
class qtform_text_input(form_text_input, qtautoplugin):
	
	def __init__(self, name, experiment, script=None):

		form_text_input.__init__(self, name, experiment, script)
		qtautoplugin.__init__(self, __file__)	

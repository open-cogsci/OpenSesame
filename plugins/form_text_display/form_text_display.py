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
from libqtopensesame import qtplugin
from openexp.canvas import canvas
import openexp.keyboard
import os.path
import shlex
from PyQt4 import QtGui, QtCore

form_base = plugins.import_plugin('form_base')

default_script = """
set form_text 'Your message'
set form_title '<span size=24>Title</span>'
set ok_text 'Ok'
set rows 1;4;1
set cols 1;1;1
widget 0 0 3 1 label text=[form_title]
widget 0 1 3 1 label text=[form_text] center=no
widget 1 2 1 1 button text=[ok_text]
"""

class form_text_display(form_base.form_base):

	def __init__(self, name, experiment, string=None):

		"""
		Constructor

		Arguments:
		name -- the name of the item
		experiment -- the experiment instance

		Keyword arguments:
		string -- a definition string
		"""

		if string == None:
			string = default_script
		form_base.form_base.__init__(self, name, experiment, string, \
			item_type='form_text_display', description= \
			'A simple text display form')			
			
	def from_string(self, script):
	
		"""
		Re-generate the form from a definition script
		
		Arguments:
		script -- the definition script
		"""
	
		self._widgets = []
		form_base.form_base.from_string(self, script)
		
class qtform_text_display(form_text_display, qtplugin.qtplugin):

	"""GUI controls"""

	def __init__(self, name, experiment, string=None):

		"""
		Constructor

		Arguments:
		name -- the name of the item
		experiment -- the experiment instance

		Keyword arguments:
		string -- a definition string
		"""
		
		form_text_display.__init__(self, name, experiment, string)
		qtplugin.qtplugin.__init__(self, __file__)

	def init_edit_widget(self):

		"""Initialize the controls"""

		self.lock = True
		qtplugin.qtplugin.init_edit_widget(self, False)
		self.add_line_edit_control('form_title', 'Form title', 'Form title')
		self.add_line_edit_control('ok_text', 'Ok-button text', \
			'Ok-button text')
		self.add_editor_control('form_text', 'Main form text', \
			'Main form text')		
		self.lock = False

	def apply_edit_changes(self):

		"""Apply the controls"""

		if not qtplugin.qtplugin.apply_edit_changes(self, False) or self.lock:
			return False
		return True

	def edit_widget(self):

		"""Update the controls"""

		self.lock = True
		qtplugin.qtplugin.edit_widget(self)
		self.lock = False
		return self._edit_widget
		

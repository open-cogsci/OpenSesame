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
from libqtopensesame import qtplugin
form_base = plugins.import_plugin('form_base')

default_script = """
set form_text 'Your message'
set rows 1
set cols 1;1;1
set margins 50;100;50;100
set only_render 'yes'
widget 0 0 3 1 label text=[form_text] center=no
"""


class form_text_render(form_base.form_base):

	initial_view = u'controls'

	def __init__(self, name, experiment, string=None):

		"""
		Constructor

		Arguments:
		name -- the name of the item
		experiment -- the experiment instance

		Keyword arguments:
		string -- a definition string
		"""

		if string is None or string.strip() == u'':
			string = default_script
		super(form_text_render, self).__init__(name, experiment, string, \
			item_type='form_text_render', description= \
			'A simple text display form')

	def from_string(self, script):

		"""
		Re-generate the form from a definition script

		Arguments:
		script -- the definition script
		"""

		self._widgets = []
		super(form_text_render, self).from_string(script)

class qtform_text_render(form_text_render, qtplugin.qtplugin):

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

		form_text_render.__init__(self, name, experiment, string)
		qtplugin.qtplugin.__init__(self, __file__)

	def init_edit_widget(self):

		"""Initialize the controls"""

		self.lock = True
		qtplugin.qtplugin.init_edit_widget(self, False)
		self.add_editor_control('form_text', 'Main form text', \
			tooltip='Main form text')
		self.lock = False

	def apply_edit_changes(self):

		"""Apply the controls"""

		if not qtplugin.qtplugin.apply_edit_changes(self) or self.lock:
			return False
		return True

	def edit_widget(self):

		"""Update the controls"""

		self.lock = True
		qtplugin.qtplugin.edit_widget(self)
		self.lock = False
		return self._edit_widget

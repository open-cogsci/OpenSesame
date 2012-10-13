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
from PyQt4 import QtGui, QtCore

class form_multiple_choice(item.item):

	def __init__(self, name, experiment, string=None):

		"""
		Constructor

		Arguments:
		name -- the name of the item
		experiment -- the experiment instance

		Keyword arguments:
		string -- a definition string
		"""
		
		self.item_type = 'form_multiple_choice'
		self.options = 'Yes\nNo\nMaybe'
		self.question = 'Your question'
		self.form_title = 'Form title'
		self.form_var = 'response'
		self.description = 'A simple multiple choice item'
		self.advance_immediately = 'yes'
		self.allow_multiple = 'yes'
		self.button_text = 'Ok'
		item.item.__init__(self, name, experiment, string)			
		
	def run(self):
		
		"""Run the item"""
		
		# Parse the option list
		option_list = unicode(self.get('options')).split()
		if len(option_list) == 0:
			raise exceptions.runtime_error( \
			'You must specify at least one response option in form_multiple_choice item "%s"' \
			% self.name)
			
		# Determine whether a button is shown and determine the number of rows
		rows = len(option_list) + 2
		if self.get('advance_immediately') == 'no' or \
			self.get('allow_multiple') == 'yes':
			show_button = True
			click_accepts = False
			rows += 1
		else:
			show_button = False
			click_accepts = True
			
		# Determine the group for the checkboxes
		if self.get('allow_multiple') == 'no':
			group = 'response_group'
		else:
			group = None			
			
		# The variable in which the response is stored
		var = self.get('form_var')
		
		# Build the form
		form = widgets.form(self.experiment, cols=1, rows=rows)		
		form.set_widget(widgets.label(form, self.get('form_title')), (0,0))
		form.set_widget(widgets.label(form, self.get('question')), (0,1))
		i = 2
		for option in option_list:
			form.set_widget(widgets.checkbox(form, option, group=group, \
				click_accepts=click_accepts, var=var), (0,i))
			i += 1
		if show_button:
			form.set_widget(widgets.button(form, self.get('button_text')), \
				(0,i))

		# Go!
		form._exec()
		return True
		
	def var_info(self):
		
		"""
		Return a list of dictionaries with variable descriptions

		Returns:
		A list of (name, description) tuples
		"""
		
		return item.item.var_info(self) + \
			[(self.get('form_var'), '[Depends on response]')]				
							
class qtform_multiple_choice(form_multiple_choice, qtplugin.qtplugin):

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
		
		form_multiple_choice.__init__(self, name, experiment, string)
		qtplugin.qtplugin.__init__(self, __file__)

	def init_edit_widget(self):

		"""Initialize the controls"""

		self.lock = True
		qtplugin.qtplugin.init_edit_widget(self, False)
		self.add_line_edit_control('form_title', 'Form title', tooltip= \
			'Form title')
		self.add_line_edit_control('form_var', 'Response variable', \
			tooltip='Response variable')
		self.add_checkbox_control('allow_multiple', \
			'Allow multiple options to be selected', \
			tooltip='Allow multiple options to be selected',)
		self.add_checkbox_control('advance_immediately', \
			'Advance immediately to the next item once a selection has been made', \
			tooltip='Advance immediately to the next item once a selection has been made')
		self.add_line_edit_control('button_text', 'Button text', \
			tooltip='Text for the button to advance to the next item')
		self.add_editor_control('question', 'Your question', \
			tooltip='Your question')		
		self.add_editor_control('options', \
			'Response options (different options on different lines)', \
			tooltip='Response options')					
		self.auto_apply_edit_changes()
		self.lock = False

	def apply_edit_changes(self):

		"""Apply the controls"""

		if not qtplugin.qtplugin.apply_edit_changes(self, False) or self.lock:
			return False			
		return True
		
	def auto_apply_edit_changes(self, rebuild=True):
		
		"""
		Apply the auto-widget controls

		Keyword arguments:
		rebuild -- deprecated (does nothing) (default=True)
		"""		
			
		qtplugin.qtplugin.auto_apply_edit_changes(self, rebuild)
		# The advance_immediately option is not applicable if multiple items can
		# be selected
		self.auto_checkbox['advance_immediately'].setEnabled( \
			self.get('allow_multiple') == 'no')
		self.auto_line_edit['button_text'].setEnabled( \
			self.get('allow_multiple') == 'yes' or \
			self.get('advance_immediately') == 'no')	

	def edit_widget(self):

		"""Update the controls"""

		self.lock = True
		qtplugin.qtplugin.edit_widget(self)
		self.lock = False
		return self._edit_widget
		

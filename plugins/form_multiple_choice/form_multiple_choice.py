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

from libopensesame.exceptions import osexception
from libopensesame import item, generic_response, widgets, plugins
from libqtopensesame.items.qtautoplugin import qtautoplugin
from openexp.canvas import canvas
import openexp.keyboard
import os.path
from PyQt4 import QtGui, QtCore

class form_multiple_choice(item.item):
	
	description = u'A simple multiple choice item'

	def __init__(self, name, experiment, string=None):

		"""
		Constructor

		Arguments:
		name		--	The name of the item.
		experiment	--	The experiment instance.

		Keyword arguments:
		string		--	A definition string. (default=None)
		"""
		
		self.options = u'Yes\nNo\nMaybe'
		self.question = u'Your question'
		self.form_title = u'Form title'
		self.form_var = u'response'
		self.advance_immediately = u'yes'
		self.allow_multiple = u'yes'
		self.button_text = u'Ok'
		item.item.__init__(self, name, experiment, string)
		
	def run(self):
		
		"""Run the item"""
		
		# Parse the option list
		option_list = self.get(u'options').split(u'\n') # split by return
		option_list.pop(len(option_list)-1) # remove last (empty) option
		if len(option_list) == 0:
			raise osexception( \
				u'You must specify at least one response option in form_multiple_choice item "%s"' \
				% self.name)
			
		# Determine whether a button is shown and determine the number of rows
		rows = len(option_list) + 2
		if self.get(u'advance_immediately') == u'no' or \
			self.get(u'allow_multiple') == u'yes':
			show_button = True
			click_accepts = False
			rows += 1
		else:
			show_button = False
			click_accepts = True
			
		# Determine the group for the checkboxes
		if self.get(u'allow_multiple') == u'no':
			group = u'response_group'
		else:
			group = None			
			
		# The variable in which the response is stored
		var = self.get(u'form_var')
		
		# Build the form
		form = widgets.form(self.experiment, cols=1, rows=rows)		
		form.set_widget(widgets.label(form, self.get(u'form_title')), (0,0))
		form.set_widget(widgets.label(form, self.get(u'question')), (0,1))
		i = 2
		for option in option_list:
			form.set_widget(widgets.checkbox(form, option, group=group, \
				click_accepts=click_accepts, var=var), (0,i))
			i += 1
		if show_button:
			form.set_widget(widgets.button(form, self.get(u'button_text')), \
				(0,i))

		# Go!
		form._exec()
		
	def var_info(self):
		
		"""
		Return a list of dictionaries with variable descriptions

		Returns:
		A list of (name, description) tuples
		"""
		
		return item.item.var_info(self) + \
			[(self.get(u'form_var'), u'[Depends on response]')]

class qtform_multiple_choice(form_multiple_choice, qtautoplugin):

	"""GUI controls"""

	def __init__(self, name, experiment, string=None):

		"""
		Constructor

		Arguments:
		name		--	The name of the item.
		experiment	--	The experiment instance.

		Keyword arguments:
		string		--	A definition string. (default=None)
		"""
		
		form_multiple_choice.__init__(self, name, experiment, string)
		qtautoplugin.__init__(self, __file__)
		self.custom_interactions()
		
	def apply_edit_changes(self):

		"""Apply the controls"""

		if not qtautoplugin.apply_edit_changes(self) or self.lock:
			return False
		self.custom_interactions()
		return True
	
	def custom_interactions(self):
		
		"""
		The advance_immediately option is not applicable if multiple items can
		be selected.
		"""
		
		self.checkbox_advance_immediately.setEnabled(self.get( \
			u'allow_multiple') == u'no')
		self.line_edit_button_text.setEnabled(self.get(u'allow_multiple') == \
			u'yes' or self.get(u'advance_immediately') == u'no')
		


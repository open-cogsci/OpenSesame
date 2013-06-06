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

import os
from libqtopensesame.items.qtplugin import qtplugin
from libqtopensesame.misc import _

class qtautoplugin(qtplugin):

	"""A class that processes auto-plugins defined in a JSON file"""
	
	def __init__(self, plugin_file):
		
		qtplugin.__init__(self, plugin_file)				
					
	def init_edit_widget(self):

		"""Construct the GUI controls based on info.json"""

		# Import json only when required, as it is not necessary for the
		# runtime environment and may be not available on all platforms,
		# notably Android.
		import json
	
		self.lock = True
		qtplugin.init_edit_widget(self, False)		
		# Load info.json
		json_path = os.path.join(self.plugin_folder, u'info.json')
		self.json = json.load(open(json_path))				
		# Some options are required. Which options are requires depends on the
		# specific widget.
		required  = [
			([u'checkbox', u'color_edit', u'combobox', u'editor', u'filepool', \
				u'line_edit', u'spinbox', u'text'], [u'label']),
			([u'checkbox', u'color_edit', u'combobox', u'editor', u'filepool', \
				u'line_edit', u'spinbox'], [u'var']),
			([u'spinbox', u'slider'], [u'min_val', u'max_val']),
			([u'combobox'], [u'options']),
			]
		# Keywords are optional parameters that are set to some default if they
		# are not specified.
		keywords = {
			u'tooltip' : None,
			u'min_width' : None,
			u'prefix' : u'',
			u'suffix' : u'',
			u'left_label' : u'min.',
			u'right_label' : u'max.',
			u'syntax' : False
			}
		# This indicates whether we should pad the controls with a stretch at
		# the end.
		need_stretch = True
		for c in self.json[u'controls']:			
			# Check whether all required options have been specified
			if u'type' not in c:
				raise Exception(_( \
					u'You must specify "type" for %s controls in info.json') \
					% option)
			for types, options in required:
				if c[u'type'] in types:
					for option in options:
						if option not in c:
							raise Exception(_( \
								u'You must specify "%s" for %s controls in info.json') \
								% (option, c[u'type']))
			# Set missing keywords to None
			for keyword, default in keywords.iteritems():
				if keyword not in c:
					c[keyword] = default
			# Parse checkbox
			if c[u'type'] == u'checkbox':
				widget = self.add_checkbox_control(c[u'var'], c[u'label'], \
					tooltip=c[u'tooltip'])
			# Parse color_edit
			elif c[u'type'] == u'color_edit':
				widget = self.add_color_edit_control(c[u'var'], c[u'label'], \
					tooltip=c[u'tooltip'], min_width=c[u'min_width'])
			# Parse combobox
			elif c[u'type'] == u'combobox':
				widget = self.add_combobox_control(c[u'var'], c[u'label'], \
					c[u'options'], tooltip=c[u'tooltip'])
			# Parse editor
			elif c[u'type'] == u'editor':
				widget = self.add_editor_control(c[u'var'], c[u'label'], \
					syntax=c[u'syntax'], tooltip=c[u'tooltip'])
				need_stretch = False
			# Parse filepool
			elif c[u'type'] == u'filepool':
				widget = self.add_filepool_control(c[u'var'], c[u'label'], \
					tooltip=c[u'tooltip'])
			# Parse line_edit
			elif c[u'type'] == u'line_edit':
				widget = self.add_line_edit_control(c[u'var'], c[u'label'], \
					tooltip=c[u'tooltip'], min_width=c[u'min_width'])
			# Parse spinbox
			elif c[u'type'] == u'spinbox':
				widget = self.add_spinbox_control(c[u'var'], c[u'label'], \
					c[u'min_val'], c[u'max_val'], prefix=c[u'prefix'], suffix= \
					c[u'suffix'], tooltip=c[u'tooltip'])
			# Parse slider
			elif c[u'type'] == u'slider':
				widget = self.add_slider_control(c[u'var'], c[u'label'], \
					c[u'min_val'], c[u'max_val'], left_label=c[u'left_label'], \
					right_label=c[u'right_label'], tooltip=c[u'tooltip'])
			# Parse text
			elif c[u'type'] == u'text':
				widget = self.add_text(c[u'label'])
			else:
				raise Exception(_(u'"%s" is not a valid qtautoplugin control') \
					% controls[u'type'])
			# Add the widget as an item property when the 'name' option is
			# specified.
			if u'name' in c:
				if hasattr(self, c[u'name']):
					raise Exception(_( \
						u'Name "%s" is already taken in qtautoplugin control') \
						% c[u'name'])
				setattr(self, c[u'name'], widget)
		if need_stretch:
			self.add_stretch()
		self.lock = True

	def apply_edit_changes(self):

		"""Applies the controls. I.e. sets the variables from the controls."""

		if not qtplugin.apply_edit_changes(self, False) or self.lock:
			return False
		self.experiment.main_window.refresh(self.name)
		return True

	def edit_widget(self):

		"""Sets the controls based on the variables."""

		self.lock = True
		qtplugin.edit_widget(self)
		self.lock = False
		return self._edit_widget	
	
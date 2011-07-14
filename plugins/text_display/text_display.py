"""
This file is part of opensesame.

opensesame is free software: you can redistribute it and/or modify
it under the terms of the GNU General Public License as published by
the Free Software Foundation, either version 3 of the License, or
(at your option) any later version.

opensesame is distributed in the hope that it will be useful,
but WITHOUT ANY WARRANTY; without even the implied warranty of
MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
GNU General Public License for more details.

You should have received a copy of the GNU General Public License
along with opensesame.  If not, see <http://www.gnu.org/licenses/>.
"""


from libopensesame import item, generic_response, exceptions
from libqtopensesame import qtplugin
import openexp.canvas
import os.path
from PyQt4 import QtGui, QtCore

class text_display(item.item, generic_response.generic_response):

	"""
	This class handles the basic functionality of the
	item. It does not deal with GUI stuff.	
	"""

	def __init__(self, name, experiment, string = None):
	
		"""
		Constructor
		"""
		
		self.item_type = "text_display"
		self.description = "Presents a display consisting of text"
		self.duration = "keypress"
		self.align = "center"
		self.content = "Enter your text here."
		self.maxchar = 50
		
		# Pass the word on to the parent		
		item.item.__init__(self, name, experiment, string)
		
		# These lines makes sure that the icons and help file are recognized by
		# OpenSesame. Copy-paste these lines at the end of your plugin's constructor
		self.experiment.resources["%s.png" % self.item_type] = os.path.join(os.path.split(__file__)[0], "%s.png" % self.item_type)
		self.experiment.resources["%s_large.png" % self.item_type] = os.path.join(os.path.split(__file__)[0], "%s_large.png" % self.item_type)			
		self.experiment.resources["%s.html" % self.item_type] = os.path.join(os.path.split(__file__)[0], "%s.html" % self.item_type)
				
	def prepare(self):
	
		"""
		Prepare the item. In this case this means drawing a fixation
		dot to an offline canvas.
		"""
		
		# Pass the word on to the parent
		item.item.prepare(self)		
		
		# Create an offline canvas
		self.c = openexp.canvas.canvas(self.experiment, self.get("background"), self.get("foreground"))		
		self.c.set_font(self.get("font_family"), self.get("font_size"))
		
		content = self.experiment.unsanitize(self.eval_text(self.get("content"))).split("\n")

		# Do line wrapping
		_content = []
		for line in content:
			while len(line) > self.get("maxchar"):
				i = line.rfind(" ", 0, self.get("maxchar"))
				if i < 0:
					raise exceptions.runtime_error("Failed to do line wrapping in text_display '%s'. Perhaps one of the words is longer than the maximum number of characters per line?" % self.name)
				_content.append(line[:i])
				line = line[i+1:]
			_content.append(line)
		content = _content
		
		if self.get("align") != "center":

			try:
				max_width = 0
				max_height = 0 
				for line in content:
					size = self.c.text_size(line)
					max_width = max(max_width, size[0])
					max_height = max(max_height, size[1])
			except:
				raise exceptions.runtime_error("Failed to use alignment '%s' in text_display '%s'. Perhaps this alignment is not supported by the back-end. Please use 'center' alignment." % (self.get("align"), self.name))
				
		line_nr = -len(content) / 2
		for line in content:
		
			if self.get("align") == "center":
				self.c.textline(line, line_nr)
			elif self.get("align") == "left":
				self.c.text(line, False, self.c.xcenter() - 0.5 * max_width, self.c.ycenter() + 1.5 * line_nr * max_height)
			else:
				width = self.c.text_size(line)[0]
				self.c.text(line, False, self.c.xcenter() + 0.5 * max_width - width, self.c.ycenter() + 1.5 * line_nr * max_height)
			
			line_nr += 1			
		
		generic_response.generic_response.prepare(self)		
		return True
				
	def run(self):
	
		"""
		Run the item. In this case this means putting the offline canvas
		to the display and waiting for the specified duration.
		"""
		
		# Show the canvas
		self.set_item_onset(self.c.show())
		self.set_sri()
		self.process_response()					
		return True

	def var_info(self):

		return generic_response.generic_response.var_info(self)	
					
class qttext_display(text_display, qtplugin.qtplugin):

	def __init__(self, name, experiment, string = None):
	
		"""
		Initialize the GUI part of the plugin
		"""
		
		# Pass the word on to the parents		
		text_display.__init__(self, name, experiment, string)		
		qtplugin.qtplugin.__init__(self, __file__)	
		
	def init_edit_widget(self):
	
		"""
		Build the edit widget
		"""
		
		self.lock = True
		
		# Pass the word on to the parent		
		qtplugin.qtplugin.init_edit_widget(self, False)
		
		self.add_line_edit_control("duration", "Duration", tooltip = "Expecting a value in milliseconds, 'keypress' or 'mouseclick'")
		self.add_line_edit_control("foreground", "Foreground", tooltip = "Expecting a colorname (e.g., 'blue') or an HTML color (e.g., '#0000FF')")
		self.add_line_edit_control("background", "Background", tooltip = "Expecting a colorname (e.g., 'blue') or an HTML color (e.g., '#0000FF')")		
		self.add_combobox_control("font_family", "Font family", ["mono", "sans", "serif"], tooltip = "The font style")
		self.add_spinbox_control("font_size", "Font size", 1, 512, suffix = "pt", tooltip = "The font size")
		self.add_spinbox_control("maxchar", "Wrap line after", 1, 1000, suffix = " characters", tooltip = "Maximum number of characters per line")
		self.add_combobox_control("align", "Text alignment", ["left", "center", "right"], tooltip = "Text alignment")		
		
		# Content editor		
		self.add_editor_control("content", "Text", tooltip = "The text to be displayed")
				
		self.lock = False		
		
	def apply_edit_changes(self):
	
		"""
		Apply changes to the edit widget
		"""
		
		if not qtplugin.qtplugin.apply_edit_changes(self, False) or self.lock:
			return		
			
		self.experiment.main_window.refresh(self.name)		

	def edit_widget(self):
	
		"""
		Refresh and return the edit widget
		"""
		
		self.lock = True

		qtplugin.qtplugin.edit_widget(self)
		
		self.lock = False
		
		return self._edit_widget

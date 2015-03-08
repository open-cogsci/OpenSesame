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

from libopensesame.exceptions import osexception
from libopensesame.generic_response import generic_response
from libopensesame.item import item
from libqtopensesame.items.qtautoplugin import qtautoplugin
import openexp.canvas
import os.path
from PyQt4 import QtGui, QtCore

class text_display(item, generic_response):

	"""Basic text display plug-in"""

	description = u"Presents a display consisting of text"

	def __init__(self, name, experiment, string=None):

		"""
		Constructor.

		Arguments:
		name		--	The name of the item,
		experiment	--	An experiment object.

		Keyword arguments:
		string		--	A definition string. (default=None)
		"""

		self.duration = u"keypress"
		self.align = u"center"
		self.content = u"Enter your text here."
		self.maxchar = 50
		item.__init__(self, name, experiment, string)

	def prepare(self):

		"""Prepares the text display canvas."""

		# Pass the word on to the parent
		item.prepare(self)
		# Create an offline canvas
		self.c = openexp.canvas.canvas(self.experiment, self.var.get( \
			u"background"), self.var.get(u"foreground"))
		self.c.set_font(self.var.get(u"font_family"), self.var.get(u"font_size"))
		# Make sure that the content is a unicode string that is evaluated
		# for variables and then split into separated lines, using either the
		# os-specific or the Unix-style line separator.
		content = self.unistr(self.var.get(u'content'))
		content = content.replace(os.linesep, u'\n')
		content = self.eval_text(content).split(u"\n")
		# Do line wrapping
		_content = []
		for line in content:
			while len(line) > self.var.get(u"maxchar"):
				i = line.rfind(" ", 0, self.var.get(u"maxchar"))
				if i < 0:
					raise osexception( \
						u"Failed to do line wrapping in text_display '%s'. Perhaps one of the words is longer than the maximum number of characters per line?" \
						% self.name)
				_content.append(line[:i])
				line = line[i+1:]
			_content.append(line)
		content = _content

		if self.var.get(u"align") != u"center":
			try:
				max_width = 0
				max_height = 0
				for line in content:
					size = self.c.text_size(line)
					max_width = max(max_width, size[0])
					max_height = max(max_height, size[1])
			except:
				raise osexception( \
					u"Failed to use alignment '%s' in text_display '%s'. Perhaps this alignment is not supported by the back-end. Please use 'center' alignment." \
					% (self.var.get(u"align"), self.name))

		line_nr = -len(content) / 2
		for line in content:

			if self.var.get(u"align") == u"center":
				self.c.textline(line, line_nr)
			elif self.var.get(u"align") == u"left":
				self.c.text(line, False, self.c.xcenter()-0.5*max_width, \
					self.c.ycenter()+1.5*line_nr*max_height)
			else:
				width = self.c.text_size(line)[0]
				self.c.text(line, False, self.c.xcenter()+0.5*max_width-width, \
					self.c.ycenter()+1.5*line_nr*max_height)

			line_nr += 1

		generic_response.prepare(self)

	def run(self):

		"""Shows the text_display canvas."""

		# Show the canvas
		self.set_item_onset(self.c.show())
		self.set_sri()
		self.process_response()

	def var_info(self):

		"""
		Gives a list of dictionaries with variable descriptions.

		Returns:
		A list of (name, description) tuples
		"""

		return item.var_info(self) + generic_response.var_info(self)

class qttext_display(text_display, qtautoplugin):

	"""Automatic GUI class."""

	def __init__(self, name, experiment, script=None):

		text_display.__init__(self, name, experiment, script)
		qtautoplugin.__init__(self, __file__)

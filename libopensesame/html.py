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

from HTMLParser import HTMLParser
from libopensesame import debug

class html(HTMLParser):

	"""
	A simple HTML parser that deals with a subset of HTML tags and renders text
	onto an openexp canvas. Currently, the following tags are supported: <b>,
	<i>, <br />, and <span>. For <span> you can pass size and style keywords.	
	"""	
	
	valid_end_tags = 'i', 'b', 'span'
	valid_start_tags = 'i', 'b', 'span', 'br'	
			
	def handle_data(self, data):
	
		"""
		Receive a single piece of text that has the same style
		
		Arguments:
		data -- a data string
		"""

		style = self.style()
		while len(data) > 0:
			i = data[1:].find(' ')
			if i < 0:
				break
			word = data[:i+1]
			data = data[i+1:]	
			self.paragraph.append( (word, style) )
		self.paragraph.append( (data, style) )				
		
	def handle_endtag(self, tag):
	
		"""
		Handle a closing tag
		
		Arguments:
		tag -- the closing tag
		"""
	
		if tag not in self.valid_end_tags:
			return
	
		if self.current_tag != tag:
			print 'Warning: expecting closing tag for %s, got %s' % \
				(self.current_tag, tag)
	
		self.pop_style()
			
	def handle_starttag(self, tag, attrs):
	
		"""
		Handle an opening tag
		
		Arguments:
		tag -- the closing tag
		attrs -- the tag attributes
		"""	
	
		if tag not in self.valid_start_tags:
			return	
	
		if tag == 'br':
			self.text.append(self.paragraph)
			self.paragraph = []
			return

		self.current_tag = tag

		if tag == 'span':
			for var, val in attrs:
				self.push_style( **{var : val} )
		elif tag == 'b':
			self.push_style(bold=True)
		elif tag == 'i':
			self.push_style(italic=True)
		elif tag == 'u':
			self.push_style(underline=True)				
		else:
			print 'Unrecognized tag:', tag
				
	def render(self, text, x, y, canvas):
	
		"""
		Render an HTML formatted string onto a canvas
		
		Arguments:
		text -- the text string
		x -- the left-most coordinate
		y -- the top coordinate
		canvas -- an openexp canvas
		"""		
	
		debug.msg(text)
		self.canvas = canvas		
		self.default_style = {
			'style' : canvas.experiment.get('font_family'),
			'bold' : canvas.experiment.get('font_bold') == 'yes',
			'italic' : canvas.experiment.get('font_italic') == 'yes',			
			'color' : canvas.experiment.get('foreground'),
			'size' : canvas.experiment.get('font_size')
			}	
	
		# First parse the HTML
		self.text = []
		self.paragraph = []
		self.style_stack = []
		self.current_tag = None
		self.push_style()				
		self.feed(text)
		self.text.append(self.paragraph)
		
		# Now render it onto the canvas
		_y = y
		for paragraph in self.text:
			_x = x
			for word, style in paragraph:
			
				# Set the style
				canvas.set_font(style['style'], int(style['size']), \
					bold=style['bold'], italic=style['italic'])
				canvas.set_fgcolor(str(style['color']))		
				
				# Line wrap if we run out of the screen
				dx, dy = canvas.text_size(word)
				if _x+dx > canvas.experiment.get('width'):
					_x = x
					_y += dy
					word = word.lstrip()
				
				# Draw!
				canvas.text(word, center=False, x=_x, y=_y)
				_x += dx
			_y += dy
				
	def pop_style(self):
	
		"""Pop a style from the style stack"""
	
		self.style_stack.pop()		
		if len(self.style_stack) == 0:
			self.push_style()
				
	def push_style(self, **keywords):
	
		"""
		Push a new style onto the style stack
		
		Keyword arguments:
		**keywords -- a keyword dictionary with style attributes		
		"""
	
		if len(self.style_stack) == 0:
			current_style = self.default_style.copy()
		else:
			current_style = self.style_stack[-1].copy()		
		for tag, val in keywords.iteritems():
			current_style[tag] = val
		self.style_stack.append(current_style) 
		
	def style(self):
	
		"""
		Get the current style
		
		Returns:
		A style dictionary
		"""
	
		return self.style_stack[-1].copy()

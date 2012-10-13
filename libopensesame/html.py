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
	
	valid_end_tags = 'i', 'b', 'u', 'span'
	valid_start_tags = 'i', 'b', 'u', 'span', 'br'	
			
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
			debug.msg('Warning: expecting closing tag for %s, got %s' % \
				(self.current_tag, tag), reason='warning')
	
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
			style = {}
			for var, val in attrs:
				style[var] = val
			self.push_style(**style)
		elif tag == 'b':
			self.push_style(bold=True)
		elif tag == 'i':
			self.push_style(italic=True)
		elif tag == 'u':
			self.push_style(underline=True)				
		else:
			debug.msg('Unrecognized tag: %s')
				
	def render(self, text, x, y, canvas, max_width=None, center=False, \
		color=None, html=True):
	
		"""
		Render an HTML formatted string onto a canvas
		
		Arguments:
		text -- the text string
		x -- the left-most coordinate
		y -- the top coordinate
		canvas -- an openexp canvas
		
		Keyword arguments:
		max_width -- the maximum width, after which line wrapping should occur,
					 or None to wrap at screen edge (default=None)
		center -- indicates whether the text should be center aligned
				  (default=False)
		color -- indicates the color of the text or None for canvas default
				 (default=None)
		html -- indicates whether HTML should be parsed (default=True)				 
		"""		

		debug.msg(text)

		# Make sure that it's a string
		text = canvas.experiment.unistr(text)
	
		# Convert line breaks to HTML break tags
		text = text.replace('\n', '<br />')

		# Initialize the style	
		self.canvas = canvas		
		self.default_style = {
			'style' : canvas.font_style,
			'bold' : canvas.font_bold,
			'italic' : canvas.font_italic,			
			'color' : canvas.fgcolor,
			'size' : canvas.font_size,
			'underline' : canvas.font_underline
			}
		backup_style = self.default_style.copy()
			
		# Optionally override color
		if color != None:
			self.default_style['color'] = color
			
		# Set the maximum width
		if max_width == None:
			max_x = canvas.experiment.width
		else:
			max_x = x + max_width
			
		# First parse the HTML
		self.text = []
		self.paragraph = []
		self.style_stack = []
		self.current_tag = None
		self.push_style()
		
		# Optionally parse HTML
		if html:			
			self.feed(text)
		else:
			self.handle_data(text)
		self.text.append(self.paragraph)
		
		# If we want to center the next, we need a dry run to calculate all the
		# line lengths and determine the vertical and horizontal offset for each
		# line
		if center:
			l_x_offset = []
			_y = y
			for paragraph in self.text:
				_x = x
				dy = canvas.text_size('dummy')[1]				
				for word, style in paragraph:
			
					# Set the style
					canvas.set_font(style['style'], int(style['size']), \
						bold=style['bold'], italic=style['italic'], underline= \
						style['underline'])
				
					# Line wrap if we run out of the screen
					dx, dy = canvas.text_size(word)
					if _x+dx > max_x + (max_x-x):
						l_x_offset.append(-(_x-x)/2)
						_x = x
						_y += dy
						word = word.lstrip()
				
					# Draw!
					_x += dx
				l_x_offset.append(-(_x-x)/2)
				_y += dy			
			l_x_offset.reverse()
			y_offset = -(_y-y)/2
		
		# Now render it onto the canvas
		if center:
			_y = y+y_offset	
		else:
			_y = y
		for paragraph in self.text:
			if center:
				_x = x+l_x_offset.pop()
			else:
				_x = x
			dy = canvas.text_size('dummy')[1]
			for word, style in paragraph:
			
				# Set the style
				canvas.set_font(style['style'], int(style['size']), \
					bold=style['bold'], italic=style['italic'], underline= \
					style['underline'])
				canvas.set_fgcolor(style['color'])		
				
				# Line wrap if we run out of the screen
				dx, dy = canvas.text_size(word)
				if _x+dx > max_x:
					if center:
						_x = x+l_x_offset.pop()
					else:
						_x = x
					_y += dy
					word = word.lstrip()
				
				# Draw!
				canvas._text(word, _x, _y)
				_x += dx
			_y += dy
			
		# Restore the canvas font and colors
		canvas.set_fgcolor(backup_style['color'])
		canvas.set_font(backup_style['style'], int(backup_style['size']), \
			bold=backup_style['bold'], italic=backup_style['italic'])
						
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

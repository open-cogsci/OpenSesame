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
from HTMLParser import HTMLParser
from libopensesame import debug

try:
	from bidi.algorithm import get_display as bidi_func
except:
	debug.msg( \
		u'Failed to import bidi. Bi-directional-text support will not be available', \
		reason=u'warning')
	bidi_func = None

class html(HTMLParser):

	"""
	A simple HTML parser that deals with a subset of HTML tags and renders text
	onto an openexp canvas. Currently, the following tags are supported: <b>,
	<i>, <br />, and <span>. For <span> you can pass size and style keywords.
	"""

	valid_end_tags = u'i', u'b', u'u', u'span'
	valid_start_tags = u'i', u'b', u'u', u'span', u'br'
	
	def handle_data(self, data):

		"""
		Receive a single piece of text that has the same style

		Arguments:
		data -- a data string
		"""

		style = self.style()
		while len(data) > 0:
			i = data[1:].find(u' ')
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
			debug.msg(u'Warning: expecting closing tag for %s, got %s' % \
				(self.current_tag, tag), reason=u'warning')

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

		if tag == u'br':
			self.text.append(self.paragraph)
			self.paragraph = []
			return

		self.current_tag = tag

		if tag == u'span':
			style = {}
			for var, val in attrs:
				style[str(var)] = val
			self.push_style(**style)
		elif tag == u'b':
			self.push_style(bold=True)
		elif tag == u'i':
			self.push_style(italic=True)
		elif tag == u'u':
			self.push_style(underline=True)
		else:
			debug.msg(u'Unrecognized tag: %s' % tag)

	def render(self, text, x, y, canvas, max_width=None, center=False, \
		color=None, bidi=False, html=True):

		"""
		Renders an HTML formatted string onto a canvas.

		Arguments:
		text		-- 	The text string.
		x			--	The left-most coordinate.
		y			--	The top coordinate.
		canvas		--	An openexp canvas.

		Keyword arguments:
		max_width 	--	The maximum width, after which line wrapping should
						occur, or None to wrap at screen edge. (default=None)
		center 		--	Indicates whether the text should be center aligned.
						(default=False)
		color		--	Indicates the color of the text or None for canvas
						default. (default=None)
		bidi		--	Indicates whether bi-directional text support should be
						enabled. (default=False)
		html		--	Indicates whether HTML should be parsed. (default=True)
		"""

		debug.msg(text)
		# Parse bi-directional strings
		if bidi and bidi_func != None:
			text = bidi_func(text)
		# Make sure that it's a string
		text = canvas.experiment.unistr(text)
		# Convert line breaks to HTML break tags
		text = text.replace(os.linesep, u'<br />').replace(u'\n', u'<br />')

		# Initialize the style
		self.canvas = canvas
		self.default_style = {
			u'style' : canvas.font_style,
			u'bold' : canvas.font_bold,
			u'italic' : canvas.font_italic,
			u'color' : canvas.fgcolor,
			u'size' : canvas.font_size,
			u'underline' : canvas.font_underline
			}
		backup_style = self.default_style.copy()

		# Optionally override color
		if color != None:
			self.default_style[u'color'] = color

		# Set the maximum width
		if max_width == None:
			max_x = canvas.experiment.width
		else:
			if center:
				max_x = x + max_width/2
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
				dy = canvas.text_size(u'dummy')[1]
				for word, style in paragraph:

					# Set the style
					canvas.set_font(style[u'style'], int(style[u'size']), \
						bold=style[u'bold'], italic=style[u'italic'], \
						underline=style[u'underline'])

					# Line wrap if we run out of the screen
					dx, dy = canvas.text_size(word)
					if _x+dx > max_x + (max_x-x):
						l_x_offset.append(-(_x-x)/2)
						_x = x
						_y += dy
						dx = canvas.text_size(word.lstrip())[0]
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
			dy = canvas.text_size(u'dummy')[1]
			for word, style in paragraph:

				# Set the style
				canvas.set_font(style[u'style'], int(style[u'size']), \
					bold=style[u'bold'], italic=style[u'italic'], underline= \
					style[u'underline'])
				canvas.set_fgcolor(style[u'color'])

				# Line wrap if we run out of the screen
				dx, dy = canvas.text_size(word)
				if _x+dx > max_x:
					if center:
						_x = x+l_x_offset.pop()
					else:
						_x = x
					_y += dy
					dx = canvas.text_size(word.lstrip())[0]
					word = word.lstrip()

				# Draw!
				canvas._text(word, _x, _y)
				_x += dx
			_y += dy

		# Restore the canvas font and colors
		canvas.set_fgcolor(backup_style[u'color'])
		canvas.set_font(backup_style[u'style'], int(backup_style[u'size']), \
			bold=backup_style[u'bold'], italic=backup_style[u'italic'])

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

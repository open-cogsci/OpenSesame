#-*- coding:utf-8 -*-

"""
This file is part of openexp.

openexp is free software: you can redistribute it and/or modify
it under the terms of the GNU General Public License as published by
the Free Software Foundation, either version 3 of the License, or
(at your option) any later version.

openexp is distributed in the hope that it will be useful,
but WITHOUT ANY WARRANTY; without even the implied warranty of
MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
GNU General Public License for more details.

You should have received a copy of the GNU General Public License
along with openexp.  If not, see <http://www.gnu.org/licenses/>.
"""

import pygame
from pygame.locals import *
import random
import openexp.canvas
import math
import subprocess
import os
import os.path
import tempfile
from libopensesame.exceptions import osexception
from libopensesame import debug, html, misc

# Translation mapping from envelope names
env_synonyms = {}
env_synonyms[u"c"] = u"c"
env_synonyms[u"circular"] = u"c"
env_synonyms[u"round"] = u"c"

env_synonyms[u"g"] = u"g"
env_synonyms[u"gaussian"] = u"g"
env_synonyms[u"gauss"] = u"g"
env_synonyms[u"normal"] = u"g"

env_synonyms[u"r"] = u"r"
env_synonyms[u"rectangular"] = u"r"
env_synonyms[u"rectangle"] = u"r"

env_synonyms[u"g"] = u"g"
env_synonyms[u"rect"] = u"g"
env_synonyms[u"square"] = u"g"
env_synonyms[None] = u"g"

env_synonyms[u"l"] = u"l"
env_synonyms[u"linear"] = u"l"
env_synonyms[u"lin"] = u"l"
env_synonyms[u"ln"] = u"l"
env_synonyms[u"l"] = u"l"

class legacy:

	"""
	The legacy backend is the default backend which uses PyGame to handle all
	display operations.

	This class serves as a template for creating OpenSesame video backends.
	Let's say you want to create a dummy backend. First, create dummy.py in the
	openexp.video folder. In dummy.py, create a dummy class, which is derived
	from openexp.canvas.canvas and which implements all the functions specified
	below.

	After you have done this, the new backend can be activated by adding
	"set video_backend dummy" to the general script. This will make OpenSesame
	use the dummy class instead of the default legacy backend.

	A few guidelines:
	-- Catch exceptions wherever possible and raise an
	   osexception with a clear and descriptive error
	   message.
	-- If you create a temporary file, add its path to the
	   openexp.canvas.temp_files list.
	-- Do not deviate from the guidelines. All back-ends should be
	   interchangeable and transparent to OpenSesame. You are free to add
	   functionality to this class, to be used in inline scripts, but this
	   should not break the basic functionality.
	-- Print debugging output using the debug.msg() function
	"""

	# The settings variable is used by the GUI to provide a list of back-end
	# settings
	settings = {
		u"pygame_hwsurface" : {
			u"name" : u"Hardware surface",
			u"description" : u"Create a hardware surface",
			u"default" : u"yes"
			},
		u"pygame_doublebuf" : {
			u"name" : u"Double buffering",
			u"description" : u"Use double buffering",
			u"default" : u"yes"
			},
		u"pygame_window_frame" : {
			u"name" : u"Draw window frame",
			u"description" : u"Draw a frame in window mode",
			u"default" : u"yes",
			},
		u"pygame_window_pos" : {
			u"name" : u"Window position",
			u"description" : u"Window position in window mode (format: 'x,y' or 'auto')",
			u"default" : u"auto",
			}
		}

	def __init__(self, experiment, bgcolor=None, fgcolor=None, auto_prepare=True):

		"""<DOC>
		Initializes the canvas.

		Arguments:
		experiment -- An instance of libopensesame.experiment.experiment.

		Keyword arguments:
		bgcolor -- A human-readable background color or None to use #
				   experiment default (default=None).
		fgcolor -- A human-readable foreground color or None to use #
				   experiment default (default=None).
		auto_prepare -- Indicates whether the canvas should be automatically #
					    prepared after each drawing operation, so that #
					    canvas.show() will be maximally efficient. If #
					    auto_prepare is turned off, drawing operations may #
					    be faster, but canvas.show() will take longer, #
					    unless canvas.prepare() is explicitly called in #
					    advance. Generally, it only makes sense to disable #
					    auto_prepare when you want to draw a large number #
						of stimuli, as in the second example below. #
						Currently, the auto_prepare parameter only applies #
						to the xpyriment backend, and is ignored by the other #
						backends (default=True).

		Example:
		>>> from openexp.canvas import canvas
		>>> my_canvas = canvas(exp)
		>>> my_canvas.fixdot()
		>>> my_canvas.show()

		Example:
		>>> from openexp.canvas import canvas
		>>> from random import randint
		>>> my_canvas = canvas(exp, auto_prepare=False)
		>>> for i in range(1000):
		>>>		x = randint(0, self.get('width'))
		>>>		y = randint(0, self.get('height'))
		>>> 	my_canvas.fixdot(x, y)
		>>> my_canvas.prepare()
		>>> my_canvas.show()

		</DOC>"""

		self.experiment = experiment
		self.html = html.html()
		if fgcolor == None:
			fgcolor = self.experiment.get(u"foreground")
		if bgcolor == None:
			bgcolor = self.experiment.get(u"background")
		self.set_fgcolor(fgcolor)
		self.set_bgcolor(bgcolor)
		self.penwidth = 1
		self.antialias = True
		self.surface = self.experiment.surface.copy()
		self._current_font = None
		self.bidi = self.experiment.get(u'bidi')==u'yes'
		self.set_font(style=self.experiment.font_family, size= \
			self.experiment.font_size, bold=self.experiment.font_bold==u'yes', \
			italic=self.experiment.font_italic==u'yes', underline= \
			self.experiment.font_underline==u'yes')
		self.clear()

	def color(self, color):

		"""
		Transforms a "human-readable" color into the format that is used by the#
		back-end (e.g., a PyGame color).

		Arguments:
		color -- A color in one the following formats (by example):
			255, 255, 255 (rgb)
			255, 255, 255, 255 (rgba)
			#f57900 (case-insensitive html)
			100 (integer intensity value 0 .. 255, for gray-scale)
			0.1 (float intensity value 0 .. 1.0, for gray-scale)

		Returns:
		A color in the back-end format
		"""

		return _color(color)

	def _font(self):

		"""
		Creates a PyGame font instance.

		Returns:
		A PyGame font.
		"""

		if self._current_font == None:
			# First see if the font refers to a file in the resources/ filepool
			try:
				font_path = self.experiment.resource(u'%s.ttf' % \
					self.font_style)
				self._current_font = pygame.font.Font(font_path, self.font_size)
			# If not, try to match a system font
			except:
				self._current_font = pygame.font.SysFont(self.font_style, \
					self.font_size)
			self._current_font.set_bold(self.font_bold)
			self._current_font.set_italic(self.font_italic)
			self._current_font.set_underline(self.font_underline)
		return self._current_font

	def flip(self, x=True, y=False):

		"""
		Flips the canvas along the x- and/ or y-axis. Note: This does not #
		refresh the display, like e.g., pygame.display.flip(), which is handled #
		by show().

		Keyword arguments:
		x -- A Boolean indicating whether the canvas should be flipped #
			 horizontally (default=True).
		y -- A Boolean indicating whether the canvas should be flipped #
			 vertically (default=False).

		Example:
		>>> from openexp.canvas import canvas
		>>> my_canvas = canvas(exp)
		>>> my_canvas.fixdot(x=100, color='green')
		>>> my_canvas.flip(x=True)
		"""

		self.surface = pygame.transform.flip(self.surface, x, y)

	def copy(self, canvas):

		"""<DOC>
		Turns the current canvas into a copy of the passed canvas. Note: If you #
		want to create a copy of a sketchpad canvas, it is more convenient to #
		use the inline_script.copy_sketchpad() function.

		Arguments:
		canvas -- The canvas to copy.

		Example:
		>>> from openexp.canvas import canvas
		>>> my_canvas = canvas(exp)
		>>> my_canvas.fixdot(x=100, color='green')
		>>> my_copied_canvas = canvas(exp)
		>>> my_copied_canvas.copy(my_canvas)
		>>> my_copied_canvas.fixdot(x=200, color="blue")
		>>> my_copied_canvas.show()
		</DOC>"""

		self.surface = canvas.surface.copy()
		self.font_style = canvas.font_style
		self.font_style = canvas.font_style
		self.penwidth = canvas.penwidth
		self.fgcolor = canvas.fgcolor
		self.bgcolor = canvas.bgcolor

	def xcenter(self):

		"""<DOC>
		Returns:
		The center X coordinate in pixels.

		Example:
		>>> from openexp.canvas import canvas
		>>> my_canvas = canvas(exp)
		>>> x1 = my_canvas.xcenter() - 100
		>>> y1 = my_canvas.ycenter() - 100
		>>> x2 = my_canvas.xcenter() + 100
		>>> y2 = my_canvas.ycenter() + 100
		>>> my_canvas.line(x1, y1, x2, y2)
		</DOC>"""

		return self.experiment.get(u'width') / 2

	def ycenter(self):

		"""<DOC>
		Returns:
		The center Y coordinate in pixels.

		Example:
		>>> from openexp.canvas import canvas
		>>> my_canvas = canvas(exp)
		>>> x1 = my_canvas.xcenter() - 100
		>>> y1 = my_canvas.ycenter() - 100
		>>> x2 = my_canvas.xcenter() + 100
		>>> y2 = my_canvas.ycenter() + 100
		>>> my_canvas.line(x1, y1, x2, y2)
		</DOC>"""

		return self.experiment.get(u'height') / 2

	def prepare(self):

		"""<DOC>
		Finishes up pending canvas operations (if any), so that a subsequent #
		call to show() is extra fast. It's generally not necessary to call this #
		function, unless you use a specific back-end that requires this. Also, #
		see the note on auto_prepare under __init__().
		</DOC>"""

		pass

	def show(self):

		"""<DOC>
		Puts ('flips') the canvas onto the screen.

		Returns:
		A timestamp containing the time at which the canvas actually appeared on #
		the screen (or a best guess).

		Example:
		>>> from openexp.canvas import canvas
		>>> my_canvas = canvas(exp)
		>>> my_canvas.fixdot()
		>>> t = my_canvas.show()
		>>> exp.set('time_fixdot', t)
		</DOC>"""

		self.experiment.surface.blit(self.surface, (0, 0))
		self.experiment.last_shown_canvas = self.surface
		pygame.display.flip()
		return pygame.time.get_ticks()


	def clear(self, color=None):

		"""<DOC>
		Clears the canvas with the current background color. Note that it is #
		generally better to use a different canvas for each experimental display, #
		than to use a single canvas and repeatedly clear and redraw it.

		Keyword arguments:
		color -- A custom human-readable background color to be used. This does #
				not affect the default background color as set by set_bgcolor(). #
				(Default=None)

		Example:
		>>> from openexp.canvas import canvas
		>>> my_canvas = canvas(exp)
		>>> my_canvas.fixdot(color='green')
		>>> my_canvas.show()
		>>> self.sleep(1000)
		>>> my_canvas.clear()
		>>> my_canvas.fixdot(color='red')
		>>> my_canvas.show()
		</DOC>"""

		if color != None:
			color = self.color(color)
		else:
			color = self.bgcolor
		self.surface.fill(color)

	def set_bidi(self, bidi):

		"""<DOC>
		Enables or disables bi-directional text support.

		Arguments:
		bidi	--	True to enable bi-directional text support, False to
					disable.
		</DOC>"""

		self.bidi = bidi

	def set_penwidth(self, penwidth):

		"""<DOC>
		Sets the pen width for subsequent drawing operations.

		Arguments:
		penwidth -- A pen width in pixels.

		Example:
		>>> from openexp.canvas import canvas
		>>> my_canvas = canvas(exp)
		>>> my_canvas.set_penwidth(10)
		>>> my_canvas.line(100, 100, 200, 200)
		</DOC>"""

		self.penwidth = penwidth

	def set_fgcolor(self, color):

		"""<DOC>
		Sets the foreground color for subsequent drawing operations.

		Arguments:
		color -- A color. Acceptable formats are human-readable colors, such as #
				 'red'; and HTML colors, such as '#FF0000'.

		Example:
		>>> from openexp.canvas import canvas
		>>> my_canvas = canvas(exp)
		>>> my_canvas.set_fgcolor('green')
		>>> my_canvas.text('Green text', y=200)
		>>> my_canvas.set_fgcolor('red')
		>>> my_canvas.text('Red text', y=400)
		</DOC>"""

		self.fgcolor = self.color(color)

	def set_bgcolor(self, color):

		"""<DOC>
		Sets the background color for the canvas.

		Arguments:
		color -- A color. Acceptable formats are human-readable colors, such as #
				 'red'; and HTML colors, such as '#FF0000'.

		Example:
		>>> from openexp.canvas import canvas
		>>> my_canvas = canvas(exp)
		>>> my_canvas.set_bgcolor('gray')
		>>> my_canvas.clear()
		</DOC>"""

		self.bgcolor = self.color(color)

	def set_font(self, style=None, size=None, italic=None, bold=None, underline=None):

		"""<DOC>
		Sets the font for subsequent drawing operations.

		Keyword arguments:
		style -- A font style. This can be one of the default fonts #
				 (e.g., 'mono'), a system font (e.g., 'arial'). #
				 or the name of a `.ttf` font file in the file pool (without #
				 the `.ttf` extension).
		size -- A font size in pixels (default=None).
		italic -- Indicates if the font should be italic (default=None).
		bold -- Indicates if the font should be bold (default=None).
		underline -- Indicates if the font should be underlined (default=None).

		Example:
		>>> from openexp.canvas import canvas
		>>> my_canvas = canvas(exp)
		>>> my_canvas.set_font(style='serif', italic=True)
		>>> my_canvas.text('Text in italic serif')
		</DOC>"""

		self._current_font = None
		if style != None: self.font_style = style
		if size != None: self.font_size = size
		if italic != None: self.font_italic = italic
		if bold != None: self.font_bold = bold
		if underline != None: self.font_underline = underline

	def fixdot(self, x=None, y=None, color=None, style=u'default'):

		"""<DOC>
		Draws a fixation dot. Various styles are available ('default' equals #
		'medium-open'):

		- 'large-filled' is a filled circle with a 16px radius.
		- 'medium-filled' is a filled circle with an 8px radius.
		- 'small-filled' is a filled circle with a 4px radius.
		- 'large-open' is a filled circle with a 16px radius and a 2px hole.
		- 'medium-open' is a filled circle with an 8px radius and a 2px hole.
		- 'small-open' is a filled circle with a 4px radius and a 2px hole.
		- 'large-cross' is 16px cross.
		- 'medium-cross' is an 8px cross.
		- 'small-cross' is a 4px cross.

		Keyword arguments:
		x		--	The center X coordinate. None = center (default=None).
		y 		--	The center Y coordinate. None = center (default=None).
		color	--	A custom human-readable foreground color. This does not #
					affect the default foreground color as set by #
					set_fgcolor(). (default=None)
		style	--	One of: default, large-filled, medium-filled, small-filled, #
					large-open, medium-open, small-open, large-cross, #
					medium-cross, small-cross. default equals medium-open. #
					(default=u'default')

		Example:
		>>> from openexp.canvas import canvas
		>>> my_canvas = canvas(exp)
		>>> my_canvas.fixdot()
		"""

		if color != None:
			color = self.color(color)
		else:
			color = self.fgcolor
		if x == None:
			x = self.xcenter()
		if y == None:
			y = self.ycenter()

		h = 2
		if u'large' in style:
			s = 16
		elif u'medium' in style or style == u'default':
			s = 8
		elif u'small' in style:
			s = 4
		else:
			raise osexception(u'Unknown style: %s' % self.style)

		if u'open' in style or style == u'default':
			self.ellipse(x-s, y-s, 2*s, 2*s, True, color=color)
			self.ellipse(x-h, y-h, 2*h, 2*h, True, color=self.bgcolor)
		elif u'filled' in style:
			self.ellipse(x-s, y-s, 2*s, 2*s, True, color=color)
		elif u'cross' in style:
			self.line(x, y-s, x, y+s, color=color)
			self.line(x-s, y, x+s, y, color=color)
		else:
			raise osexception(u'Unknown style: %s' % self.style)

	def circle(self, x, y, r, fill=False, color=None):

		"""<DOC>
		Draws a circle.

		Arguments:
		x -- The center X coordinate.
		y -- The center Y coordinate.
		r -- The radius.

		Keyword arguments:
		fill -- A Boolean indicating whether the circle is outlined (False) #
				or filled (True). (Default=False)
		color -- A custom human-readable foreground color. This does not #
				 affect the default foreground color as set by #
				 set_fgcolor(). (Default=None)

		Example:
		>>> from openexp.canvas import canvas
		>>> my_canvas = canvas(exp)
		>>> my_canvas.circle(100, 100, 50, fill=True, color='red')
		</DOC>"""

		self.ellipse(x-r, y-r, 2*r, 2*r, fill=fill, color=color)

	def line(self, sx, sy, ex, ey, color=None):

		"""<DOC>
		Draws a line.

		Arguments:
		sx -- The left coordinate.
		sy -- The top coordinate.
		ex -- The right coordinate.
		ey -- The bottom coordinate.

		Keyword arguments:
		color -- A custom human-readable foreground color. This does not #
				 affect the default foreground color as set by #
				 set_fgcolor(). (Default=None)

		Example:
		>>> from openexp.canvas import canvas
		>>> my_canvas = canvas(exp)
		>>> w = self.get('width')
		>>> h = self.get('height')
		>>> my_canvas.line(0, 0, w, h)
		</DOC>"""

		if color != None:
			color = self.color(color)
		else:
			color = self.fgcolor
		pygame.draw.line(self.surface, color, (sx, sy), (ex, ey), self.penwidth)

	def arrow(self, sx, sy, ex, ey, arrow_size=5, color=None):

		"""<DOC>
		Draws an arrow. An arrow is a line, with an arrowhead at (ex, ey). The #
		angle between the arrowhead lines and the arrow line is 45 degrees.

		Arguments:
		sx -- The left coordinate.
		sy -- The top coordinate.
		ex -- The right coordinate.
		ey -- The bottom coordinate.

		Keyword arguments:
		arrow_size -- The length of the arrowhead lines (default=5).
		color -- A custom human-readable foreground color. This does not affect #
				the default foreground color as set by set_fgcolor(). #
				(Default=None)

		Example:
		>>> from openexp.canvas import canvas
		>>> my_canvas = canvas(exp)
		>>> w = self.get('width')/2
		>>> h = self.get('height')/2
		>>> my_canvas.line(0, 0, w, h, arrow_size=10)
		</DOC>"""

		self.line(sx, sy, ex, ey, color=color)
		a = math.atan2(ey - sy, ex - sx)
		_sx = ex + arrow_size * math.cos(a + math.radians(135))
		_sy = ey + arrow_size * math.sin(a + math.radians(135))
		self.line(_sx, _sy, ex, ey, color=color)
		_sx = ex + arrow_size * math.cos(a + math.radians(225))
		_sy = ey + arrow_size * math.sin(a + math.radians(225))
		self.line(_sx, _sy, ex, ey, color=color)

	def rect(self, x, y, w, h, fill=False, color=None):

		"""<DOC>
		Draws a rectangle.

		Arguments:
		x -- The left X coordinate.
		y -- The top Y coordinate.
		w -- The width.
		h -- The height.

		Keyword arguments:
		fill -- A Boolean indicating whether the rectangle is outlined (False) #
				or filled (True). (Default=False)
		color -- A custom human-readable foreground color. This does not affect #
				the default foreground color as set by set_fgcolor(). #
				(Default=None)

		Example:
		>>> from openexp.canvas import canvas
		>>> my_canvas = canvas(exp)
		>>> w = self.get('width')-10
		>>> h = self.get('height')-10
		>>> my_canvas.rect(10, 10, w, h, fill=True)
		</DOC>"""

		if color != None:
			color = self.color(color)
		else:
			color = self.fgcolor
		if fill:
			pygame.draw.rect(self.surface, color, (x, y, w, h), 0)
		else:
			pygame.draw.rect(self.surface, color, (x, y, w, h), self.penwidth)

	def ellipse(self, x, y, w, h, fill=False, color=None):

		"""<DOC>
		Draws an ellipse.

		Arguments:
		x -- The left X coordinate.
		y -- The top Y coordinate.
		w -- The width.
		h -- The height.

		Keyword arguments:
		fill -- A Boolean indicating whether the ellipse is outlined (False) or #
				filled (True). (Default=False)
		color -- A custom foreground color. This does not affect the default #
				 foreground color as set by set_fgcolor(). (Default=None)

		Example:
		>>> from openexp.canvas import canvas
		>>> my_canvas = canvas(exp)
		>>> w = self.get('width')-10
		>>> h = self.get('height')-10
		>>> my_canvas.ellipse(10, 10, w, h, fill=True)
		</DOC>"""

		if color != None:
			color = self.color(color)
		else:
			color = self.fgcolor
		x = int(x)
		y = int(y)
		w = int(w)
		h = int(h)
		if fill:
			pygame.draw.ellipse(self.surface, color, (x, y, w, h), 0)
		else:
			# Because the default way of drawing thick lines gives ugly results
			# for ellipses, we draw thick ellipses manually, by drawing an
			# ellipse with the background color inside of it
			i = self.penwidth / 2
			j = self.penwidth - i
			pygame.draw.ellipse(self.surface, color, (x-i, y-i, w+2*i, h+2*i), \
				0)
			pygame.draw.ellipse(self.surface, self.bgcolor, (x+j, y+j, w-2*j, \
				h-2*j), 0)

	def polygon(self, vertices, fill=False, color=None):

		"""<DOC>
		Draws a polygon that consists of multiple vertices (i.e. a shape of #
		points connected by lines).

		Arguments:
		vertices -- A list of tuples, where each tuple corresponds to a vertex. #
					For example, [(100,100), (200,100), (100,200)] will draw a #
					triangle.

		Keyword arguments:
		fill -- A Boolean indicating whether the rectangle is outlined (False) #
				or filled (True). (Default=False)
		color -- A custom human-readable foreground color. This does not affect #
				the default foreground color as set by set_fgcolor(). #
				(Default=None)

		Example:
		>>> from openexp.canvas import canvas
		>>> my_canvas = canvas(exp)
		>>> n1 = 0,0
		>>> n2 = 100, 100
		>>> n3 = 0, 100
		>>> my_canvas.polygon([n1, n2, n3])
		</DOC>"""

		if color != None:
			color = self.color(color)
		else:
			color = self.fgcolor
		if fill:
			width = 0
		else:
			width = self.penwidth
		pygame.draw.polygon(self.surface, color, vertices, width)

	def text_size(self, text):

		"""<DOC>
		Determines the size of a text string in pixels.

		Arguments:
		text -- The text string.

		Returns:
		A (width, height) tuple containing the dimensions of the text string.

		Example:
		>>> from openexp.canvas import canvas
		>>> my_canvas = canvas(exp)
		>>> w, h = my_canvas.text_size('Some text')
		</DOC>"""

		return self._font().size(text)

	def text(self, text, center=True, x=None, y=None, max_width=None, color=None, bidi=None, html=True):

		"""<DOC>
		Draws text.

		Arguments:
		text		--	The text string.

		Keyword arguments:
		center		--	A Boolean indicating whether the coordinates reflect the
						center (True) or top-left (default=True).
		x			--	The X coordinate. None = center. (Default=None)
		y			--	The Y coordinate. None = center. (Default=None)
		max_width	--	The maximum width of the text, before wrapping to a new
						line, or None to wrap at screen edge (default=None)
		color		--	A custom human-readable foreground color. This does not
						affect the default foreground color as set by
						set_fgcolor(). (Default=None)
		bidi		--	True or False for bi-directional text support, or None
						to use experiment default. This does not affect the
						default bidi setting as set by set_bidi().
						(Default=None)
		html		--	Indicates whether HTML tags should be parsed
						(default=True).

		Example:
		>>> from openexp.canvas import canvas
		>>> my_canvas = canvas(exp)
		>>> my_canvas.text('Some text with <b>boldface</b> and <i>italics</i>')
		</DOC>"""

		if color != None: color = self.color(color)
		else: color = self.fgcolor
		if bidi == None: bidi = self.bidi
		if x == None: x = self.xcenter()
		if y == None: y = self.ycenter()
		self.html.reset()
		self.html.render(text, x, y, self, max_width=max_width, center=center, \
			color=color, html=html, bidi=bidi)

	def _text(self, text, x, y):

		"""
		A simple function that renders a string of text with the canvas default
		settings. This is the only function that needs to be re-implemented in
		other back-ends, as it is the only function that should handle actual
		text rendering.

		Arguments:
		text -- The text.
		x -- The x-coordinate.
		y -- The y-coordinate.
		"""

		font = self._font()
		surface = font.render(text, self.antialias, self.fgcolor)
		self.surface.blit(surface, (x, y))

	def textline(self, text, line, color=None):

		"""<DOC>
		A convenience function that draws a line of text based on a line number. #
		The text strings are centered on the X-axis and vertically spaced with #
		1.5 times the line height as determined by text_size().

		Arguments:
		text -- The text string.
		line -- A line number, where 0 is the center and > 0 is below the #
				center.

		Keyword arguments:
		color -- A human-readable custom foreground color. This does not affect #
				the default 	foreground color as set by set_fgcolor(). #
				(Default=None)

		Example:
		>>> from openexp.canvas import canvas
		>>> my_canvas = canvas(exp)
		>>> my_canvas.textline('A line', 0)
		>>> my_canvas.textline('Another line', 1)
		</DOC>"""

		font = self._font()
		size = self.text_size(text)
		self.text(text, True, self.xcenter(), self.ycenter()+1.5*line*size[1], \
			color=color)

	def image(self, fname, center=True, x=None, y=None, scale=None):

		"""<DOC>
		Draws an image from file. This function does not look in the file #
		pool, but takes an absolute path.

		Arguments:
		fname		--	The path of the file. If this is a Unicode string, it #
						is intepreted as utf-8 encoding.

		Keyword arguments:
		center		--	A Boolean indicating whether the given coordinates #
						reflect the center (True) or the top-left (False) of #
						the image default=True).
		x			--	The X coordinate. None = center. (Default=None)
		y			--	The Y coordinate. None = center. (Default=None)
		scale		--	The scaling factor of the image. 1.0 or None = #
						no scaling, 2.0 = twice as large, etc. (default=None).

		Example:
		>>> from openexp.canvas import canvas
		>>> my_canvas = canvas(exp)
		>>> # Determine the absolute path:
		>>> path = exp.get_file(u'image_in_pool.png')
		>>> my_canvas.image(path)
		</DOC>"""

		if isinstance(fname, unicode):
			fname = fname.encode(self.experiment.encoding)
		try:
			surface = pygame.image.load(fname)
		except pygame.error as e:
			raise osexception( \
				u"'%s' is not a supported image format" % fname)

		if scale != None:
			try:
				surface = pygame.transform.smoothscale(surface, \
					(int(surface.get_width()*scale), \
					int(surface.get_height()*scale)))
			except:
				debug.msg(u"smooth scaling failed for '%s'" % fname, reason=\
					u"warning")
				surface = pygame.transform.scale(surface, \
					(int(surface.get_width()*scale), \
					int(surface.get_height()*scale)))

		size = surface.get_size()
		if x == None:
			x = self.xcenter()
		if y == None:
			y = self.ycenter()
		if center:
			x -= size[0] / 2
			y -= size[1] / 2
		self.surface.blit(surface, (x, y))

	def gabor(self, x, y, orient, freq, env=u"gaussian", size=96, stdev=12, phase=0, col1=u"white", col2=u"black", bgmode=u"avg"):

		"""<DOC>
		Draws a Gabor patch. The exact rendering of the Gabor patch depends on the #
		back-end.

		Arguments:
		x -- The center X coordinate.
		y -- The center Y coordinate.
		orient -- Orientation in degrees [0 .. 360].
		freq -- Frequency in cycles/px of the sinusoid.

		Keyword arguments:
		env -- Any of the following: "gaussian", "linear", "circular", #
			   "rectangle" (default="gaussian").
		size -- Size in pixels (default=96).
		stdev -- Standard deviation in pixels of the gaussian. Only applicable #
				 if env = "gaussian". (Default=12)
		phase -- Phase of the sinusoid [0.0 .. 1.0] (default=0).
		col1 -- Human-readable color for the tops (default="white").
		col2 -- Human-readable color for the troughs. Note: This parameter is #
				ignored by the psycho backend. (Default="black").
		bgmode -- Specifies whether the background is the average of col1 and #
				  col2 (bgmode = "avg", a typical Gabor patch) or equal to col2 #
				  ("col2"), useful for blending into the background. Note: this #
				  parameter is ignored by the psycho backend. (Default="avg")

		Example:
		>>> from openexp.canvas import canvas
		>>> my_canvas = canvas(exp)
		>>> my_canvas.gabor(100, 100, 45, .05)
		</DOC>"""

		surface = _gabor(orient, freq, env, size, stdev, phase, col1, col2, \
			bgmode)
		self.surface.blit(surface, (x - 0.5 * size, y - 0.5 * size))

	def noise_patch(self, x, y, env=u"gaussian", size=96, stdev=12, col1=u"white", col2=u"black", bgmode=u"avg"):

		"""<DOC>
		Draws a patch of noise, with an envelope. The exact rendering of the noise #
		patch depends on the back-end.

		Arguments:
		x -- The center X coordinate.
		y -- The center Y coordinate.

		Keyword arguments:
		env -- Any of the following: "gaussian", "linear", "circular", #
			   "rectangle" (default="gaussian").
		size -- Size in pixels (default=96).
		stdev -- Standard deviation in pixels of the gaussian. Only applicable #
				 if env = "gaussian". (Default=12)
		phase -- Phase of the sinusoid [0.0 .. 1.0] (default=0).
		col1 -- Human-readable color for the tops (default="white").
		col2 -- Human-readable color for the troughs (default="black").
		bgmode -- Specifies whether the background is the average of col1 and #
				  col2 (bgmode="avg", a typical noise patch) or equal to col2 #
				  ("col2"), useful for blending into the background #
				  (default="avg").

		Example:
		>>> from openexp.canvas import canvas
		>>> my_canvas = canvas(exp)
		>>> my_canvas.noise_patch(100, 100, env='circular')
		</DOC>"""

		surface = _noise_patch(env, size, stdev, col1, col2, bgmode)
		self.surface.blit(surface, (x - 0.5 * size, y - 0.5 * size))

"""
Static methods
"""

def init_display(experiment):

	"""
	Initialize the display before the experiment begins.

	Arguments:
	experiment -- An instance of libopensesame.experiment.experiment. The
				  following properties are of particular importance:
				  experiment.fullscreen (bool), experiment.width (int) and
				  experiment.height (int). The experiment also contains default
				  font settings as experiment.font_family (str) and
				  experiment.font_size (int).
	"""

	# Intialize PyGame
	pygame.init()

	# Set the window icon
	surf = pygame.Surface( (32, 32) )
	surf.fill( (255, 255, 255) )
	pygame.draw.circle(surf, (0, 0, 255), (16, 16), 10, 4)
	pygame.display.set_icon(surf)

	# Determine the video mode
	mode = 0
	if experiment.get_check(u"pygame_hwsurface", u"yes", [u"yes", u"no"]) == \
		u"yes":
		mode = mode | pygame.HWSURFACE
		print( \
			u"openexp._canvas.legacy.init_display(): enabling hardware surface")
	else:
		print( \
			u"openexp._canvas.legacy.init_display(): not enabling hardware surface")

	if experiment.get_check(u"pygame_doublebuf", u"yes", [u"yes", u"no"]) == \
		u"yes":
		mode = mode | pygame.DOUBLEBUF
		print( \
			u"openexp._canvas.legacy.init_display(): enabling double buffering")
	else:
		print( \
			u"openexp._canvas.legacy.init_display(): not enabling double buffering")

	if pygame.display.mode_ok(experiment.resolution(), mode):
		print(u"openexp._canvas.legacy.init_display(): video mode ok")
	else:
		print( \
			u"openexp._canvas.legacy.init_display(): warning: video mode not ok")

	if experiment.fullscreen:
		mode = mode | pygame.FULLSCREEN

	if experiment.get_check(u'pygame_window_frame', u'yes', [u'yes', u'no']) \
		== u'no':
		mode = mode | pygame.NOFRAME

	if experiment.get_check(u'pygame_window_pos', u'auto') != u'auto':
		os.environ[u'SDL_VIDEO_WINDOW_POS'] = experiment.get( \
			u'pygame_window_pos')

	# Create the window and the surface
	experiment.window = pygame.display.set_mode(experiment.resolution(), mode)
	pygame.display.set_caption(u'OpenSesame (legacy backend)')
	pygame.mouse.set_visible(False)
	experiment.surface = pygame.display.get_surface()

	# Create a font, falling back to the default font
	experiment.font = pygame.font.Font(experiment.resource(u"%s.ttf" \
		% experiment.font_family), experiment.font_size)
	if experiment.font == None:
		debug.msg(u"'%s.ttf' not found, falling back to default font" \
			% experiment.font_family)
		experiment.font = pygame.font.Font(None, experiment.font_size)

	# Set the time functions to use pygame
	experiment._time_func = pygame.time.get_ticks
	experiment._sleep_func = pygame.time.delay
	experiment.time = experiment._time_func
	experiment.sleep = experiment._sleep_func

def close_display(experiment):

	"""
	Close the display after the experiment is finished.

	Arguments:
	experiment -- An instance of libopensesame.experiment.experiment
	"""

	pygame.display.quit()

"""
The functions below are specific to the legacy backend and do not have to be
implemented in other backends.
"""

canvas_cache = {}

def _color(color):

	"""
	See canvas.color()
	"""

	if isinstance(color, unicode):
		return pygame.Color(str(color))
	if isinstance(color, str):
		return pygame.Color(color)
	if isinstance(color, int):
		return pygame.Color(color, color, color, 255)
	if isinstance(color, float):
		i = int(255 * color)
		return pygame.Color(i, i, i, 255)
	if isinstance(color, tuple):
		if len(color) == 3:
			return pygame.Color(color[0], color[1], color[2], 255)
		if len(color) > 3:
			return pygame.Color(color[0], color[1], color[2], color[3])
		raise osexception(u'Unknown color: %s' % color)
	if isinstance(color, pygame.Color):
		return color
	raise osexception(u'Unknown color: %s' % color)

def _gabor(orient, freq, env=u"gaussian", size=96, stdev=12, phase=0, col1= \
	u"white", col2=u"black", bgmode=u"avg"):

	"""
	Returns a pygame surface containing a Gabor patch.
	See canvas.gabor()
	"""

	env = _match_env(env)
	# Generating a Gabor patch takes quite some time, so keep
	# a cache of previously generated Gabor patches to speed up
	# the process.
	global canvas_cache
	key = u"gabor_%s_%s_%s_%s_%s_%s_%s_%s_%s" % (orient, freq, env, size, \
		stdev, phase, col1, col2, bgmode)
	if key in canvas_cache:
		return canvas_cache[key]
	# Create a surface
	surface = pygame.Surface( (size, size) )
	px = pygame.PixelArray(surface)
	# Conver the orientation to radians
	orient = math.radians(orient)
	col1 = _color(col1)
	col2 = _color(col2)
	# rx and ry reflect the real coordinates in the
	# target image
	for rx in range(size):
		for ry in range(size):
			# Distance from the center
			dx = rx - 0.5 * size
			dy = ry - 0.5 * size
			# Get the coordinates (x, y) in the unrotated
			# Gabor patch
			t = math.atan2(dy, dx) + orient
			r = math.sqrt(dx ** 2 + dy ** 2)
			ux = r * math.cos(t)
			uy = r * math.sin(t)
			# Get the amplitude without the envelope (0 .. 1)
			amp = 0.5 + 0.5 * math.cos(2.0 * math.pi * (ux * freq + phase))
			# The envelope adjustment
			if env == "g":
				f = math.exp(-0.5 * (ux / stdev) ** 2 - 0.5 * (uy / stdev) ** 2)
			elif env == "l":
				f = max(0, (0.5 * size - r) / (0.5 * size))
			elif env == "c":
				if (r > 0.5 * size):
					f = 0.0
				else:
					f = 1.0
			else:
				f = 1.0
			# Apply the envelope
			if bgmode == u"avg":
				amp = amp * f + 0.5 * (1.0 - f)
			else:
				amp = amp * f
			r = col1.r * amp + col2.r * (1.0 - amp)
			g = col1.g * amp + col2.g * (1.0 - amp)
			b = col1.b * amp + col2.b * (1.0 - amp)
			px[rx][ry] = r, g, b
	canvas_cache[key] = surface
	del px
	return surface

def _noise_patch(env=u"gaussian", size=96, stdev=12, col1=u"white", col2= \
	u"black", bgmode=u"avg"):

	"""
	Returns a pygame surface containing a noise patch.
	See canvas.noise_patch()
	"""

	env = _match_env(env)
	# Generating a noise patch takes quite some time, so keep
	# a cache of previously generated noise patches to speed up
	# the process.
	global canvas_cache
	key = u"noise_%s_%s_%s_%s_%s_%s" % (env, size, stdev, col1, col2, bgmode)
	if key in canvas_cache:
		return canvas_cache[key]
	# Create a surface
	surface = pygame.Surface( (size, size) )
	px = pygame.PixelArray(surface)
	col1 = _color(col1)
	col2 = _color(col2)
	# rx and ry reflect the real coordinates in the
	# target image
	for rx in range(size):
		for ry in range(size):
			# Distance from the center
			ux = rx - 0.5 * size
			uy = ry - 0.5 * size
			r = math.sqrt(ux ** 2 + uy ** 2)
			# Get the amplitude without the envelope (0 .. 1)
			amp = random.random()
			# The envelope adjustment
			if env == u"g":
				f = math.exp(-0.5 * (ux / stdev) ** 2 - 0.5 * (uy / stdev) ** 2)
			elif env == u"l":
				f = max(0, (0.5 * size - r) / (0.5 * size))
			elif env == u"c":
				if (r > 0.5 * size):
					f = 0.0
				else:
					f = 1.0
			else:
				f = 1.0
			# Apply the envelope
			if bgmode == u"avg":
				amp = amp * f + 0.5 * (1.0 - f)
			else:
				amp = amp * f
			r = col1.r * amp + col2.r * (1.0 - amp)
			g = col1.g * amp + col2.g * (1.0 - amp)
			b = col1.b * amp + col2.b * (1.0 - amp)
			px[rx][ry] = r, g, b
	canvas_cache[key] = surface
	del px
	return surface

def _match_env(env):

	"""
	Allows for easy translation between various envelope names

	Arguments:
	env -- an envelope name

	Exception:
	Throws an osexception if an unknown envelope was specified

	Returns:
	A standard envelope name ("c", "g", "r" or "l")
	"""

	global env_synonyms
	if env not in env_synonyms:
		raise osexception(u"'%s' is not a valid envelope" % env)
	return env_synonyms[env]

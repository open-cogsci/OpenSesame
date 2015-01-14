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

import random
import pygame
import math
from libopensesame.exceptions import osexception

# If available, use the yaml.inherit metaclass to copy the docstrings from
# canvas onto the back-end-specific implementations of this class (legacy, etc.)
try:
	from yamldoc import inherit as docinherit
except:
	docinherit = type

class canvas(object):

	"""
	desc: |
		The `canvas` class is used for display presentation.

		__Important note:__

		When using a `canvas` all coordinates are specified
		relative to the top-left of the display, and not, as in `sketchpad`s,
		relative to the display center.

		__Example__:

		~~~ {.python}
		# Create a canvas with a central fixation dot and show it.
		from openexp.canvas import canvas
		my_canvas = canvas(exp)
		my_canvas.fixdot()
		my_canvas.show()
		~~~

		__Function list:__

		%--
		toc:
			mindepth: 2
			maxdepth: 2
		--%

		%--
		constant:
			arg_fgcolor: |
				A human-readable foreground color, such as 'red', an
				HTML-style color value, such as '#FF0000', or `None` to use the
				canvas default. This argument will not change the canvas default
				foreground as set by [canvas.set_fgcolor].
			arg_bgcolor: |
				A human-readable background color, such as 'red', an
				HTML-style color value, such as '#FF0000', or `None` to use the
				canvas default. This argument will not change the canvas default
				background as set by [canvas.set_bgcolor].
			arg_penwidth: |
				A penwidth in pixels, or `None` to use the canvas default. This
				argument will not change the canvas default penwidth as set by
				[canvas.set_penwidth].
			arg_max_width: |
				The maximum width of the text in pixels, before wrapping to a
				new line, or `None` to wrap at screen edge.
			arg_bidi: |
				A bool indicating bi-directional text support should be enabled,
				or `None` to use the experiment default. This does not affect
				the canvas default bidi setting as set by [canvas.set_bidi].
			arg_html: |
				A bool indicating whether a subset of HTML tags should be
				interpreted. For more information, see </usage/text/>.
			arg_bgmode: |
				Specifies whether the background is the average of col1 col2
				('avg', corresponding to a typical Gabor patch), or equal to
				col2 ('col2'), useful for blending into the	background. Note:
				this parameter is ignored by the psycho backend, which uses
				increasing transparency for the background.
			arg_fill: |
				Specifies whether the shape should be filled (True) or consist
				of an outline (False).
		--%
	"""

	__metaclass__ = docinherit

	def __init__(self, experiment, bgcolor=None, fgcolor=None,
		auto_prepare=True):

		"""
		desc:
			Constructor to create a new `canvas` object.

		arguments:
			experiment:
				desc:	The experiment object.
				type:	experiment

		keywords:
			bgcolor:
				desc:	A human-readable background color or None to use
						experiment default.
				type:	[str, unicode, NoneType]
			fgcolor:
				desc:	A human-readable foreground color or None to use
						experiment default.
				type:	[str, unicode, NoneType]
			auto_prepare:
				desc:	Indicates whether the canvas should be automatically
						prepared after each drawing operation, so that
						[canvas.show] will be maximally efficient. If
						auto_prepare is turned off, drawing operations may
						be faster, but [canvas.show] will take longer,
						unless [canvas.prepare] is explicitly called in
						advance. Generally, it only makes sense to disable
						auto_prepare when you want to draw a large number
						of stimuli, as in the second example below.
						Currently, the auto_prepare parameter only applies
						to the xpyriment backend, and is ignored by the
						other backends.
				type:	bool

		example: |
			# Example 1: Show a central fixation dot.
			from openexp.canvas import canvas
			my_canvas = canvas(exp)
			my_canvas.fixdot()
			my_canvas.show()

			# Example 2: Show many randomly positioned fixation dot. Here we
			# disable `auto_prepare`, so that drawing goes more quickly.
			from openexp.canvas import canvas
			from random import randint
			my_canvas = canvas(exp, auto_prepare=False)
			for i in range(1000):
				x = randint(0, self.get('width'))
				y = randint(0, self.get('height'))
				my_canvas.fixdot(x, y)
			my_canvas.prepare()
			my_canvas.show()
		"""

		raise NotImplementedError()

	def color(self, color):

		"""
		desc:
			Transforms a "human-readable" color into the format that is used by
			the back-end (e.g., a PyGame color).

		visible: False

		arguments:
			color: |
				A color in one the following formats (by example):
				- 255, 255, 255 (rgb)
				- 255, 255, 255, 255 (rgba)
				- #f57900 (case-insensitive html)
				- 100 (integer intensity value 0 .. 255, for gray-scale)
				- 0.1 (float intensity value 0 .. 1.0, for gray-scale)

		returns:
			A color in a back-end-specific format.
		"""

		raise NotImplementedError()

	def copy(self, canvas):

		"""
		desc: |
			Turns the current `canvas` into a copy of the passed `canvas`.

			__Note:__

			If you want to create a copy of a `sketchpad` `canvas`, you can also
			use the `inline_script.copy_sketchpad` function.

		arguments:
			canvas:
				desc:	The `canvas` to copy.
				type:	canvas

		example: |
			from openexp.canvas import canvas
			my_canvas = canvas(exp)
			my_canvas.fixdot(x=100, color='green')
			my_copied_canvas = canvas(exp)
			my_copied_canvas.copy(my_canvas)
			my_copied_canvas.fixdot(x=200, color="blue")
			my_copied_canvas.show()
		"""

		raise NotImplementedError()

	def xcenter(self):

		"""
		desc:
			Returns the center X coordinate of the `canvas` in pixels.

		returns:
			desc:	The center X coordinate.
			type:	int

		example: |
			# Draw a diagonal line through the center of the canvas
			from openexp.canvas import canvas
			my_canvas = canvas(exp)
			x1 = my_canvas.xcenter() - 100
			y1 = my_canvas.ycenter() - 100
			x2 = my_canvas.xcenter() + 100
			y2 = my_canvas.ycenter() + 100
			my_canvas.line(x1, y1, x2, y2)
		"""

		return self.experiment.get(u'width') / 2

	def ycenter(self):

		"""
		desc:
			Returns the center Y coordinate of the `canvas` in pixels.

		returns:
			desc:	The center Y coordinate.
			type:	int

		example: |
			# Draw a diagonal line through the center of the canvas
			from openexp.canvas import canvas
			my_canvas = canvas(exp)
			x1 = my_canvas.xcenter() - 100
			y1 = my_canvas.ycenter() - 100
			x2 = my_canvas.xcenter() + 100
			y2 = my_canvas.ycenter() + 100
			my_canvas.line(x1, y1, x2, y2)
		"""

		return self.experiment.get(u'height') / 2

	def prepare(self):

		"""
		desc:
			Finishes pending canvas operations (if any), so that a subsequent
			call to [canvas.show] is extra fast. It's only necessary to call
			this function if you have disabled `auto_prepare` in
			[canvas.__init__].
		"""

		pass

	def show(self):

		"""
		desc:
			Shows, or 'flips', the canvas on the screen.

		returns:
			desc:
				A timestamp of the time at which the canvas actually appeared on
				the screen, or a best guess if precise temporal information is
				not available. For more information about timing, see
				</misc/timing>. Depending on the back-end the timestamp is an
				`int` or a `float`.
			type:
				[int, float]


		example: |
			from openexp.canvas import canvas
			my_canvas = canvas(exp)
			my_canvas.fixdot()
			t = my_canvas.show()
			exp.set('time_fixdot', t)
		"""

		raise NotImplementedError()

	def clear(self, color=None):

		"""
		desc:
			Clears the canvas with the current background color. Note that it is
			generally faster to use a different canvas for each experimental
			display than to use a single canvas and repeatedly clear and redraw
			it.

		keywords:
			color:
				desc:	"%arg_bgcolor"
				type:	[str, unicode, NoneType]

		example: |
			from openexp.canvas import canvas
			my_canvas = canvas(exp)
			my_canvas.fixdot(color='green')
			my_canvas.show()
			self.sleep(1000)
			my_canvas.clear()
			my_canvas.fixdot(color='red')
			my_canvas.show()
		"""

		raise NotImplementedError()

	def set_bidi(self, bidi):

		"""
		desc:
			Enables or disables bi-directional text support.

		arguments:
			bidi:
				desc:	True to enable bi-directional text support, False to
						disable.
				type:	bool

		example: |
			from openexp.canvas import canvas
			my_canvas = canvas(exp)
			my_canvas.set_bidi(True)
			my_canvas.text(u'חלק מטקסט')
		"""

		self.bidi = bidi

	def set_penwidth(self, penwidth):

		"""
		desc:
			Sets the default penwidth for subsequent drawing operations.

		arguments:
			penwidth:
				desc:	A penwidth in pixels.
				type:	int

		example: |
			from openexp.canvas import canvas
			my_canvas = canvas(exp)
			my_canvas.set_penwidth(10)
			my_canvas.line(100, 100, 200, 200)
		"""

		self.penwidth = penwidth

	def set_fgcolor(self, color):

		"""
		desc:
			Sets the default foreground color for subsequent drawing operations.

		arguments:
			color:
				desc:	"%arg_fgcolor"
				type:	[str, unicode]

		example: |
			from openexp.canvas import canvas
			my_canvas = canvas(exp)
			my_canvas.set_fgcolor('green')
			my_canvas.text('Green text', y=200)
			my_canvas.set_fgcolor('red')
			my_canvas.text('Red text', y=400)
		"""

		self.fgcolor = self.color(color)

	def set_bgcolor(self, color):

		"""
		desc:
			Sets the default background color for subsequent drawing operations,
			notably [canvas.clear].

		arguments:
			color:
				desc:	"%arg_bgcolor"
				type:	[str, unicode]

		example: |
			from openexp.canvas import canvas
			my_canvas = canvas(exp)
			my_canvas.set_bgcolor('gray')
			my_canvas.clear()
		"""

		self.bgcolor = self.color(color)

	def set_font(self, style=None, size=None, italic=None, bold=None,
		underline=None):

		"""
		desc:
			Sets the default font for subsequent drawing operations, notably
			[canvas.text].

		keywords:
			style:
				desc:	A font family. This can be one of the default fonts
						(e.g., 'mono'), a system font (e.g., 'arial'), the
						name of a `.ttf` font file in the file pool (without
						the `.ttf` extension), or `None` to use the experiment
						default.
				type:	[str, unicode]
			size:
				desc:	A font size in pixels, or `None` to use the experiment
						default.
				type:	int
			italic:
				desc:	A bool indicating whether the font should be italic, or
						`None` to use the experiment default.
				type:	bool, NoneType
			bold:
				desc:	A bool indicating whether the font should be bold, or
						`None` to use the experiment default.
				type:	bool, NoneType
			underline:
				desc:	A bool indicating whether the font should be underlined,
						or `None` to use the experiment default.
				type:	bool, NoneType

		example: |
			from openexp.canvas import canvas
			my_canvas = canvas(exp)
			my_canvas.set_font(style='serif', italic=True)
			my_canvas.text('Text in italic serif')
		"""

		if style != None: self.font_style = style
		if size != None: self.font_size = size
		if italic != None: self.font_italic = italic
		if bold != None: self.font_bold = bold
		if underline != None: self.font_underline = underline

	def fixdot(self, x=None, y=None, color=None, style=u'default'):

		"""
		desc: |
			Draws a fixation dot.

			- 'large-filled' is a filled circle with a 16px radius.
			- 'medium-filled' is a filled circle with an 8px radius.
			- 'small-filled' is a filled circle with a 4px radius.
			- 'large-open' is a filled circle with a 16px radius and a 2px hole.
			- 'medium-open' is a filled circle with an 8px radius and a 2px hole.
			- 'small-open' is a filled circle with a 4px radius and a 2px hole.
			- 'large-cross' is 16px cross.
			- 'medium-cross' is an 8px cross.
			- 'small-cross' is a 4px cross.

		keywords:
			x:
				desc:	The X coordinate of the dot center, or None to draw a
						horizontally centered dot.
				type:	[int, NoneType]
			y:
				desc:	The Y coordinate of the dot center, or None to draw a
						vertically centered dot.
				type:	[int, NoneType]
			color:
				desc:	"%arg_fgcolor"
				type:	[str, unicode, NoneType]
			style:
				desc: |
						The fixation-dot style. One of: default, large-filled,
						medium-filled, small-filled, large-open, medium-open,
						small-open, large-cross, medium-cross, or small-cross.
						default equals medium-open.
				type:	[str, unicode]

		example: |
			from openexp.canvas import canvas
			my_canvas = canvas(exp)
			my_canvas.fixdot()
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

	def circle(self, x, y, r, fill=False, color=None, penwidth=None):

		"""
		desc:
			Draws a circle.

		arguments:
			x:
				desc:	The center X coordinate of the circle.
				type:	int
			y:
				desc:	The center Y coordinate of the circle.
				type:	int
			r:
				desc:	The radius of the circle.
				type:	int

		keywords:
			fill:
				desc:	"%arg_fill"
				type:	bool
			color:
				desc:	"%arg_fgcolor"
				type:	[str, unicode, NoneType]
			penwidth:
				desc:	"%arg_penwidth"
				type:	int

		example: |
			from openexp.canvas import canvas
			my_canvas = canvas(exp)
			my_canvas.circle(100, 100, 50, fill=True, color='red')
		"""

		self.ellipse(x-r, y-r, 2*r, 2*r, fill=fill, color=color,
			penwidth=penwidth)

	def line(self, sx, sy, ex, ey, color=None, penwidth=None):

		"""
		desc:
			Draws a line.

		arguments:
			sx:
				desc:	The left X coordinate.
				type:	int
			sy:
				desc:	The top Y coordinate.
				type:	int
			ex:
				desc:	The right X coordinate.
				type:	int
			ey:
				desc:	The bottom Y coordinate.
				type:	int

		keywords:
			color:
				desc:	"%arg_fgcolor"
				type:	[str, unicode, NoneType]
			penwidth:
				desc:	"%arg_penwidth"
				type:	int

		Example: |
			from openexp.canvas import canvas
			my_canvas = canvas(exp)
			w = self.get('width')
			h = self.get('height')
			my_canvas.line(0, 0, w, h)
		"""

		raise NotImplementedError()

	def arrow(self, sx, sy, ex, ey, arrow_size=5, color=None, penwidth=None):

		"""
		desc:
			Draws an arrow. An arrow is a line, with an arrowhead at (ex, ey).
			The angle between the arrowhead lines and the arrow line is 45
			degrees.

		arguments:
			sx:
				desc:	The left X coordinate.
				type:	int
			sy:
				desc:	The top Y coordinate.
				type:	int
			ex:
				desc:	The right X coordinate.
				type:	int
			ey:
				desc:	The bottom Y coordinate.
				type:	int

		keywords:
			arrow_size:
				desc:	The length of the arrow-head lines in pixels.
				type:	int
			color:
				desc:	"%arg_fgcolor"
				type:	[str, unicode, NoneType]
			penwidth:
				desc:	"%arg_penwidth"
				type:	int

		Example: |
			from openexp.canvas import canvas
			my_canvas = canvas(exp)
			w = self.get('width')/2
			h = self.get('height')/2
			my_canvas.arrow(0, 0, w, h, arrow_size=10)
		"""

		self.line(sx, sy, ex, ey, color=color, penwidth=penwidth)
		a = math.atan2(ey - sy, ex - sx)
		_sx = ex + arrow_size * math.cos(a + math.radians(135))
		_sy = ey + arrow_size * math.sin(a + math.radians(135))
		self.line(_sx, _sy, ex, ey, color=color, penwidth=penwidth)
		_sx = ex + arrow_size * math.cos(a + math.radians(225))
		_sy = ey + arrow_size * math.sin(a + math.radians(225))
		self.line(_sx, _sy, ex, ey, color=color, penwidth=penwidth)

	def rect(self, x, y, w, h, fill=False, color=None, penwidth=None):

		"""
		desc:
			Draws a rectangle.

		arguments:
			x:
				desc:	The left X coordinate.
				type:	int
			y:
				desc:	The top Y coordinate.
				type:	int
			w:
				desc:	The width.
				type:	int
			h:
				desc:	The height.
				type:	int

		keywords:
			fill:
				desc:	"%arg_fill"
				type:	bool
			color:
				desc:	"%arg_fgcolor"
				type:	[str, unicode, NoneType]
			penwidth:
				desc:	"%arg_penwidth"
				type:	int

		example: |
			from openexp.canvas import canvas
			my_canvas = canvas(exp)
			w = self.get('width')-10
			h = self.get('height')-10
			my_canvas.rect(10, 10, w, h, fill=True)
		"""

		raise NotImplementedError()

	def ellipse(self, x, y, w, h, fill=False, color=None, penwidth=None):

		"""
		desc:
			Draws an ellipse.

		arguments:
			x:
				desc:	The left X coordinate.
				type:	int
			y:
				desc:	The top Y coordinate.
				type:	int
			w:
				desc:	The width.
				type:	int
			h:
				desc:	The height.
				type:	int

		keywords:
			fill:
				desc:	"%arg_fill"
				type:	bool
			color:
				desc:	"%arg_fgcolor"
				type:	[str, unicode, NoneType]
			penwidth:
				desc:	"%arg_penwidth"
				type:	int

		example: |
			from openexp.canvas import canvas
			my_canvas = canvas(exp)
			w = self.get('width')-10
			h = self.get('height')-10
			my_canvas.ellipse(10, 10, w, h, fill=True)
		"""

		raise NotImplementedError()

	def polygon(self, vertices, fill=False, color=None, penwidth=None):

		"""
		desc:
			Draws a polygon that defined by a list of vertices. I.e. a shape of
			points connected by lines.

		arguments:
			vertices:
				desc:	A list of tuples, where each tuple corresponds to a
						vertex. For example, [(100,100), (200,100), (100,200)]
						will draw a triangle.
				type:	list

		keywords:
			fill:
				desc:	"%arg_fill"
				type:	bool
			color:
				desc:	"%arg_fgcolor"
				type:	[str, unicode, NoneType]
			penwidth:
				desc:	"%arg_penwidth"
				type:	int

		example: |
			from openexp.canvas import canvas
			my_canvas = canvas(exp)
			n1 = 0,0
			n2 = 100, 100
			n3 = 0, 100
			my_canvas.polygon([n1, n2, n3])
		"""

		raise NotImplementedError()

	def text_size(self, text, max_width=None, bidi=None, html=True):

		"""
		desc:
			Determines the size of a text string in pixels.

		arguments:
			text:
				desc:	A string of text.
				type:	[str, unicode]

		keywords:
			max_width:
				desc:	"%arg_max_width"
				type:	[int, NoneType]
			bidi:
				desc:	"%arg_bidi"
				type:	[bool, NoneType]
			html:
				desc:	"%arg_html"
				type:	bool

		returns:
			desc:	A (width, height) tuple containing the dimensions of the
					text string.
			type:	tuple

		example: |
			from openexp.canvas import canvas
			my_canvas = canvas(exp)
			w, h = my_canvas.text_size('Some text')
		"""

		self.html.reset()
		width, height = self.html.render(text, 0, 0, self, max_width=max_width,
			html=html, bidi=bidi, dry_run=True)
		return width, height

	def text(self, text, center=True, x=None, y=None, max_width=None,
		color=None, bidi=None, html=True):

		"""
		desc:
			Draws text.

		arguments:
			text:
				desc:	A string of text.
				type:	[str, unicode]

		keywords:
			center:
				desc:	A bool indicating whether the coordinates reflect the
						center (True) or top-left (False) of the text.
				type:	bool
			x:
				desc:	The X coordinate, or None to draw horizontally centered
						text.
				type:	[int, NoneType]
			y:
				desc:	The Y coordinate, or None to draw vertically centered
						text.
				type:	[int, NoneType]
			max_width:
				desc:	"%arg_max_width"
				type:	[int, NoneType]
			color:
				desc:	"%arg_fgcolor"
				type:	[str, unicode, NoneType]
			bidi:
				desc:	"%arg_bidi"
				type:	[bool, NoneType]
			html:
				desc:	"%arg_html"
				type:	bool

		example: |
			from openexp.canvas import canvas
			my_canvas = canvas(exp)
			my_canvas.text('Some text with <b>boldface</b> and <i>italics</i>')
		"""

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
		desc:
			A simple function that renders a string of text with the canvas
			default settings. This function needs to be re-implemented in
			each back-ends, as it handles actual text rendering.

		visible:		False

		arguments:
			text:
				desc:	A string of text.
				type:	[str, unicode]
			x:
				desc:	The X coordinate.
				type:	int
			y:
				desc:	The Y coordinate.
				type:	int
		"""

		raise NotImplementedError()

	def _text_size(self, text):

		"""
		desc:
			Determines the size of a string of text for the default font. This
			function is for internal use, and should be re-implemented for each
			back-end.

		visible:		False

		arguments:
			text:
				desc:	A string of text.
				type:	[str, unicode]

		returns:
			desc:		A (width, height) tuple.
			type:		tuple
		"""

		raise NotImplementedError()

	def textline(self, text, line, color=None):

		"""
		desc: |
			A convenience function that draws a line of text based on a line
			number. The text strings are centered on the X-axis and vertically
			spaced with 1.5 times the line height as determined by text_size().

			__Note:__

			This function has been deprecated.

		visible:		False

		arguments:
			text:
				desc:	A string of text.
				type:	[str, unicode]
			line:
				desc:	A line number, where 0 is the center and > 0 is below
						the center.
				type:	int

		keywords:
			color:
				desc:	"%arg_fgcolor"
				type:	[str, unicode, NoneType]
		"""

		size = self.text_size(text)
		self.text(text, True, self.xcenter(), self.ycenter()+1.5*line*size[1],
			color=color)

	def image(self, fname, center=True, x=None, y=None, scale=None):

		"""
		desc:
			Draws an image from file. This function does not look in the file
			pool, but takes an absolute path.

		arguments:
			fname:
				desc:	The filename of the image. If this is a `str` it is
						assumed to be in utf-8 encoding.
				type:	[str, unicode]

		keywords:
			center:
				desc:	A bool indicating whether coordinates indicate the
						center (True) or top-left (False).
				type:	bool
			x:
				desc:	The X coordinate, or `None` to draw a horizontally
						centered image.
				type:	[int, NoneType]
			y:
				desc:	The Y coordinate, or `None` to draw a vertically
						centered image.
				type:	[int, NoneType]
			scale:
				desc:	The scaling factor of the image. `None` or 1 indicate
						the original size. 2.0 indicates a 200% zoom, etc.
				type:	[float, int, NoneType]

		example: |
			from openexp.canvas import canvas
			my_canvas = canvas(exp)
			# Determine the absolute path:
			path = exp.get_file(u'image_in_pool.png')
			my_canvas.image(path)
		"""

		raise NotImplementedError()

	def gabor(self, x, y, orient, freq, env=u'gaussian', size=96, stdev=12,
		phase=0, col1=u'white', col2=u'black', bgmode=u'avg'):

		"""
		desc: |
			Draws a Gabor patch. Note: The exact rendering of the Gabor patch
			depends on the back-end.

		arguments:
			x:
				desc:	The center X coordinate.
				type:	int
			y:
				desc:	The center Y coordinate.
				type:	int
			orient:
				desc:	Orientation in degrees [0 .. 360].
				type:	[float, int]
			freq:
				desc:	Frequency in cycles/px of the sinusoid.
				type:	[float, int]

		keywords:
			env:
				desc:	The envelope that determines the shape of the patch. Can
						be "gaussian", "linear", "circular", or "rectangular".
				type:	[str, unicode]
			size:
				desc:	A size in pixels.
				type:	[float, int]
			stdev:
				desc:	Standard deviation in pixels of the gaussian. Only
						applicable to gaussian envelopes.
				type:	[float, int]
			phase:
				desc:	Phase of the sinusoid [0.0 .. 1.0].
				type:	[float, int]
			col1:
				desc:	A color for the peaks.
				type:	[str, unicode]
			col2:
				desc: |
						A color for the troughs. Note: The psycho back-end
						ignores this parameter and always uses the inverse of
						`col1` for the throughs.
				type:	[str, unicode]
			bgmode:
				desc:	"%arg_bgmode"
				type:	[str, unicode]

		example: |
			from openexp.canvas import canvas
			my_canvas = canvas(exp)
			my_canvas.gabor(100, 100, 45, .05)
		"""

		raise NotImplementedError()

	def noise_patch(self, x, y, env=u'gaussian', size=96, stdev=12,
		col1=u'white', col2=u'black', bgmode=u'avg'):

		"""
		desc:
			Draws a patch of noise, with an envelope. The exact rendering of the
			noise patch depends on the back-end.

		arguments:
			x:
				desc:	The center X coordinate.
				type:	int
			y:
				desc:	The center Y coordinate.
				type:	int

		keywords:
			env:
				desc:	The envelope that determines the shape of the patch. Can
						be "gaussian", "linear", "circular", or "rectangular".
				type:	[str, unicode]
			size:
				desc:	A size in pixels.
				type:	[float, int]
			stdev:
				desc:	Standard deviation in pixels of the gaussian. Only
						applicable to gaussian envelopes.
				type:	[float, int]
			col1:
				desc:	The first color.
				type:	[str, unicode]
			col2:
				desc: |
						The second color. Note: The psycho back-end ignores this
						parameter and always uses the inverse of `col1`.
				type:	[str, unicode]
			bgmode:
				desc: 	"%arg_bgmode"
				type:	[str, unicode]

		example: |
			from openexp.canvas import canvas
			my_canvas = canvas(exp)
			my_canvas.noise_patch(100, 100, env='circular')
		"""

		raise NotImplementedError()

def init_display(experiment):

	"""
	desc:
		Initializes the display before the experiment begins.

	arguments:
		experiment:
			desc:	An experiment object.
			type:	experiment
	"""

	raise NotImplementedError()

def close_display(experiment):

	"""
	desc:
		Closes the display after the experiment is finished.

	arguments:
		experiment:
			desc:	An experiment object.
			type:	experiment
	"""

	raise NotImplementedError()

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

canvas_cache = {}

def _gabor(orient, freq, env=u"gaussian", size=96, stdev=12, phase=0,
	col1=u"white", col2=u"black", bgmode=u"avg"):

	"""
	desc:
		Returns a pygame surface containing a Gabor patch. For arguments,
		see [canvas.gabor].
	"""

	env = _match_env(env)
	# Generating a Gabor patch takes quite some time, so keep
	# a cache of previously generated Gabor patches to speed up
	# the process.
	global canvas_cache
	key = u"gabor_%s_%s_%s_%s_%s_%s_%s_%s_%s" % (orient, freq, env, size,
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
			px[rx][ry] = round(r), round(g), round(b)
	canvas_cache[key] = surface
	del px
	return surface

def _noise_patch(env=u"gaussian", size=96, stdev=12, col1=u"white",
	col2=u"black", bgmode=u"avg"):

	"""
	desc:
		Returns a pygame surface containing a noise patch. For arguments,
		see [canvas.noise_patch].
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
			px[rx][ry] = round(r), round(g), round(b)
	canvas_cache[key] = surface
	del px
	return surface

def _match_env(env):

	"""
	desc:
		Translation between various envelope names.

	arguments:
		env:
			desc:	An envelope name.
			type:	[str, unicode]

	returns:
		desc: A standard envelope name ("c", "g", "r" or "l")
		type: unicode
	"""

	global env_synonyms
	if env not in env_synonyms:
		raise osexception(u"'%s' is not a valid envelope" % env)
	return env_synonyms[env]

def _color(color):

	"""
	desc:
		Creates a PyGame color object.

	returns:
		A pygame color object.
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

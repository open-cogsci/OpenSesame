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
import warnings
import random
import pygame
import math
from libopensesame.exceptions import osexception
from libopensesame.html import html
from openexp.backend import backend, configurable
from openexp.color import color

class canvas(backend):

	"""
	desc: |
		The `canvas` class is used to present visual stimuli.

		__Example__:

		~~~ .python
		# Create and show a canvas with a central fixation dot
		my_canvas = canvas()
		my_canvas.fixdot()
		my_canvas.show()
		~~~
		
		If drawing on a `canvas` is slow, especially if you draw many stimuli,
		you should disable `auto_prepare` and explicitly call `canvas.prepare()`
		after all drawing operations are done, but before calling
		`canvas.show()`.
		
		__Example__:

		~~~ .python
		import random
		import string

		# Create and show a canvas with a grid of random letters
		my_canvas = canvas(auto_prepare=False)
		for x, y in xy_grid(n=10, spacing=20):
			letter = random.choice(string.ascii_uppercase)
			my_canvas.text(text=letter, x=x, y=y)
		my_canvas.prepare()
		my_canvas.show()
		~~~		

		[TOC]

		## Things to know

		### Coordinates

		- When *Uniform coordinates* is set to 'yes', coordinates are
		  relative to the center of the display. That is, (0,0) is the center.
		  This is the default as of OpenSesame 3.0.0.
		- When *Uniform coordinates* is set to 'no', coordinates are relative to
		  the top-left of the display. That is, (0,0) is the top-left. This was
		  the default in OpenSesame 2.9.X and earlier.

		### Style keywords

		All functions that accept `**style_args` take the following keyword
		arguments:

		- `color` specifies the foreground color. For valid color
		  specifications, see [colors].
		- `background_color` specifies the background color. For valid color
		  specifications, see [colors].
		- `fill` indicates whether rectangles, circles, polygons, and ellipses
		  are filled (`True`), or drawn as an outline (`False`).
		- `penwidth` indicates a penwidth in pixels and should be `int` or
		  `float`.
		- `bidi` indicates whether bidirectional-text support is enabled, and
		  should be `True` or `False`.
		- `html` indicates whether HTML-tags are interpreted, and should be
		  `True` or `False`. For supported tags, see [/usage/text/]().
		- `font_family` is the name of a font family, such as 'sans'.
		- `font_size` is a font size in pixels.
		- `font_italic` indicates whether text should italics, and should be
		  `True` or `False`.
		- `font_bold` indicates whether text should bold, and should be
		  `True` or `False`.
		- `font_underline` indicates whether text should underlined, and should
		  be `True` or `False`.

		~~~ .python
		# Draw a green fixation dot
		my_canvas = canvas()
		my_canvas.fixdot(color='green')
		my_canvas.show()
		~~~

		Style keywords only affect the current drawing operation (except when
		passed to [canvas.\_\_init\_\_][__init__]). To change the style for all
		subsequent drawing operations, set style properties, such as
		[canvas.color], directly:

		~~~ .python
		# Draw a red cross with a 2px penwidth
		my_canvas = canvas()
		my_canvas.color = u'red'
		my_canvas.penwidth = 2
		my_canvas.line(-10, -10, 10, 10)
		my_canvas.line(-10, 10, 10, -10)
		my_canvas.show()
		~~~

		Or pass the style properties to [canvas.\_\_init\_\_][__init__]:

		~~~ .python
		# Draw a red cross with a 2px penwidth
		my_canvas = canvas(color=u'red', penwidth=2)
		my_canvas.line(-10, -10, 10, 10)
		my_canvas.line(-10, 10, 10, -10)
		my_canvas.show()
		~~~

		### Colors

		You can specify colors in the following CSS3-compatible ways:

		- __Color names:__ 'red', 'black', etc. A full list of valid color names
		  can be found
		  [here](http://www.w3.org/TR/SVG11/types.html#ColorKeywords).
		- __Seven-character hexadecimal strings:__ '#FF0000', '#000000', etc.
		  Here, values range from '00' to 'FF', so that '#FF0000' is bright red.
		- __Four-character hexadecimal strings:__ '#F00', '#000', etc. Here,
		  values range from '0' to 'F' so that '#F00' is bright red.
		- __RGB strings:__ 'rgb(255,0,0)', 'rgb(0,0,0)', etc. Here, values
		  range from '0' to '255' so that 'rgb(255,0,0)' is bright red.
		- __RGB percentage strings:__ 'rgb(100%,0%,0%)', 'rgb(0%,0%,0%)', etc.
		  Here, values range from '0%' to '100%' so that 'rgb(100%,0%,0%)' is
		  bright red.
		- __RGB tuples:__ `(255, 0, 0)`, `(0, 0 ,0)`, etc. Here, values range
		  from `0` to `255` so that `(255,0,0)' is bright red.
		- __Luminance values:__  `255`, `0`, etc. Here, values range from `0` to
		  `255` so that `255` is white.

		~~~ .python
		# Various ways to specify green
		my_canvas.fixdot(color=u'green')
		my_canvas.fixdot(color=u'#00ff00')
		my_canvas.fixdot(color=u'#0f0')
		my_canvas.fixdot(color=u'rgb(0,255,0)')
		my_canvas.fixdot(color=u'rgb(0%,100%,0%)')
		my_canvas.fixdot(color=(0,255,0))
		# Specify a luminance value (white)
		my_canvas.fixdot(color=255)
		~~~

		%--
		constant:
			arg_max_width: |
				The maximum width of the text in pixels, before wrapping to a
				new line, or `None` to wrap at screen edge.
			arg_bgmode: |
				Specifies whether the background is the average of col1 col2
				('avg', corresponding to a typical Gabor patch), or equal to
				col2 ('col2'), useful for blending into the	background. Note:
				this parameter is ignored by the psycho backend, which uses
				increasing transparency for the background.
			arg_style: |
				Optional [style keywords] that specify the style of the current
				drawing operation. This does not affect subsequent drawing
				operations.
		--%
	"""

	def __init__(self, experiment, auto_prepare=True, **style_args):

		"""
		desc: |
			Constructor to create a new `canvas` object. You do not generally
			call this constructor directly, but use the `canvas()` function,
			which is described here: [/python/common/]().

		arguments:
			experiment:
				desc:	The experiment object.
				type:	experiment

		keywords:
			auto_prepare:
				desc:	Indicates whether the canvas should be automatically
						prepared after each drawing operation, so that
						[canvas.show] will be maximally efficient. If
						auto_prepare is turned off, drawing operations may
						be faster, but [canvas.show] will take longer,
						unless [canvas.prepare] is explicitly called in
						advance. Generally, it only makes sense to disable
						auto_prepare when you want to draw a large number
						of stimuli, as in the second example above.
						Currently, the auto_prepare parameter only applies
						to the xpyriment backend, and is ignored by the
						other backends.
				type:	bool

		keyword-dict:
			style_args:
				Optional [style keywords], which will be used as the default
				for all drawing operations on this `canvas`.

		example: |
			# Example 1: Show a central fixation dot.
			my_canvas = canvas()
			my_canvas.fixdot()
			my_canvas.show()

			# Example 2: Show many randomly positioned fixation dot. Here we
			# disable `auto_prepare`, so that drawing goes more quickly.
			from random import randint
			my_canvas = canvas(auto_prepare=False)
			for i in range(1000):
				x = randint(0, my_canvas.width)
				y = randint(0, my_canvas.height)
				my_canvas.fixdot(x, y)
			my_canvas.prepare()
			my_canvas.show()
		"""

		self.experiment = experiment
		self._width = self.experiment.var.width
		self._height = self.experiment.var.height
		self.auto_prepare = auto_prepare
		backend.__init__(self, configurables={
			u'color' : None,
			u'background_color' : None,
			u'fill' : self.assert_bool,
			u'penwidth' : self.assert_numeric,
			u'bidi' : self.assert_bool,
			u'html' : self.assert_bool,
			u'font_family' : self.assert_string,
			u'font_size' : self.assert_numeric,
			u'font_italic' : self.assert_bool,
			u'font_bold' : self.assert_bool,
			u'font_underline' : self.assert_bool,
			}, **style_args)
		self.html_renderer = html()

	def set_config(self, **cfg):

		# Remap deprecated names
		if u'bgcolor' in cfg:
			warnings.warn(u'bgcolor is a deprecated style argument. '
				'Use background_color instead.',
				DeprecationWarning)
			cfg[u'background_color'] = cfg[u'bgcolor']
			del cfg['bgcolor']
		if u'fgcolor' in cfg:
			warnings.warn(u'fgcolor is a deprecated style argument. '
				'Use color instead.', DeprecationWarning)
			cfg[u'color'] = cfg[u'fgcolor']
			del cfg['fgcolor']
		if u'font_style' in cfg:
			warnings.warn(u'font_style is a deprecated style argument. '
				'Use font_family instead.',	DeprecationWarning)
			cfg[u'font_family'] = cfg[u'font_style']
			del cfg['font_style']
		# Convert color to backend specific colors
		if u'color' in cfg and not hasattr(cfg[u'color'], u'backend_color'):
			cfg[u'color'] = color(self.experiment, cfg[u'color'])
		if u'background_color' in cfg \
			and not hasattr(cfg[u'background_color'], u'backend_color'):
			cfg[u'background_color'] = color(self.experiment,
				cfg[u'background_color'])
		backend.set_config(self, **cfg)

	def default_config(self):

		return {
			u'penwidth' 		: 1,
			u'fill'				: False,
			u'html'				: True,
			u'bidi'				: self.experiment.var.bidi==u'yes',
			u'color'			: self.experiment.var.foreground,
			u'background_color'	: self.experiment.var.background,
			u'font_size'		: self.experiment.var.font_size,
			u'font_family'		: self.experiment.var.font_family,
			u'font_bold'		: self.experiment.var.font_bold==u'yes',
			u'font_italic'		: self.experiment.var.font_italic==u'yes',
			u'font_underline'	: self.experiment.var.font_underline==u'yes',
			}

	@property
	def size(self):

		"""
		name:
			size

		desc:
			The size of the canvas as a `(width, height)` tuple. This is a
			read-only property.
		"""

		return self._width, self._height

	@property
	def width(self):

		"""
		name:
			width

		desc:
			The width of the canvas. This is a read-only property.
		"""

		return self._width

	@property
	def height(self):

		"""
		name:
			height

		desc:
			The height of the canvas. This is a read-only property.
		"""

		return self._height

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
			my_canvas = canvas()
			my_canvas.fixdot(x=100, color='green')
			my_copied_canvas = canvas()
			my_copied_canvas.copy(my_canvas)
			my_copied_canvas.fixdot(x=200, color="blue")
			my_copied_canvas.show()
		"""

		raise NotImplementedError()

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
			my_canvas = canvas()
			my_canvas.fixdot()
			t = my_canvas.show()
			exp.set('time_fixdot', t)
		"""

		raise NotImplementedError()

	@configurable
	def clear(self, **style_args):

		"""
		desc:
			Clears the canvas with the current background color. Note that it is
			generally faster to use a different canvas for each experimental
			display than to use a single canvas and repeatedly clear and redraw
			it.

		keyword-dict:
			style_args:	"%arg_style"

		example: |
			my_canvas = canvas()
			my_canvas.fixdot(color='green')
			my_canvas.show()
			sleep(1000)
			my_canvas.clear()
			my_canvas.fixdot(color='red')
			my_canvas.show()
		"""

		raise NotImplementedError()

	@configurable
	def fixdot(self, x=None, y=None, style=u'default', **style_args):

		"""
		desc: |
			Draws a fixation dot. The default style is medium-open.

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
			style:
				desc: |
						The fixation-dot style. One of: default, large-filled,
						medium-filled, small-filled, large-open, medium-open,
						small-open, large-cross, medium-cross, or small-cross.
						default equals medium-open.
				type:	[str, unicode]

		keyword-dict:
			style_args:	"%arg_style"

		example: |
			my_canvas = canvas()
			my_canvas.fixdot()
		"""

		if x is None:
			if self.uniform_coordinates:
				x = 0
			else:
				x = self._width/2
		if y is None:
			if self.uniform_coordinates:
				y = 0
			else:
				y = self._height/2
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
			self.ellipse(x-s, y-s, 2*s, 2*s, fill=True)
			self.ellipse(x-h, y-h, 2*h, 2*h, fill=True,
				color=self.background_color)
		elif u'filled' in style:
			self.ellipse(x-s, y-s, 2*s, 2*s, fill=True)
		elif u'cross' in style:
			self.line(x, y-s, x, y+s)
			self.line(x-s, y, x+s, y)
		else:
			raise osexception(u'Unknown style: %s' % self.style)

	@configurable
	def circle(self, x, y, r, **style_args):

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

		keyword-dict:
			style_args:	"%arg_style"

		example: |
			my_canvas = canvas()
			my_canvas.circle(100, 100, 50, fill=True, color='red')
		"""

		self.ellipse(x-r, y-r, 2*r, 2*r)

	@configurable
	def line(self, sx, sy, ex, ey, **style_args):

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

		keyword-dict:
			style_args:	"%arg_style"

		Example: |
			my_canvas = canvas()
			w = self.var.width
			h = self.var.height
			my_canvas.line(0, 0, w, h)
		"""

		raise NotImplementedError()

	@configurable
	def arrow(self, sx, sy, ex, ey, body_length=0.8, body_width=.5,
		head_width=30, **style_args):

		"""
		desc:
			Draws an arrow. An arrow is a polygon consisting of 7 vertices,
			with an arrowhead pointing at (ex, ey).

		arguments:
			sx:
				desc:	The X coordinate of the arrow's base.
				type:	int
			sy:
				desc:	The Y coordinate of the arrow's base.
				type:	int
			ex:
				desc:	The X coordinate of the arrow's tip.
				type:	int
			ey:
				desc:	The Y coordinate of the arrow's tip..
				type:	int

		keywords:
			body_length:
				desc:	Proportional length of the arrow body relative to
						the full arrow [0-1].
				type:	float
			body_width:
				desc:	Proportional width (thickness) of the arrow body
						relative to the full arrow [0-1].
				type:	float
			head_width:
				desc:	Width (thickness) of the arrow head in pixels.
				type:	float

		Example: |
			my_canvas = canvas()
			w = var.width/2
			h = var.height/2
			my_canvas.arrow(0, 0, w, h, head_width=100, body_length=0.5)
			my_canvas.show()
		"""

		self.polygon(self.arrow_shape(sx, sy, ex, ey, body_width=body_width,
			body_length=body_length, head_width=head_width))

	@configurable
	def rect(self, x, y, w, h, **style_args):

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

		keyword-dict:
			style_args:	"%arg_style"

		example: |
			my_canvas = canvas()
			my_canvas.rect(-10, -10, 20, 20, fill=True)
		"""

		raise NotImplementedError()

	@configurable
	def ellipse(self, x, y, w, h, **style_args):

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

		keyword-dict:
			style_args:	"%arg_style"

		example: |
			my_canvas = canvas()
			my_canvas.ellipse(-10, -10, 20, 20, fill=True)
		"""

		raise NotImplementedError()

	@configurable
	def polygon(self, vertices, **style_args):

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

		keyword-dict:
			style_args:	"%arg_style"

		example: |
			my_canvas = canvas()
			n1 = 0,0
			n2 = 100, 100
			n3 = 0, 100
			my_canvas.polygon([n1, n2, n3])
		"""

		raise NotImplementedError()

	@configurable
	def text_size(self, text, max_width=None, **style_args):

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

		keyword-dict:
			style_args:	"%arg_style"

		returns:
			desc:	A (width, height) tuple containing the dimensions of the
					text string.
			type:	tuple

		example: |
			my_canvas = canvas()
			w, h = my_canvas.text_size('Some text')
		"""

		self.html_renderer.reset()
		width, height = self.html_renderer.render(text, 0, 0, self,
			max_width=max_width, dry_run=True)
		return width, height

	@configurable
	def text(self, text, center=True, x=None, y=None, max_width=None,
		**style_args):

		"""
		desc:
			Draws text.

		arguments:
			text:
				desc:	A string of text. When using Python 2, this should be
						either `unicode` or a utf-8-encoded `str`. When using
						Python 3, this should be either `str` or a utf-8-encoded
						`bytes`.
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

		keyword-dict:
			style_args:	"%arg_style"

		example: |
			my_canvas = canvas()
			my_canvas.text('Some text with <b>boldface</b> and <i>italics</i>')
		"""

		x, y = self.none_to_center(x, y)
		self.html_renderer.reset()
		self.html_renderer.render(text, x, y, self, max_width=max_width,
			center=center)

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

	def image(self, fname, center=True, x=None, y=None, scale=None):

		"""
		desc:
			Draws an image from file. This function does not look in the file
			pool, but takes an absolute path.

		arguments:
			fname:
				desc:	The filename of the image. When using Python 2, this
						should be either `unicode` or a utf-8-encoded `str`.
						When using Python 3, this should be either `str` or a
						utf-8-encoded `bytes`.
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
			my_canvas = canvas()
			# Determine the absolute path:
			path = exp.pool[u'image_in_pool.png']
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
			my_canvas = canvas()
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
			my_canvas = canvas()
			my_canvas.noise_patch(100, 100, env='circular')
		"""

		raise NotImplementedError()

	# Deprecated functions

	def xcenter(self):

		"""
		visible:	False
		desc:		deprecated
		"""

		return self.experiment.var.get(u'width') / 2

	def ycenter(self):

		"""
		visible:	False
		desc:		deprecated
		"""

		return self.experiment.var.get(u'height') / 2

	def set_bidi(self, bidi):

		"""
		visible:	False
		desc:		deprecated
		"""

		self.bidi = bidi

	def set_penwidth(self, penwidth):

		"""
		visible:	False
		desc:		deprecated
		"""

		self.penwidth = penwidth

	def set_fgcolor(self, color):

		"""
		visible:	False
		desc:		deprecated
		"""

		self.color = color

	def set_bgcolor(self, color):

		"""
		visible:	False
		desc:		deprecated
		"""

		self.bgcolor = self.color

	def set_font(self, style=None, size=None, italic=None, bold=None,
		underline=None):

		"""
		visible:	False
		desc:		deprecated
		"""

		if style is not None: self.font_family = style
		if size is not None: self.font_size = size
		if italic is not None: self.font_italic = italic
		if bold is not None: self.font_bold = bold
		if underline is not None: self.font_underline = underline

	@staticmethod
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

	@staticmethod
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

	@staticmethod
	def arrow_shape(sx, sy, ex, ey, body_length=0.8, body_width=.5,
		head_width=30):

		"""
		visible: False

		returns:
			Returns a list of (x, y) tuples that specify an arrow shape. See
			canvas.canvas() for keywords.
		"""

		# length
		d = math.sqrt((ey-sy)**2 + (sx-ex)**2)
		# direction
		angle = math.atan2(ey-sy,ex-sx)
		_head_width = (1-body_width)/2.0
		body_width = body_width/2.0
		# calculate coordinates
		p4 = (ex,ey)
		p1 = (sx +body_width * head_width * math.cos(angle - math.pi/2),\
			sy + body_width * head_width * math.sin(angle - math.pi/2))
		p2 = (p1[0] + body_length*math.cos(angle) * d, \
		 	p1[1] + body_length * math.sin(angle) * d)
		p3 = (p2[0]+_head_width * head_width * math.cos(angle-math.pi/2),\
			p2[1] + _head_width * head_width * math.sin(angle-math.pi/2))
		p7 = (sx + body_width * head_width*math.cos(angle + math.pi/2),\
			sy + body_width * head_width*math.sin(angle + math.pi/2))
		p6 = (p7[0] + body_length * math.cos(angle) * d, \
		 	p7[1] + body_length * math.sin(angle) * d)
		p5 = (p6[0]+_head_width * head_width * math.cos(angle+math.pi/2),\
			p6[1]+_head_width * head_width * math.sin(angle+math.pi/2))
		return [p1, p2, p3, p4, p5, p6, p7]

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

def _color(col):

	"""
	desc:
		Wrapper function for _gabor and _noise_patch to convert color names to
		PyGame color objects.

	argumens:
		col:	A color specification.

	returns:
		A PyGame color object.
	"""

	from openexp._color.legacy import legacy
	return legacy(None, col).backend_color

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
	try:
		px = pygame.PixelArray(surface)
	except:
		px = None
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
			if px is None:
				surface.set_at((rx, ry), (round(r), round(g), round(b)))
			else:
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
	try:
		px = pygame.PixelArray(surface)
	except:
		px = None
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
			if px is None:
				surface.set_at((rx, ry), (round(r), round(g), round(b)))
			else:
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

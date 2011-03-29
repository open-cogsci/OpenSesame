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

import openexp.canvas

class template(openexp.canvas.canvas):

	"""
	This class serves as a template for creating OpenSesame video back-ends. Let's say
	you want to create a dummy backend. First, create dummy.py in the openexp.video
	folder. In dummy.py, create a dummy class, which is derived from openexp.canvas.canvas
	and which implements all the functions specified below.
		
	A few guidelines:
	-- Catch exceptions wherever possible and raise an openexp.exceptions.canvas_error
	   with a clear and descriptive error message.
	-- If you create a temporary file, add its path to the openexp.canvas.temp_files list.
	-- Do not deviate from the guidelines. All back-ends should be interchangeable and 
	   transparent to OpenSesame. You are free to add functionality to this class, to be 
	   used in inline scripts, but this should not break the basic functionality.
	-- Print debugging output only if experiment.debug == True and preferrably in the
	   following format: "template.__init__(): Debug message here".
	"""
	
	def __init__(self, experiment, bgcolor = "black", fgcolor = "white"):
		
		"""
		Initializes the canvas. The specified colors should be used as a 
		default for subsequent drawing operations.
		
		Arguments:
		experiment -- an instance of libopensesame.experiment.experiment
		
		Keyword arguments:
		bgcolor -- a human-readable background color (default = "black")
		fgcolor -- a human-readable foreground color (default = "white")
		"""		
		
		pass
		
	def color(self, color):
	
		"""
		Transforms a "human readable" color into the format that
		is used by the back-end (e.g., a PyGame color).
		
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
	
		pass				
		
	def flip(self, x = True, y = False):
		
		"""
		Flips the canvas along the x- and/ or y-axis. Note: This does not refresh the display,
		like e.g., pygame.display.flip(), which is handled by show().
		
		Keyword arguments:
		x -- A boolean indicating whether the canvas should be flipped horizontally (default = True)
		y -- A boolean indicating whether the canvas should be flipped vertically (default = False)
		"""
		
		pass		
		
	def copy(self, canvas):
	
		"""
		Turn the current canvas into a copy of the passed canvas.
		
		Arguments:
		canvas -- The canvas to copy.
		"""
		
		pass
		
	def xcenter(self):
		
		"""
		Returns:
		The center X coordinate in pixels.
		"""
		
		pass
	
	def ycenter(self):
		
		"""
		Returns:
		The center Y coordinate in pixels.
		"""
		
		pass		
		
	def show(self):
		
		"""
		Puts the canvas onto the screen.
		"""

		pass
		
	def clear(self):
		
		"""
		Clears the canvas with the current background color.
		"""
		
		pass
		
	def set_penwidth(self, penwidth):
		
		"""
		Sets the pen width for subsequent drawing operations.
		
		Arguments:
		penwidth -- A pen width in pixels
		"""
		
		pass
		
	def set_fgcolor(self, color):
		
		"""
		Sets the foreground color for subsequent drawing operations.
		
		Arguments:
		color -- A human readable color
		"""
		
		pass
		
	def set_bgcolor(self, color):
		
		"""
		Sets the background color for subsequent drawing operations.
		
		Arguments:
		color -- A human readable color
		"""
		
		pass
		
	def set_font(self, style, size):
	
		"""
		Sets the font for subsequent drawing operations.
		
		Arguments:
		style -- A font located in the resources folder (without the .ttf extension)
		size -- A font size in pixels		
		"""
		
		pass
		
	def fixdot(self, x = None, y = None):
		
		"""
		Draws a standard fixation dot, which is a big circle (r = 8px) with the
		foreground color and a smaller circle (r = 2px) of the background color.
		
		Keyword arguments:
		x -- The center X coordinate. None = center (default = None)
		y -- The center Y coordinate. None = center (default = None)
		"""
		pass		
		
	def circle(self, x, y, r, fill = False):
		
		"""
		Draws a circle.
		
		Arguments:
		x -- The center X coordinate
		y -- The center Y coordinate
		r -- The radius
		
		Keyword arguments:
		fill -- A boolean indicating whether the circle is outlined (False) or filled (True)
		"""
		
		pass

	def line(self, sx, sy, ex, ey):
		
		"""
		Draws a line. Should accept parameters where sx > ex or sy > ey as well.
		
		Arguments:
		sx -- The left coordinate
		sy -- The top coordinate
		ex -- The right coordinate
		ey -- The bottom coordinate
		"""
		
		pass
		
	def arrow(self, sx, sy, ex, ey, arrow_size = 5):
		
		"""
		Draws an arrow. An arrow is a line, with an arrowhead at (ex, ey). The angle between
		the arrowhead lines and the arrow line is 45 degrees.
		
		Arguments:
		sx -- The left coordinate
		sy -- The top coordinate
		ex -- The right coordinate
		ey -- The bottom coordinate
		
		Keyword arguments:
		arrow_size -- The length of the arrowhead lines (default = 5)
		"""
		
		pass
		
	def rect(self, x, y, w, h, fill = False):
		
		"""
		Draws a rectangle. Should accept parameters where w < 0 or h < 0 as well.
		
		Arguments:
		x -- The left X coordinate.
		y -- The top Y coordinate.
		w -- The width.
		h -- The height.
				
		Keyword arguments:
		fill -- A boolean indicating whether the rectangle is outlined (False) or filled (True)
		"""
		
		pass
			
	def ellipse(self, x, y, w, h, fill = False):
		
		"""
		Draws an ellipse. Should accept parameters where w < 0 or h < 0 as well.
		
		Arguments:
		x -- The left X coordinate.
		y -- The top Y coordinate.
		w -- The width.
		h -- The height.
				
		Keyword arguments:
		fill -- A boolean indicating whether the ellipse is outlined (False) or filled (True)
		"""
		
		pass	
			
	def text_size(self, text):
	
		"""
		Determines the size of a text string in pixels.
		
		Arguments:
		text -- The text string
		
		Returns:
		A (width, height) tuple containing the dimensions of the text string
		"""
		
		pass
		
	def text(self, text, center = True, x = None, y = None):
		
		"""
		Draws text.
		
		Arguments:
		text -- The text string
		
		Keyword arguments:
		center -- A boolean indicating whether the coordinates reflect the center (True)
				  or top-left (default = True)
		x -- The X coordinate. None = center. (default = None)
		y -- The Y coordinate. None = center. (default = None)
		"""
			
		pass
		
	def textline(self, text, line):
		
		"""
		A convenience function that draws a line of text based on a 
		line number. The text strings are centered on the X-axis and
		vertically spaced with 1.5 the line height as determined by
		text_size().
		
		Arguments:
		text -- The text string
		line -- A line number, where 0 is the center and > 0 is below the center.
		"""
		
		pass
		
	def image(self, fname, center = True, x = None, y = None, scale = None):
		
		"""
		Draws an image from file. This function does not look in the file
		pool, but takes an absolute path.
		
		Arguments:
		fname -- The path of the file
		
		Keyword arguments:
		center -- A boolean indicating whether the given coordinates reflect the
				  center (True) or the top-left (False) of the image. (default = True)
		x -- The X coordinate. None = center. (default = None)
		y -- The Y coordinate. None = center. (default = None)
		scale -- The scaling factor of the image. 1.0 or None = no scaling, 2.0 = twice as large, etc. (default = None)
		"""
		
		pass		
					
	def gabor(self, x, y, orient, freq, env = "gaussian", size = 96, stdev = 12, phase = 0, col1 = "white", col2 = "black", bgmode = "avg"):
	
		"""
		Draws a Gabor patch. This function is derived from the online Gabor patch generator
		<http://www.cogsci.nl/software/online-gabor-patch-generator>	
		
		Arguments:
		x -- The center X coordinate
		y -- The center Y coordinate
		orient -- Orientation in degrees [0 .. 360]
		freq -- Frequency in cycles/px of the sinusoid
		
		Keyword arguments:	
		env -- Any of the following: "gaussian", "linear", "circular", "rectangle" (default = "gaussian")
		size -- Size in pixels (default = 96)
		stdev -- Standard deviation in pixels of the gaussian. Only applicable if env = "gaussian". (default = 12)
		phase -- Phase of the sinusoid [0.0 .. 1.0] (default = 0)
		col1: -- Human readable color for the tops (default = "white")
		col2 -- Human readable color for the troughs (default = "black")
		bgmode -- Specifies whether the background is the average of col1 and col2 (bgmode = "avg", a typical Gabor patch)
				  or equal to col2 ("col2"), useful for blending into the background. (default = "avg")
		"""	
		
		pass
		
	def noise_patch(self, x, y, env = "gaussian", size = 96, stdev = 12, col1 = "white", col2 = "black", bgmode = "avg"):
	
		"""
		Draws a patch of noise, with an envelope.
		
		Arguments:
		x -- The center X coordinate
		y -- The center Y coordinate
		
		Keyword arguments:	
		env -- Any of the following: "gaussian", "linear", "circular", "rectangle" (default = "gaussian")
		size -- Size in pixels (default = 96)
		stdev -- Standard deviation in pixels of the gaussian. Only applicable if env = "gaussian". (default = 12)
		phase -- Phase of the sinusoid [0.0 .. 1.0] (default = 0)
		col1: -- Human readable color for the tops (default = "white")
		col2 -- Human readable color for the troughs (default = "black")
		bgmode -- Specifies whether the background is the average of col1 and col2 (bgmode = "avg", a typical Gabor patch)
				  or equal to col2 ("col2"), useful for blending into the background. (default = "avg")
		"""	
		
		pass
		
def init_display(experiment):

	"""
	Initialize the display before the experiment begins.
	
	Arguments:
	experiment -- An instance of libopensesame.experiment.experiment	
	"""

	pass
	
def close_display(experiment):

	"""
	Close the display after the experiment is finished.
	
	Arguments:
	experiment -- An instance of libopensesame.experiment.experiment	
	"""

	pass

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

from libopensesame.widgets._image import image

class image_button(image):

	"""
	desc: |
		The image_button widget is a clickable image.

		__Example (OpenSesame script):__

		~~~
		widget 0 0 1 1 image_button path='5.png' var='response'
		~~~

		__Example (Python):__

		~~~ {.python}
		from libopensesame import widgets
		form = widgets.form(self.experiment)
		# The full path to the image needs to be provided.
		# self.experiment.get_file() can be used to retrieve the full path
		# to an image in the file pool.
		image_button = widgets.image_button(form,
			path=self.experiment.get_file('5.png'), var='response')
		form.set_widget(image_button, (0,0))
		form._exec()
		~~~

		__Function list:__

		%--
		toc:
			mindepth: 2
			maxdepth: 2
		--%
	"""

	def __init__(self, form, path=None, adjust=True, frame=False, image_id=None,
		var=None):
	
		"""
		desc:
			Constructor.

		arguments:
			form:
				desc:	The parent form.
				type:	form

		keywords:
			path:
				desc:	The full path to the image. To show an image from the
						file pool, you need to first use `experiment.get_file`
						to determine the full path to the image.
				type:	[str, unicode, NoneType]
			adjust:
				desc:	Indicates whether the image should be scaled according
						to the size of the widget.
				type:	bool
			frame:
				desc:	Indicates whether a frame should be drawn around the
						widget.
				type:	bool
			image_id:
				desc:	An id to identify the image when it is clicked. If
						`None`, the path to the image is used as id.
				type:	[str, unicode, NoneType]
			var:
				desc:	The name of the experimental variable that should be
						used to log the widget status.
				type:	[str, unicode, NoneType]
		"""
	
		image.__init__(self, form, path, adjust=adjust, frame=frame)
		if image_id == None:
			self.image_id = path
		else:
			self.image_id = image_id
		self.type = u'image_button'
		self.var = var
		self.set_var(False)				
				
	def on_mouse_click(self, pos):
	
		"""
		desc:
			Is called whenever the user clicks on the widget. Returns the
			image_id or the path to the image if no image_id has been specified.
		
		arguments:
			pos:
				desc:	An (x, y) coordinate tuple.
				type:	tuple
		"""
	
		self.set_var(True)
		return self.image_id


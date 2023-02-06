# -*- coding:utf-8 -*-

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
from libopensesame.widgets._image import ImageWidget


class ImageButton(ImageWidget):

    r"""The image_button widget is a clickable image.

    __Example (OpenSesame
    script):__

    ~~~
    widget 0 0 1 1 image_button path='5.png' var='response'
    ~~~
    __Example (Python):__

    ~~~ .python
    form = Form()
    # The full path to the
    image needs to be provided.
    # self.experiment.pool can be used to retrieve
    the full path
    # to an image in the file pool.
    image_button =
    ImageButton(path=pool['5.png'], var='response')
    form.set_widget(image_button, (0,0))
    form._exec()
    ~~~

    [TOC]
    """
    def __init__(self, form, path=None, adjust=True, frame=False, image_id=None,
                 var=None):
        r"""Constructor to create a new `ImageButton` object. You do not
        generally call this constructor directly, but use the
        `ImageButton()`
        factory function, which is described here:
        [/python/common/]().

        Parameters
        ----------
        form : form
            The parent form.
        path : str, unicode, NoneType, optional
            The full path to the image. To show an image from the file pool,
            you need to first use `experiment.get_file` to determine the full
            path to the image.
        adjust : bool, optional
            Indicates whether the image should be scaled according to the size
            of the widget.
        frame : bool, optional
            Indicates whether a frame should be drawn around the widget.
        image_id : str, unicode, NoneType, optional
            An id to identify the image when it is clicked. If `None`, the path
            to the image is used as id.
        var : str, unicode, NoneType, optional
            The name of the experimental variable that should be used to log
            the widget status.
        """
        ImageWidget.__init__(self, form, path, adjust=adjust, frame=frame)
        self.image_id = path if image_id is None else image_id
        self.type = u'image_button'
        self.var = var
        self.set_var(False)

    def on_mouse_click(self, pos):
        r"""Is called whenever the user clicks on the widget. Returns the
        image_id or the path to the image if no image_id has been specified.

        Parameters
        ----------
        pos : tuple
            An (x, y) coordinate tuple.
        """
        self.theme_engine.click()
        self.set_var(True)
        return self.image_id


image_button = ImageButton

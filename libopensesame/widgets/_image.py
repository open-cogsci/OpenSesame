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
from libopensesame import misc
from libopensesame.widgets._widget import Widget
from PIL import Image
from libopensesame.exceptions import ImageDoesNotExist, UnsupportedImageFormat
from openexp.canvas_elements import Image as ImageElement
import os
import sys


class ImageWidget(Widget):

    r"""The `Image` widget is used to display a non-interactive image.
    __Example (OpenSesame script):__

    ~~~
    widget 0 0 1 1 image path='5.png'
    ~~~
    __Example (Python):__

    ~~~ .python
    form = Form()
    # The full path to the
    image needs to be provided.
    # self.experiment.pool can be used to retrieve
    the full path
    # to an image in the file pool.
    image =
    ImageWidget(path=pool['5.png'])
    form.set_widget(image, (0,0))
    form._exec()
    ~~~

    [TOC]
    """
    def __init__(self, form, path=None, adjust=True, frame=False):
        r"""Constructor to create a new `ImageWidget` object. You do not
        generally call this constructor directly, but use the
        `ImageWidget()`
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
        """
        if isinstance(adjust, str):
            adjust = adjust == u'yes'
        if isinstance(frame, str):
            frame = frame == u'yes'
        Widget.__init__(self, form)
        self.adjust = adjust
        self.frame = frame
        self.path = path
        self.type = u'image'

    def _init_canvas_elements(self):
        r"""Initializes all canvas elements."""
        _path = safe_str(self.path, enc=sys.getfilesystemencoding())
        if not os.path.exists(_path):
            raise ImageDoesNotExist(_path)
        x, y, w, h = self.rect
        x += w/2
        y += h/2
        self.canvas.add_element(
            ImageElement(_path, x=x, y=y, scale=self.scale, center=True)
            .construct(self.canvas)
        )
        Widget._init_canvas_elements(self)
        if self.frame:
            self._update_frame(self.rect)

    def set_rect(self, rect):
        r"""Sets the widget geometry.

        Parameters
        ----------
        rect : tuple
            A (left, top, width, height) tuple.
        """
        self.rect = rect
        _path = safe_str(self.path, enc=sys.getfilesystemencoding())
        if not os.path.isfile(_path):
            raise ImageDoesNotExist(_path)
        if self.adjust:
            x, y, w, h = self.rect
            try:
                img = Image.open(_path)
                img_w, img_h = img.size
            except:
                try:
                    import pygame
                    img = pygame.image.load(_path)
                except:
                    raise UnsupportedImageFormat(_path)
                img_w, img_h = img.get_size()
            scale_x = 1.*w/img_w
            scale_y = 1.*h/img_h
            self.scale = min(scale_x, scale_y)
        else:
            self.scale = 1
        Widget.set_rect(self, rect)


image = ImageWidget

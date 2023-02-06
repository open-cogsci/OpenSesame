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
from libopensesame.widgets._label import Label


class Button(Label):

    r"""The `Button` widget is a clickable text string, by default surrounded
    by
    a button-like frame.

    __Example (OpenSesame script):__

    ~~~
    widget 0 0 1
    1 button text='Click me!' center='yes' frame='yes' var='response'
    ~~~
    Defining a button widget with Python inline code:

    __Example (Python):__
    ~~~ .python
    form = Form()
    button = Button(text='Click me!', frame=True,
    center=True, var='response')
    form.set_widget(button, (0,0))
    form._exec()
    ~~~

    [TOC]
    """
    def __init__(self, form, text=u'button', frame=True, center=True, var=None):
        r"""Constructor to create a new `Button` object. You do not generally
        call this constructor directly, but use the `Button()` factory
        function, which is described here: [/python/common/]().

        Parameters
        ----------
        form : form
            The parent form.
        text : str, unicode, optional
            Button text.
        frame : bool, optional
            Indicates whether a frame should be drawn around the widget.
        center : bool, optional
            Indicates whether the text should be centered.
        var : str, unicode, NoneType, optional
            The name of the experimental variable that should be used to log
            the widget status.
        """
        Label.__init__(self, form, text, frame=frame, center=center)
        self.type = u'button'
        self.var = var
        self.set_var(False)

    def on_mouse_click(self, pos):
        r"""Is called when the user clicks on the button. Returns the button
        text.

        Parameters
        ----------
        pos : tuple
            An (x, y) coordinates tuple.

        Returns
        -------
        unicode
            The button text.
        """
        self.theme_engine.click()
        self.set_var(True)
        return self.text


button = Button

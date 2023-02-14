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
import warnings
import random
import itertools
import math
from openexp.backend import Backend, configurable
from openexp.color import Color
from PIL import Image as PILImage
from collections import OrderedDict
from openexp.canvas_elements import (
    Line,
    Rect,
    Polygon,
    Ellipse,
    Image,
    Gabor,
    NoisePatch,
    Circle,
    FixDot,
    ElementFactory,
    RichText,
    Arrow
)
from openexp._canvas._element.element import Element
from openexp._canvas._element.group import Group


class Canvas(Backend):

    r"""The `Canvas` class is used to present visual stimuli. You generally
    create a `Canvas` object with the `Canvas()` factory function, as
    described
    in the section [Creating a Canvas](#creating-a-canvas).

    __Example__:

    ~~~
    .python
    # Create and show a canvas with a central fixation dot
    my_canvas =
    Canvas()
    my_canvas.fixdot()
    my_canvas.show()
    ~~~

    __Example__:

    As of
    OpenSesame 3.2, you can also add `Canvas` elements as objects.
    See also the
    section on [Naming, accessing, and modifying elements](#naming-accessing-
    and-modifying-elements).

    ~~~ .python
    # Create a canvas with a fixation dot
    and a rectangle
    my_canvas = Canvas()
    my_canvas['my_fixdot'] = FixDot()
    my_canvas.show()
    ~~~

    [TOC]

    ## Things to know

    ### Creating a Canvas

    You
    generally create a `Canvas` with the `Canvas()` factory function:

    ~~~
    .python
    my_canvas = Canvas()
    ~~~

    Optionally, you can pass [Style
    keywords](#style-keywords) to `Canvas()`
    to set the default style:

    ~~~
    .python
    my_canvas = Canvas(color='green')
    my_canvas.fixdot() # Will be
    green
    ~~~

    ### Style keywords

    All functions that accept `**style_args`
    take the following keyword
    arguments:

    - `color` specifies the foreground
    color. For valid color
            specifications, see [colors](#colors).
    -
    `background_color` specifies the background color. For valid color
    specifications, see [colors](#colors).
    - `fill` indicates whether
    rectangles, circles, polygons, and ellipses
            are filled (`True`), or
    drawn as an outline (`False`).
    - `penwidth` indicates a penwidth in pixels
    and should be `int` or
            `float`.
    - `html` indicates whether HTML-
    tags are interpreted, and should be
            `True` or `False`. For
    supported tags, see [/usage/text/]().
    - `font_family` is the name of a font
    family, such as 'sans'.
    - `font_size` is a font size in pixels.
    -
    `font_italic` indicates whether text should italics, and should be
    `True` or `False`.
    - `font_bold` indicates whether text should bold, and
    should be
            `True` or `False`.
    - `font_underline` indicates whether
    text should underlined, and should
            be `True` or `False`.

    ~~~
    .python
    # Draw a green fixation dot
    my_canvas = Canvas()
    my_canvas.fixdot(color='green')
    my_canvas.show()
    ~~~

    Style keywords only
    affect the current drawing operation (except when
    passed to `Canvas()`
    while creating the `Canvas`). To change the style
    for all subsequent
    drawing operations, set style properties, such as
    `canvas.color`, directly:
    ~~~ .python
    # Draw a red cross with a 2px penwidth
    my_canvas = Canvas()
    my_canvas.color = u'red'
    my_canvas.penwidth = 2
    my_canvas.line(-10, -10,
    10, 10)
    my_canvas.line(-10, 10, 10, -10)
    my_canvas.show()
    ~~~

    Or pass the
    style properties to `Canvas()`:

    ~~~ .python
    # Draw a red cross with a 2px
    penwidth
    my_canvas = Canvas(color=u'red', penwidth=2)
    my_canvas.line(-10,
    -10, 10, 10)
    my_canvas.line(-10, 10, 10, -10)
    my_canvas.show()
    ~~~


    ###
    Colors

    You can specify colors in the following ways. This includes
    CSS3-type
    color specifications, but also supports some extra
    specifications,
    such as CIE l\* a\* b\* color space.

    __Version note:__ The
    `hsv`, `hsl`, and `lab` color spaces are new in
    v3.3.0.

    - __Color names:__
    'red', 'black', etc. A full list of valid color names
            can be found
    [here](http://www.w3.org/TR/SVG11/types.html#ColorKeywords).
    - __Seven-
    character hexadecimal strings:__ `#FF0000`, `#000000`, etc.
            Here,
    values range from `00` to `FF`, so that `#FF0000` is bright red.
    - __Four-
    character hexadecimal strings:__ `#F00`, `#000`, etc. Here,
            values
    range from '0' to 'F' so that `#F00` is bright red.
    - __RGB strings:__
    `rgb(255,0,0)`, `rgb(0,0,0)`, etc. Here, values
            range from 0 to 255
    so that `rgb(255,0,0)` is bright red.
    - __RGB percentage strings:__
    `rgb(100%,0%,0%)`, `rgb(0%,0%,0%)`, etc.
            Here, values range from 0%
    to 100% so that `rgb(100%,0%,0%)` is
            bright red.
    - __RGB tuples:__
    `(255, 0, 0)`, `(0, 0 ,0)`, etc. Here, values range
            from `0` to
    `255` so that `(255,0,0)' is bright red.
    - __HSV strings:__ `hsv(120, 100%,
    100%)`. In the [HSV](https://en.wikipedia.org/wiki/HSL_and_HSV)
    color space, the hue parameter is an angle from 0 to 359, and the
    saturation and value parameters are percentages from 0% to 100%.
    - __HSL
    strings:__ `hsl(120, 100%, 50%)`. In the
    [HSL](https://en.wikipedia.org/wiki/HSL_and_HSV)
            color space, the
    hue parameter is an angle from 0 to 359, and the
            saturation and
    lightness parameters are percentages from 0% to 100%.
    - __LAB strings:__
    `lab(53, -20, 0)`. In the
    [CIELAB](https://en.wikipedia.org/wiki/CIELAB_color_space)
            color
    space, the parameters reflect lightness (`l*`),
            green-red axis
    (`a*`, negative is green), and blue-yellow axis
            (`b*`, negative is
    blue). This uses the D65 white point and the
            sRGB transfer
    function, as implemented [here](https://www.psychopy.org/_modules/psychopy/
    tools/colorspacetools.html).
    - __Luminance values:__  `255`, `0`, etc.
    Here, values range from `0` to
            `255` so that `255` is white.

    ~~~
    .python
    # Various ways to specify green
    my_canvas.fixdot(color='green')  #
    Dark green
    my_canvas.fixdot(color='#00ff00')
    my_canvas.fixdot(color='#0f0')
    my_canvas.fixdot(color='rgb(0, 255, 0)')
    my_canvas.fixdot(color='rgb(0%,
    100%, 0%)')
    my_canvas.fixdot(color='hsl(100, 100%, 50%)')
    my_canvas.fixdot(color='hsv(0, 100%, 100%)')
    my_canvas.fixdot(color='lab(53, -20, 0)')  # Dark green
    my_canvas.fixdot(color=(0, 255, 0))
    # Specify a luminance value (white)
    my_canvas.fixdot(color=255)
    ~~~


    ### Naming, accessing, and modifying
    elements

    As of OpenSesame 3.2, the `Canvas` supports an object-based
    interface
    that allows you to name elements, and to access and modify
    elements
    individually, without having to redraw the entire `Canvas`.

    For
    example, the following will first add a red `Line` element to a
    `Canvas`
    and show it, then change the color of the line to green and
    show it again,
    and then finally delete the line and show the canvas
    again (which is now
    blank). The name of the element (`my_line`) is used
    to refer to the element
    for all the operations.

    ~~~ .python
    my_canvas = Canvas()
    my_canvas['my_line'] = Line(-100, -100, 100, 100, color='red')
    my_canvas.show()
    clock.sleep(1000)
    my_canvas['my_line'].color = 'green'
    my_canvas.show()
    clock.sleep(1000)
    del my_canvas['my_line']
    my_canvas.show()
    ~~~

    You can also add an element without explicitly
    providing a name for it.
    In that case, a name is generated automatically
    (e.g. `stim0`).

    ~~~ .python
    my_canvas = Canvas()
    my_canvas += FixDot()
    my_canvas.show()
    ~~~

    If you add a list of elements, they will be
    automatically grouped
    together, and you can refer to the entire group by
    name.

    ~~~ .python
    my_canvas = Canvas()
    my_canvas['my_cross'] = [
    Line(-100, 0, 100, 0),
            Line(0, -100, 0, 100)
    ]
    my_canvas.show()
    ~~~
    To check whether a particular `x,y` coordinate falls within the bounding
    rectangle of an element, you can use `in`:

    ~~~ .python
    my_mouse =
    Mouse(visible=True)
    my_canvas = Canvas()
    my_canvas['rect'] = Rect(-100,
    -100, 200, 200)
    my_canvas.show()
    button, (x, y), time =
    my_mouse.get_click()
    if (x, y) in my_canvas['rect']:
            print('Clicked
    in rectangle')
    else:
            print('Clicked outside of rectangle')
    ~~~

    You
    can also get a list of the names of all elements that contain an
    `x,y`
    coordinate, using the `Canvas.elements_at()` function, documented
    below.
    %--
    constant:
            arg_max_width: |
                    The maximum width of
    the text in pixels, before wrapping to a
                    new line, or
    `None` to wrap at screen edge.
            arg_bgmode: |
    Specifies whether the background is the average of col1 col2
    ('avg', corresponding to a typical Gabor patch), or equal to
    col2 ('col2'), useful for blending into the background. Note:
    this parameter is ignored by the psycho backend, which uses
    increasing transparency for the background.
            arg_style: |
    Optional [style keywords](#style-keywords) that specify the
    style of the current drawing operation. This does not affect
    subsequent drawing operations.
            arg_center: |
                    A bool
    indicating whether the coordinates reflect the center
    (`True`) or top-left (`False`) of the text.
    --%
    """
    # The maximum duration that Canvas.show() should take, which is set to one
    # frame duration on a 60 Hz monitor. If Canvas.show() takes longer, a
    # warning given.
    MAX_SHOW_DT = 16

    def __init__(self, experiment, auto_prepare=True, **style_args):
        r"""Constructor to create a new `Canvas` object. You do not generally
        call this constructor directly, but use the `Canvas()` factory
        function, which is described here: [/python/common/]().

        Parameters
        ----------
        experiment : experiment
            The experiment object.
        auto_prepare : bool, optional
            Indicates whether the canvas should be automatically prepared after
            each drawing operation, so that [canvas.show] will be maximally
            efficient. If auto_prepare is turned off, drawing operations may be
            faster, but [canvas.show] will take longer, unless [canvas.prepare]
            is explicitly called in advance. This option exists mostly for
            historical purposes, because there are currently no backends for
            which it is necessary to disable auto prepare.
        **style_args : dict
            Optional [style keywords](#style-keywords), which will be used as
            the default for all drawing operations on this `Canvas`.


        Examples
        --------
        >>> my_canvas = Canvas()
        >>> my_canvas.fixdot()
        >>> my_canvas.show()
        """
        self.experiment = experiment
        self._width = self.experiment.var.width
        self._height = self.experiment.var.height
        self.auto_prepare = auto_prepare
        Backend.__init__(self, configurables={
            u'color': None,
            u'background_color': None,
            u'fill': self.assert_bool,
            u'penwidth': self.assert_numeric,
            u'html': self.assert_bool,
            u'font_family': self.assert_string,
            u'font_size': self.assert_numeric,
            u'font_italic': self.assert_bool,
            u'font_bold': self.assert_bool,
            u'font_underline': self.assert_bool,
        }, **style_args)
        self._elements = OrderedDict()
        self._stimnr = 0

    def __enter__(self):
        r"""The context manager provides an elegant way to disable auto
        preparation. However, it is hidden for now because none of the backends
        require it.
        """
        self._original_auto_prepare = self.auto_prepare
        self.auto_prepare = False
        return self

    def __exit__(self, exc_type, exc_value, traceback):
        r"""The context manager provides an elegant way to disable auto
        preparation. However, it is hidden for now because none of the backends
        require it.
        """
        self.auto_prepare = self._original_auto_prepare
        self.prepare()

    def __setitem__(self, key, value):
        r"""Sets a named element. If a list of elements is provided, a Group is
        automatically created.
        """
        if key in self._elements:
            raise ValueError('An element with the name "%s" already exists' %
                             key)
        if isinstance(value, list):
            value = Group(self, [e.construct(self)
                                 if isinstance(e, ElementFactory) else e for e in value])
        if isinstance(value, ElementFactory):
            value = value.construct(self)
        if not isinstance(value, Element):
            raise TypeError('%s is not a canvas element but %s' %
                            (key, type(value)))
        self._elements[key] = value

    def __delitem__(self, key):
        r"""Deletes an element by name."""
        del self._elements[key]

    def __getitem__(self, key):
        r"""Retrieves an element by name."""
        return self._elements[key]

    def __len__(self):
        r"""Gets the number of elements, where a Group counts as 1."""
        return len(self._elements)

    def __contains__(self, key):
        r"""Checks whether a named element is in the Canvas."""
        return key in self._elements

    def __iter__(self):
        r"""Iterates over the elements."""
        for name, stim in self._elements.items():
            yield name, stim

    def __iadd__(self, element):
        r"""Adds an unnamed element."""
        while 'stim%d' % self._stimnr in self._elements:
            self._stimnr += 1
        self['stim%d' % self._stimnr] = element
        return self

    def _get_name_element(self, element):
        r"""Gets a name, element tuple for an element or element name (i.e. get
        both if you have only one).

        Parameters
        ----------
        element : Element, str
            A SKETCHPAD element, or its name.

        Returns
        -------
        A (name, element) tuple.
        """
        if isinstance(element, str):
            return element, self._elements[element]
        for name, _element in self._elements.items():
            if element is _element:
                return name, element
        raise ValueError('"%s" not found in canvas"' % element)

    def elements_at(self, x, y):
        r"""*New in v3.2.0*

        Gets the names of elements that contain a
        particular `x, y`
        coordinate.

        Parameters
        ----------
        x : int, float
            An X coordinate.
        y : int, float
            A Y coordinate.

        Returns
        -------
        list
            A `list` of element names that contain the coordinate `x, y`.

        Examples
        --------
        >>> # Create and show a canvas with two partly overlapping rectangles
        >>> my_canvas = Canvas()
        >>> my_canvas['right_rect'] = Rect(x=-200, y=-100, w=200, h=200, color='red')
        >>> my_canvas['left_rect'] = Rect(x=-100, y=-100, w=200, h=200, color='green')
        >>> my_canvas.show()
        >>> # Collect a mouse click and print the names of the elements that
        >>> # contain the clicked point
        >>> my_mouse = Mouse(visible=True)
        >>> button, pos, time = my_mouse.get_click()
        >>> if pos is not None:
        >>>     x, y = pos
        >>>     print('Clicked on elements: %s' % my_canvas.elements_at(x, y))
        """
        elements = []
        for name, element in self:
            try:
                if (x, y) in element:
                    elements.append(name)
            except NotImplementedError:
                pass
        return elements

    def lower_to_bottom(self, element):
        r"""Lowers an element to the bottom, so that it is drawn first; that
        is, it becomes the background.

        Parameters
        ----------
        element : Element, str
            A SKETCHPAD element, or its name.
        """
        first_name, first_element = self._get_name_element(element)
        self._elements.pop(first_name)
        _elements = OrderedDict()
        _elements[first_name] = first_element
        for name, element in self._elements.items():
            _elements[name] = element
        self._elements = _elements

    def raise_to_top(self, element):
        r"""Raises an element to the top, so that it is drawn last; that is, it
        becomes the foreground.

        Parameters
        ----------
        element : Element, str
            A SKETCHPAD element, or its name.
        """
        last_name, last_element = self._get_name_element(element)
        self._elements.pop(last_name)
        _elements = OrderedDict()
        for name, element in self._elements.items():
            _elements[name] = element
        _elements[last_name] = last_element
        self._elements = _elements

    def add_element(self, element, name=None):
        r"""An alternative to the dict and += API. For internal use."""
        if name is None:
            self.__iadd__(element)
            return
        self._elements[name] = element

    def rename_element(self, old_name, new_name):
        r"""Renames an element."""
        element = self._elements.pop(old_name)
        i = 1
        name = new_name
        while name in self._elements:
            name = '%s_%d' % (new_name, i)
            i += 1
        self._elements[name] = element

    def set_config(self, **cfg):

        # Convert color to backend specific colors
        if u'color' in cfg and not hasattr(cfg[u'color'], u'backend_color'):
            cfg[u'color'] = Color(self.experiment, cfg[u'color'])
        if u'background_color' in cfg \
                and not hasattr(cfg[u'background_color'], u'backend_color'):
            cfg[u'background_color'] = Color(self.experiment,
                                             cfg[u'background_color'])
        Backend.set_config(self, **cfg)

    def default_config(self):

        return {
            u'penwidth': 1,
            u'fill': False,
            u'html': True,
            u'color': self.experiment.var.foreground,
            u'background_color': self.experiment.var.background,
            u'font_size': self.experiment.var.font_size,
            u'font_family': self.experiment.var.font_family,
            u'font_bold': self.experiment.var.font_bold == u'yes',
            u'font_italic': self.experiment.var.font_italic == u'yes',
            u'font_underline': self.experiment.var.font_underline == u'yes',
        }

    @property
    def size(self):
        r"""The size of the canvas as a `(width, height)` tuple. This is a
        read-only property.
        """
        return self._width, self._height

    @property
    def width(self):
        r"""The width of the canvas. This is a read-only property."""
        return self._width

    @property
    def height(self):
        r"""The height of the canvas. This is a read-only property."""
        return self._height

    @property
    def left(self):
        r"""The x coordinate of the left edge of the display. This is a read-
        only property.
        """
        return self._left

    @property
    def right(self):
        r"""The x coordinate of the right edge of the display. This is a read-
        only property.
        """
        return self._right

    @property
    def top(self):
        r"""The y coordinate of the top edge of the display. This is a read-
        only property.
        """
        return self._top

    @property
    def bottom(self):
        r"""The y coordinate of the bottom edge of the display. This is a read-
        only property.
        """
        return self._bottom

    def copy(self, canvas):
        r"""Turns the current `Canvas` into a copy of the passed `Canvas`.
        __Warning:__

        Copying `Canvas` objects can result in unpredictable
        behavior. In
        many cases, a better solution is to recreate multiple
        `Canvas`
        objects from scratch, and/ or to use the element interface to
        update `Canvas` elements individually.

        Parameters
        ----------
        canvas : canvas
            The `Canvas` to copy.

        Examples
        --------
        >>> my_canvas = Canvas()
        >>> my_canvas.fixdot(x=100, color='green')
        >>> my_copied_canvas = Canvas()
        >>> my_copied_canvas.copy(my_canvas)
        >>> my_copied_canvas.fixdot(x=200, color="blue")
        >>> my_copied_canvas.show()
        """
        self._elements = OrderedDict([
            (name, element.copy(self))
            for name, element in canvas._elements.items()
        ])
        self.set_config(**canvas.get_config())

    def prepare(self):
        r"""Finishes pending canvas operations (if any), so that a subsequent
        call to [canvas.show] is extra fast. It's only necessary to call this
        function if you have disabled `auto_prepare` in [canvas.__init__].
        """
        for name, element in self._elements.items():
            if element.visible:
                element.prepare()

    def show(self):
        r"""Shows, or 'flips', the canvas on the screen.

        Returns
        -------
        int, float
            A timestamp of the time at which the canvas actually appeared on
            the screen, or a best guess if precise temporal information is not
            available. For more information about timing, see </misc/timing>.
            Depending on the back-end the timestamp is an `int` or a `float`.

        Examples
        --------
        >>> my_canvas = Canvas()
        >>> my_canvas.fixdot()
        >>> t = my_canvas.show()
        >>> exp.set('time_fixdot', t)
        """
        raise NotImplementedError()

    @configurable
    def clear(self, **style_args):
        r"""Clears the canvas with the current background color. Note that it
        is generally faster to use a different canvas for each experimental
        display than to use a single canvas and repeatedly clear and redraw it.

        Parameters
        ----------
        **style_args : dict
            %arg_style


        Examples
        --------
        >>> my_canvas = Canvas()
        >>> my_canvas.fixdot(color='green')
        >>> my_canvas.show()
        >>> clock.sleep(1000)
        >>> my_canvas.clear()
        >>> my_canvas.fixdot(color='red')
        >>> my_canvas.show()
        """
        raise NotImplementedError()

    def fixdot(self, x=None, y=None, style=u'default', **style_args):
        r"""Draws a fixation dot. The default style is medium-open.

        - 'large-
        filled' is a filled circle with a 16px radius.
        - 'medium-filled' is a
        filled circle with an 8px radius.
        - 'small-filled' is a filled circle
        with a 4px radius.
        - 'large-open' is a filled circle with a 16px radius
        and a 2px hole.
        - 'medium-open' is a filled circle with an 8px radius
        and a 2px hole.
        - 'small-open' is a filled circle with a 4px radius and
        a 2px hole.
        - 'large-cross' is 16px cross.
        - 'medium-cross' is an 8px
        cross.
        - 'small-cross' is a 4px cross.

        Parameters
        ----------
        x : int, NoneType, optional
            The X coordinate of the dot center, or None to draw a horizontally
            centered dot.
        y : int, NoneType, optional
            The Y coordinate of the dot center, or None to draw a vertically
            centered dot.
        style : str, unicode, optional
            The fixation-dot style. One of: default, large-filled,
            medium-
            filled, small-filled, large-open, medium-open,
            small-open, large-
            cross, medium-cross, or small-cross.
            default equals medium-open.
        **style_args : dict
            %arg_style


        Examples
        --------
        >>> my_canvas = Canvas()
        >>> # Function interface
        >>> my_canvas.fixdot()
        >>> # Element interface
        >>> my_canvas['my_fixdot'] = FixDot()
        """
        self += FixDot(x=x, y=y, style=style, **style_args)
        return 'stim%d' % self._stimnr

    def circle(self, x, y, r, **style_args):
        r"""Draws a circle.

        Parameters
        ----------
        x : int
            The center X coordinate of the circle.
        y : int
            The center Y coordinate of the circle.
        r : int
            The radius of the circle.
        **style_args : dict
            %arg_style


        Examples
        --------
        >>> my_canvas = Canvas()
        >>> # Function interface
        >>> my_canvas.circle(100, 100, 50, fill=True, color='red')
        >>> # Element interface
        >>> my_canvas['my_circle'] = Circle(100, 100, 50, fill=True, color='red')
        """
        self += Circle(x, y, r, **style_args)
        return 'stim%d' % self._stimnr

    def line(self, sx, sy, ex, ey, **style_args):
        r"""Draws a line.

        Parameters
        ----------
        sx : int
            The left X coordinate.
        sy : int
            The top Y coordinate.
        ex : int
            The right X coordinate.
        ey : int
            The bottom Y coordinate.
        **style_args : dict
            %arg_style
        """
        self += Line(sx, sy, ex, ey, **style_args)
        return 'stim%d' % self._stimnr

    def arrow(self, sx, sy, ex, ey, body_length=0.8, body_width=.5,
              head_width=30, **style_args):
        r"""Draws an arrow. An arrow is a polygon consisting of 7 vertices,
        with an arrowhead pointing at (ex, ey).

        Parameters
        ----------
        sx : int
            The X coordinate of the arrow's base.
        sy : int
            The Y coordinate of the arrow's base.
        ex : int
            The X coordinate of the arrow's tip.
        ey : int
            The Y coordinate of the arrow's tip..
        body_length : float, optional
            Proportional length of the arrow body relative to the full arrow
            [0-1].
        body_width : float, optional
            Proportional width (thickness) of the arrow body relative to the
            full arrow [0-1].
        head_width : float, optional
            Width (thickness) of the arrow head in pixels.
        """
        self += Arrow(sx, sy, ex, ey, body_width=body_width,
                      body_length=body_length, head_width=head_width, **style_args)
        return 'stim%d' % self._stimnr

    def rect(self, x, y, w, h, **style_args):
        r"""Draws a rectangle.

        Parameters
        ----------
        x : int
            The left X coordinate.
        y : int
            The top Y coordinate.
        w : int
            The width.
        h : int
            The height.
        **style_args : dict
            %arg_style


        Examples
        --------
        >>> my_canvas = Canvas()
        >>> # Function interface
        >>> my_canvas.rect(-10, -10, 20, 20, fill=True)
        >>> # Element interface
        >>> my_canvas['my_rect'] = Rect(-10, -10, 20, 20, fill=True)
        """
        self += Rect(x, y, w, h, **style_args)
        return 'stim%d' % self._stimnr

    def ellipse(self, x, y, w, h, **style_args):
        r"""Draws an ellipse.

        Parameters
        ----------
        x : int
            The left X coordinate.
        y : int
            The top Y coordinate.
        w : int
            The width.
        h : int
            The height.
        **style_args : dict
            %arg_style


        Examples
        --------
        >>> my_canvas = Canvas()
        >>> # Function interface
        >>> my_canvas.ellipse(-10, -10, 20, 20, fill=True)
        >>> # Element interface
        >>> my_canvas['my_ellipse'] = Ellipse(-10, -10, 20, 20, fill=True)
        """
        self += Ellipse(x, y, w, h, **style_args)
        return 'stim%d' % self._stimnr

    def polygon(self, vertices, **style_args):
        r"""Draws a polygon that defined by a list of vertices. I.e. a shape of
        points connected by lines.

        Parameters
        ----------
        vertices : list
            A list of tuples, where each tuple corresponds to a vertex. For
            example, [(100,100), (200,100), (100,200)] will draw a triangle.
        **style_args : dict
            %arg_style


        Examples
        --------
        >>> my_canvas = Canvas()
        >>> n1 = 0,0
        >>> n2 = 100, 100
        >>> n3 = 0, 100
        >>> # Function interface
        >>> my_canvas.polygon([n1, n2, n3])
        >>> # Element interface
        >>> my_canvas['my_polygon'] = Polygon([n1, n2, n3])
        """
        self += Polygon(vertices, **style_args)
        return 'stim%d' % self._stimnr

    def text_size(self, text, center=True, max_width=None, **style_args):
        r"""Determines the size of a text string in pixels.

        Parameters
        ----------
        text : str, unicode
            A string of text.
        center : bool, optional
            %arg_center
        max_width : int, NoneType, optional
            %arg_max_width
        **style_args : dict
            %arg_style


        Returns
        -------
        tuple
            A (width, height) tuple containing the dimensions of the text
            string.

        Examples
        --------
        >>> my_canvas = Canvas()
        >>> w, h = my_canvas.text_size('Some text')
        """
        return RichText(
            text,
            center=center,
            max_width=max_width,
            font_size=self.font_size,
            font_family=self.font_family,
            font_bold=self.font_bold,
            font_italic=self.font_italic
        ).construct(self.__class__(self.experiment)).size

    def text(self, text, center=True, x=None, y=None, max_width=None,
             **style_args):
        r"""Draws text.

        Parameters
        ----------
        text : str, unicode
            A string of text. When using Python 2, this should be either
            `unicode` or a utf-8-encoded `str`. When using Python 3, this
            should be either `str` or a utf-8-encoded `bytes`.
        center : bool, optional
            %arg_center
        x : int, NoneType, optional
            The X coordinate, or None to draw horizontally centered text.
        y : int, NoneType, optional
            The Y coordinate, or None to draw vertically centered text.
        max_width : int, NoneType, optional
            %arg_max_width
        **style_args : dict
            %arg_style


        Examples
        --------
        >>> my_canvas = Canvas()
        >>> # Function interface
        >>> my_canvas.text('Some text with <b>boldface</b> and <i>italics</i>')
        >>> # Element interface
        >>> my_canvas['my_text'] = Text('Some text with <b>boldface</b> and <i>italics</i>')
        """
        self += RichText(text, center=center, x=x, y=y, max_width=max_width,
                         **style_args)
        return 'stim%d' % self._stimnr

    def image(self, fname, center=True, x=None, y=None, scale=None,
              rotation=None):
        r"""Draws an image from file. This function does not look in the file
        pool, but takes an absolute path.

        Parameters
        ----------
        fname : str, unicode
            The filename of the image. When using Python 2, this should be
            either `unicode` or a utf-8-encoded `str`. When using Python 3,
            this should be either `str` or a utf-8-encoded `bytes`.
        center : bool, optional
            A bool indicating whether coordinates indicate the center (True) or
            top-left (False).
        x : int, NoneType, optional
            The X coordinate, or `None` to draw a horizontally centered image.
        y : int, NoneType, optional
            The Y coordinate, or `None` to draw a vertically centered image.
        scale : float, int, NoneType, optional
            The scaling factor of the image. `None` or 1 indicate the original
            size. 2.0 indicates a 200% zoom, etc.
        rotation : float, int, NoneType, optional
            The rotation of the image `None` or 0 indicate the original
            rotation. Positive values indicate a clockwise rotation in degrees.

        Examples
        --------
        >>> my_canvas = Canvas()
        >>> # Determine the absolute path:
        >>> path = exp.pool[u'image_in_pool.png']
        >>> # Function interface
        >>> my_canvas.image(path)
        >>> # Element interface
        >>> my_canvas['my_image'] = Image(path)
        """
        self += Image(
            fname, center=center, x=x, y=y, scale=scale, rotation=rotation
        )
        return 'stim%d' % self._stimnr

    def gabor(self, x, y, orient, freq, env=u'gaussian', size=96, stdev=12,
              phase=0, col1=u'white', col2=u'black', bgmode=u'avg'):
        r"""Draws a Gabor patch. Note: The exact rendering of the Gabor patch
        depends on the back-end.

        Parameters
        ----------
        x : int
            The center X coordinate.
        y : int
            The center Y coordinate.
        orient : float, int
            Orientation in degrees [0 .. 360]. This refers to a
            clockwise
            rotation from a vertical.

            __Version note:__ In version 3.2.6 and
            earlier, the
            orientation was *counterclockwise* for the *legacy*
            and
            *xpyriment* backends, and clockwise for the *psycho*
            backends.
            As of 3.2.7, the orientation is *clockwise*
            for all backends.
        freq : float, int
            Frequency in cycles/px of the sinusoid.
        env : str, unicode, optional
            The envelope that determines the shape of the patch. Can be
            "gaussian", "linear", "circular", or "rectangular".
        size : float, int, optional
            A size in pixels.
        stdev : float, int, optional
            Standard deviation in pixels of the gaussian. Only applicable to
            gaussian envelopes.
        phase : float, int, optional
            Phase of the sinusoid [0.0 .. 1.0].
        col1 : str, unicode, optional
            A color for the peaks.
        col2 : str, unicode, optional
            A color for the troughs. Note: The psycho back-end
            ignores this
            parameter and always uses the inverse of
            `col1` for the throughs.
        bgmode : str, unicode, optional
            %arg_bgmode

        Examples
        --------
        >>> my_canvas = Canvas()
        >>> # Function interface
        >>> my_canvas.gabor(100, 100, 45, .05)
        >>> # Element interface
        >>> my_canvas['my_gabor'] = Gabor(100, 100, 45, .05)
        """
        self += Gabor(x, y, orient, freq, env=env, size=size,
                      stdev=stdev, phase=phase, col1=col1, col2=col2, bgmode=bgmode)
        return 'stim%d' % self._stimnr

    def noise_patch(self, x, y, env=u'gaussian', size=96, stdev=12,
                    col1=u'white', col2=u'black', bgmode=u'avg'):
        r"""Draws a patch of noise, with an envelope. The exact rendering of
        the noise patch depends on the back-end.

        Parameters
        ----------
        x : int
            The center X coordinate.
        y : int
            The center Y coordinate.
        env : str, unicode, optional
            The envelope that determines the shape of the patch. Can be
            "gaussian", "linear", "circular", or "rectangular".
        size : float, int, optional
            A size in pixels.
        stdev : float, int, optional
            Standard deviation in pixels of the gaussian. Only applicable to
            gaussian envelopes.
        col1 : str, unicode, optional
            The first color.
        col2 : str, unicode, optional
            The second color. Note: The psycho back-end ignores this
            parameter
            and always uses the inverse of `col1`.
        bgmode : str, unicode, optional
            %arg_bgmode

        Examples
        --------
        >>> my_canvas = Canvas()
        >>> # Function interface
        >>> my_canvas.noise_patch(100, 100, env='circular')
        >>> # Element interface
        >>> my_canvas['my_noise_patch'] = NoisePatch(100, 100, env='circular')
        """
        self += NoisePatch(x, y, env=env, size=size, stdev=stdev,
                           col1=col1, col2=col2, bgmode=bgmode)
        return 'stim%d' % self._stimnr

    @staticmethod
    def init_display(experiment):
        r"""Initializes the display before the experiment begins.

        Parameters
        ----------
        experiment : experiment
            An experiment object.
        """
        raise NotImplementedError()

    @staticmethod
    def close_display(experiment):
        r"""Closes the display after the experiment is finished.

        Parameters
        ----------
        experiment : experiment
            An experiment object.
        """
        raise NotImplementedError()


# Translation mapping from envelope names
ENV_SYNONYMS = {
    u"c": u"c",
    u"circular": u"c",
    u"round": u"c",
    u"g": u"g",
    u"gaussian": u"g",
    u"gauss": u"g",
    u"normal": u"g",
    u"r": u"r",
    u"rectangular": u"r",
    u"rectangle": u"r",
    u"g": u"g",
    u"rect": u"g",
    u"square": u"g",
    None: u"g",
    u"l": u"l",
    u"linear": u"l",
    u"lin": u"l",
    u"ln": u"l",
    u"l": u"l"
}

canvas_cache = {}


def _color(col):
    r"""Wrapper function for _gabor and _noise_patch to convert color names to
    PyGame color objects.

    Parameters
    ----------
    col
        A color specification.

    Returns
    -------
    A PyGame color object.
    """
    from openexp._color.legacy import Legacy
    return Legacy(None, col).backend_color


def _xyr(x, y, size, orient=0):
    r"""Gets the coordinates relative to the center and compensating for the
    rotation.
    """
    dx = x - 0.5 * size
    dy = y - 0.5 * size
    t = math.atan2(dy, dx) + orient
    r = math.sqrt(dx ** 2 + dy ** 2)
    return r * math.cos(t), r * math.sin(t), r


def _gabor(
        orient,
        freq,
        env=u"gaussian",
        size=96,
        stdev=12,
        phase=0,
        col1=u"white",
        col2=u"black",
        bgmode=u"avg"
):
    r"""Returns a pygame surface containing a Gabor patch. For arguments, see
    [canvas.gabor].
    """
    env = _match_env(env)
    # Generating a Gabor patch takes quite some time, so keep
    # a cache of previously generated Gabor patches to speed up
    # the process.
    global canvas_cache
    key = u"gabor_%s_%s_%s_%s_%s_%s_%s_%s_%s" % (
        orient,
        freq,
        env,
        size,
        stdev,
        phase,
        col1,
        col2,
        bgmode
    )
    if key in canvas_cache:
        return canvas_cache[key]
    im = PILImage.new(u'RGB', (size, size))
    px = im.load()
    # Conver the orientation to radians
    orient = math.radians(-orient)
    col1 = _color(col1)
    col2 = _color(col2)
    # rx and ry reflect the real coordinates in the
    # target image
    for rx, ry in itertools.product(range(size), range(size)):
        ux, uy, r = _xyr(rx, ry, size, orient)
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
        elif bgmode == u"col2":
            amp = amp * f
        else:
            raise ValueError(
                u"Invalid argument for bgmode: %s "
                u"(should be one of 'avg','col2')"
                % bgmode
            )
        r = col1.r * amp + col2.r * (1.0 - amp)
        g = col1.g * amp + col2.g * (1.0 - amp)
        b = col1.b * amp + col2.b * (1.0 - amp)
        px[rx, ry] = int(r), int(g), int(b)
    canvas_cache[key] = im
    return im


def _noise_patch(
        env=u"gaussian",
        size=96,
        stdev=12,
        col1=u"white",
        col2=u"black",
        bgmode=u"avg"
):
    r"""Returns a pygame surface containing a noise patch. For arguments, see
    [canvas.noise_patch].
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
    im = PILImage.new(u'RGB', (size, size))
    px = im.load()
    col1 = _color(col1)
    col2 = _color(col2)
    # rx and ry reflect the real coordinates in the
    # target image
    for rx, ry in itertools.product(range(size), range(size)):
        ux, uy, r = _xyr(rx, ry, size)
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
        elif bgmode == u"col2":
            amp = amp * f
        else:
            raise ValueError(
                u"Invalid argument for bgmode: %s "
                u"(should be one of 'avg','col2')"
                % bgmode
            )
        r = col1.r * amp + col2.r * (1.0 - amp)
        g = col1.g * amp + col2.g * (1.0 - amp)
        b = col1.b * amp + col2.b * (1.0 - amp)
        px[rx, ry] = int(r), int(g), int(b)
    canvas_cache[key] = im
    return im


def _match_env(env):
    r"""Translation between various envelope names.

    Parameters
    ----------
    env : str, unicode
        An envelope name.

    Returns
    -------
    unicode
        A standard envelope name ("c", "g", "r" or "l")
    """
    if env not in ENV_SYNONYMS:
        raise ValueError(u"'%s' is not a valid envelope" % env)
    return ENV_SYNONYMS[env]


# Non PEP-8 alias for backwards compatibility
canvas = Canvas

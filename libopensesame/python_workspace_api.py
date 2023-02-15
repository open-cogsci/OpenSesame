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

---
desc:
	Functions that are globally accessible in `inline_script` items.
---
"""
from libopensesame.py3compat import *
import random
import math
import warnings
# The classes below are unused, but imported so that they are available in the
# workspace.
from openexp.canvas_elements import (Rect, Line, Text, Ellipse, Circle,
                                     FixDot, Gabor, NoisePatch, Image, Arrow,
                                     Polygon)
from libopensesame.widgets.widget_factory import (Label, Button, ImageWidget,
                                                  ImageButton, TextInput,
                                                  RatingScale, Checkbox)


# Factory functions


def Form(*args, **kwargs):
    r"""A factory function that creates a new `Form` object. For a
    description
    of possible keywords, see:

    - %link:manual/forms/widgets%

    Returns
    -------
    canvas
        A `Form` object.

    Examples
    --------
    >>> form = Form()
    >>> label = Label(text='label')
    >>> button = Button(text='Ok')
    >>> form.set_widget(label, (0,0))
    >>> form.set_widget(button, (0,1))
    >>> form._exec()
    """
    from libopensesame.widgets import form
    return form(experiment, **kwargs)


def Canvas(auto_prepare=True, **style_args):
    r"""A factory function that creates a new `Canvas` object. For a
    description of possible keywords, see:

    - %link:manual/python/canvas%

    Returns
    -------
    canvas
        A `Canvas` object.

    Examples
    --------
    >>> my_canvas = Canvas(color=u'red', penwidth=2)
    >>> my_canvas.line(-10, -10, 10, 10)
    >>> my_canvas.line(-10, 10, 10, -10)
    >>> my_canvas.show()
    """
    from openexp.canvas import Canvas
    return Canvas(experiment, auto_prepare=auto_prepare, **style_args)


def Keyboard(**resp_args):
    r"""A factory function that creates a new `Keyboard` object. For a
    description of possible keywords, see:

    - %link:manual/python/keyboard%

    Returns
    -------
    keyboard
        A `Keyboard` object.

    Examples
    --------
    >>> my_keyboard = Keyboard(keylist=[u'a', u'b'], timeout=5000)
    >>> key, time = my_keyboard.get_key()
    """
    from openexp.keyboard import Keyboard
    return Keyboard(experiment, **resp_args)


def Mouse(**resp_args):
    r"""A factory function that creates a new `Mouse` object. For a
    description
    of possible keywords, see:

    - %link:manual/python/mouse%

    Returns
    -------
    mouse
        A `mouse` object.

    Examples
    --------
    >>> my_mouse = Mouse(keylist=[1,3], timeout=5000)
    >>> button, time = my_mouse.get_button()
    """
    from openexp.mouse import Mouse
    return Mouse(experiment, **resp_args)


def Sampler(src, **playback_args):
    r"""A factory function that creates a new `Sampler` object. For a
    description of possible keywords, see:

    - %link:manual/python/sampler%

    Returns
    -------
    sampler
        A SAMPLER object.

    Examples
    --------
    >>> src = pool['bark.ogg']
    >>> my_sampler = Sampler(src, volume=.5, pan='left')
    >>> my_sampler.play()
    """
    from openexp.sampler import Sampler
    return Sampler(experiment, src, **playback_args)


# Miscellaneous API	functions


def Synth(osc="sine", freq=440, length=100, attack=0, decay=5):
    r"""A factory function that synthesizes a sound and returns it as a
    `Sampler` object.

    Parameters
    ----------
    osc : str, unicode, optional
        Oscillator, can be "sine", "saw", "square" or "white_noise".
    freq : str, unicode, int, float, optional
        Frequency, either an integer value (value in hertz) or a string ("A1",
        "eb2", etc.).
    length : int, float, optional
        The length of the sound in milliseconds.
    attack : int, float, optional
        The attack (fade-in) time in milliseconds.
    decay : int, float, optional
        The decay (fade-out) time in milliseconds.

    Returns
    -------
    sampler
        A SAMPLER object.

    Examples
    --------
    >>> my_sampler = Synth(freq=u'b2', length=500)
    """
    from openexp.synth import Synth
    return Synth(experiment, osc=osc, freq=freq, length=length, attack=attack,
                 decay=decay)


def copy_sketchpad(name):
    r"""Returns a copy of a `sketchpad`'s canvas.

    Parameters
    ----------
    name : str, unicode
        The name of the `sketchpad`.

    Returns
    -------
    canvas
        A copy of the `sketchpad`'s canvas.

    Examples
    --------
    >>> my_canvas = copy_sketchpad('my_sketchpad')
    >>> my_canvas.show()
    """
    c = Canvas()
    c.copy(experiment.items[name].canvas)
    return c


def reset_feedback():
    r"""Resets all feedback variables to their initial state.

    Examples
    --------
    >>> reset_feedback()
    """
    experiment.reset_feedback()


def set_subject_nr(nr):
    r"""Sets the subject number and parity (even/ odd). This function is called
    automatically when an experiment is started, so you only need to call it
    yourself if you overwrite the subject number that was specified when the
    experiment was launched.

    Parameters
    ----------
    nr : int
        The subject nr.

    Examples
    --------
    >>> set_subject_nr(1)
    >>> print('Subject nr = %d' % var.subject_nr)
    >>> print('Subject parity = %s' % var.subject_parity)
    """
    experiment.set_subject(nr)


def sometimes(p=.5):
    r"""Returns True with a certain probability. (For more advanced
    randomization, use the Python `random` module.)

    Parameters
    ----------
    p : float, optional
        The probability of returning True.

    Returns
    -------
    bool
        True or False

    Examples
    --------
    >>> if sometimes():
    >>>         print('Sometimes you win')
    >>> else:
    >>>         print('Sometimes you loose')
    """
    if (not isinstance(p, float) and not isinstance(p, int)) or p < 0 or p > 1:
        raise ValueError(
            f'p should be a numeric value between 0 and 1, not {p}')
    return random.random() < p


def pause():
    r"""Pauses the experiment."""
    experiment.pause()


def register_cleanup_function(fnc):
    r"""Registers a clean-up function, which is executed when the experiment
    ends. Clean-up functions are executed at the very end, after the display,
    sound device, and log file have been closed. Clean-up functions are also
    executed when the experiment crashes.

    Examples
    --------
    >>> def my_cleanup_function():
    >>>         print(u'The experiment is finished!')
    >>> register_cleanup_function(my_cleanup_function)
    """
    experiment.cleanup_functions.append(fnc)


def xy_from_polar(rho, phi, pole=(0, 0)):
    r"""Converts polar coordinates (distance, angle) to Cartesian coordinates
    (x, y).

    Parameters
    ----------
    rho : float
        The radial coordinate, also distance or eccentricity.
    phi : float
        The angular coordinate. This reflects a clockwise rotation in degrees
        (i.e. not radians), where 0 is straight right.
    pole : tuple, optional
        The refence point.

    Returns
    -------
    tuple
        An (x, y) coordinate tuple.

    Examples
    --------
    >>> # Draw a cross
    >>> x1, y1 = xy_from_polar(100, 45)
    >>> x2, y2 = xy_from_polar(100, -45)
    >>> c = Canvas()
    >>> c.line(x1, y1, -x1, -y1)
    >>> c.line(x2, y2, -x2, -y2)
    >>> c.show()
    """
    try:
        rho = float(rho)
    except:
        raise TypeError('rho should be numeric in xy_from_polar()')
    try:
        phi = float(phi)
    except:
        raise TypeError('phi should be numeric in xy_from_polar()')
    phi = math.radians(phi)
    ox, oy = parse_pole(pole)
    x = rho * math.cos(phi) + ox
    y = rho * math.sin(phi) + oy
    return x, y


def xy_to_polar(x, y, pole=(0, 0)):
    r"""Converts Cartesian coordinates (x, y) to polar coordinates (distance,
    angle).

    Parameters
    ----------
    x : float
        The X coordinate.
    y : float
        The Y coordinate.
    pole : tuple, optional
        The refence point.

    Returns
    -------
    tuple
        An (rho, phi) coordinate tuple. Here, `rho` is the radial coordinate,
        also distance or eccentricity. `phi` is the angular coordinate in
        degrees (i.e. not radians), and reflects a counterclockwise rotation,
        where 0 is straight right.

    Examples
    --------
    >>> rho, phi = xy_to_polar(100, 100)
    """
    try:
        x = float(x)
    except:
        raise TypeError('x should be numeric in xy_to_polar()')
    try:
        y = float(y)
    except:
        raise TypeError('y should be numeric in xy_to_polar()')
    ox, oy = parse_pole(pole)
    dx = x-ox
    dy = y-oy
    rho = math.sqrt(dx**2 + dy**2)
    phi = math.degrees(math.atan2(dy, dx))
    return rho, phi


def xy_distance(x1, y1, x2, y2):
    r"""Gives the distance between two points.

    Parameters
    ----------
    x1 : float
        The x coordinate of the first point.
    y1 : float
        The y coordinate of the first point.
    x2 : float
        The x coordinate of the second point.
    y2 : float
        The y coordinate of the second point.

    Returns
    -------
    float
        The distance between the two points.
    """
    try:
        x1 = float(x1)
        y1 = float(y1)
        x2 = float(x2)
        y2 = float(y2)
    except:
        raise TypeError('Coordinates should be numeric in xy_distance()')
    return math.sqrt((x1-x2)**2+(y1-y2)**2)


def xy_circle(n, rho, phi0=0, pole=(0, 0)):
    r"""Generates a list of points (x,y coordinates) in a circle. This can be
    used to draw stimuli in a circular arrangement.

    Parameters
    ----------
    n : int
        The number of x,y coordinates to generate.
    rho : float
        The radial coordinate, also distance or eccentricity, of the first
        point.
    phi0 : float, optional
        The angular coordinate for the first coordinate. This is a
        counterclockwise rotation in degrees (i.e. not radians), where 0 is
        straight right.
    pole : tuple, optional
        The refence point.

    Returns
    -------
    list
        A list of (x,y) coordinate tuples.

    Examples
    --------
    >>> # Draw 8 rectangles around a central fixation dot
    >>> c = Canvas()
    >>> c.fixdot()
    >>> for x, y in xy_circle(8, 100):
    >>>         c.rect(x-10, y-10, 20, 20)
    >>> c.show()
    """
    try:
        n = int(n)
        if n < 0:
            raise ValueError()
    except (ValueError, TypeError):
        raise ValueError('n should be a non-negative integer in xy_circle()')
    try:
        phi0 = float(phi0)
    except (ValueError, TypeError):
        raise TypeError('phi0 should be numeric in xy_circle()')
    l = []
    for i in range(n):
        l.append(xy_from_polar(rho, phi0, pole=pole))
        phi0 += 360./n
    return l


def xy_grid(n, spacing, pole=(0, 0)):
    r"""Generates a list of points (x,y coordinates) in a grid. This can be
    used to draw stimuli in a grid arrangement.

    Parameters
    ----------
    n : int, tuple
        An `int` that indicates the number of columns and rows, so that `n=2`
        indicates a 2x2 grid, or a (n_col, n_row) `tuple`, so that `n=(2,3)`
        indicates a 2x3 grid.
    spacing : float
        A numeric value that indicates the spacing between cells, or a
        (col_spacing, row_spacing) tuple.
    pole : tuple, optional
        The refence point.

    Returns
    -------
    list
        A list of (x,y) coordinate tuples.

    Examples
    --------
    >>> # Draw a 4x4 grid of rectangles
    >>> c = Canvas()
    >>> c.fixdot()
    >>> for x, y in xy_grid(4, 100):
    >>>         c.rect(x-10, y-10, 20, 20)
    >>> c.show()
    """
    try:
        n_col, n_row = n
    except:
        n_col = n_row = n
    try:
        n_col = int(n_col)
        n_row = int(n_row)
        assert(n_col >= 0)
        assert(n_row >= 0)
    except:
        raise ValueError('n should be a non-negative integer or a tuple of '
                         'two non-negative integers in xy_grid()')
    try:
        s_col, s_row = spacing
    except:
        s_col = s_row = spacing
    try:
        s_col = float(s_col)
        s_row = float(s_row)
        assert(s_col >= 0)
        assert(s_row >= 0)
    except:
        raise ValueError('spacing should be a non-negative numeric or a '
                         'tuple of two non-negative numerics in xy_grid()')
    pole = parse_pole(pole)
    l = []
    for row in range(n_row):
        y = (row - (n_row-1) / 2.) * s_row + pole[1]
        for col in range(n_col):
            x = (col - (n_col-1) / 2.) * s_col + pole[0]
            l.append((x, y))
    return l


def xy_random(n, width, height, min_dist=0, pole=(0, 0)):
    r"""Generates a list of random points (x,y coordinates) with a minimum
    spacing between each pair of points. This function will raise an
    Exception when the coordinate list cannot be generated,  typically because
    there are too many points, the min_dist is set too high, or the width or
    height are set too low.

    Parameters
    ----------
    n : int
        The number of points to generate.
    width : float
        The width of the field with random points.
    height : float
        The height of the field with random points.
    min_dist : float, optional
        The minimum distance between each point.
    pole : tuple, optional
        The refence point.

    Returns
    -------
    list
        A list of (x,y) coordinate tuples.

    Examples
    --------
    >>> # Draw a 50 rectangles in a random grid
    >>> c = Canvas()
    >>> c.fixdot()
    >>> for x, y in xy_random(50, 500, 500, min_dist=40):
    >>>         c.rect(x-10, y-10, 20, 20)
    >>> c.show()
    """
    try:
        n = int(n)
        if n < 0:
            raise ValueError()
    except (ValueError, TypeError):
        raise ValueError('n should be a non-negative integer in xy_circle()')
    try:
        width = float(width)
    except:
        raise TypeError('width should be numeric in xy_random()')
    try:
        height = float(height)
    except:
        raise TypeError('height should be numeric in xy_random()')
    try:
        min_dist = float(min_dist)
    except:
        raise TypeError('min_dist should be numeric in xy_random()')
    pole = parse_pole(pole)
    max_try = 1000
    for t1 in range(max_try):
        l = []
        for i in range(n):
            for t2 in range(max_try):
                x1 = (random.random()-.5)*width + pole[0]
                y1 = (random.random()-.5)*height + pole[1]
                for x2, y2 in l:
                    if xy_distance(x1, y1, x2, y2) < min_dist:
                        break
                else:
                    # Point does not collide, so add to the list
                    l.append((x1, y1))
                    break
            else:
                # All level-2 tries have failed, so break to start a new level-1
                # try.
                break
        else:
            # All points have been successfully added, so return the list
            return l
    # All level-1 tries have failed
    raise RuntimeError('Failed to generate random coordinates in xy_random()')


# Helper functions that are not part of the public API


def parse_pole(pole):
    """
    visible: False
    """
    try:
        ox = float(pole[0])
        oy = float(pole[1])
        assert(len(pole) == 2)
    except:
        raise ValueError('pole should be a tuple (or similar) of length '
                         'with two numeric values')
    return ox, oy


def set_aliases():
    """
    visible: False
    """
    # Non PEP-8 alias for backwards compatibility
    global canvas, sampler, synth, keyboard, mouse
    canvas = Canvas
    sampler = Sampler
    synth = Synth
    keyboard = Keyboard
    mouse = Mouse

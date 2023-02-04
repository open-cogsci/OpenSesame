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
import re
import webcolors
import colorsys
import numbers
from libopensesame.exceptions import osexception

RGB_HEX6 = r'#(?P<r>[0-9a-fA-F]{2})(?P<g>[0-9a-fA-F]{2})(?P<b>[0-9a-fA-F]{2})$'
RGB_HEX3 = r'#(?P<r>[0-9a-fA-F])(?P<g>[0-9a-fA-F])(?P<b>[0-9a-fA-F])$'
RGB_255 = r'rgb\(\s*(?P<r>\d+)\s*,\s*(?P<g>\d+)\s*,\s*(?P<b>\d+)\s*\)\s*$'
RGB_PERC = r'rgb\(\s*(?P<r>[+-]?(\d+(\.\d*)?|\.\d+)([eE][+-]?\d+)?)%\s*,\s*(?P<g>[+-]?(\d+(\.\d*)?|\.\d+)([eE][+-]?\d+)?)%\s*,\s*(?P<b>[+-]?(\d+(\.\d*)?|\.\d+)([eE][+-]?\d+)?)%\s*\)\s*$'
HSL = r'hsl\(\s*(?P<h>[+-]?(\d+(\.\d*)?|\.\d+)([eE][+-]?\d+)?)\s*,\s*(?P<s>[+-]?(\d+(\.\d*)?|\.\d+)([eE][+-]?\d+)?)%\s*,\s*(?P<l>[+-]?(\d+(\.\d*)?|\.\d+)([eE][+-]?\d+)?)%\s*\)\s*$'
HSV = r'hsv\(\s*(?P<h>[+-]?(\d+(\.\d*)?|\.\d+)([eE][+-]?\d+)?)\s*,\s*(?P<s>[+-]?(\d+(\.\d*)?|\.\d+)([eE][+-]?\d+)?)%\s*,\s*(?P<v>[+-]?(\d+(\.\d*)?|\.\d+)([eE][+-]?\d+)?)%\s*\)\s*$'
LAB = r'lab\(\s*(?P<l>[+-]?(\d+(\.\d*)?|\.\d+)([eE][+-]?\d+)?)\s*,\s*(?P<a>[+-]?(\d+(\.\d*)?|\.\d+)([eE][+-]?\d+)?)\s*,\s*(?P<b>[+-]?(\d+(\.\d*)?|\.\d+)([eE][+-]?\d+)?)\s*\)\s*$'


def _is_rgb(colorspec):

    return (
        hasattr(colorspec, '__len__')
        and len(colorspec) == 3
        and all(
            isinstance(i, numbers.Integral)
            and 0 <= i <= 255
            for i in colorspec
        )
    )


def _raise_invalid(colorspec):

    raise osexception(
        u'Invalid color specification: {}'.format(safe_decode(colorspec))
    )


class Color(object):

    """
    desc:
            Converts various color specifications to a back-end specific format.
            Valid color specificatons are described in more detail in
            openexp._canvas.canvas.canvas.
    """

    def __init__(self, experiment, colorspec):
        """
        desc:
                Constructor.

        arguments:
                experiment:
                        desc:	The experiment object.
                        type:	experiment
                colorspec:
                        desc:	A color specification.
                        type:	[str, unicode, tuple, int]
        """

        self.experiment = experiment
        self.colorspec = colorspec
        self.hexcolor = self.to_hex(self.colorspec)
        self.backend_color = self.to_backend_color(self.hexcolor)

    def __repr__(self):
        """
        returns:
                A representation of the color, which matches the color
                specification.
        """

        return self.colorspec

    @staticmethod
    def to_hex(colorspec):
        """
        desc:
                Converts a color specificaton to a seven-character lowercase
                hexadecimal color string, such as '#ff0000'.

        arguments:
                colorspec:
                        desc:	A color specification.
                        type:	[str, unicode, array-like, int]

        returns:
                desc:	A hexadecimal color specification.
                type:	unicode
        """

        if isinstance(colorspec, int):  # 0-255 luminance value
            return webcolors.rgb_to_hex((colorspec, colorspec, colorspec))
        if _is_rgb(colorspec):
            return webcolors.rgb_to_hex(colorspec)
        if not isinstance(colorspec, basestring):
            _raise_invalid(colorspec)
        try:  # 0-255 luminance value passed as string
            colorspec = int(colorspec)
        except ValueError:
            pass
        else:
            return webcolors.rgb_to_hex((colorspec, colorspec, colorspec))
        try:
            return webcolors.name_to_hex(colorspec)
        except ValueError:
            pass
        m = re.match(RGB_HEX6, colorspec)
        if m:
            return colorspec.lower()
        m = re.match(RGB_HEX3, colorspec)
        if m:
            return webcolors.rgb_to_hex((
                int(m.group('r') * 2, base=16),
                int(m.group('g') * 2, base=16),
                int(m.group('b') * 2, base=16)
            ))
        m = re.match(RGB_255, colorspec)
        if m:
            return webcolors.rgb_to_hex(
                (int(m.group('r')), int(m.group('g')), int(m.group('b')))
            )
        m = re.match(RGB_PERC, colorspec)
        if m:
            return webcolors.rgb_percent_to_hex(
                (m.group('r'), m.group('g'), m.group('b'))
            )
        m = re.match(HSL, colorspec)
        if m:
            # RGB values between 0 and 1
            r, g, b = colorsys.hls_to_rgb(
                float(m.group('h')) / 360,
                float(m.group('l')) / 100,
                float(m.group('s')) / 100
            )
            return webcolors.rgb_to_hex(
                (int(r * 255), int(g * 255), int(b * 255))
            )
        m = re.match(HSV, colorspec)
        if m:
            # RGB values between 0 and 1
            r, g, b = colorsys.hsv_to_rgb(
                float(m.group('h')) / 360,
                float(m.group('s')) / 100,
                float(m.group('v')) / 100
            )
            return webcolors.rgb_to_hex(
                (int(r * 255), int(g * 255), int(b * 255))
            )
        m = re.match(LAB, colorspec)
        if m:
            try:
                from psychopy.tools import colorspacetools as cst
            except ImportError:
                raise osexception(u'CIE L*a*b* color space requires PsychoPy')
            # RGB values are between -1 and 1
            r, g, b = cst.cielab2rgb(
                (
                    float(m.group('l')),
                    float(m.group('a')),
                    float(m.group('b'))
                ),
                transferFunc=cst.srgbTF
            )
            return webcolors.rgb_to_hex((
                int((r + 1) * 127.5),
                int((g + 1) * 127.5),
                int((b + 1) * 127.5),
            ))
        _raise_invalid(colorspec)

    def to_backend_color(self, hexcolor):
        """
        desc:
                Converts a hexadecimal color string to a backend-specific color
                object.

        arguments:
                hexcolor:
                        desc:	A hexadecimal color specification.
                        type:	[str, unicode]

        returns:
                A backend-specific color object.
        """

        return hexcolor


# Non PEP-8 alias for backwards compatibility
color = Color

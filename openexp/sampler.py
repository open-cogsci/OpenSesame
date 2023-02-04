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
from openexp import backend


def Sampler(experiment, *arglist, **kwdict):
    """
    desc:
            A factory that returns a back-end specific sampler object.

    arguments:
            experiment:
                    desc:	The experiment object.
                    type:	experiment

    argument-list:
            arglist:	See sampler.__init__().

    keyword-dict:
            kwdict:		See sampler.__init__().
    """

    cls = backend.get_backend_class(experiment, u'sampler')
    return cls(experiment, *arglist, **kwdict)


def init_sound(experiment):
    """
    desc:
            Calls the back-end specific init_sound function.

    arguments:
            experiment:		The experiment object.
            type:			experiment
    """

    cls = backend.get_backend_class(experiment, u'sampler')
    cls.init_sound(experiment)


def close_sound(experiment):
    """
    desc:
            Calls the back-end specific close_sound function.

    arguments:
            experiment:		The experiment object.
            type:			experiment
    """

    cls = backend.get_backend_class(experiment, u'sampler')
    cls.close_sound(experiment)


# Non PEP-8 alias for backwards compatibility
sampler = Sampler

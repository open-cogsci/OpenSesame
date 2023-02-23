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
from libopensesame.exceptions import BackendNotSupported
from libopensesame.misc import camel_case
from importlib import import_module
from . import _libjoystick


def LibJoystick(experiment, **kwargs):
    r"""A factory that returns a back-end specific joystick module.

    Parameters
    ----------
    experiment
        The experiment object.
    **kwargs : dict
        Keyords to be passed on the joystick init.
    """
    if experiment.var.canvas_backend == u'psycho':
        raise BackendNotSupported(
            'The joystick plug-in does not yet support the psycho back-end')
    backend = u'legacy'
    mod = import_module(f'{_libjoystick.__package__}.{backend}')
    cls = getattr(mod, camel_case(backend))
    return cls(experiment, **kwargs)

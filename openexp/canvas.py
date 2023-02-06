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
from libopensesame.oslogging import oslogger
import tempfile
import os

# A list of temporary files that should be cleaned up.
temp_files = []


def Canvas(experiment, *arglist, **kwdict):
    r"""A factory that returns a back-end specific canvas object.

    Parameters
    ----------
    experiment : experiment
        The experiment object.
    *arglist : list
        See canvas.__init__().
    **kwdict : dict
        See canvas.__init__().
    """
    cls = backend.get_backend_class(experiment, u'canvas')
    return cls(experiment, *arglist, **kwdict)


def init_display(experiment):
    r"""Calls the back-end specific init_display function.

    Parameters
    ----------
    experiment
        The experiment object.
    type
        experiment
    """
    cls = backend.get_backend_class(experiment, u'canvas')
    cls.init_display(experiment)


def close_display(experiment):
    r"""Calls the back-end specific close_display function.

    Parameters
    ----------
    experiment
        The experiment object.
    type
        experiment
    """
    cls = backend.get_backend_class(experiment, u'canvas')
    cls.close_display(experiment)


def clean_up(verbose=False):
    r"""Cleans up temporary pool folders.

    Parameters
    ----------
    verbose : bool, optional
        Indicates if debugging output should be provided.
    """
    global temp_files
    if verbose:
        oslogger.debug(u"cleaning up temporary pool folders")
    for path in temp_files:
        if verbose:
            oslogger.debug(u"removing '%s'" % path)
        try:
            os.remove(path)
        except Exception as e:
            if verbose:
                oslogger.error(u"failed to remove '%s': %s" % (path, e))


def gabor_file(*arglist, **kwdict):
    r"""Creates a temporary file containing a Gabor patch.

    Parameters
    ----------
    *arglist : list
        See canvas.gabor() for a description of arguments.
    **kwdict : dict
        See canvas.gabor() for a description of keywords.


    Returns
    -------
    A path to the image file.
    """
    from openexp._canvas import canvas as _canvas
    fd, fname = tempfile.mkstemp(suffix=u'.png')
    temp_files.append(fname)
    im = _canvas._gabor(*arglist, **kwdict)
    im.save(fname)
    os.close(fd)
    return fname


def noise_file(*arglist, **kwdict):
    r"""Creates a temporary file containing a noise patch.

    Parameters
    ----------
    *arglist : list
        See canvas.noise_path() for a description of arguments.
    **kwdict : dict
        See canvas.noise_path() for a description of keywords.


    Returns
    -------
    A path to the image file.
    """
    from openexp._canvas import canvas as _canvas
    fd, fname = tempfile.mkstemp(suffix=u'.png')
    temp_files.append(fname)
    im = _canvas._noise_patch(*arglist, **kwdict)
    im.save(fname)
    os.close(fd)
    return fname


# Non PEP-8 alias for backwards compatibility
canvas = Canvas

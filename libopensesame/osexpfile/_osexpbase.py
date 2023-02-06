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


class OSExpBase:

    def __init__(self, exp):

        self._format = None
        self._exp = exp

    @staticmethod
    def valid_extension(path):
        """
        desc:
                Checks whether a path ends with one of the known extensions for an
                experiment file.

        arguments:
                path:	The path to check.

        returns:
                type:	bool
        """

        return any(
            path.lower().endswith(ext) for ext in [
                u'.opensesame',
                u'.opensesame.tar.gz',
                u'.osexp'
            ]
        )

    @property
    def format(self):
        """
        desc:
                The format of the experiment, which can be:

                - script: a script (ie. not from file)
                - scriptfile: plain-text file
                - targz: targz archive
                - tar: tar archive
        """

        if self._format is None:
            self._format = self._determine_format()
        return self._format

    @property
    def experiment_path(self):
        """
        desc:
                The path to the experiment file, or None if the experiment was
                loaded from script.
        """

        return self._experiment_path

    @property
    def script(self):
        """
        desc:
                The experiment script.
        """

        raise NotImplementedError()

    def _determine_format(self):

        raise NotImplementedError()

    @property
    def _syntax(self):
        """
        visible: False

        desc:
                A shortcut to the experiment syntax object.
        """

        return self._exp._syntax

    @property
    def _pool(self):
        """
        visible: False

        desc:
                A shortcut to the experiment pool object.
        """

        return self._exp.pool

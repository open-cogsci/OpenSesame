# coding-utf-8

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
import sys
import logging
import logging.handlers


MAXBYTES = 10 * 1024 ** 2
BACKUPCOUNT = 1


class OSLogger(object):

    def __init__(self, name=u'default'):

        self._name = name
        self._formatter = logging.Formatter(
            u'[%(asctime)s:%(levelname)s:%(name)s] %(message)s'
        )
        self._logger = logging.getLogger(name)
        self._logger.propagate = False
        self.add_handler(self.StreamHandler(sys.stdout))
        if self.debug_mode:
            self._logger.setLevel(logging.DEBUG)
            self.add_handler(self.RotatingFileHandler())
        else:
            self._logger.setLevel(logging.INFO)

    def RotatingFileHandler(self, path=u'opensesame.log', level=logging.DEBUG):

        h = logging.handlers.RotatingFileHandler(
            path,
            maxBytes=MAXBYTES,
            backupCount=BACKUPCOUNT,
            encoding=u'utf-8'
        )
        h.setLevel(level)
        h.setFormatter(self._formatter)
        return h

    def StreamHandler(self, stream, level=logging.INFO):

        h = logging.StreamHandler(stream=stream)
        h.setLevel(level)
        h.setFormatter(self._formatter)
        return h

    @property
    def debug_mode(self):

        return '--debug' in sys.argv or '-d' in sys.argv

    def add_handler(self, handler):

        self._logger.addHandler(handler)

    def remove_handler(self, handler):

        self._logger.removeHandler(handler)

    @property
    def debug(self):

        return self._logger.debug

    @property
    def info(self):

        return self._logger.info

    @property
    def warning(self):

        return self._logger.warning

    @property
    def error(self):

        return self._logger.error

    @property
    def critical(self):

        return self._logger.critical

    @property
    def name(self):

        return self._logger.name

    @name.setter
    def name(self, name):

        self._logger.name = name


oslogger = OSLogger()

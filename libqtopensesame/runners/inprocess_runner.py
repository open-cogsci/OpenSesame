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
from libopensesame.oslogging import oslogger
from libopensesame.exceptions import osexception
from libqtopensesame.runners import BaseRunner


class InprocessRunner(BaseRunner):

    """Runs an experiment in the traditional way, in the same process."""
    def execute(self):
        """See base_runner.execute()."""
        # Exceptions during the run phase are important and returned so that the
        # user is notified.
        retval = None
        try:
            self.experiment.run()
        except Exception as e:
            if not isinstance(e, osexception):
                retval = osexception(u'Unexpected error', e)
            else:
                retval = e
        # Exceptions during the end phase are less important and only printed
        # to the debug window.
        try:
            self.experiment.end()
        except Exception as _e:
            oslogger.error(u'exception during experiment.end(): %s' % _e)
        return retval

    def workspace_globals(self):
        """See base_runner."""
        if not hasattr(self, u'experiment'):
            return {}
        return self.experiment.python_workspace._globals

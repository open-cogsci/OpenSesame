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
import time
import os
import json
from libopensesame.py3compat import *
from libopensesame.exceptions import osexception
from libqtopensesame.extensions import BaseExtension
from libopensesame import misc
from libqtopensesame.misc.translate import translation_context
_ = translation_context(u'after_experiment', category=u'extension')


class AfterExperiment(BaseExtension):

    def event_end_experiment(self, ret_val):
        r"""Handles the end of an experiment.

        Parameters
        ----------
        ret_val : Exception, NoneType
            An Exception, or None if no exception occurred.
        """
        if ret_val is None:
            self.handle_success()
        else:
            self.handle_exception(ret_val)

    @property
    def _logfile(self):
        """Returns the path to the logfile of the last run, or None if this
        could not be determined.
        """
        # Depending on the runner, the logfile is either a property of the
        # var object ...
        var = self.extension_manager.provide(
            'jupyter_workspace_variable',
            name='var'
        )
        try:
            if var and 'logfile' in var:
                return var.logfile
        except TypeError:
            # JupyterConsole returns a custom FailedToGetWorkspaceVariable
            # Exception when an error occurs. This is not iterable and results
            # in a TypeError.
            pass
        # ... or it is a global variable in the workspace
        logfile = self.extension_manager.provide(
            'jupyter_workspace_variable',
            name='logfile'
        )
        if logfile:
            return logfile

    @property
    def _extra_data_files(self):
        """Returns list of extra data files, such as eye-tracking data."""
        data_files = self.extension_manager.provide(
            'jupyter_workspace_variable',
            name='data_files'
        )
        if not data_files:
            return
        try:
            return [path for path in data_files if path != self._logfile]
        except TypeError:
            # JupyterConsole returns a custom FailedToGetWorkspaceVariable
            # Exception when an error occurs. This is not iterable and results
            # in a TypeError.
            pass

    def event_after_experiment_copy_logfile(self):
        r"""Copies the logfile to the file pool."""
        if self._logfile is None:
            return
        self.main_window.ui.pool_widget.add([self._logfile],
                                            rename=True)

    def event_after_experiment_open_logfile_folder(self):
        r"""Opens the logfile folder."""
        if self._logfile is None:
            return
        misc.open_url(os.path.dirname(self._logfile))

    def event_after_experiment_open_logfile(self):
        r"""Opens the logfile."""
        if self._logfile is None:
            return
        misc.open_url(self._logfile)

    def handle_success(self):
        r"""Shows a summary after successful completion of the experiment."""
        logfile = self._logfile
        if logfile is None:
            logfile = u'Unknown logfile'
        md = safe_read(self.ext_resource(u'finished.md')) % {
            u'time': time.ctime(),
            u'logfile': logfile
        }
        if self._extra_data_files:
            md += u'\n' \
                + _(u'The following extra data files where created:') + u'\n\n'
            for data_file in self._extra_data_files:
                md += u'- `' + data_file + u'`\n'
            md += u'\n'
        self.tabwidget.open_markdown(
            md, u'os-finished-success', _(u'Finished'))

    def handle_exception(self, e):
        r"""Shows a summary when the experiment was aborted.

        Parameters
        ----------
        e : Exception
            The Exception that caused the experiment to stop.
        """
        if not isinstance(e, osexception):
            e = osexception(msg=u'Unexpected error', exception=e)
        if e.user_triggered:
            icon = u'os-finished-user-interrupt'
            title = _(u'Aborted')
            md = _(u'# Aborted\n\n- ') + e.markdown()
        else:
            icon = u'os-finished-error'
            title = _(u'Stopped')
            md = _(u'# Stopped\n\nThe experiment did not finish normally for the following reason:\n\n- ') \
                + e.markdown()
        self.console.write(e)
        self.tabwidget.open_markdown(md, icon, title)

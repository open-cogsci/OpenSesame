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
from libopensesame import metadata
from libqtopensesame.extensions import base_extension
from libqtopensesame.misc.config import cfg
from libqtopensesame.misc.translate import translation_context
_ = translation_context(u'opensesame_3_notifications', category=u'extension')


class opensesame_3_notifications(base_extension):

    r"""Provides tips for new users of OpenSesame 3."""
    def event_os3n_dismiss_old_experiment(self):
        r"""Permanently disables the old-experiment tab."""
        cfg.os3n_old_experiment_notification = False
        self.main_window.tabwidget.close_current()

    def event_open_experiment(self, path):
        r"""Opens a notification tab when opening an experiment that was
        created with an older version of OpenSesame.

        Parameters
        ----------
        path : unicode
            The full path of the experiment file.
        """
        exp_api = self.experiment.front_matter[u'API']
        # If the major API of the experiment is the same, and the minor API is
        # the same or older
        if exp_api.version[0] == metadata.api.version[0] and \
                exp_api.version[1] <= metadata.api.version[1]:
            return
        self.main_window.current_path = None
        self.main_window.window_message(u'New experiment')
        self.main_window.set_unsaved(True)
        if not cfg.os3n_old_experiment_notification:
            return
        src = u'old-experiment.md' if exp_api < metadata.api \
            else u'new-experiment.md'
        self.tabwidget.open_markdown(self.ext_resource(src))

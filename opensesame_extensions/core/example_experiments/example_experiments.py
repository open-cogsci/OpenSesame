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
import os
from libqtopensesame.extensions import BaseExtension
from libopensesame.experiment import Experiment


class ExampleExperiments(BaseExtension):

    def event_startup(self):
        self.initialized = False

    def add_experiment(self, path):
        r"""Processes one experiment.

        Parameters
        ----------
        path : str
            The experiment folder name.
        """
        src = os.path.join(self.example_folder, path, u'experiment.osexp')
        if not os.path.exists(src):
            return
        try:
            e = Experiment(u'dummy', src, experiment_path=os.path.dirname(src))
        except Exception as e:
            oslogger.warning(f'failed to load experiment: {e}')
            return
        d = e.front_matter
        # We need to use forward slashes, also on Windows, otherwise it leads
        # to an invalid URL when prefixed with opensesame://
        d[u'src'] = src.replace(u'\\', u'/')
        if u'Title' not in d:
            d[u'Title'] = u'No title'
        if u'Description' not in d:
            d[u'Description'] = u'No description'
        self.experiments.append(d)

    def initialize(self):
        r"""Initializes the plug-in by building a Markdown page with examples.
        """
        self.set_busy()
        self.example_folder = os.path.join(self.extension_folder, 'examples')
        self.experiments = []
        for path in sorted(os.listdir(self.example_folder)):
            self.add_experiment(path)
        self.generate_markdown()
        self.set_busy(False)

    def generate_markdown(self):
        r"""Generates a Markdown string of all experiment info."""
        self.md = u'# Example experiments\n\n'
        for d in self.experiments:
            self.md += (
                u'[%(Title)s](opensesame://%(src)s)  \n'
                u'*%(Description)s*  \n'
            ) % d
            if u'Citation' in d:
                self.md += u'\n* <small>%s</small>\n' % d[u'Citation']
            self.md += u'\n<hr />\n'

    def activate(self):
        r"""Shows the list of example experiments."""
        if not self.initialized:
            self.initialize()
        self.tabwidget.open_markdown(self.md, icon=u'help-contents',
                                     title=u'Example experiments')

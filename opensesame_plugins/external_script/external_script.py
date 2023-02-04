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
from libopensesame.exceptions import osexception
from libopensesame.item import item
from libqtopensesame.items.qtautoplugin import qtautoplugin
import imp


class external_script(item):

    description = \
        u"Run Python code directly from a script file"

    def reset(self):
        """
        desc:
                Resets plug-in to initial state.
        """

        self.module = None
        self.var.file = u''
        self.var.prepare_func = u'prepare'
        self.var.run_func = u'run'

    def prepare(self):
        """
        desc:
                Prepares the item.
        """

        item.prepare(self)
        if self.module is None:
            path = self.experiment.pool[self.var.file]
            self.experiment.python_workspace.run_file(path)
        self.prepare_bytecode = self.experiment.python_workspace._compile(
            u'%s()' % self.var.prepare_func)
        self.run_bytecode = self.experiment.python_workspace._compile(
            u'%s()' % self.var.run_func)
        self.experiment.python_workspace._exec(self.prepare_bytecode)

    def run(self):
        """
        desc:
                Runs the item.
        """

        self.set_item_onset()
        self.experiment.python_workspace._exec(self.run_bytecode)


class qtexternal_script(external_script, qtautoplugin):

    def __init__(self, name, experiment, script=None):

        # Call parent constructors.
        external_script.__init__(self, name, experiment, script)
        qtautoplugin.__init__(self, __file__)

#!/usr/bin/env python
#-*- coding:utf-8 -*-

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
import unittest
import os
from libopensesame.experiment import experiment

class check_headless(unittest.TestCase):

    """
    desc:
        Runs several experiments in headless mode (i.e. on a virtual X server)
        to see if they execute correctly.
    """
    def runTest(self):

        """
        desc:
            Walks through the test.
        """
        from qtpy.QtWidgets import QApplication
        app = QApplication([])
        experiment_path = os.path.join(os.path.dirname(__file__), u'data')
        for experiment_file in [
                u'sketchpad_test.osexp',
                u'response_test.osexp',
                u'loop_test.osexp'
            ]:
            print(u'Testing %s' % experiment_file)
            for backend in (u'legacy',):
                e = experiment(
                    logfile=u'/tmp/tmp.csv',
                    experiment_path=experiment_path,
                    string=os.path.join(experiment_path, experiment_file)
                )
                e.var.canvas_backend = backend
                e.run()

if __name__ == '__main__':
    unittest.main()

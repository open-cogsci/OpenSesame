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
from config.utils import DATA_PATH

# The experiments are executed fully offscreen, so that no windows are opened
# while the tests are running, and no real display is required. The legacy
# canvas backend is based on pygame, which renders through SDL; the dummy SDL
# driver emulates a display without opening a window. The Qt platform is set
# to offscreen, because a Qt application is created as well.
os.environ.setdefault('SDL_VIDEODRIVER', 'dummy')
# The sampler and synth items play sound through SDL audio; the dummy audio
# driver emulates a sound device so no real audio hardware is required.
os.environ.setdefault('SDL_AUDIODRIVER', 'dummy')
os.environ.setdefault('QT_QPA_PLATFORM', 'offscreen')

class check_headless(unittest.TestCase):
    """Runs several experiments in headless mode (i.e. fully offscreen, so
    that no windows are opened on the display) to see if they execute
    correctly.
    """
    def runTest(self):
        experiment_path = DATA_PATH
        for experiment_file in ['sketchpad_test.osexp', 'response_test.osexp',
                                'loop_test.osexp', 'mouse_response_test.osexp',
                                'feedback_test.osexp', 'sampler_test.osexp']:
            print('Testing %s' % experiment_file)
            for backend in ('legacy',):
                e = experiment(
                    logfile='/tmp/tmp.csv',
                    experiment_path=experiment_path,
                    string=os.path.join(experiment_path, experiment_file)
                )
                e.var.canvas_backend = backend
                e.run()

if __name__ == '__main__':
    unittest.main()

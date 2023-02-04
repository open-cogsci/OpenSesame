#!/usr/bin/env python
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

import os
hiddenExts = '.pyc', '.pyo'


def updateHidden(folder):
    """
    Scans a folder and adds all files of a particular type to the .hidden file,
    to avoid a cluttered view in Nautilus

    Arguments:
    folder -- the folder to process
    """

    print('Scanning', folder)
    f = open(os.path.join(folder, '.hidden'), 'w')
    for fname in os.listdir(folder):
        if fname[0] == '.':
            continue
        path = os.path.join(folder, fname)
        if os.path.isdir(path):
            updateHidden(path)
        elif os.path.splitext(fname)[1] in hiddenExts:
            print('Hiding', fname)
            f.write(fname+'\n')
    f.close()


updateHidden('.')

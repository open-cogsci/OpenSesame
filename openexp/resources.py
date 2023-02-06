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
from pathlib import Path


class Resources:
    """A central object where resources (package data) can be stored."""
    
    def __init__(self):
        self._folders = [Path(__file__).parent / 'resources']
        self._resources = {}
    
    def add_resource_folder(self, path):
        self._folders.append(Path(path))
    
    def __getitem__(self, key):
        key = key
        if key in self._resources:
            return self._resources[key]
        for folder in self._folders:
            if (folder / key).exists():
                return str(folder / key)
        raise FileNotFoundError(f'failed to find resource {key}')
        
    def __setitem__(self, key, path):
        self._resources[key] = path


resources = Resources()

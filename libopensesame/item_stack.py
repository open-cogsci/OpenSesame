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


class ItemStack:
    """Keeps track of which item is currently active."""
    
    def __init__(self):
        self.clear()

    def clear(self):
        """Clears the stack."""
        self._stack = []

    def push(self, item, phase):
        """Adds a new item to the stack.

        Parameters
        ----------
        item : str
            The item to add.
        """
        self._stack.append((item, phase))

    def pop(self):
        """Pops the last item from the stack.

        Returns
        -------
        str
            The popped item.
        """
        return self._stack.pop()

    def __str__(self):

        return '.'.join(['%s[%s]' % i for i in self._stack])
        
    def __getitem__(self, key):
        return self._stack[key]


# Create a single instance of the stack
item_stack_singleton = ItemStack()

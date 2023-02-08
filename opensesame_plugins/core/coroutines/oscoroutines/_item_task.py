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
from ._base_task import BaseTask
from libopensesame.item_stack import item_stack_singleton


class ItemTask(BaseTask):

    r"""A task controls the coroutine for one item."""
    def __init__(self, coroutines, _item, start_time, end_time,
                 abort_on_end=False):
        r"""Constructor.

        Parameters
        ----------
        item : item
            An item object.
        """
        if not hasattr(_item, u'coroutine'):
            raise osexception(
                u'%s not supported by coroutines' % _item.item_type)
        self._item = _item
        super().__init__(coroutines, start_time, end_time, abort_on_end)
        self.coroutines.event(u'initialize %s' % _item.coroutine)

    def step(self):
        """See base_task."""
        item_stack_singleton.push(self._item.name, u'coroutines_step')
        retval = base_task.step(self)
        item_stack_singleton.pop()
        return retval

    def launch(self):
        """See base_task."""
        item_stack_singleton.push(self._item.name, u'coroutines_prepare')
        self._item.prepare()
        item_stack_singleton.pop()
        # New-style coroutines take a coroutines keyword, which is used to
        # communicate the coroutines item. Old-style coroutines do not.
        try:
            self.coroutine = self._item.coroutine(coroutines=self.coroutines)
        except TypeError:
            self.coroutine = self._item.coroutine()
        self.coroutines.event('launch %s' % self._item)
        item_stack_singleton.push(self._item.name, u'coroutines_launch')
        self.coroutine.send(None)
        item_stack_singleton.pop()

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
from libqtopensesame.misc import drag_and_drop
from libqtopensesame.misc.base_component import BaseComponent


class BaseDraggable:

    r"""A base class for components that support drag and drop."""
    def set_supported_drop_types(self, types=None):

        if not hasattr(self, u'setAcceptDrops'):
            raise TypeError(u'Object does not support drops')
        if types is None:
            self.setAcceptDrops(False)
            self.supported_drop_types = None
            return
        self.setAcceptDrops(True)
        self.supported_drop_types = types

    def dragEnterEvent(self, e):
        r"""Handles drag-enter events to see if they are supported

        Parameters
        ----------
        e : QDragEnterEvent
            A drag-enter event.
        """
        if not hasattr(self, u'supported_drop_types'):
            e.ignore()
            return
        data = drag_and_drop.receive(e)
        if drag_and_drop.matches(data, self.supported_drop_types):
            e.accept()
        else:
            e.ignore()

    def dropEvent(self, e):
        r"""Handles drop events and accepts them if supported.

        Parameters
        ----------
        e : QDropEvent
            A drop event.
        """
        if not hasattr(self, u'supported_drop_types'):
            e.ignore()
            return
        data = drag_and_drop.receive(e)
        if drag_and_drop.matches(data, self.supported_drop_types):
            e.accept()
            self.accept_drop(data)
        else:
            e.ignore()

    def accept_drop(self, data):
        r"""Is called after a supported drop type. Should be re-implemented.

        Parameters
        ----------
        data : dict
            The drop data.
        """
        pass


# Alias for backwards compatibility
base_draggable = BaseDraggable

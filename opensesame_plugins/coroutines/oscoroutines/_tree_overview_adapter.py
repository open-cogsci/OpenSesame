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
from libqtopensesame.widgets.tree_overview import tree_overview


class tree_overview_adapter(tree_overview):

    r"""Extends the tree overview so that it treats coroutines as sequences,
    and supports start and end times.
    """
    def __init__(self, coroutines, main_window, overview_mode=True):
        """See tree_overview."""
        self.coroutines = coroutines
        super(tree_overview_adapter, self).__init__(main_window,
                                                    overview_mode=overview_mode)

    def text_edited(self, treeitem, col):
        """See tree_overview."""
        # Renames and run-if edits are handled by the original tree overview,
        # which needs to be tricked into thinking that the coroutines item is
        # a sequence.
        if col in (0, 1):
            self.coroutines.item_type = u'sequence'
            super(tree_overview_adapter, self).text_edited(treeitem, col)
            self.coroutines.item_type = u'coroutines'
            return
        # Don't allow editing the times of the top-level coroutines
        if treeitem.parent() is None:
            self.itemChanged.disconnect()
            treeitem.setText(col, u'')
            self.itemChanged.connect(self.text_edited)
            return
        # Change the start/ end time
        parent_item_name, ancestry = treeitem.ancestry()
        parent_item_name, index = self.parent_from_ancestry(ancestry)
        _time = treeitem.text(col).strip()
        if _time == u'':
            _time = 0
        item_name, start_time, end_time, cond = self.coroutines.schedule[index]
        if col == 2:
            start_time = _time
        elif col == 3:
            # In the GUI one-shot coroutines are not associated with an
            # end time. In the runtime, their end time is equal to the start
            # time.
            if self.coroutines.is_oneshot_coroutine(item_name):
                _time = u''
                end_time = start_time
            else:
                end_time = _time
        else:
            raise TypeError(u'col should be in 0-3 range')
        self.coroutines.schedule[index] = item_name, start_time, end_time, cond
        self.itemChanged.disconnect()
        treeitem.setText(col, str(_time))
        self.itemChanged.connect(self.text_edited)
        self.text_change.emit()

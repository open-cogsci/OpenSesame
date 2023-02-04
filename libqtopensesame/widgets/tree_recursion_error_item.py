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
from libqtopensesame.widgets.tree_base_item import tree_base_item
from libqtopensesame.misc.translate import translation_context
_ = translation_context(u'tree_recursion_error_item', category=u'core')


class tree_recursion_error_item(tree_base_item):

    """
    desc:
            A placeholder item that is shown when there is a recursion in the
            experiment that prevents the item tree from being built.
    """

    def __init__(self, main_window):
        """
        desc:
                Constructor.

        arguments:
                main_window:
                        desc:	The main-window object.
                        type:	qtopensesame
        """

        super(tree_recursion_error_item, self).__init__()
        self.setup(main_window)
        self.setText(0, _(u'Recursion detected'))
        self.setIcon(0, self.theme.qicon(u'dialog-error'))
        self._droppable = False
        self._draggable = False
        self.name = u'__recursion_error__'

    def open_tab(self):

        self.main_window.tabwidget.open_general_script()

"""This file is part of OpenSesame.

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
from qtpy.QtWidgets import QStyledItemDelegate, QLineEdit
from qtpy.QtGui import QFocusEvent
from qtpy.QtCore import Qt, QRect


# Indicates how far the editor should be shifted to the right to make sure it
# doesn't overlap the icon
ICON_MARGIN = 22


class ItemNameEditor(QLineEdit):
    """A custom editor for item names that checks whether the item name ends
    with a '_[item_type]' suffix, and if so, ignores this suffix when selecting
    the text. This encourages users to leave this suffix untouched, thus
    resulting in more meaningful item names.
    """
    def focusInEvent(self, event):
        super().focusInEvent(event)
        item_name = self.text()
        items = self.parent().experiment.items
        # When used in the context of the general properties widget, there is
        # actually no item name, but rather the name of the experiment
        if item_name not in items:
            return
        item_type = self.parent().experiment.items[item_name].item_type
        item_suffix = f'_{item_type}'
        if item_name.endswith(item_suffix):
            self.setSelection(0, len(item_name) - len(item_suffix))


class ItemNameDelegate(QStyledItemDelegate):
    """A delegate that makes uses the custom ItemNameEditor for editing item
    names. The geometry update is required to make sure that the custom 
    editor appears at the correct location, taking into account both the header
    (if present) and the icon.
    """
    def createEditor(self, parent, option, index):
        editor = ItemNameEditor(self.parent())
        text = index.data()
        editor.setText(text)
        return editor

    def updateEditorGeometry(self, editor, option, index):
        r = QRect(option.rect)
        header_height = editor.parent().header().height()
        r.moveTop(r.top() + header_height)
        r.moveLeft(r.left() + ICON_MARGIN)
        editor.setGeometry(r)

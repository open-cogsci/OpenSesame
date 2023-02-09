# coding=utf-8

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
from qtpy.QtCore import Qt
from qtpy.QtWidgets import (
    QDialog,
    QLineEdit,
    QVBoxLayout,
    QListWidget,
    QListWidgetItem
)
from libqtopensesame.extensions import BaseExtension
from libqtopensesame.misc.translate import translation_context
from libqtopensesame.misc.config import cfg
_ = translation_context(u'QuickSelector', category=u'extension')

STYLESHEET = '''
QuickSelectorDialog {{
    background-color: {background};
    color: {foreground};
    padding: 8px;
    border-radius: 4px;
}}
QLineEdit {{
    margin-bottom: 4px;
}}
QLineEdit, QListWidget {{
    color: {foreground};
    border: none;
    font-family: {font_family};
    font-size: {font_size}px;
    background-color: {selected_background};
    padding: 4px;
}}
'''


class SearchBox(QLineEdit):

    def keyPressEvent(self, e):

        if e.key() in (Qt.Key_Down, Qt.Key_Home):
            self.parent().focus_result_box()
            return
        if e.key() in (Qt.Key_Up, Qt.Key_End):
            self.parent().focus_result_box(jump_to_last=True)
            return
        if e.key() in (Qt.Key_Enter, Qt.Key_Return):
            self.parent().select_top_result()
            return
        super(SearchBox, self).keyPressEvent(e)


class ResultBox(QListWidget):

    def keyPressEvent(self, e):

        if (
            (e.key() == Qt.Key_Up and not self.currentRow()) or
            e.key() not in (
                Qt.Key_Down,
                Qt.Key_Up,
                Qt.Key_Return,
                Qt.Key_Enter,
                Qt.Key_PageUp,
                Qt.Key_PageDown
            )
        ):
            self.parent().focus_search_box(e)
            return
        super(ResultBox, self).keyPressEvent(e)


class QuickSelectorDialog(QDialog):

    def __init__(self, parent, haystack, placeholder_text, default):

        from pygments import styles, token

        super(QuickSelectorDialog, self).__init__(
            parent,
            Qt.FramelessWindowHint
        )
        # The Text token is not always defined, in which case the color
        # defaults to black, which is ugly. Therefore, retry with the generic
        # token.
        style = styles.get_style_by_name(cfg.pyqode_color_scheme)
        foreground = style.styles.get(token.Text)
        if not foreground:
            foreground = style.styles.get(token.Token)
        self.setWindowTitle(u'Quick Selector')
        self.setStyleSheet(STYLESHEET.format(
            background=style.highlight_color,
            selected_background=style.background_color,
            foreground=foreground,
            font_family=cfg.pyqode_font_name,
            font_size=cfg.pyqode_font_size
        ))
        # Already create a lowercase version of the label for performance
        self._haystack = [
            (label.lower(), label, data, on_select)
            for label, data, on_select in haystack
        ]
        self._default = default
        self._search_box = SearchBox(self)
        self._search_box.textEdited.connect(self._search)
        if placeholder_text:
            self._search_box.setPlaceholderText(placeholder_text)
        self._result_box = ResultBox(self)
        self._result_box.setTextElideMode(Qt.ElideMiddle)
        self._result_box.itemActivated.connect(self._select)
        self._result_box.setVerticalScrollBarPolicy(Qt.ScrollBarAlwaysOff)
        self._result_box.setHorizontalScrollBarPolicy(Qt.ScrollBarAlwaysOff)
        self._layout = QVBoxLayout(self)
        self._layout.addWidget(self._search_box)
        self._layout.addWidget(self._result_box)
        self.setMinimumWidth(cfg.quick_selector_min_width)
        self._search(u'')

    def focus_result_box(self, jump_to_last=False):

        self._result_box.setFocus()
        self._result_box.setCurrentRow(
            self._result_box.count() - 1 if jump_to_last else 0
        )

    def focus_search_box(self, e):

        self._search_box.setFocus()
        self._search_box.keyPressEvent(e)

    def select_top_result(self):

        self._select(self._result_box.takeItem(0))

    def _search(self, needle):

        import Levenshtein

        if not needle:
            haystack = self._haystack[:]
            if self._default:
                haystack.insert(0, (self._default[0].lower(),) + self._default)
            self._result_box.clear()
            for lower_label, label, data, on_select in haystack:
                item = QListWidgetItem(label, self._result_box)
                item.data = data
                item.on_select = on_select
                self._result_box.addItem(item)
            return
        needle = needle.lower()
        needles = needle.split()
        self._result_box.show()
        self._result_box.clear()
        results = []
        for lower_label, label, data, on_select in self._haystack:
            for subneedle in needles:
                if subneedle not in lower_label:
                    break
            else:
                # We count the number of full matches of the needle in the
                # labels and divide the score by this. This was we give an
                # advantage to labels that contain multiple matches of the
                # needle, for example in the folder and file name.
                hits = max(
                    1,
                    sum(lower_label.count(s) for s in needle.split())
                )
                results.append((
                    Levenshtein.distance(needle, lower_label) / (len(label) * hits),
                    label,
                    data,
                    on_select
                ))
        for score, label, data, on_select in sorted(
            results,
            key=lambda t: t[0]
        ):
            item = QListWidgetItem(label, self._result_box)
            item.data = data
            item.on_select = on_select
            self._result_box.addItem(item)

    def _select(self, item):

        if item is None:
            return
        item.on_select(item.data)
        self.accept()


class QuickSelector(BaseExtension):

    def event_quick_select(
        self, haystack,
        placeholder_text=None,
        default=None
    ):

        QuickSelectorDialog(
            self.main_window,
            haystack,
            placeholder_text,
            default
        ).exec_()

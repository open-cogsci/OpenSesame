# -*- coding:utf-8 -*-

"""
This file is part of openexp.

openexp is free software: you can redistribute it and/or modify
it under the terms of the GNU General Public License as published by
the Free Software Foundation, either version 3 of the License, or
(at your option) any later version.

openexp is distributed in the hope that it will be useful,
but WITHOUT ANY WARRANTY; without even the implied warranty of
MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
GNU General Public License for more details.

You should have received a copy of the GNU General Public License
along with openexp.  If not, see <http://www.gnu.org/licenses/>.
"""
import os
from libopensesame.py3compat import *
from libopensesame.exceptions import osexception
from libqtopensesame.sketchpad_elements._base_element import BaseElement
from libopensesame.sketchpad_elements import Textline as TextlineRuntime
from qtpy import QtCore, QtWidgets
from libqtopensesame.misc.translate import translation_context
_ = translation_context(u'sketchpad', category=u'item')


class Textline(BaseElement, TextlineRuntime):

    r"""A textline element.
    See base_element for docstrings and function
    descriptions.
    """
    def show_edit_dialog(self):
        r"""The show-edit dialog for the textline only edits the text, not the
        full element script.
        """
        text = self.experiment.text_input(
            _(u'Edit text'),
            message=_(u'Please enter a text for the textline'),
            content=safe_decode(self.properties[u'text']).replace(
                u'<br />',
                u'\n'
            ),
            parent=self.sketchpad._edit_widget
        )
        if text is None:
            return
        self.properties[u'text'] = self.clean_text(text)
        self.sketchpad.draw()

    @classmethod
    def mouse_press(cls, sketchpad, pos):

        text = sketchpad.experiment.text_input(title=_(u'New textline'),
                                               message=_(u'Enter text'),
                                               parent=sketchpad._edit_widget)
        if text is None:
            return None
        properties = {
            u'x':			pos[0],
            u'y':			pos[1],
            u'text':		cls.clean_text(text, escape=True),
            u'color': 		sketchpad.current_color(),
            u'center': 		sketchpad.current_center(),
            u'font_family': sketchpad.current_font_family(),
            u'font_size': 	sketchpad.current_font_size(),
            u'font_bold': 	sketchpad.current_font_bold(),
            u'font_italic': sketchpad.current_font_italic(),
            u'html':		sketchpad.current_html(),
            u'show_if': 	sketchpad.current_show_if()
        }
        return Textline(sketchpad, properties=properties)

    @staticmethod
    def clean_text(text, escape=False):
        r"""Cleans text by removing quotes and converting newlines to <br />
        tags.

        Parameters
        ----------
        text
            The text to clean.
        typeescape, optional
            Indicates whether slashes should be escaped.
        type, optional
            bool

        Returns
        -------
        unicode
            Clean text.
        """
        text = str(text)
        text = text.replace(os.linesep, u'<br />')
        text = text.replace(u'\n', u'<br />')
        text = text.replace(u'"', u'')
        if escape:
            text = text.replace(u'\\', u'\\\\')
        return text

    @staticmethod
    def requires_text():
        return True

    @staticmethod
    def requires_color():
        return True

    @staticmethod
    def requires_center():
        return True


# Alias for backwards compatibility
textline = Textline

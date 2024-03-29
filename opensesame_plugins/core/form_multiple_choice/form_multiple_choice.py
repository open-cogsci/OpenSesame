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
from libopensesame.exceptions import InvalidValue, InvalidFormScript
from libopensesame.item import Item
from libopensesame import widgets
from libqtopensesame.items.qtautoplugin import QtAutoPlugin


class FormMultipleChoice(Item):

    lazy_init = False

    def reset(self):
        self.var.options = u'Yes\nNo\nMaybe'
        self.var.question = u'Your question'
        self.var.form_title = u'Form title'
        self.var.form_var = u'response'
        self.var.advance_immediately = u'yes'
        self.var.allow_multiple = u'yes'
        self.var.button_text = u'Ok'
        self.var.timeout = u'infinite'
        self.var.spacing = 10
        self.var.margins = u'50;50;50;50'
        self.var._theme = u'gray'

    def run(self):
        # Parse the option list
        option_list = self.var.options.split(u'\n')  # split by return
        # Filter out empty options
        option_list = list(filter(lambda option: option != u'', option_list))
        if not option_list:
            raise InvalidFormScript(
                'You must specify at least one response option')
        # Determine whether a button is shown and determine the number of rows
        rows = len(option_list) + 2
        if (
                self.var.advance_immediately == u'no' or
                self.var.allow_multiple == u'yes'
        ):
            show_button = True
            click_accepts = False
            rows += 1
        else:
            show_button = False
            click_accepts = True
        # Determine the group for the checkboxes
        if self.var.allow_multiple == u'no':
            group = u'response_group'
        else:
            group = None
        # The variable in which the response is stored
        var = self.var.form_var
        # Build the form
        try:
            margins = [
                float(i) for i in safe_decode(self.var.margins).split(u';')
            ]
        except (ValueError, TypeError):
            raise InvalidValue(
                'margins should be numeric values separated by a semi-colon')
        if self.var.timeout == u'infinite':
            timeout = None
        else:
            timeout = self.var.timeout
        form = widgets.form(
            self.experiment,
            cols=1,
            rows=rows,
            spacing=self.var.spacing,
            margins=margins,
            theme=self.var._theme,
            item=self,
            timeout=timeout,
            clicks=self.var.form_clicks == u'yes'
        )
        form.set_widget(widgets.label(form, self.var.form_title), (0, 0))
        form.set_widget(widgets.label(form, self.var.question), (0, 1))
        i = 2
        for option in option_list:
            form.set_widget(
                widgets.checkbox(
                    form,
                    option,
                    group=group,
                    click_accepts=click_accepts,
                    var=var
                ),
                (0, i)
            )
            i += 1
        if show_button:
            form.set_widget(widgets.button(form, self.var.button_text), (0, i))
        form._exec()

    def var_info(self):
        return (super().var_info() + 
                [(self.var.form_var, u'[Depends on response]')])


class QtFormMultipleChoice(FormMultipleChoice, QtAutoPlugin):

    def __init__(self, name, experiment, string=None):
        FormMultipleChoice.__init__(self, name, experiment, string)
        QtAutoPlugin.__init__(self, __file__)
        self.custom_interactions()

    def apply_edit_changes(self):
        if not super().apply_edit_changes() or self.lock:
            return False
        self.custom_interactions()
        return True

    def custom_interactions(self):
        """
        The advance_immediately option is not applicable if multiple items can
        be selected.
        """
        self.checkbox_advance_immediately.setEnabled(
            self.var.get(u'allow_multiple') == u'no')
        self.line_edit_button_text.setEnabled(
            self.var.get(u'allow_multiple') == u'yes' or
            self.var.get(u'advance_immediately') == u'no')

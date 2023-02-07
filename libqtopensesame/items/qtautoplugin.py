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
from libqtopensesame.items.qtplugin import QtPlugin
from libqtopensesame import validators
from libqtopensesame.misc.translate import translation_context
from libopensesame.exceptions import osexception
_ = translation_context(u'qtautoplugin', category=u'core')


class QtAutoPlugin(QtPlugin):

    """A class that processes auto-plugins defined in a YAML file"""
    def init_edit_widget(self):
        """Construct the GUI controls based on info.yaml"""
        super().init_edit_widget(False)
        item_type_translate = translation_context(self.item_type,
                                                  category=u'plugin')
        self.help_url = self.plugin_attribute('help')
        # Some options are required. Which options are requires depends on the
        # specific widget.
        required = [
            ([u'checkbox', u'color_edit', u'combobox', u'editor', u'filepool',
              u'line_edit', u'spinbox', u'text'], [u'label']),
            ([u'checkbox', u'color_edit', u'combobox', u'editor', u'filepool',
              u'line_edit', u'spinbox'], [u'var']),
            ([u'spinbox', u'slider'], [u'min_val', u'max_val']),
            ([u'combobox'], [u'options']),
        ]
        # Keywords are optional parameters that are set to some default if they
        # are not specified.
        keywords = {
            u'info': None,
            u'min_width': None,
            u'prefix': u'',
            u'suffix': u'',
            u'left_label': u'min.',
            u'right_label': u'max.',
            u'syntax': False,
            u'language': 'python'
        }
        # This indicates whether we should pad the controls with a stretch at
        # the end.
        need_stretch = True
        for c in self.plugin_attribute('controls'):
            # Check whether all required options have been specified
            if u'type' not in c:
                raise osexception(
                    _(u'You must specify "type" for %s controls in info.yaml')
                    % option)
            for types, options in required:
                if c[u'type'] in types:
                    for option in options:
                        if option not in c:
                            raise osexception(
                                _(u'You must specify "%s" for %s controls in info.yaml')
                                % (option, c[u'type']))
            if u'var' in c and not self.syntax.valid_var_name(c[u'var']):
                raise osexception(
                    _(u'Invalid variable name (%s) specified in %s plugin info') %
                    (c[u'var'], self.item_type))
            # Set missing keywords to None
            for keyword, default in keywords.items():
                if keyword not in c:
                    c[keyword] = default
            # Translate translatable fields
            c[u'label'] = item_type_translate(c[u'label'])
            if c[u'info'] is not None:
                c[u'info'] = item_type_translate(c[u'info'])
            # Parse checkbox
            if c[u'type'] == u'checkbox':
                widget = self.add_checkbox_control(c[u'var'], c[u'label'],
                                                   info=c[u'info'])
            # Parse color_edit
            elif c[u'type'] == u'color_edit':
                widget = self.add_color_edit_control(c[u'var'], c[u'label'],
                    info=c[u'info'], min_width=c[u'min_width'])
            # Parse combobox
            elif c[u'type'] == u'combobox':
                widget = self.add_combobox_control(c[u'var'], c[u'label'],
                    c[u'options'], info=c[u'info'])
            # Parse editor
            elif c[u'type'] == u'editor':
                widget = self.add_editor_control(c[u'var'], c[u'label'],
                    syntax=c[u'syntax'], language=c[u'language'])
                need_stretch = False
            # Parse filepool
            elif c[u'type'] == u'filepool':
                widget = self.add_filepool_control(c[u'var'], c[u'label'],
                    info=c[u'info'])
            # Parse line_edit
            elif c[u'type'] == u'line_edit':
                widget = self.add_line_edit_control(c[u'var'], c[u'label'],
                    info=c[u'info'], min_width=c[u'min_width'])
            # Parse spinbox
            elif c[u'type'] == u'spinbox':
                widget = self.add_spinbox_control(c[u'var'], c[u'label'],
                    c[u'min_val'], c[u'max_val'], prefix=c[u'prefix'],
                    suffix=c[u'suffix'], info=c[u'info'])
            # Parse slider
            elif c[u'type'] == u'slider':
                widget = self.add_slider_control(c[u'var'], c[u'label'],
                    c[u'min_val'], c[u'max_val'], left_label=c[u'left_label'],
                    right_label=c[u'right_label'], info=c[u'info'])
            # Parse text
            elif c[u'type'] == u'text':
                widget = self.add_text(c[u'label'])
            else:
                raise Exception(_(u'"%s" is not a valid qtautoplugin control')
                                % controls[u'type'])
            # Add an optional validator
            if u'validator' in c:
                try:
                    validator = getattr(validators,
                                        u'%s_validator' % c[u'validator'])
                except:
                    raise osexception(
                        u'Invalid validator: %s' % c[u'validator'])
                widget.setValidator(validator(self.main_window))
            # Add the widget as an item property when the 'name' option is
            # specified.
            if u'name' in c:
                if hasattr(self, c[u'name']):
                    raise Exception(_(u'Name "%s" is already taken in qtautoplugin control')
                                    % c[u'name'])
                setattr(self, c[u'name'], widget)
        if need_stretch:
            self.add_stretch()

    def apply_edit_changes(self):
        """Applies the controls. I.e. sets the variables from the controls."""
        if not super().apply_edit_changes() or self.lock:
            return False
        return True

    def edit_widget(self):
        """Sets the controls based on the variables."""
        self.lock = True
        super().edit_widget()
        self.lock = False
        return self._edit_widget


# Alias for backwards compatibility
qtautoplugin = QtAutoPlugin

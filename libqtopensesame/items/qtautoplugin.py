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
_ = translation_context('qtautoplugin', category='core')


class QtAutoPlugin(QtPlugin):

    """A class that processes auto-plugins defined in a YAML file"""
    def init_edit_widget(self):
        """Construct the GUI controls based on info.yaml"""
        super().init_edit_widget(False)
        item_type_translate = translation_context(self.item_type,
                                                  category='plugin')
        # The help url should be specified as `help_url`. However, old-style
        # plugins used `help`.
        self.help_url = self.plugin_attribute('help_url')
        if self.help_url is None:
            self.help_url = self.plugin_attribute('help')
        # Some options are required. Which options are requires depends on the
        # specific widget.
        required = [
            (['checkbox', 'color_edit', 'combobox', 'editor', 'filepool',
              'line_edit', 'spinbox', 'text'], ['label']),
            (['checkbox', 'color_edit', 'combobox', 'editor', 'filepool',
              'line_edit', 'spinbox'], ['var']),
            (['spinbox', 'slider'], ['min_val', 'max_val']),
            (['combobox'], ['options']),
        ]
        # Keywords are optional parameters that are set to some default if they
        # are not specified.
        keywords = {
            'info': None,
            'min_width': None,
            'prefix': '',
            'suffix': '',
            'left_label': 'min.',
            'right_label': 'max.',
            'syntax': False,
            'language': 'python'
        }
        # This indicates whether we should pad the controls with a stretch at
        # the end.
        need_stretch = True
        for c in self.plugin_attribute('controls'):
            # Check whether all required options have been specified
            if 'type' not in c:
                raise RuntimeError(
                    _('You must specify "type" for %s controls in info.yaml')
                    % option)
            for types, options in required:
                if c['type'] in types:
                    for option in options:
                        if option not in c:
                            raise RuntimeError(
                                _('You must specify "%s" for %s controls in info.yaml')
                                % (option, c['type']))
            if 'var' in c and not self.syntax.valid_var_name(c['var']):
                raise RuntimeError(
                    _('Invalid variable name (%s) specified in %s plugin info') %
                    (c['var'], self.item_type))
            # Set missing keywords to None
            for keyword, default in keywords.items():
                if keyword not in c:
                    c[keyword] = default
            # Translate translatable fields
            c['label'] = item_type_translate(c['label'])
            if c['info'] is not None:
                c['info'] = item_type_translate(c['info'])
            # Parse checkbox
            if c['type'] == 'checkbox':
                widget = self.add_checkbox_control(c['var'], c['label'],
                                                   info=c['info'])
            # Parse color_edit
            elif c['type'] == 'color_edit':
                widget = self.add_color_edit_control(c['var'], c['label'],
                    info=c['info'], min_width=c['min_width'])
            # Parse combobox
            elif c['type'] == 'combobox':
                widget = self.add_combobox_control(c['var'], c['label'],
                    c['options'], info=c['info'])
            # Parse editor
            elif c['type'] == 'editor':
                widget = self.add_editor_control(c['var'], c['label'],
                    syntax=c['syntax'], language=c['language'])
                need_stretch = False
            # Parse filepool
            elif c['type'] == 'filepool':
                widget = self.add_filepool_control(c['var'], c['label'],
                    info=c['info'])
            # Parse line_edit
            elif c['type'] == 'line_edit':
                widget = self.add_line_edit_control(c['var'], c['label'],
                    info=c['info'], min_width=c['min_width'])
            # Parse line_edit
            elif c['type'] == 'conditional_expression':
                widget = self.add_conditional_expression_control(
                    c['var'], c['label'], c['verb'], info=c['info'],
                    min_width=c['min_width'])
            # Parse spinbox
            elif c['type'] == 'spinbox':
                widget = self.add_spinbox_control(c['var'], c['label'],
                    c['min_val'], c['max_val'], prefix=c['prefix'],
                    suffix=c['suffix'], info=c['info'])
            # Parse slider
            elif c['type'] == 'slider':
                widget = self.add_slider_control(c['var'], c['label'],
                    c['min_val'], c['max_val'], left_label=c['left_label'],
                    right_label=c['right_label'], info=c['info'])
            # Parse text
            elif c['type'] == 'text':
                widget = self.add_text(c['label'])
            else:
                raise Exception(_('"%s" is not a valid qtautoplugin control')
                                % controls['type'])
            # Add an optional validator
            if 'validator' in c:
                try:
                    validator = getattr(validators,
                                        '%s_validator' % c['validator'])
                except:
                    raise RuntimeError(
                        'Invalid validator: %s' % c['validator'])
                widget.setValidator(validator(self.main_window))
            # Add the widget as an item property when the 'name' option is
            # specified.
            if 'name' in c:
                if hasattr(self, c['name']):
                    raise RuntimeError(
                        _('Name "%s" is already taken in qtautoplugin control')
                        % c['name'])
                setattr(self, c['name'], widget)
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

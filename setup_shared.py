#-*- coding:utf-8 -*-

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

---
desc:
	Contains setup settings that are shared between the various
	platform-specific setup scripts.
---
"""

# List of included plug-ins
included_plugins = [
	'advanced_delay',
	'coroutines',
	'fixation_dot',
	'form_base',
	'form_text_input',
	'form_consent',
	'form_text_display',
	'form_multiple_choice',
	'joystick',
	'notepad',
	'parallel',
	'port_reader',
	'repeat_cycle',
	'reset_feedback',
	'srbox',
	'text_display',
	'text_input',
	'touch_response',
	'quest_staircase_init',
	'quest_staircase_next',
	]

# List of included extensions
included_extensions = [
	'after_experiment',
	'analytics',
	'automatic_backup',
	'bug_report',
	'example_experiments',
	'file_handler',
	'get_started',
	'help',
	'notifications',
	'plugin_manager',
	'preload_items',
	'pyqode_manager',
	'quick_switcher',
	'system_check',
	'system_information',
	'tab_to_dockwidget',
	'toolbar_menu',
	'variable_inspector',
	'restore_ui_elements',
	'undo_manager',
	'update_checker',
]

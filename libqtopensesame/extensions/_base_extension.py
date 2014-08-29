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
"""

import os
from PyQt4 import QtCore, QtGui
from libopensesame import debug
from libopensesame.exceptions import osexception
from libqtopensesame.misc import _
from libqtopensesame.misc.config import cfg
from libqtopensesame.misc.base_subcomponent import base_subcomponent

class base_extension(base_subcomponent):

	"""
	desc:
		A base class for GUI extensions.
	"""

	def __init__(self, main_window, info={}):

		"""
		desc:
			Constructor.

		arguments:
			main_window:	The main-window object.

		keywords:
			info:			A dictionary with extension properties that have
							been read from info.[json|txt].
		"""

		debug.msg(u'creating %s' % self.name())
		self.info = info
		self.setup(main_window)
		self.register_ui_files()
		self.create_action()
		self.register_config()

	@property
	def menubar(self):

		"""
		returns:
			desc:	Gives the menubar.
			type:	QMenuBar
		"""

		return self.main_window.menuBar()

	@property
	def toolbar(self):

		"""
		returns:
			desc:	Gives the main toolbar.
			type:	QToolBar
		"""

		return self.main_window.ui.toolbar_main

	@property
	def tabwidget(self):

		"""
		returns:
			desc:	Gives the tab widget.
			type:	QTabWidget
		"""

		return self.main_window.ui.tabwidget

	@property
	def statusbar(self):

		"""
		returns:
			desc:	Gives the statusbar.
			type:	QStatusBar
		"""

		return self.main_window.statusBar()

	@property
	def set_status(self):
		return self.main_window.set_status

	def label(self):

		"""
		desc:
			Gives the label that is used for the menu and toolbar entry.
			Normally, this is specified in info.json.

		returns:
			desc:	A label text.
			type:	unicode
		"""

		label = self.info.get(u'label', None)
		if label != None:
			return _(label)
		return None

	def icon(self):

		"""
		desc:
			Gives the name of the icon that is used for the menu and toolbar
			entry. Normally, this is specified in info.json.

		returns:
			desc:	The name of an icon.
			type:	unicode
		"""

		return self.info.get(u'icon', u'applications-utilities')

	def shortcut(self):

		"""
		desc:
			Gives the keyboard shortcut that activates the extension. Normally,
			this is specified in info.json. A shortcut only works if the
			extension has either a toolbar ot menu entry.

		returns:
			desc:	The keyboard shortcut.
			type:	unicode
		"""

		return self.info.get(u'shortcut', None)

	def menu_pos(self):

		"""
		desc:
			Describes the position of the extension in the menu. Normally,
			this is specified in info.json.

		returns:
			desc:	A (submenu, menuindex, separator_before, separator_after)
					tuple, or None if the extension has no menu entry.
			type:	[tuple, NoneType]
		"""

		menu_pos = self.info.get(u'menu', None)
		if menu_pos == None:
			return None
		return (menu_pos.get(u'submenu', None),
			menu_pos.get(u'index', -1),
			menu_pos.get(u'separator_before', False),
			menu_pos.get(u'separator_after', False))

	def toolbar_pos(self):

		"""
		desc:
			Describes the position of the extension in the toolbar. Normally,
			this is specified in info.json.

		returns:
			desc:	An (index, separator_before, separator_after)
					tuple, or None if the extension has no toolbar entry.
			type:	[tuple, NoneType]
		"""

		toolbar_pos = self.info.get(u'toolbar', None)
		if toolbar_pos == None:
			return None
		return (toolbar_pos.get(u'index', -1),
			toolbar_pos.get(u'separator_before', False),
			toolbar_pos.get(u'separator_after', False))

	def activate(self):

		"""
		desc:
			Is called when the extension is activated through a keyboard
			shortcut, or a menu/ toolbar click.
		"""

		pass

	def add_action(self, widget, action, index, separator_before,
		separator_after):

		"""
		visible:
			False

		desc:
			Adds an action to a widget that supports actions (i.e. a QMenu or
			a QToolBar).

		arguments:
			widget:				The widget to add the action to.
			action:				The action to add.
			index:				The index of the action.
			separator_before:	Indicates whether a separator should be added
								before the action.
			separator_action:	Indicates whether a separator should be added
								before the action.
		"""

		if index >= len(widget.actions()) or index < -len(widget.actions()) \
			or index == -1:
			before = None
			widget.addAction(action)
		else:
			if index < 0:
				index += 1
			before = widget.actions()[index]
		if separator_after:
			if before == None:
				before = widget.addSeparator()
			else:
				before = widget.insertSeparator(before)
		if before == None:
			widget.addAction(action)
		else:
			widget.insertAction(before, action)
		if separator_before:
			widget.insertSeparator(action)

	def get_submenu(self, menu_text):

		"""
		desc:
			Gets the submenu that matches the menu text. If no match is found
			a new submenu is created.

		arguments:
			menu_text:	The menu text. This should match an object in
						main_window.ui.menu_[menu_text].

		returns:
			type:	QMenu
		"""

		menu_name = u'menu_%s' % menu_text.lower()
		if not hasattr(self.main_window.ui, menu_name):
			menu_name = u'menu_tools'
			menu = QtGui.QMenu(menu_text)
			self.menubar.addMenu(menu)
			setattr(self.main_window.ui, menu_name, menu)
		return getattr(self.main_window.ui, menu_name)

	def fire(self, event, **kwdict):

		if hasattr(self, u'event_%s' % event):
			debug.msg(u'extensions %s received event_%s' % (self.name(), event))
			getattr(self, u'event_%s' % event)(**kwdict)

	def name(self):

		return self.__class__.__name__

	def register_ui_files(self):

		for path in os.listdir(self.info[u'plugin_folder']):
			if path.endswith(u'.ui'):
				self.experiment.resources[u'extensions.%s.%s' % (self.name(),
					os.path.splitext(path)[0])] = os.path.join(
					self.info[u'plugin_folder'], path)

	def create_action(self):

		if self.label() != None:
			# Create an action to be inserted into the menu and/ or toolbar
			icon = self.icon()
			if isinstance(icon, basestring):
				icon = self.theme.qicon(icon)
			action = QtGui.QAction(icon, self.label(), self.main_window)
			action.triggered.connect(self.activate)
			if self.shortcut() != None:
				action.setShortcuts([self.shortcut()])
			# Insert the action into the menu
			if self.menu_pos() != None:
				submenu_text, index, separator_before, separator_after = \
					self.menu_pos()
				submenu = self.get_submenu(submenu_text)
				self.add_action(submenu, action, index, separator_before,
					separator_after)
			# Insert the action into the toolbar
			if self.toolbar_pos() != None:
				index, separator_before, separator_after = self.toolbar_pos()
				self.add_action(self.toolbar, action, index, separator_before,
					separator_after)

	def supported_events(self):

		events = []
		for event in dir(self):
			if event.startswith(u'event_'):
				events.append(event[6:])
				debug.msg(u'extension %s supports %s' % (self.name(), event))
		return events

	def register_config(self):

		for setting, default in self.info.get(u'settings', {}).items():
			cfg.register(setting, default=default)

	def settings_widget(self):

		"""
		desc:
			Creates a settings QWidget for the extension, or returns None if
			no settings have been defined.

		returns:
			A settings QWidget or None.
		"""

		r = 10000000 # Maximumum range for spinbox widgets
		if u'settings' not in self.info:
			return None
		group = QtGui.QGroupBox(_(u'Extension: %s') % self.name(),
			self.main_window)
		layout = QtGui.QFormLayout(group)
		self.settings_controls = {}
		for setting, default in self.info[u'settings'].items():
			value = cfg[setting]
			label = QtGui.QLabel(_(setting))
			if isinstance(default, bool):
				control = QtGui.QCheckBox(self.main_window)
				control.setChecked(bool(value))
				control.clicked.connect(self.apply_settings_widget)
			elif isinstance(default, int):
				try:
					value = int(value)
				except:
					value = default
				control = QtGui.QSpinBox(self.main_window)
				control.setRange(-r, r)
				control.setValue(value)
				control.editingFinished.connect(self.apply_settings_widget)
			elif isinstance(default, float):
				try:
					value = float(value)
				except:
					value = default
				control = QtGui.QDoubleSpinBox(self.main_window)
				control.setRange(-r, r)
				control.setValue(value)
				control.editingFinished.connect(self.apply_settings_widget)
			else:
				control = QtGui.QLineEdit(self.experiment.unistr(value))
				control.editingFinished.connect(self.apply_settings_widget)
			self.settings_controls[setting] = control
			layout.addRow(label, control)
		group.setLayout(layout)
		return group

	def apply_settings_widget(self):

		"""
		desc:
			Applies the settings widget.
		"""

		for setting, default in self.info[u'settings'].items():
			control = self.settings_controls[setting]
			if isinstance(default, bool):
				cfg[setting] = control.isChecked()
			elif isinstance(default, int) or isinstance(default, float):
				cfg[setting] = control.value()
			else:
				cfg[setting] = unicode(control.text())

	def ext_resource(self, resource):

		path = os.path.join(self.info[u'plugin_folder'], resource)
		if not os.path.exists(path):
			raise osexception(u'Extension resource not found: %s' % path)
		return path

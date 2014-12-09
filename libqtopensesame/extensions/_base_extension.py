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

		"""
		returns:
			desc:	A shortcut to `qtopensesame.set_status`.
		"""

		return self.main_window.set_status

	def label(self):

		"""
		desc:
			Gives the label that is used for the menu and toolbar entry.
			Normally, this is specified in info.json, but you can override this
			function to implement custom logic.

		returns:
			desc:	A label text or None.
			type:	[unicode, NoneType]
		"""

		label = self.info.get(u'label', None)
		if label != None:
			return _(label, context=self.name())
		return None

	def tooltip(self):

		"""
		desc:
			Gives the tooltip that is used for the menu and toolbar entry.
			Normally, this is specified in info.json, but you can override this
			function to implement custom logic.

		returns:
			desc:	A tooltip text.
			type:	[unicode, NoneType]
		"""

		tooltip = self.info.get(u'tooltip', None)
		if tooltip != None:
			return _(tooltip, context=self.name())
		return None


	def checkable(self):

		"""
		desc:
			Indicates whether the extension action is checkable or not.
			Normally, this is specified in info.json, but you can override this
			function to implement custom logic.

		returns:
			type:	bool
		"""

		return self.info.get(u'checkable', False)

	def set_checked(self, checked):

		"""
		desc:
			Sets the checked status of the action. If there is no action, or if
			the action is not checkable, this is silently ignored.

		arguments:
			checked:
				desc:	The checked status.
				type:	bool
		"""

		if self.action == None or not self.checkable():
			return
		self.action.setChecked(checked)

	def icon(self):

		"""
		desc:
			Gives the name of the icon that is used for the menu and toolbar
			entry. Normally, this is specified in info.json, but you can
			override this function to implement custom logic.

		returns:
			desc:	The name of an icon.
			type:	unicode
		"""

		return self.info.get(u'icon', u'applications-utilities')

	def shortcut(self):

		"""
		desc:
			Gives the keyboard shortcut that activates the extension. Normally,
			this is specified in info.json, but you can override this
			function to implement custom logic. A shortcut only works if the
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
			this is specified in info.json, but you can override this
			function to implement custom logic.

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
			this is specified in info.json, but you can override this
			function to implement custom logic.

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
			shortcut, or a menu/ toolbar click. Override this function to
			implement your extension's behavior.
		"""

		pass

	def _activate(self):

		"""
		visible:
			False

		desc:
			A wrapper around [activate] to catch Exceptions.
		"""

		try:
			self.activate()
		except Exception as e:
			if not isinstance(e, osexception):
				e = osexception(msg=u'Extension error', exception=e)
			self.notify(
				u'Extension %s misbehaved on activate (see debug window for stack trace)' \
				% self.name())
			self.main_window.print_debug_window(e)

	def add_action(self, widget, action, index, separator_before,
		separator_after):

		"""
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

		"""
		desc:
			Calls an event function, if it exists.

		arguments:
			event:
				desc:	The event name, which is handled by a function called
						`event_[event name]`.
				type:	[str, unicode]

		keyword-dict:
			kwdict:		A keyword dictionary with event-specific keywords.
		"""

		if hasattr(self, u'event_%s' % event):
			debug.msg(u'extensions %s received event_%s' % (self.name(), event))
			getattr(self, u'event_%s' % event)(**kwdict)

	def name(self):

		"""
		returns:
			desc:	The name of the extension, i.e. the extension class name.
			type:	unicode
		"""

		return self.__class__.__name__.decode(u'utf-8')

	def register_ui_files(self):

		"""
		desc:
			Registers all .ui files in the extension folder so that they can
			be retrieved as extensions.[extension name].[ui name].
		"""

		for path in os.listdir(self.info[u'plugin_folder']):
			if path.endswith(u'.ui'):
				self.experiment.resources[u'extensions.%s.%s' % (self.name(),
					os.path.splitext(path)[0])] = os.path.join(
					self.info[u'plugin_folder'], path)

	def create_action(self):

		"""
		desc:
			Creates a QAction for the extension, and adds it to the menubar
			and/ or the toolbar.
		"""

		if self.label() != None:
			# Create an action to be inserted into the menu and/ or toolbar
			icon = self.icon()
			if isinstance(icon, basestring):
				icon = self.theme.qicon(icon)
			self.action = QtGui.QAction(icon, self.label(), self.main_window)
			self.action.triggered.connect(self._activate)
			self.action.setCheckable(self.checkable())
			if self.tooltip() != None:
				self.action.setToolTip(self.tooltip())
			if self.shortcut() != None:
				self.action.setShortcuts([self.shortcut()])
			# Insert the action into the menu
			if self.menu_pos() != None:
				submenu_text, index, separator_before, separator_after = \
					self.menu_pos()
				submenu = self.get_submenu(submenu_text)
				self.add_action(submenu, self.action, index, separator_before,
					separator_after)
			# Insert the action into the toolbar
			if self.toolbar_pos() != None:
				index, separator_before, separator_after = self.toolbar_pos()
				self.add_action(self.toolbar, self.action, index,
					separator_before, separator_after)
		else:
			self.action = None

	def supported_events(self):

		"""
		desc:
			Gives the events that are supported by the extension. This is done
			by introspecting which `event_[event name]` functions exist.

		returns:
			desc:	A list of supported events.
			type:	list
		"""

		events = []
		for event in dir(self):
			if event.startswith(u'event_'):
				events.append(event[6:])
				debug.msg(u'extension %s supports %s' % (self.name(), event))
		return events

	def register_config(self):

		"""
		desc:
			Registers the extension settings in the config object.
		"""

		for setting, default in self.info.get(u'settings', {}).items():
			cfg.register(setting, default=default)

	def settings_widget(self):

		"""
		desc:
			Creates a settings QWidget for the extension, or returns None if
			no settings have been defined. Override this function to implement
			a more fancy non-default settings menu.

		returns:
			A settings QWidget or None.
		"""

		r = 10000000 # Maximumum range for spinbox widgets
		if u'settings' not in self.info:
			return None
		group = QtGui.QGroupBox(_(u'Extension: %s', context=self.name()) % self.name(),
			self.main_window)
		layout = QtGui.QFormLayout(group)
		self.settings_controls = {}
		for setting, default in self.info[u'settings'].items():
			value = cfg[setting]
			label = QtGui.QLabel(_(setting, context=self.name()))
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
			Applies the settings widget. This function is called automatically
			when a default settings widget is created by [settings_widget].
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

		"""
		desc:
			Finds an extension resource, i.e. a file in the extension folder,
			and returns the full path to the resource. An `osexception` is
			raised if the resource does not exist.

		arguments:
			resource:
				desc:	The name of a resource.
				type:	[str, unicode]

		returns:
			desc:	The full path to the resource.
			type:	unicode
		"""

		path = os.path.join(self.info[u'plugin_folder'], resource)
		if not os.path.exists(path):
			raise osexception(u'Extension resource not found: %s' % path)
		return path

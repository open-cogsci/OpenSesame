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

from libopensesame.py3compat import *
import textwrap
from qtpy import QtCore, QtWidgets
from libopensesame.exceptions import osexception
from libopensesame.oslogging import oslogger
from libqtopensesame.widgets.item_view_button import item_view_button
from libqtopensesame.widgets.tree_item_item import tree_item_item
from libqtopensesame.widgets.qtitem_splitter import qtitem_splitter
from libqtopensesame.widgets import header_widget
from libqtopensesame._input.pool_select import pool_select
from libqtopensesame.misc.translate import translation_context
_ = translation_context(u'qtitem', category=u'core')


def requires_init(fnc):

	"""
	desc:
		A decorator that makes sure that an item's controls are initialized
		before a function is called.
	"""

	def inner(self, *args, **kwargs):

		if self.container_widget is None:
			self.init_edit_widget()
		return fnc(self, *args, **kwargs)

	return inner


def wait_cursor(fnc):

	"""
	desc:
		A decorator that shows a waiting cursor during the function
	"""

	def inner(self, *args, **kwargs):

		if self.main_window.is_busy():
			return fnc(self, *args, **kwargs)
		self.main_window.set_busy(True)
		retval = fnc(self, *args, **kwargs)
		self.main_window.set_busy(False)
		return retval

	return inner


class qtitem(object):

	"""Base class for the GUI controls of other items"""

	initial_view = u'controls'
	label_align = u'right'
	help_url = None
	lazy_init = True

	def __init__(self):

		"""Constructor"""

		# The auto-widgets are stored in name -> (var, widget) dictionaries
		self.auto_line_edit = {}
		self.auto_combobox = {}
		self.auto_spinbox = {}
		self.auto_slider = {}
		self.auto_editor = {}
		self.auto_checkbox = {}
		# Lazy initialization means that the control widgets are initialized
		# only when they are shown for the first time. This dramatically speeds
		# up opening of files. However, with some items this is not currently
		# possible, because their widgets are also referred when they are not
		# shown. Currently this means the inline_script.
		if self.lazy_init:
			self.container_widget = None
		else:
			self.init_edit_widget()
		self._dirty = False
		self._shown = False
		self.lock = False
		self.maximized = False
		self.set_validator()
		oslogger.debug(u'created %s' % self.name)
		self.cached_script = self.to_string()

	@property
	def main_window(self):
		return self.experiment.main_window

	@property
	def overview_area(self):
		return self.experiment.main_window.ui.itemtree

	@property
	def theme(self):
		return self.experiment.main_window.theme

	@property
	def tabwidget(self):
		return self.experiment.main_window.tabwidget

	@property
	def console(self):
		return self.experiment.main_window.console

	@property
	def extension_manager(self):
		return self.experiment.main_window.extension_manager

	@property
	def default_description(self):
		return _(u'Default description')

	def open_tab(self, select_in_tree=True):

		"""
		desc:
			Opens the tab if it wasn't yet open, and switches to it.
		"""

		unsaved = self.main_window.unsaved_changes
		self.tabwidget.add(self.widget(), self.item_icon(), self.name)
		self.main_window.set_unsaved(unsaved)
		if select_in_tree:
			self.experiment.main_window.ui.itemtree.select_item(
				self.name,
				open_tab=False
			)

	def close_tab(self):

		"""
		desc:
			Closes the tab if it was open.
		"""

		self.tabwidget.remove(self.widget())

	def set_focus(self):

		"""
		desc:
			Gives focus to the most important widget.
		"""

		if hasattr(self, u'focus_widget') and self.focus_widget is not None:
			self.focus_widget.setFocus()

	def set_focus_widget(self, widget, override=False):

		"""
		desc:
			Sets the widget that receives focus when the tab is opened.

		arguments:
			widget:
				desc:	The widget to receive focus or `None` to reset.
				type:	[QWidget, NoneType]

		keywords:
			override:
				desc:	Indicates whether the focus widget should be changed if
						there already is a focus widget.
				type:	bool
		"""

		if override or not hasattr(self, u'focus_widget') or self.focus_widget is None:
			self.focus_widget = widget

	def update_item_icon(self):

		"""
		desc:
			Updates the item icon.
		"""

		self.tabwidget.set_icon(self.widget(), self.item_icon())
		self.experiment.items.set_icon(self.name, self.item_icon())
		self.header_item_icon.setPixmap(
			self.theme.qpixmap(self.item_icon(), 32))

	def item_icon(self):

		"""
		returns:
			desc:	The name of the item icon.
			type:	unicode
		"""

		return self.item_type

	def show_tab(self):

		"""
		desc:
			Is called when the tab becomes visible, and updated the contents.
		"""

		# The first time that the tab is shown, the view is determined. For
		# the controls view, nothing needs to be done, because this is the
		# default view after initialization.
		if not self._shown:
			self._shown = True
			self.main_window.ui.itemtree.inhibit_drag = True
			oslogger.debug(u'Invalid initial_view: %s' % self.initial_view)
			if self.initial_view == u'script':
				self.set_view_script()
			elif self.initial_view == u'split':
				self.set_view_split()
			elif self.initial_view != u'controls':
				oslogger.warning(u'Invalid initial_view: %s' % self.initial_view)
		self.extension_manager.fire(u'prepare_open_item', name=self.name)
		self.update_script()
		self.edit_widget()
		self.main_window.ui.itemtree.select_item(self.name, open_tab=False)
		self.extension_manager.fire(u'open_item', name=self.name)

	@requires_init
	def widget(self):

		"""
		returns:
			desc:	The widget that is added to the tabwidget.
			type:	QWidget
		"""

		return self.container_widget

	def init_edit_widget(self, stretch=True):

		"""
		desc:
			Builds the UI.

		keywords:
			stretch:
				desc:	Indicates whether a vertical stretch should be added to
						the bottom of the controls. This is necessary if the
						controls don't expand.
				type:	bool
		"""

		oslogger.debug(u'initializing controls for {}'.format(self.name))
		# Header widget
		self.header = header_widget.header_widget(self)
		self.header_hbox = QtWidgets.QHBoxLayout()
		self.header_item_icon = self.theme.qlabel(self.item_icon())
		self.header_hbox.addWidget(self.header_item_icon)
		self.header_hbox.addWidget(self.header)
		self.header_hbox.setContentsMargins(0, 0, 0, 0)
		self.header_hbox.setSpacing(12)
		# Maximize button
		self.button_toggle_maximize = QtWidgets.QPushButton(
			self.theme.qicon(u'view-fullscreen'), u'')
		self.button_toggle_maximize.setToolTip(_(u'Toggle pop-out'))
		self.button_toggle_maximize.setIconSize(QtCore.QSize(16, 16))
		self.button_toggle_maximize.clicked.connect(self.toggle_maximize)
		self.header_hbox.addWidget(self.button_toggle_maximize)
		# View button
		self.button_view = item_view_button(self)
		self.header_hbox.addWidget(self.button_view)
		# Help button
		self.button_help = QtWidgets.QPushButton(self.theme.qicon(u"help"), u"")
		self.button_help.setToolTip(
			_(u"Tell me more about the %s item") % self.item_type)
		self.button_help.setIconSize(QtCore.QSize(16, 16))
		self.button_help.clicked.connect(self.open_help_tab)
		self.header_hbox.addWidget(self.button_help)
		self.header_widget = QtWidgets.QWidget()
		self.header_widget.setLayout(self.header_hbox)
		# The edit_grid is the layout that contains the actual controls for the
		# items.
		self.edit_grid = QtWidgets.QFormLayout()
		if self.label_align == u'right':
			self.edit_grid.setLabelAlignment(QtCore.Qt.AlignRight)
		self.edit_grid.setFieldGrowthPolicy(
			QtWidgets.QFormLayout.FieldsStayAtSizeHint)
		self.edit_grid.setContentsMargins(0, 0, 0, 0)
		self.edit_grid.setVerticalSpacing(6)
		self.edit_grid.setHorizontalSpacing(12)
		self.edit_grid_widget = QtWidgets.QWidget()
		self.edit_grid_widget.setLayout(self.edit_grid)
		# The edit_vbox contains the edit_grid and the header widget
		self.edit_vbox = QtWidgets.QVBoxLayout()
		self.edit_vbox.addWidget(self.edit_grid_widget)
		self.edit_vbox.setContentsMargins(0, 0, 0, 0)
		self.edit_vbox.setSpacing(12)
		if stretch:
			self.edit_vbox.addStretch()
		self._edit_widget = QtWidgets.QWidget()
		self._edit_widget.setWindowIcon(self.theme.qicon(self.item_type))
		self._edit_widget.setLayout(self.edit_vbox)
		# The script widget is not initialized yet, to improve performance.
		# This will happen only when the script is shown.
		self._script_widget = None
		self._script_frame = QtWidgets.QWidget()
		# The container_widget is the top-level widget that is actually inserted
		# into the tab widget.
		self.splitter = qtitem_splitter(self)
		self.set_view_controls()
		self.splitter.splitterMoved.connect(self.splitter_moved)
		self.container_vbox = QtWidgets.QVBoxLayout()
		self.container_vbox.setContentsMargins(12, 12, 12, 12)
		self.container_vbox.setSpacing(18)
		self.container_vbox.addWidget(self.header_widget)
		self.container_vbox.addWidget(self.splitter)
		self.container_widget = QtWidgets.QWidget()
		self.container_widget.setLayout(self.container_vbox)
		self.container_widget.on_activate = self.show_tab
		self.container_widget.__item__ = self.name

	@wait_cursor
	def init_script_widget(self):

		from pyqode_extras.widgets import OpenSesameCodeEdit

		oslogger.debug(u'initializing script widget for {}'.format(self.name))
		self._script_widget = OpenSesameCodeEdit(self.main_window)
		self._script_widget.focusOutEvent = self._script_focus_out
		self.extension_manager.fire(
			u'register_editor',
			editor=self._script_widget
		)
		self._script_button = QtWidgets.QPushButton(
			self.theme.qicon(u'dialog-apply'),
			_(u'Apply')
		)
		self._script_button.is_apply_button = True
		self._script_button.clicked.connect(
			self.apply_script_changes_and_switch_view
		)
		self._script_button_layout = QtWidgets.QHBoxLayout()
		self._script_button_layout.setContentsMargins(0, 0, 0, 0)
		self._script_button_layout.addStretch()
		self._script_button_layout.addWidget(self._script_button)
		self._script_button_widget = QtWidgets.QWidget()
		self._script_button_widget.setLayout(self._script_button_layout)
		self._script_layout = QtWidgets.QVBoxLayout()
		self._script_layout.addWidget(self._script_button_widget)
		self._script_layout.addWidget(self._script_widget)
		self._script_layout.setAlignment(QtCore.Qt.AlignRight)
		self._script_layout.setContentsMargins(0, 12, 0, 0)
		self._script_layout.setSpacing(12)
		self._script_frame.setLayout(self._script_layout)
		self.update_script(use_cache=False)

	def _script_focus_out(self, event):

		"""
		desc:
			Is called when the script editor loses focus, so that changes
			can be applied.

		arguments:
			event: a QFocusEvent
		"""

		# When the apply button is pressed, the script is also applied. But this
		# also triggers a focusOutEvent. Hence, this check avoids applying the
		# script twice.
		w = self.main_window.focusWidget()
		if (
			not isinstance(w, QtWidgets.QPushButton) or
			not hasattr(w, 'is_apply_button')
		):
			self.apply_script_changes()

	def splitter_moved(self, pos, index):

		"""
		desc:
			Is called when the splitter handle is manually moved.

		arguments:
			pos:
				desc:	The splitter-handle position.
				type:	int
			index:
				desc:	The index of the splitter handle. Since there is only
						one handle, this is always 0.
				type:	int
		"""

		sizes = self.splitter.sizes()
		self.edit_size = sizes[0]
		self.script_size = sizes[1]
		if self.script_size == 0:
			self.button_view.set_view_icon(u'controls')
		elif self.edit_size == 0:
			self.button_view.set_view_icon(u'script')
		else:
			self.button_view.set_view_icon(u'split')

	def set_view_controls(self):

		"""
		desc:
			Puts the splitter in control view.
		"""

		self.splitter.setSizes([self.splitter.width(), 0])
		self.button_view.set_view_icon(u'controls')

	def set_view_script(self):

		"""
		desc:
			Puts the splitter in script view.
		"""

		if self._script_widget is None:
			self.init_script_widget()
		self.splitter.setSizes([0, self.splitter.width()])
		self.button_view.set_view_icon(u'script')

	def set_view_split(self):

		"""
		desc:
			Puts the splitter in split view.
		"""

		if self._script_widget is None:
			self.init_script_widget()
		width = self.splitter.width() / 2
		self.splitter.setSizes([width, width])
		self.button_view.set_view_icon(u'split')

	def update(self):

		"""
		desc:
			Updates both the script and the controls.
		"""

		# Items are updated when their tab is shown, so we don't need to update
		# them if they aren't shown.
		if self.tabwidget.current_item() != self.name:
			return False
		self.update_script()
		self.edit_widget()
		return True

	def update_script(self, use_cache=True):

		"""
		desc:
			Regenerates the script and updates the script widget.
		"""

		script = self.to_string()
		if use_cache and self.cached_script == script:
			return  # nothing changed
		self.cached_script = script
		# Normally, the script starts with a 'define' line and is indented by
		# a tab. We want to undo this, and present only unindented content.
		script = script[script.find(u'\t'):]
		script = textwrap.dedent(script)
		self.main_window.set_unsaved()
		if self._script_widget is not None:
			self._script_widget.setPlainText(
				script,
				u'text/generic',
				u'utf-8'
			)
		self.extension_manager.fire(u'change_item', name=self.name)

	def edit_widget(self, *deprecated, **_deprecated):

		"""
		desc:
			This function updates the controls based on the item state.
		"""

		self.auto_edit_widget()
		self.header.refresh()

	def apply_edit_changes(self, *deprecated, **_deprecated):

		"""
		desc:
			Applies changes to the graphical controls.
		"""

		self.auto_apply_edit_changes()
		self.update_script()
		self.set_clean()
		return True

	def apply_script_changes(self, *deprecated, **_deprecated):

		"""
		desc:
			Applies changes to the script.
		"""

		if not self.validate_script():
			self.set_view_script()
			return
		new_script = self._script_widget.toPlainText()
		old_script = self.to_string()
		self.from_string(new_script)
		if old_script != new_script:
			self.main_window.set_unsaved()
			self.cached_script = new_script
		self.edit_widget()

	def apply_script_changes_and_switch_view(self, *deprecated, **_deprecated):

		"""
		desc:
			Applies changes to the script if possible. If so, switches to the
			controls view.
		"""

		if not self.validate_script():
			self.set_view_script()
			return
		self.apply_script_changes()
		self.set_view_controls()

	def validate_script(self):

		"""
		desc:
			Checks whether the script is syntactically valid. If not, the
			offending line is highlighted if QProgEdit suppors setInvalid().

		returns:
			type:	bool
		"""

		script = self._script_widget.toPlainText()
		# First create a dummy item to see if the string can be parsed.
		try:
			self.validator(self.name, self.experiment, script)
			return True
		except Exception as e:
			# If an error occurs, we first parse the first line, then the first
			# and second, and so on, until we find the error.
			l = script.split(u'\n')
			for line_nr, line in enumerate(l):
				test_script = u'\n'.join(l[:line_nr])
				try:
					self.validator(self.name, self.experiment, test_script)
				except Exception as e_:
					if not isinstance(e_, osexception):
						e_ = osexception(e_)
					from pyqode.core.api.utils import TextHelper
					TextHelper(self._script_widget).select_lines(
						line_nr - 1,
						line_nr - 1
					)
					break
			self.console.write(e)
			self.extension_manager.fire(
				u'notify',
				message=_(u'Failed to parse script. See debug window for details'),
				category=u'warning',
				always_show=True
			)
			return False

	def set_validator(self):

		"""
		desc:
			Sets the validator class, that is, the class that is used to parse
			scripts to see if they are syntactically correct. Currently, we use
			the class that defines from_string().
		"""

		import inspect
		meth = self.from_string
		for cls in inspect.getmro(self.__class__):
			if meth.__name__ in cls.__dict__:
				break
		oslogger.debug(u'validator: %s' % cls)
		self.validator = cls

	def rename(self, from_name, to_name):

		"""
		desc:
			Handles renaming of an item (not necesarrily the current item).

		arguments:
			from_name:
				desc:	The old item name.
				type:	unicode
			to_name:
				desc:	The new item name
				type:	unicode
		"""

		if self.name != from_name:
			return
		self.name = to_name
		if self.container_widget is None:
			return
		self.container_widget.__item__ = self.name
		self.header.set_name(to_name)
		index = self.tabwidget.indexOf(self.widget())
		if index is not None:
			self.tabwidget.setTabText(index, to_name)

	def open_help_tab(self):

		"""
		desc:
			Opens a help tab.
		"""

		if self.help_url is None:
			self.tabwidget.open_help(self.item_type)
		else:
			self.tabwidget.open_osdoc(self.help_url)

	def toggle_maximize(self):

		"""
		desc:
			Toggles edit-widget maximization.
		"""

		if not self.maximized:
			# Always ignore close events. This is necessary, because otherwise
			# the pop-out widget can be closed without re-enabling the main
			# window.
			self.main_window.block_close_event = True
			self.container_widget.closeEvent = lambda e: e.ignore()
			self.container_widget.setParent(None)
			self.container_widget.setWindowFlags(QtCore.Qt.WindowStaysOnTopHint|\
				QtCore.Qt.WindowMaximizeButtonHint|\
				QtCore.Qt.CustomizeWindowHint)
			self.container_widget.showMaximized()
			self.container_widget.show()
			self.button_toggle_maximize.setIcon(
				self.theme.qicon(u'view-restore'))
		else:
			self.main_window.block_close_event = False
			self.container_widget.setParent(self.main_window)
			self.open_tab()
			self.button_toggle_maximize.setIcon(
				self.theme.qicon(u'view-fullscreen'))
		self.maximized = not self.maximized
		self.button_help.setDisabled(self.maximized)
		self.main_window.setDisabled(self.maximized)

	def delete(self, item_name, item_parent=None, index=None):

		"""
		desc:
			Is called when an item is deleted (not necessarily the current one).

		arguments:
			item_name:
				desc:	The name of the item to be deleted.
				type:	str

		keywords:
			item_parent:
				desc:	The name of the parent item.
				type:	str
			index:
				desc:	The index of the item in the parent.
				type:	int
		"""

		pass

	def build_item_tree(
		self,
		toplevel=None,
		items=[],
		max_depth=-1,
		extra_info=None
	):

		"""
		desc:
			Constructs an item tree.

		keywords:
			toplevel:
				desc:	The toplevel widget.
				type:	tree_base_item
			items:
				desc:	A list of item names that have already been added, to
						prevent recursion.
				tyep:	list

		returns:
			type:	tree_item_item
		"""

		widget = tree_item_item(self, extra_info=extra_info)
		items.append(self.name)
		if toplevel is not None:
			toplevel.addChild(widget)
		return widget

	def parents(self):

		"""
		returns:
			desc:	A list of all parents (names) of the current item.
			type:	list
		"""

		l = [self.name]
		for item in self.experiment.items:
			if self.experiment.items[item].is_child_item(self.name):
				l.append(item)
		return l

	def get_ready(self):

		"""
		desc:
			This function should be overridden to do any last-minute stuff that
			and item should do before an experiment is actually run, such as
			applying pending script changes.

		returns:
			desc:	True if some action has been taken, False if nothing was
					done.
			type:	bool
		"""

		if self._dirty:
			self.apply_edit_changes()
			return True
		return False

	def auto_edit_widget(self):

		"""
		desc:
			Updates the GUI controls based on the auto-widgets.
		"""

		for var, edit in self.auto_line_edit.items():
			if isinstance(var, int):
				continue
			if var in self.var:
				val = safe_decode(self.var.get(var, _eval=False))
			else:
				val = u''
			if val != edit.text():
				edit.setText(val)

		for var, combobox in self.auto_combobox.items():
			if isinstance(var, int):
				continue
			val = self.var.get(var, _eval=False, default=u'')
			i = combobox.findText(safe_decode(val))
			# Set the combobox to the select item
			if i >= 0:
				if i != combobox.currentIndex() or not combobox.isEnabled():
					combobox.setDisabled(False)
					combobox.setCurrentIndex(i)
			# If no value was specified, set the combobox to a blank item
			elif val == u'':
				if combobox.currentIndex() >= 0 or not combobox.isEnabled():
					combobox.setDisabled(False)
					combobox.setCurrentIndex(-1)
			# If an unknown value has been specified, notify the user
			else:
				if combobox.isEnabled():
					combobox.setDisabled(True)
					self.extension_manager.fire(u'notify',
						message=_(u'"%s" is set to a variable or '
						u'unknown value and can only be edited through '
						u'the script.') % var, category=u'info')

		for var, spinbox in list(self.auto_spinbox.items()) \
			+ list(self.auto_slider.items()):
			if isinstance(var, int):
				continue
			if var in self.var:
				val = self.var.get(var, _eval=False)
				if type(val) in (float, int):
					if spinbox.value() == val and spinbox.isEnabled():
						continue
					spinbox.setDisabled(False)
					try:
						spinbox.setValue(val)
					except Exception as e:
						self.experiment.notify(
							_(u"Failed to set control '%s': %s") % (var, e))
				else:
					if not spinbox.isEnabled():
						continue
					spinbox.setDisabled(True)
					self.extension_manager.fire(u'notify',
						message=_(u'"%s" is defined using '
						'variables and can only be edited through the '
						'script.') % var, category=u'info')

		for var, checkbox in self.auto_checkbox.items():
			if isinstance(var, int):
				continue
			if var in self.var:
				val = self.var.get(var, _eval=False)
				if val in [u'yes', u'no']:
					checkbox.setDisabled(False)
					checked = val == u'yes'
					if checked != checkbox.isChecked():
						checkbox.setChecked(checked)
				else:
					checkbox.setDisabled(True)
					self.extension_manager.fire(u'notify',
						message=_(u'"%s" is defined using '
						u'variables or has an invalid value, and can only be '
						u'edited through the script.') % var,
						category=u'info')

		for var, editor in self.auto_editor.items():
			if isinstance(var, int):
				continue
			val = safe_decode(self.var.get(var, _eval=False, default=u''))
			if val != editor.toPlainText():
				editor.setPlainText(val)

	def auto_apply_edit_changes(self):

		"""
		desc:
			Applies the auto-widget controls.
		"""

		for var, edit in self.auto_line_edit.items():
			if isinstance(var, int):
				continue
			if edit.isEnabled() and isinstance(var, basestring):
				val = edit.text().strip()
				if val:
					self.var.set(var, val)
					continue
				# If no text was entered, we use a default if available ...
				if hasattr(edit, u'default'):
					self.var.set(var, edit.default)
					continue
				# ... or unset the variable if no default is available.
				self.var.unset(var)

		for var, combobox in self.auto_combobox.items():
			if isinstance(var, int):
				continue
			if combobox.isEnabled() and isinstance(var, basestring):
				self.var.set(var, combobox.currentText())

		for var, spinbox in self.auto_spinbox.items():
			if isinstance(var, int):
				continue
			if spinbox.isEnabled() and isinstance(var, basestring):
				self.var.set(var, spinbox.value())

		for var, slider in self.auto_slider.items():
			if isinstance(var, int):
				continue
			if slider.isEnabled() and isinstance(var, basestring):
				self.var.set(var, slider.value())

		for var, checkbox in self.auto_checkbox.items():
			if isinstance(var, int):
				continue
			if checkbox.isEnabled() and isinstance(var, basestring):
				val = u'yes' if checkbox.isChecked() else u'no'
				self.var.set(var, val)

		for var, editor in self.auto_editor.items():
			if isinstance(var, int):
				continue
			if isinstance(var, basestring):
				self.var.set(var, editor.toPlainText())
		return True

	def auto_add_widget(self, widget, var=None, apply_func=None):

		"""
		desc:
			Adds a widget to the list of auto-widgets.

		arguments:
			widget:
			 	type:	QWidget

		keywords:
			var:	The name of the experimental variable to be linked to the
					widget, or None to use an automatically chosen name.
			type:	[str, NoneType]
		"""

		# Use the object id as a fallback name
		if var is None:
			var = id(widget)
		if apply_func is None:
			apply_func = self.apply_edit_changes
		self.set_focus_widget(widget)
		if (
			isinstance(widget, QtWidgets.QSpinBox) or
			isinstance(widget, QtWidgets.QDoubleSpinBox)
		):
			widget.editingFinished.connect(apply_func)
			widget.valueChanged.connect(self.set_dirty)
			self.auto_spinbox[var] = widget
		elif isinstance(widget, QtWidgets.QComboBox):
			widget.activated.connect(apply_func)
			self.auto_combobox[var] = widget
		elif (
			isinstance(widget, QtWidgets.QSlider) or
			isinstance(widget, QtWidgets.QDial)
		):
			widget.valueChanged.connect(apply_func)
			self.auto_slider[var] = widget
		elif (
			isinstance(widget, QtWidgets.QLineEdit) or
			isinstance(widget, pool_select)
		):
			widget.editingFinished.connect(apply_func)
			widget.textEdited.connect(self.set_dirty)
			self.auto_line_edit[var] = widget
		elif isinstance(widget, QtWidgets.QCheckBox):
			widget.clicked.connect(apply_func)
			self.auto_checkbox[var] = widget
		else:
			raise TypeError(u"Cannot auto-add widget of type %s" % widget)

	def set_dirty(self):

		"""
		desc:
			Indicates that the item's controls have changed since being last
			applied.
		"""

		self._dirty = True

	def set_clean(self):

		"""
		desc:
			Indicates that the item's controls have all been applied.
		"""

		self._dirty = False

	def children(self):

		"""
		returns:
			desc:	A list of children, including grand children, and so on.
			type:	list
		"""

		return []
		
	def direct_children(self):
		
		"""
		returns:
			desc:	A list of direct children, which does not include grand
					children, and so on.
			type:	list
		"""		
		
		return []

	def is_child_item(self, item_name):

		"""
		desc:
			Checks if an item is somewhere downstream from the current item
			in the experimental hierarchy.

		arguments:
			item_name:
				desc:	The name of the child item.
				type:	unicode

		returns:
			desc:	True if the current item is offspring of the item, False
					otherwise.
			type:	bool
		"""

		return False

	def insert_child_item(self, item_name, index=0):

		"""
		desc:
			Inserts a child item, if applicable to the item type.

		arguments:
			item_name:
				desc:	The name of the child item.
				type:	unicode

		keywords:
			index:
				desc:	The index of the child item.
				type:	int
		"""

		pass

	def remove_child_item(self, item_name, index=0):

		"""
		desc:
			Removes a child item, if applicable to the item type.

		arguments:
			item_name:
				desc:	The name of the child item.
				type:	unicode

		keywords:
			index:
				desc:	The index of the child item, if applicable. A negative
						value indicates all instances.
				type:	int
		"""

		pass


QtItem = qtitem

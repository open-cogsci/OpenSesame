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

from PyQt4 import QtCore, QtGui
import os.path
import sip
from libopensesame.exceptions import osexception
from libopensesame import debug, item
from libqtopensesame.widgets.item_view_button import item_view_button
from libqtopensesame.widgets.tree_item_item import tree_item_item
from libqtopensesame.widgets import header_widget, user_hint_widget
from libqtopensesame.misc import _
from libqtopensesame.misc.config import cfg

class qtitem(QtCore.QObject):

	"""Base class for the GUI controls of other items"""

	def __init__(self):

		"""Constructor"""

		QtCore.QObject.__init__(self)
		# The auto-widgets are stored in name -> (var, widget) dictionaries
		self.auto_line_edit = {}
		self.auto_combobox = {}
		self.auto_spinbox = {}
		self.auto_slider = {}
		self.auto_editor = {}
		self.auto_checkbox = {}
		self.init_edit_widget()
		self.lock = False
		self.maximized = False
		debug.msg(u'created %s' % self.name)

	@property
	def main_window(self):
		return self.experiment.main_window

	@property
	def theme(self):
		return self.experiment.main_window.theme

	@property
	def tabwidget(self):
		return self.experiment.main_window.tabwidget

	def open_tab(self):

		"""
		desc:
			Opens the tab if it wasn't yet open, and switches to it.
		"""

		self.main_window.tabwidget.add(self.widget(), self.item_type, self.name)

	def close_tab(self):

		"""
		desc:
			Closes the tab if it was open.
		"""

		self.main_window.tabwidget.remove(self.widget())

	def show_tab(self):

		"""
		desc:
			Is called when the tab becomes visible, and updated the contents.
		"""

		self.update_script()
		self.edit_widget()

	def widget(self):

		"""
		returns:
			desc:	The widget that is added to the tabwidget.
			type:	QWidget
		"""

		return self.container_widget

	def show_script(self):

		self._script_widget.setVisible(not self._script_widget.isVisible())

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

		# Header widget
		self.header = header_widget.header_widget(self)
		self.user_hint_widget = user_hint_widget.user_hint_widget(
			self.experiment.main_window, self)
		self.header_hbox = QtGui.QHBoxLayout()
		self.header_hbox.addWidget(self.experiment.label_image(self.item_type))
		self.header_hbox.addWidget(self.header)
		self.header_hbox.addStretch()
		self.header_hbox.setContentsMargins(0, 5, 0, 10)

		# Maximize button
		self.button_toggle_maximize = QtGui.QPushButton(
			self.theme.qicon(u'view-fullscreen'), u'')
		self.button_toggle_maximize.setToolTip(_(u'Toggle pop-out'))
		self.button_toggle_maximize.setIconSize(QtCore.QSize(16, 16))
		self.button_toggle_maximize.clicked.connect(self.toggle_maximize)
		self.header_hbox.addWidget(self.button_toggle_maximize)
		# View button
		self.button_view = item_view_button(self)
		self.header_hbox.addWidget(self.button_view)
		# Help button
		self.button_help = QtGui.QPushButton(self.experiment.icon(u"help"), u"")
		self.button_help.setToolTip(
			_(u"Tell me more about the %s item") % self.item_type)
		self.button_help.setIconSize(QtCore.QSize(16, 16))
		self.button_help.clicked.connect(self.open_help_tab)
		self.header_hbox.addWidget(self.button_help)

		self.header_widget = QtGui.QWidget()
		self.header_widget.setLayout(self.header_hbox)

		# The edit_grid is the layout that contains the actual controls for the
		# items.
		self.edit_grid = QtGui.QGridLayout()
		self.edit_grid.setColumnStretch(2, 2)
		self.edit_grid_widget = QtGui.QWidget()
		self.edit_grid.setMargin(0)
		self.edit_grid_widget.setLayout(self.edit_grid)

		# The edit_vbox contains the edit_grid and the header widget
		self.edit_vbox = QtGui.QVBoxLayout()
		self.edit_vbox.setMargin(5)
		self.edit_vbox.addWidget(self.user_hint_widget)
		self.edit_vbox.addWidget(self.edit_grid_widget)
		if stretch:
			self.edit_vbox.addStretch()
		self._edit_widget = QtGui.QWidget()
		self._edit_widget.setWindowIcon(self.experiment.icon(self.item_type))
		self._edit_widget.setLayout(self.edit_vbox)

		# The _script_widget contains the script editor
		from QProgEdit import QTabManager
		self._script_widget = QTabManager(handler=self.apply_script_changes,
			defaultLang=u'OpenSesame',
			handlerButtonText=_(u'Apply'),
			focusOutHandler=self.apply_script_changes, cfg=cfg)
		self._script_widget.addTab(u'Script')

		# The container_widget is the top-level widget that is actually inserted
		# into the tab widget.
		self.splitter = QtGui.QSplitter(QtCore.Qt.Vertical)
		self.splitter.addWidget(self._edit_widget)
		self.splitter.addWidget(self._script_widget)
		self.set_view_controls()
		self.splitter.splitterMoved.connect(self.splitter_moved)
		self.container_vbox = QtGui.QVBoxLayout()
		self.container_vbox.addWidget(self.header_widget)
		self.container_vbox.addWidget(self.splitter)
		self.container_widget = QtGui.QWidget()
		self.container_widget.setLayout(self.container_vbox)
		self.container_widget.on_activate = self.show_tab

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

		self.splitter.setSizes([0, self.splitter.width()])
		self.button_view.set_view_icon(u'script')

	def set_view_split(self):

		"""
		desc:
			Puts the splitter in split view.
		"""

		self.splitter.setSizes([self.splitter.width()/2,
			self.splitter.width()/2])
		self.button_view.set_view_icon(u'split')

	def update(self):

		"""
		desc:
			Updates both the script and the controls.
		"""

		self.update_script()
		self.edit_widget()

	def update_script(self):

		"""
		desc:
			Regenerates the script and updates the script widget.
		"""

		# Normally, the script starts with a 'define' line and is indented by
		# a tab. We want to undo this, and present only unindented content.
		import textwrap
		script = self.to_string()
		script = script[script.find(u'\t'):]
		script = textwrap.dedent(script)
		self._script_widget.setText(script)

	def edit_widget(self, *deprecated, **_deprecated):

		"""
		desc:
			This function updates the controls based on the item state.
		"""

		debug.msg()
		self.auto_edit_widget()

	def apply_edit_changes(self, *deprecated, **_deprecated):

		"""
		desc:
			Applies changes to the graphical controls.
		"""

		debug.msg()
		self.auto_apply_edit_changes()
		self.update_script()
		return True

	def apply_script_changes(self, *deprecated, **_deprecated):

		"""
		desc:
			Applies changes to the script, by re-parsing the item from string.
		"""

		debug.msg()
		old_script = self.to_string()
		new_script = self._script_widget.text()
		try:
			self.from_string(new_script)
		except osexception as e:
			self.experiment.notify(e.html())
			self.main_window.print_debug_window(e)
			self.from_string(old_script)
		self.edit_widget()

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
		self.header.set_name(to_name)
		index = self.tabwidget.indexOf(self.widget())
		if index != None:
			self.tabwidget.setTabText(index, to_name)

	def open_help_tab(self):

		"""
		desc:
			Opens a help tab.
		"""

		self.experiment.main_window.ui.tabwidget.open_help(self.item_type)

	def toggle_maximize(self):

		"""
		desc:
			Toggles edit-widget maximization.
		"""

		if not self.maximized:
			self.container_widget.setParent(None)
			self.container_widget.setWindowFlags(QtCore.Qt.WindowStaysOnTopHint|\
				QtCore.Qt.WindowMaximizeButtonHint)
			self.container_widget.showMaximized()
			self.container_widget.show()
			self.button_toggle_maximize.setIcon(
				self.theme.qicon(u'view-restore'))
		else:
			self.container_widget.setParent(self.main_window)
			self.open_tab()
			self.button_toggle_maximize.setIcon(
				self.theme.qicon(u'view-fullscreen'))
		self.maximized = not self.maximized
		self.button_edit_script.setDisabled(self.maximized)
		self.user_hint_widget.disable(self.maximized)
		self.button_help.setDisabled(self.maximized)
		self.main_window.setDisabled(self.maximized)

	def delete(self, item_name, item_parent=None, index=None):

		"""
		Delete an item (not necessarily the current one)

		Arguments:
		item_name -- the name of the item to be deleted

		Keywords arguments:
		item_parent -- the parent item (default=None)
		index -- the index of the item in the parent (default=None)
		"""

		pass

	def build_item_tree(self, toplevel=None, items=[], max_depth=-1,
		extra_info=None):

		"""
		Construct an item tree

		Keyword arguments:
		toplevel -- the toplevel widget (default = None)
		items -- a list of items that have been added, to prevent recursion
				 (default=[])
		"""

		widget = tree_item_item(self, extra_info=extra_info)
		items.append(self.name)
		if toplevel != None:
			toplevel.addChild(widget)
		return widget

	def parents(self):

		"""
		Creates a list of all the items	that the current sequences is connected
		to upstream

		Returns:
		A list of item names
		"""

		l = [self.name]
		for item in self.experiment.items:
			if self.experiment.items[item].is_child_item(self.name):
				l.append(item)
		return l

	def variable_vars(self, exclude=[]):

		"""
		Determines if one of the variables of the current item is defined in
		terms of another variable

		Keywords arguments:
		exclude -- a list of variables that should not be checked

		Returns:
		True if there are variably defined variables, False otherwise
		"""

		for var in self.variables:
			if var not in exclude:
				val = self.variables[var]
				if self.experiment.varref(val):
					return True
		return False

	def get_ready(self):

		"""
		This function should be overridden to do any last-minute stuff that
		and item should do before an experiment is actually run, such as
		applying pending script changes.

		Returns:
		True if some action has been taken, False if nothing was done
		"""

		return False

	def auto_edit_widget(self):

		"""Update the GUI controls based on the auto-widgets"""

		debug.msg()
		for var, edit in self.auto_line_edit.iteritems():
			if self.has(var):
				edit.setText(self.unistr(self.get(var, _eval=False)))
			else:
				edit.setText(u'')

		for var, combobox in self.auto_combobox.iteritems():
			val = self.get_check(var, _eval=False, default=u'')
			i = combobox.findText(self.unistr(self.get(var, _eval=False)))
			# Set the combobox to the select item
			if i >= 0:
				combobox.setDisabled(False)
				combobox.setCurrentIndex(i)
			# If no value was specified, set the combobox to a blank item
			elif val == u'':
				combobox.setDisabled(False)
				combobox.setCurrentIndex(-1)
			# If an unknown value has been specified, notify the user
			else:
				combobox.setDisabled(True)
				self.user_hint_widget.add(_(u'"%s" is set to a '
					u'variable or unknown value and can only be edited through '
					u'the script.' % var))

		for var, spinbox in self.auto_spinbox.iteritems():
			if self.has(var):
				val = self.get(var, _eval=False)
				if type(val) in (float, int):
					spinbox.setDisabled(False)
					try:
						spinbox.setValue(val)
					except Exception as e:
						self.experiment.notify(_( \
							u"Failed to set control '%s': %s") % (var, e))
				else:
					spinbox.setDisabled(True)
					self.user_hint_widget.add(_( \
						u'"%s" is defined using variables and can only be edited through the script.' \
						% var))

		for var, slider in self.auto_slider.iteritems():
			if self.has(var):
				val = self.get(var, _eval=False)
				if type(val) in (float, int):
					slider.setDisabled(False)
					try:
						slider.setValue(val)
					except Exception as e:
						self.experiment.notify(_( \
							u"Failed to set control '%s': %s") % (var, e))
				else:
					slider.setDisabled(True)
					self.user_hint_widget.add(_( \
						u'"%s" is defined using variables and can only be edited through the script.' \
						% var))

		for var, checkbox in self.auto_checkbox.iteritems():
			if self.has(var):
				try:
					checkbox.setChecked(self.get(var, _eval=False) == u"yes")
				except Exception as e:
					self.experiment.notify(_(u"Failed to set control '%s': %s") \
						% (var, e))

		for var, qprogedit in self.auto_editor.iteritems():
			if self.has(var):
				try:
					qprogedit.setText(self.unistr(self.get(var, _eval=False)))
				except Exception as e:
					self.experiment.notify(_(u"Failed to set control '%s': %s") \
						% (var, e))

	def sanitize_check(self, s, strict=False, allow_vars=True, notify=True):

		"""
		Checks whether a string is sane (i.e. unchanged by sanitize()) and
		optionally presents a warning.

		Arguments:
		s			--	The string to check.

		Keyword arguments:
		strict		--	See sanitize().
		allow_vars	--	See sanitize().
		notify		--	Indicates whether a notification should be presented if
						the string is not sane.

		Returns:
		True if s is sane, False otherwise.
		"""

		sane = s == self.sanitize(s, strict=strict, allow_vars=allow_vars)
		if not sane and notify:
			if strict:
				self.experiment.notify(
					_(u'All non-alphanumeric characters except underscores have been stripped'))
			else:
				self.experiment.notify(
					_(u'The following characters are not allowed and have been stripped: double-quote ("), backslash (\), and newline'))
		return sane

	def auto_apply_edit_changes(self, rebuild=True):

		"""
		Apply the auto-widget controls

		Keyword arguments:
		rebuild -- deprecated (does nothing) (default=True)
		"""

		debug.msg()
		for var, edit in self.auto_line_edit.iteritems():
			if edit.isEnabled() and isinstance(var, basestring):
				val = unicode(edit.text()).strip()
				if val != u"":
					self.set(var, val)

				# If the variable has no value, we assign a default value if it
				# has been specified, and unset it otherwise.
				elif hasattr(edit, u"default"):
					self.set(var, edit.default)
				else:
					self.unset(var)

		for var, combobox in self.auto_combobox.iteritems():
			if combobox.isEnabled() and isinstance(var, basestring):
				self.set(var, unicode(combobox.currentText()))

		for var, spinbox in self.auto_spinbox.iteritems():
			if spinbox.isEnabled() and isinstance(var, basestring):
				self.set(var, spinbox.value())

		for var, slider in self.auto_slider.iteritems():
			if slider.isEnabled() and isinstance(var, basestring):
				self.set(var, slider.value())

		for var, checkbox in self.auto_checkbox.iteritems():
			if checkbox.isEnabled() and isinstance(var, basestring):
				if checkbox.isChecked():
					val = u"yes"
				else:
					val = u"no"
				self.set(var, val)

		for var, qprogedit in self.auto_editor.iteritems():
			if isinstance(var, basestring):
				self.set(var, qprogedit.text())

		return True

	def auto_add_widget(self, widget, var=None):

		"""
		Add a widget to the list of auto-widgets

		Arguments:
		widget -- a QWidget

		Keyword arguments:
		var -- the variable to be linked to the widget (default=None)
		"""

		# Use the object id as a fallback name
		if var == None:
			var = id(widget)
		debug.msg(var)

		if isinstance(widget, QtGui.QSpinBox) or isinstance(widget,
			QtGui.QDoubleSpinBox):
			widget.editingFinished.connect(self.apply_edit_changes)
			self.auto_spinbox[var] = widget

		elif isinstance(widget, QtGui.QComboBox):
			widget.activated.connect(self.apply_edit_changes)
			self.auto_combobox[var] = widget

		elif isinstance(widget, QtGui.QSlider):
			widget.editingFinished.connect(self.apply_edit_changes)
			self.auto_slider[var] = widget

		elif isinstance(widget, QtGui.QLineEdit):
			widget.editingFinished.connect(self.apply_edit_changes)
			self.auto_line_edit[var] = widget

		elif isinstance(widget, QtGui.QCheckBox):
			widget.clicked.connect(self.apply_edit_changes)
			self.auto_checkbox[var] = widget

		else:
			raise Exception(u"Cannot auto-add widget of type %s" % widget)

	def clean_cond(self, cond, default=u'always'):

		"""
		Cleans a conditional statement. May raise a dialog box if problems are
		encountered.

		Arguments:
		cond	--	A (potentially filthy) conditional statement.

		Keyword arguments:
		default	--	A default value to use for empty

		Returns:
		cond	--	A clean conditional statement conditional statements.
					(default=u'always')
		"""

		cond = self.unistr(cond)
		if not self.sanitize_check(cond):
			cond = self.sanitize(cond)
		if cond.strip() == u'':
			cond = default
		try:
			self.compile_cond(cond)
		except osexception as e:
			self.experiment.notify( \
				u'Failed to compile conditional statement "%s": %s' % (cond, e))
			return default
		return cond

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
				desc:	The index of the child item, if applicable.
				type:	int
		"""

		pass

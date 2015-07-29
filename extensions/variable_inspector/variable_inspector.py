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
from libqtopensesame.widgets.base_widget import base_widget
from libqtopensesame.extensions import base_extension
from libqtopensesame.misc import _
from libqtopensesame.misc.config import cfg
from PyQt4 import QtCore, QtGui

class table_cell(QtGui.QTableWidgetItem):

	"""
	desc:
		A sortable QTableWidgetItem.
	"""

	def __init__(self, text, info):

		"""
		desc:
			Constructor.

		arguments:
			text:		The cell text.
			sort_key:	The key to use for sorting.
		"""

		a = QtCore.Qt.AlignLeft
		f = QtGui.QFont()
		if info[u'alive']:
			f.setBold(True)
		if text is None:
			text = u''
		elif isinstance(text, list):
			text = u','.join(text)
		elif isinstance(text, int) or isinstance(text, float):
			text = str(text)
			a = QtCore.Qt.AlignRight
		QtGui.QTableWidgetItem.__init__(self, text)
		self.setFont(f)
		self.setTextAlignment(a)

class variable_inspector_widget(base_widget):

	def __init__(self, main_window, ext):

		super(variable_inspector_widget, self).__init__(main_window,
			ui=u'extensions.variable_inspector.variable_inspector')
		self.ext = ext
		self.ui.edit_variable_filter.textChanged.connect(self.refresh)
		self.ui.button_help_variables.clicked.connect(self.ext.open_help)
		self.ui.button_reset.clicked.connect(self.ext.reset)
		self.refresh()

	def var(self):

		d = self.main_window.console.get_workspace_globals()
		if u'var' in d and hasattr(d[u'var'], u'inspect'):
			return d[u'var'], True
		return self.experiment.var, False

	def refresh(self):

		# Remember the view position
		scrollpos = self.ui.table_variables.verticalScrollBar().sliderPosition()
		col = self.ui.table_variables.currentColumn()
		row = self.ui.table_variables.currentRow()
		filt = str(self.ui.edit_variable_filter.text())
		var_store, alive = self.var()
		self.ui.label_status.setText(
			_(u'Experiment status: <b>%s</b>' % self.main_window.run_status()))
		if alive and self.main_window.run_status() == u'finished':
			self.ui.widget_reset_message.show()
		else:
			self.ui.widget_reset_message.hide()
		# Filter the variables if necessary
		if len(filt) > 1:
			d = {}
			for var, info in var_store.inspect().items():
				if filt in var or (info[u'value'] is not None and \
					filt in str(info[u'value'])) or \
					filt in u' '.join(info[u'source']):
					d[var] = info
		else:
			d = var_store.inspect()
		# Populate the table
		self.ui.table_variables.setRowCount(len(d))
		for i, var in enumerate(sorted(d.keys())):
			info = d[var]
			self.ui.table_variables.setItem(i, 0, table_cell(var, info))
			self.ui.table_variables.setItem(i, 1, table_cell(info['value'],
				info))
			self.ui.table_variables.setItem(i, 2, table_cell(info['source'],
				info))
		# Restore the view position
		self.ui.table_variables.setCurrentCell(row, col)
		self.ui.table_variables.verticalScrollBar().setSliderPosition(scrollpos)

	def set_focus(self):

		"""
		desc:
			Sets the focus on the filter widget.
		"""

		self.ui.edit_variable_filter.setFocus()

class variable_inspector_dockwidget(QtGui.QDockWidget):

	def __init__(self, main_window, ext):

		super(variable_inspector_dockwidget, self).__init__(
			_(u'Variable inspector'), main_window)
		self.setWidget(variable_inspector_widget(main_window, ext))
		self.setObjectName(u'variable_inspector')

class variable_inspector(base_extension):

	"""
	desc:
		An example extension that lists all available events.
	"""

	def event_startup(self):

		self.dock_widget = variable_inspector_dockwidget(self.main_window, self)
		self.dock_widget.visibilityChanged.connect(self.set_visible)
		self.main_window.addDockWidget(QtCore.Qt.RightDockWidgetArea,
			self.dock_widget)
		self.set_visible(cfg.variable_inspector_visible)

	def open_help(self):

		self.notification_tab(u'variable_inspector.md',
			title=_(u'Help: Variable inspector'))

	def set_visible(self, visible):

		cfg.variable_inspector_visible = visible
		self.set_checked(visible)
		if visible:
			self.dock_widget.show()
		else:
			self.dock_widget.hide()

	def activate(self):

		self.set_visible(not cfg.variable_inspector_visible)

	def refresh(self):
		if self.dock_widget.isVisible():
			self.dock_widget.widget().refresh()

	def reset(self):
		self.main_window.console.reset()

	def event_change_item(self, name):
		self.refresh()

	def event_pause_experiment(self):
		self.refresh()

	def event_run_experiment(self, fullscreen):
		self.refresh()

	def event_end_experiment(self):
		self.refresh()

	def event_reset_console(self):
		self.refresh()

	def event_open_experiment(self, path):
		self.refresh()

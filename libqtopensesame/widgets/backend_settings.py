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
import sip
from libqtopensesame.misc import _
from libqtopensesame.widgets.base_widget import base_widget
from libqtopensesame.misc.base_subcomponent import base_subcomponent

class backend_settings(base_widget):

	def __init__(self, main_window):

		super(backend_settings, self).__init__(main_window,
			ui=u'widgets.backend_settings')
		self.tab_name = '__backend_settings__'

		for backend_type in ["canvas", "keyboard", "mouse", "synth", \
			"sampler"]:
			backend = self.experiment.get("%s_backend" \
				% backend_type)
			backend_module = __import__(u'openexp._%s.%s' % (backend_type, \
				backend), fromlist=[u'dummy'])
			_backend = getattr(backend_module, backend)
			group = getattr(self.ui, u'group_%s' % backend_type)
			layout = getattr(self.ui, u'layout_%s' % backend_type)
			label = getattr(self.ui, u'label_%s' % backend_type)
			# Horribly ugly way to clear the previous settings
			while layout.count() > 1:
				w = layout.itemAt(1)
				layout.removeItem(w)
				w.widget().hide()
				sip.delete(w)

			if not hasattr(_backend, "settings") or _backend.settings == \
				None:
				label.setText(_("No settings for %s") % backend)
			else:
				label.setText(_("Settings for %s:") % backend)
				layout.addWidget(settings_widget(self.main_window,
					_backend.settings))

class settings_edit(QtGui.QLineEdit, base_subcomponent):

	"""An edit widget for a single variable"""

	def __init__(self, main_window, var, val):

		"""
		Constructor

		Arguments:
		experiment -- the experiment
		var -- the variable name
		val -- the variable value

		Keywords arguments:
		parent -- parent QWidget (default=None)
		"""

		super(settings_edit, self).__init__()
		self.setup(main_window)
		self.setText(self.experiment.unistr(val))
		self.var = var
		self.editingFinished.connect(self.apply_setting)

	def apply_setting(self):

		"""Apply changes"""

		self.experiment.set(self.var, self.experiment.sanitize(self.text()))

class settings_widget(base_widget):

	"""A widget containing a number of settings"""

	def __init__(self, main_window, settings):

		"""
		Constructor

		Arguments:
		experiment -- the experiment
		settings -- the settings dictionary

		Keywords arguments:
		parent -- parent QWidget (default=None)
		"""

		super(settings_widget, self).__init__(main_window)
		self.settings = settings
		self.layout = QtGui.QFormLayout(self)
		self.layout.setFieldGrowthPolicy(QtGui.QFormLayout.FieldsStayAtSizeHint)
		self.setLayout(self.layout)
		for var, desc in settings.items():
			if self.experiment.has(var):
				val = self.experiment.get(var)
			else:
				val = desc[u"default"]
			label = QtGui.QLabel()
			label.setText(
				u"%(name)s<br /><small><i>%(description)s</i></small>" % desc)
			label.setTextFormat(QtCore.Qt.RichText)
			edit = settings_edit(self.main_window, var, val)
			self.layout.addRow(label, edit)

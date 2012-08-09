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
from libqtopensesame.ui.backend_settings_ui import \
	Ui_widget_backend_settings

class backend_settings(QtGui.QWidget):

	def __init__(self, main_window):
	
		self.main_window = main_window
		QtGui.QWidget.__init__(self, main_window)
		self.ui = Ui_widget_backend_settings()
		self.ui.setupUi(self)
		self.main_window.theme.apply_theme(self)
		self.tab_name = '__backend_settings__'
		
		for backend_type in ["canvas", "keyboard", "mouse", "synth", \
			"sampler"]:
			backend = self.main_window.experiment.get("%s_backend" \
				% backend_type)
			exec("from openexp._%s.%s import %s as _backend" % ( \
				backend_type, backend, backend))
			group = eval("self.ui.group_%s" % backend_type)
			layout = eval("self.ui.layout_%s" % backend_type)
			label = eval("self.ui.label_%s" % backend_type)

			# Horribly ugly wayo clear the previous settings
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
				layout.addWidget(settings_widget( \
					self.main_window.experiment, _backend.settings, self))
					
class settings_edit(QtGui.QLineEdit):

	"""An edit widget for a single variable"""

	def __init__(self, experiment, var, val, parent=None):

		"""
		Constructor

		Arguments:
		experiment -- the experiment
		var -- the variable name
		val -- the variable value

		Keywords arguments:
		parent -- parent QWidget (default=None)
		"""

		QtGui.QLineEdit.__init__(self, str(val))
		self._parent = parent
		self.var = var
		self.experiment = experiment
		self.editingFinished.connect(self.apply_setting)

	def apply_setting(self):

		"""Apply changes"""

		self.experiment.set(self.var, self.experiment.sanitize(self.text()))
		self._parent._parent.main_window.refresh()

class settings_widget(QtGui.QWidget):

	"""A widget containing a number of settings"""

	def __init__(self, experiment, settings, parent=None):

		"""
		Constructor

		Arguments:
		experiment -- the experiment
		settings -- the settings dictionary

		Keywords arguments:
		parent -- parent QWidget (default=None)
		"""

		QtGui.QWidget.__init__(self, parent)
		self._parent = parent
		self.experiment = experiment
		self.settings = settings
		self.layout = QtGui.QFormLayout(self)
		self.layout.setFieldGrowthPolicy(QtGui.QFormLayout.FieldsStayAtSizeHint)
		self.setLayout(self.layout)
		for var, desc in settings.items():
			if self.experiment.has(var):
				val = self.experiment.get(var)
			else:
				val = desc["default"]
			label = QtGui.QLabel()
			label.setText("%(name)s<br /><small><i>%(description)s</i></small>" % desc)
			label.setTextFormat(QtCore.Qt.RichText)
			edit = settings_edit(self.experiment, var, val, self)
			self.layout.addRow(label, edit)

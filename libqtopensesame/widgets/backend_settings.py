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
from qtpy import QtCore, QtWidgets
from libqtopensesame.widgets.base_widget import BaseWidget
from libqtopensesame.misc.base_subcomponent import BaseSubcomponent
from openexp import backend
from libqtopensesame.misc.translate import translation_context
_ = translation_context(u'backend_settings', category=u'core')


class BackendSettings(BaseWidget):

    def __init__(self, main_window):

        super().__init__(main_window, ui=u'widgets.backend_settings')
        self.tab_name = u'__backend_settings__'
        for backend_type in backend._backend_types:
            try:
                _backend = backend.get_backend_class(self.experiment,
                                                     backend_type)
            except:
                _backend = None
            layout = getattr(self.ui, u'layout_%s' % backend_type)
            label = getattr(self.ui, u'label_%s' % backend_type)
            # Horribly ugly way to clear the previous settings
            while layout.count() > 1:
                w = layout.itemAt(1)
                layout.removeItem(w)
                w.widget().hide()
            if _backend is None:
                label.setText(_(u"Failed to load backend"))
            elif not hasattr(_backend, u"settings") or _backend.settings == \
                    None:
                label.setText(_(u"No settings for %s") % _backend.__name__)
            else:
                label.setText(_(u"Settings for %s:") % _backend.__name__)
                layout.addWidget(settings_widget(self.main_window,
                                                 _backend.settings))


class SettingsEdit(QtWidgets.QLineEdit, BaseSubcomponent):

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
        super().__init__()
        self.setup(main_window)
        self.setText(safe_decode(val))
        self.var = var
        self.editingFinished.connect(self.apply_setting)

    def apply_setting(self):
        """Apply changes"""
        self.experiment.var.set(
            self.var, self.experiment.syntax.sanitize(self.text()))


class SettingsWidget(BaseWidget):

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
        super().__init__(main_window)
        self.settings = settings
        self.layout = QtWidgets.QFormLayout(self)
        self.layout.setFieldGrowthPolicy(
            QtWidgets.QFormLayout.FieldsStayAtSizeHint)
        self.setLayout(self.layout)
        for var, desc in settings.items():
            if var in self.experiment.var:
                val = self.experiment.var.get(var)
            else:
                val = desc[u"default"]
            label = QtWidgets.QLabel()
            label.setText(
                u"%(name)s<br /><small><i>%(description)s</i></small>" % desc)
            label.setTextFormat(QtCore.Qt.RichText)
            edit = settings_edit(self.main_window, var, val)
            self.layout.addRow(label, edit)


# Alias for backwards compatibility
backend_settings = BackendSettings
settings_edit = SettingsEdit
settings_widget = SettingsWidget

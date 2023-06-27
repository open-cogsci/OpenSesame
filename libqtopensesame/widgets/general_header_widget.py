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
from libqtopensesame.widgets.header_widget import HeaderWidget
from libqtopensesame.misc.translate import translation_context
_ = translation_context('general_header_widget', category='core')


class GeneralHeaderWidget(HeaderWidget):
    """The widget containing the clickable title and description of the
    experiment.
    
    Parameters
    ----------
    general_tab
        A general_properties object.
    main_window
        A qtopensesame object.
    """
    def __init__(self, general_tab, main_window):
        super().__init__(main_window.experiment)
        self.general_tab = general_tab

    def refresh(self):
        """Updates the header so that it's content match the item."""
        self.set_name(self.experiment.var.title)
        self.set_desc(self.experiment.var.description)
        
    def set_name(self, name, label_type=None):
        """Sets the name.

        Parameters
        ----------
        name
            A name
        """
        super().set_name(name, _('experiment properties'))

    def apply_name(self):
        """Applies the name change and revert the edit control back to the
        static label.
        """
        if self.label_name.isVisible():
            return
        self.label_name.show()
        self.label_type.show()
        self.edit_name.hide()
        self.general_tab.apply_changes()
        self.refresh()

    def apply_desc(self):
        """Applies the description change and revert the edit back to the
        label.
        """
        if self.label_desc.isVisible():
            return
        self.label_desc.show()
        self.edit_desc.hide()
        self.general_tab.apply_changes()
        self.refresh()


# Alias for backwards compatibility
general_header_widget = GeneralHeaderWidget

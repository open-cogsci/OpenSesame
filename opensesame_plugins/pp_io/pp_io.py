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
from libopensesame import item
from libqtopensesame import qtplugin

from qtpy import QtWidgets, QtCore

import warnings
import os

import imp

try:
    if os.name == 'posix':
        # import the local modified version of pyparallel
        # that allows for non-exclusive connections to the parport
        path_to_file = os.path.join(
            os.path.dirname(__file__), "parallelppdev.py")
        parallel = imp.load_source('parallel', path_to_file)
        #import parallelppdev as parallel
    else:
        import parallel
except ImportError:
    warnings.warn(
        "The parallel module could not load, please make sure you have installed pyparallel.")

# we only want one instance of pp, so here's a global var
_pp = None


class pp_io(item.item):

    """
    This class (the class with the same name as the module)
    handles the basic functionality of the item. It does
    not deal with GUI stuff.
    """
    def __init__(self, name, experiment, string=None):
        """
        Constructor
        """
        # The item_typeshould match the name of the module
        self.item_type = "pp_io"

        # Provide a short accurate description of the item's functionality
        self.description = "Allows setting pins on the parallel port"

        # Set some item-specific variables
        self.value = 1
        self.duration = 1

        # The parent handles the rest of the contruction
        item.item.__init__(self, name, experiment, string)

        # add cleanup code
        self.experiment.cleanup_functions.append(self.clean_up_the_mess)

    def clean_up_the_mess(self):
        global _pp
        if self.experiment.debug:
            print("pp_io.clean_up_this_mess(): deleting _pp")
        if not _pp is None:
            del _pp

    def prepare(self):
        """
        Prepare the item. In this case this means doing little.
        """
        # Pass the word on to the parent
        item.item.prepare(self)

        # get the global pp instance and initialize it if
        # necessary
        global _pp
        if _pp is None:
            try:
                _pp = parallel.Parallel()
            except OSError:
                warnings.warn("Could not access /dev/parport0.")
        self.pp = _pp

        # This function prepares a self._duration_func() function based
        # on the compensation and duration variables.
        self.prepare_duration()

        # Report success
        return True

    def run(self):
        """
        Run the item. In this case this means putting the offline canvas
        to the display and waiting for the specified duration.
        """
        # Set the pp value
        if not self.pp is None:
            self.set_item_onset(self.pp.setData(self.value))

        # This function has been prepared by self.prepare_duration()
        self._duration_func()

        # unless duration was zero, turn it off
        if not self.pp is None and self.duration != 0:
            self.pp.setData(0)

        # Report success
        return True


class qtpp_io(pp_io, qtplugin.qtplugin):

    """
    This class (the class named qt[name of module] handles
    the GUI part of the plugin. For more information about
    GUI programming using qtpy, see:
    <http://www.riverbankcomputing.co.uk/static/Docs/qtpy/html/classes.html>
    """
    def __init__(self, name, experiment, string=None):
        """
        Constructor
        """
        # Pass the word on to the parents
        pp_io.__init__(self, name, experiment, string)
        qtplugin.qtplugin.__init__(self, __file__)

    def init_edit_widget(self):
        """
        This function creates the controls for the edit
        widget.
        """
        # Lock the widget until we're doing creating it
        self.lock = True

        # Pass the word on to the parent
        qtplugin.qtplugin.init_edit_widget(self, False)

        # Create the controls
        #
        # A number of convenience functions are available which
        # automatically create controls, which are also automatically
        # updated and applied. If you set the varname to None, the
        # controls will be created, but not automatically updated
        # and applied.
        #
        # qtplugin.add_combobox_control(varname, label, list_of_options)
        # - creates a QComboBox
        # qtplugin.add_line_edit_control(varname, label)
        # - creates a QLineEdit
        # qtplugin.add_spinbox_control(varname, label, min, max, suffix = suffix, prefix = prefix)

        self.add_spinbox_control(
            "value", "Value", 0, 255, tooltip="Value to set port")
        self.add_line_edit_control(
            "duration", "Duration", tooltip="Expecting a value in milliseconds, 'keypress' or 'mouseclick'")

        # Add a stretch to the edit_vbox, so that the controls do not
        # stretch to the bottom of the window.
        self.edit_vbox.addStretch()

        # Unlock
        self.lock = True

    def apply_edit_changes(self):
        """
        Set the variables based on the controls
        """
        # Abort if the parent reports failure of if the controls are locked
        if not qtplugin.qtplugin.apply_edit_changes(self) or self.lock:
            return False

        # Refresh the main window, so that changes become visible everywhere
        self.experiment.main_window.refresh(self.name)

        # Report success
        return True

    def edit_widget(self):
        """
        Set the controls based on the variables
        """
        # Lock the controls, otherwise a recursive loop might aris
        # in which updating the controls causes the variables to be
        # updated, which causes the controls to be updated, etc...
        self.lock = True

        # Let the parent handle everything
        qtplugin.qtplugin.edit_widget(self)

        # Unlock
        self.lock = False

        # Return the _edit_widget
        return self._edit_widget

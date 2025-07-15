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
import os
import sys
import re
import traceback
import tempfile
from qtpy import QtWidgets, QtCore
from libqtopensesame.misc.config import cfg
from libopensesame.oslogging import oslogger
from libopensesame.experiment import Experiment
from libopensesame.py3compat import safe_decode
from libqtopensesame.misc.translate import translation_context
_ = translation_context('base_runner', category='core')


class ExperimentSettingsDialog(QtWidgets.QDialog):
    """A dialog for collecting experiment settings (subject number, logfile,
    fullscreen).
    """
    
    def __init__(self, parent, default_subject_nr, default_logfile,
                 default_fullscreen):
        super().__init__(parent)
        self.setWindowTitle(_('Experiment Settings'))        
        # Hide window decoration
        self.setWindowFlags(QtCore.Qt.Dialog | QtCore.Qt.FramelessWindowHint)
        self.setModal(True)
        
        # Optional: Remove window decorations for a cleaner look
        # Uncomment the next line if you want a frameless dialog
        # self.setWindowFlags(QtCore.Qt.FramelessWindowHint | QtCore.Qt.Dialog)
        
        # Create widgets
        layout = QtWidgets.QVBoxLayout()
        
        # Subject number
        subject_layout = QtWidgets.QHBoxLayout()
        subject_label = QtWidgets.QLabel(_('Subject number:'))
        subject_label.setFixedWidth(120)
        self.subject_spinbox = QtWidgets.QSpinBox()
        self.subject_spinbox.setMinimum(0)
        self.subject_spinbox.setMaximum(9999)
        self.subject_spinbox.setValue(default_subject_nr)
        self.subject_spinbox.valueChanged.connect(self._on_subject_changed)
        subject_layout.addWidget(subject_label)
        subject_layout.addWidget(self.subject_spinbox)
        
        # Logfile
        logfile_layout = QtWidgets.QHBoxLayout()
        logfile_label = QtWidgets.QLabel(_('Logfile:'))
        logfile_label.setFixedWidth(120)
        self.logfile_edit = QtWidgets.QLineEdit(default_logfile)
        self.browse_button = QtWidgets.QPushButton(_('Browse...'))
        self.browse_button.clicked.connect(self._browse_logfile)
        self.browse_button.setFixedWidth(80)
        logfile_layout.addWidget(logfile_label)
        logfile_layout.addWidget(self.logfile_edit)
        logfile_layout.addWidget(self.browse_button)
        
        # Fullscreen
        fullscreen_layout = QtWidgets.QHBoxLayout()
        self.fullscreen_checkbox = QtWidgets.QCheckBox(
            _('Fullscreen'))
        self.fullscreen_checkbox.setChecked(default_fullscreen)
        fullscreen_layout.addWidget(self.fullscreen_checkbox)
        
        # Buttons
        button_box = QtWidgets.QDialogButtonBox(
            QtWidgets.QDialogButtonBox.Ok | QtWidgets.QDialogButtonBox.Cancel
        )
        button_box.accepted.connect(self.accept)
        button_box.rejected.connect(self.reject)
        
        # Add everything to layout
        layout.addLayout(subject_layout)
        layout.addLayout(logfile_layout)
        layout.addLayout(fullscreen_layout)
        layout.addWidget(button_box)
        
        self.setLayout(layout)
        
        # Store the logfile directory for updating when subject changes
        self._logfile_dir = os.path.dirname(default_logfile)
        self._logfile_extension = os.path.splitext(default_logfile)[1] or '.csv'
        
        # Size the dialog to fit its contents exactly
        self.adjustSize()
        self.setFixedSize(self.size())
        
    def _on_subject_changed(self, value):
        """Update the logfile name when subject number changes."""
        logfile = os.path.join(
            self._logfile_dir,
            f'subject-{value}{self._logfile_extension}'
        )
        self.logfile_edit.setText(logfile)
        
    def _browse_logfile(self):
        """Open a file dialog to browse for logfile location."""
        file_filter = f'Log files (*{self._logfile_extension});;All files (*.*)'
        logfile, __ = QtWidgets.QFileDialog.getSaveFileName(
            self,
            _("Choose location for logfile"),
            self.logfile_edit.text(),
            filter=file_filter
        )
        if logfile:
            self.logfile_edit.setText(logfile)
            self._logfile_dir = os.path.dirname(logfile)
            self._logfile_extension = os.path.splitext(logfile)[1] \
                or self._logfile_extension
    
    def get_values(self):
        """Return the values from the dialog."""
        return {'subject_nr': self.subject_spinbox.value(),
                'logfile': self.logfile_edit.text(),
                'fullscreen': self.fullscreen_checkbox.isChecked()}

class BaseRunner:
    """
    A runner implements a specific way to execute an OpenSesame experiment from
    within the GUI. The base_runner is an abstract runner that is inherited by
    actual runners.

    Parameters
    ----------
    main_window : QtOpenSesame
        The main OpenSesame window.
    """
    
    valid_logfile_extensions = '.csv', '.txt', '.dat', '.log', '.json'
    supports_kill = False

    def __init__(self, main_window):
        self.main_window = main_window
        self.paused = False
        self.experiment = None

    @property
    def tabwidget(self):
        """Convenience property to access the tab widget."""
        return self.main_window.tabwidget

    def execute(self):
        """
        Executes the experiments. This function should be transparent and leave
        no mess to clean up for the GUI.

        Returns
        -------
        Exception or None
            None if the experiment finished cleanly, or an Exception if one
            occurred.
        """
        raise NotImplementedError("Subclasses must implement execute()")

    def _get_next_subject_number(self):
        """
        Find the next available subject number by looking at existing logfiles.
        
        Returns
        -------
        int
            The next available subject number.
        """
        try:
            # Look for files matching subject-N.* pattern
            pattern = re.compile(r'subject-(\d+)\.')
            existing_numbers = []
            
            if os.path.exists(cfg.default_logfile_folder):
                for filename in os.listdir(cfg.default_logfile_folder):
                    match = pattern.match(filename)
                    if match:
                        existing_numbers.append(int(match.group(1)))
            
            # If we found existing numbers, return the highest + 1
            if existing_numbers:
                return max(existing_numbers) + 1
            
            return 1
            
        except Exception as e:
            oslogger.warning(f'Failed to determine next subject number: {e}')
            return 1

    def _get_quick_settings(self):
        """
        Get default settings for quick run mode.
        
        Returns
        -------
        dict
            Settings dictionary with subject_nr, logfile, and fullscreen.
        """
        subject_nr = 999
        logfile = os.path.join(cfg.default_logfile_folder, cfg.quick_run_logfile)        
        # Try to write to the default location
        try:
            with open(logfile, 'w'):
                pass
            os.remove(logfile)
        except Exception:
            # Fall back to temp directory
            oslogger.warning(f'Failed to open {logfile}')
            logfile = os.path.join(
                safe_decode(tempfile.gettempdir(),
                            enc=sys.getfilesystemencoding()),
                safe_decode(tempfile.gettempprefix(),
                            enc=sys.getfilesystemencoding()) + 'quickrun.csv'
            )
            oslogger.warning(f'Using temporary file {logfile}')        
        return {'subject_nr': subject_nr,
                'logfile': logfile,
                'fullscreen': False}

    def get_experiment_settings(self, quick=False):
        """
        Gets the subject number, logfile, and fullscreen setting through a 
        unified dialog or quick defaults.

        Parameters
        ----------
        quick : bool, optional
            Whether to use default settings without showing a dialog.

        Returns
        -------
        dict or None
            A dictionary with 'subject_nr', 'logfile', and 'fullscreen' keys,
            or None if cancelled.
        """
        if quick:
            return self._get_quick_settings()
        
        # Normal mode - show dialog with intelligent defaults
        default_subject_nr = self._get_next_subject_number()
        default_logfile = os.path.normpath(os.path.join(
            cfg.default_logfile_folder,
            f'subject-{default_subject_nr}.csv'
        ))
        
        dialog = ExperimentSettingsDialog(
            self.main_window.ui.centralwidget,
            default_subject_nr,
            default_logfile,
            cfg.run_fullscreen
        )
        
        if dialog.exec_() != QtWidgets.QDialog.Accepted:
            return None
            
        values = dialog.get_values()
        
        # Validate and clean up logfile
        logfile = values['logfile']
        
        # Add extension if missing
        if os.path.splitext(logfile)[1].lower() not in self.valid_logfile_extensions:
            logfile += '.csv'
            values['logfile'] = logfile
        
        # Check if writable
        try:
            with open(logfile, 'w'):
                pass
            os.remove(logfile)
        except Exception:
            self.main_window.notify(
                _("The logfile '%s' is not writable. Please choose "
                  "another location for the logfile.") % logfile
            )
            return None
        
        # Remember settings for next time
        cfg.default_logfile_folder = os.path.dirname(logfile)
        cfg.run_fullscreen = values['fullscreen']
        
        return values

    def init_experiment(self, quick=False):
        """
        Initializes a new experiment, which is a newly generated instance of
        the experiment currently active in the user interface.
        
        Parameters
        ----------
        quick : bool, optional
            Whether to use default settings for the log-file and subject number.

        Returns
        -------
        bool
            True if the experiment was successfully initiated, False otherwise.
        """
        # First tell the experiment to get ready and generate the script
        try:
            script = self.main_window.experiment.to_string()
        except Exception as e:
            md = _('# Error\n\nFailed to generate experiment for the '
                   'following reason:\n\n- ') + e.markdown()
            self.tabwidget.open_markdown(md)
            return False
        
        # Get experiment settings
        settings = self.get_experiment_settings(quick=quick)
        if settings is None:
            return False
        
        # Determine experiment path
        experiment_path = None
        if self.main_window.experiment.experiment_path is not None:
            experiment_path = self.main_window.experiment.experiment_path
            if self.main_window.current_path is not None:
                experiment_path = os.path.join(
                    experiment_path,
                    self.main_window.current_path
                )
        
        # Build a new experiment
        try:
            self.experiment = Experiment(
                string=script,
                pool_folder=self.main_window.experiment.pool.folder(),
                experiment_path=experiment_path,
                fullscreen=settings['fullscreen'],
                subject_nr=settings['subject_nr'],
                logfile=settings['logfile']
            )
        except Exception as e:
            md = _('# Error\n\nFailed to parse experiment for the '
                   'following reason:\n\n- ') + safe_decode(e)
            traceback.print_exc()
            self.tabwidget.open_markdown(md)
            return False
            
        return True

    def run(self, quick=False):
        """
        Runs the experiment.

        Parameters
        ----------
        quick : bool, optional
            Whether to use default settings for the log-file and subject number.
        """
        self.main_window.set_run_status('running')        
        self.main_window.extension_manager.fire('init_experiment')        
        if not self.init_experiment(quick=quick):
            self.main_window.extension_manager.fire('run_experiment_canceled')
            self.main_window.set_run_status('idle')
            return            
        # Get fullscreen setting for the event
        fullscreen = cfg.run_fullscreen if quick else None
        self.main_window.extension_manager.fire('run_experiment',
                                                fullscreen=fullscreen)
        ret_val = self.execute()        
        # PsychoPy sometimes deletes the _ built-in
        if '_' not in __builtins__:
            oslogger.warning('Re-installing missing gettext built-in')
            import gettext
            gettext.NullTranslations().install()            
        self.main_window.set_run_status('finished')
        self.main_window.extension_manager.fire(
            'set_workspace_globals',
            global_dict=self.workspace_globals())
        self.main_window.extension_manager.fire('end_experiment',
                                                ret_val=ret_val)        
        if ret_val is None:
            self.main_window.extension_manager.fire(
                'process_data_files',
                data_files=self.data_files())

    def kill(self):
        """
        Kills a running experiment.
        
        Note: Only available if supports_kill is True.
        """
        if not self.supports_kill:
            raise NotImplementedError(
                "This runner does not support killing experiments")

    def workspace_globals(self):
        """
        Returns the experiment's globals dictionary as it was when the
        experiment finished.

        Returns
        -------
        dict
            A globals dictionary.
        """
        return {}

    def data_files(self):
        """
        Returns a list of data files generated by the experiment.
        
        Returns
        -------
        list
            List of data file paths.
        """
        return self.workspace_globals().get('data_files', [])

    def pause(self):
        """Called when the experiment is paused."""
        if self.paused:
            return
            
        self.main_window.extension_manager.fire(
            'set_workspace_globals',
            global_dict=self.workspace_globals()
        )
        print('The experiment has been paused. Switch back to the experiment '
              'window and press space to resume.')
        self.main_window.set_run_status('paused')
        self.main_window.extension_manager.fire('pause_experiment')
        self.paused = True

    def resume(self):
        """Called when the experiment is resumed/unpaused."""
        if not self.paused:
            return
            
        self.paused = False
        self.main_window.set_run_status('running')
        self.main_window.extension_manager.fire('resume_experiment')

    @staticmethod
    def has_heartbeat():
        """
        Indicates whether the runner supports heartbeats.
        
        Heartbeats are used to update the variable inspector during experiment
        execution.
        
        Returns
        -------
        bool
            True if heartbeats are supported, False otherwise.
        """
        return False

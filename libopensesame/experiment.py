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
from openexp import backend
import opensesame_plugins
from libopensesame.plugin_manager import PluginManager
from libopensesame.var_store import VarStore
from libopensesame.item_store import ItemStore
from libopensesame.response_store import ResponseStore
from libopensesame.file_pool_store import FilePoolStore
from libopensesame.syntax import Syntax
from libopensesame.exceptions import UserAborted, ItemDoesNotExist, \
    InvalidOpenSesameScript
from libopensesame.item import Item
from libopensesame import misc, metadata
from libopensesame.item_stack import item_stack_singleton
from libopensesame.oslogging import oslogger
from libopensesame.py3compat import *
import os
import sys
import pickle
import time
import warnings
import gc


class Experiment(Item):

    """A special item that controls the flow of the experiment."""
    description = 'The main experiment item'

    def __init__(self, name='experiment', string=None, pool_folder=None,
                 experiment_path=None, fullscreen=False,
                 logfile='defaultlog.csv', subject_nr=0, workspace=None,
                 resources={}, heartbeat_interval=1):
        """Constructor. The experiment is created automatically be OpenSesame
        and you will generally not need to create it yourself.

        Parameters
        ----------
        name : str, unicode, optional
            The name of the experiment.
        string : str, unicode, NoneType, optional
            A string containing the experiment definition, the name of an
            OpenSesame experiment file, or `None` to create a blank experiment.
        pool_folder : str, unicode, NoneType, optional
            A specific folder to be used for the file pool, or `None` to use a
            new temporary folder.
        experiment_path : str, optional
            The path of the experiment file. This is the folder that the
            experiment is in, not the path to the experiment file.
        fullscreen : bool, optional
            Indicates whether the experiment should be executed in fullscreen.
        logfile : unicode, str, optional
            The logfile path.
        subject_nr : int, optional
            The subject number.
        workspace : python_workspace, NoneType, optional
            A `python_workspace` object to be used for executing custom Python
            code, or `None` to create a new workspace.
        resources : dict, optional
            A dictionary with names as keys and paths as values. This serves as
            a look-up table for resources.
        heartbeat_interval : int, float, optional
            A heartbeat interval in seconds, or <= 0 to disable heartbeats.
        """
        # Make sure the logger is started
        if not oslogger.started:
            oslogger.start()
            oslogger.debug('starting logger in experiment init')
        self.var = VarStore(self)
        self.pool = FilePoolStore(self, folder=pool_folder)
        self._responses = ResponseStore(self)
        # The _syntax and items objects may already have been created by
        # libqtopensesame.experiment.
        if not hasattr(self, '_syntax'):
            self._syntax = Syntax(self)
        if not hasattr(self, 'items'):
            self.items = ItemStore(self)
        if not hasattr(self, '_plugin_manager'):
            self._plugin_manager = PluginManager(opensesame_plugins)
        if workspace is None:
            from libopensesame.python_workspace import PythonWorkspace
            self._python_workspace = PythonWorkspace(self)
        else:
            self._python_workspace = workspace
        self.running = False
        self.heartbeat_interval = heartbeat_interval
        self.plugin_folder = 'plugins'
        self._start_response_interval = None
        self.cleanup_functions = []
        self.restart = False
        self.resources = resources
        self.paused = False
        self.output_channel = None
        self.reset()

        # Logfile parameters
        self._log = None
        self.logfile = logfile
        # A list of data files, which may include more than just the OpenSesame
        # logfile, for example if data is also recorded using some other method.
        self.data_files = []

        # This is some duplication of the option parser in qtopensesame,
        # but nevertheless keep it so we don't need qtopensesame
        self.debug = '--debug' in sys.argv or '-d' in sys.argv
        if string is not None:
            string = self.open(string)
        Item.__init__(self, name, self, string)
        # Default subject info
        self.set_subject(subject_nr)
        # Fullscreen needs to be set after the experiment has been parsed from
        # script, otherwise it will be overridden by the script.
        self.var.fullscreen = 'yes' if fullscreen else 'no'
        # Restore experiment path, which is either the full path (including
        # filename), only the folder, or None.
        if experiment_path is not None:
            if os.path.isfile(experiment_path):
                self.var.experiment_path, self.var.experiment_file = \
                    self.experiment_path, self.experiment_file = \
                    os.path.split(experiment_path)
            else:
                self.var.experiment_path = self.experiment_path \
                    = experiment_path
        # When a template is opened, it should not result in the experiment
        # path being defined, because it is intended to be saved as a new
        # experiment. Templates are identified by the is_template variable,
        # which is removed when the file is opened.
        if self.var.get('is_template', 0):
            self.experiment_path = self.var.experiment_path = None
            del self.var.is_template
        if not py3 and backend.backend_guess(self, 'sampler') == 'psycho':
            self.var.sampler_backend = 'legacy'
            oslogger.warning(
                'The psycho sampler backend is not compatible with Python 2. '
                'Falling back to legacy sampler backend'
            )

    @property
    def default_title(self):
        return 'New experiment'

    def reset(self):
        # Set default variables
        self.var.start = 'experiment'
        self.var.title = self.default_title
        self.var.round_decimals = 2
        self.var.form_clicks = 'no'
        self.var.disable_garbage_collection = 'yes'
        # Sound parameters
        self.var.sound_freq = 48000
        self.var.sound_sample_size = -16  # Negative values mean signed
        self.var.sound_channels = 2
        self.var.sound_buf_size = 1024
        # Default backend
        self.var.canvas_backend = 'psycho'
        # Display parameters
        self.var.width = 1024
        self.var.height = 768
        self.var.background = 'black'
        self.var.foreground = 'white'
        # Font parameters
        self.var.font_size = 18
        self.var.font_family = 'mono'
        self.var.font_italic = 'no'
        self.var.font_bold = 'no'
        self.var.font_underline = 'no'

    def module_container(self):
        """Specify the module that contains the item modules"""
        return 'libopensesame'

    def item_prefix(self):
        """A prefix for the plug-in classes, so that [prefix][plugin] class is
        used instead of the [plugin] class.
        """
        return ''

    def set_subject(self, nr):
        """Sets the subject number and parity (even/ odd). This function is
        called automatically when an experiment is started, so you do not
        generally need to call it yourself.

        Parameters
        ----------
        nr : int
            The subject nr.

        Examples
        --------
        >>> exp.set_subject(1)
        >>> print('Subject nr = %d' % exp.get('subject_nr'))
        >>> print('Subject parity = %s' % exp.get('subject_parity'))
        """
        # Set the subject nr and parity
        self.var.subject_nr = nr
        if nr % 2 == 0:
            self.var.subject_parity = 'even'
        else:
            self.var.subject_parity = 'odd'

    def read_definition(self, s):
        """Extracts a the definition of a single item from the string.

        Parameters
        ----------
        s: str
            The definition string.

        Returns
        -------
        tuple
            A (str, str) tuple with the full string minus the definition string
            and the definition string.
        """
        # Read the string until the end of the definition
        def_str = ''
        line = next(s, None)
        if line is None:
            return None, ''
        get_next = False
        while True:
            if len(line) > 0:
                if line[0] != '\t':
                    break
                else:
                    def_str += line + '\n'
            line = next(s, None)
            if line is None:
                break
        return line, def_str

    def from_string(self, string):
        """Reads the entire experiment from a string.

        Parameters
        ----------
        string
            The definition string.
        """
        self.var.clear(preserve=['experiment_path', 'experiment_file'])
        self.reset()
        self.comments = []
        oslogger.debug(u"building experiment")
        if string is None:
            return
        self.front_matter, string = self._syntax.parse_front_matter(string)
        if self.experiment.front_matter['API'].version[0] < 2:
            # Old experiment scripts were saved in ASCII, and require decoding
            # of U+XXXX unicode characters.
            string = self.syntax.from_ascii(string)
        s = iter(string.split('\n'))
        line = next(s, None)
        while line is not None:
            get_next = True
            l = self.syntax.split(line)
            if l:
                self.parse_variable(line)
                # Parse definitions
                if l[0] == u"define":
                    if len(l) != 3:
                        raise InvalidOpenSesameScript(
                            'Failed to parse definition', line=line)
                    item_type = l[1]
                    item_name = self.syntax.sanitize(l[2])
                    line, def_str = self.read_definition(s)
                    get_next = False
                    self.items.new(
                        _type=item_type,
                        name=item_name,
                        script=def_str,
                        allow_rename=False
                    )
            # Advance to next line
            if get_next:
                line = next(s, None)

    def transmit_workspace(self, **extra):
        """Sends the current workspace through the output channel. If there is
        no output channel, this function does nothing.

        Parameters
        ----------
        **extra : dict
            Any extra items in the workspace dict to be sent.
        """
        if self.output_channel is None:
            return
        d = self.python_workspace._globals.copy()
        d.update(extra)
        for key, value in d.copy().items():
            try:
                pickle.dumps(value)
            except:
                del d[key]
        self.output_channel.put(d)

    def set_output_channel(self, output_channel):
        """Sets the output channel, which is used to communicate the workspace
        between the experiment and the launch process (typically the GUI).

        Parameters
        ----------
        output_channel    The output object, which must support a `put` method.
        """
        if not hasattr(output_channel, 'put'):
            raise RuntimeError(f'Invalid output_channel: {output_channel}')
        self.output_channel = output_channel

    def run(self):
        """Runs the experiment."""
        # Save the date and time, and the version of OpenSesame
        self.var.datetime = safe_decode(
            time.strftime('%c'),
            enc=self.encoding,
            errors='ignore'
        )
        self.var.opensesame_version = metadata.__version__
        self.var.opensesame_codename = metadata.codename
        self.running = True
        self.init_random()
        self.init_display()
        self.init_clock()
        self.init_sound()
        self.init_log()
        self.python_workspace.init_globals()
        self.reset_feedback()
        self.init_heartbeat()
        oslogger.info(u"experiment started")
        if self.var.start in self.items:
            item_stack_singleton.clear()
            if self.var.disable_garbage_collection == 'yes':
                oslogger.info('disabling garbage collection')
                gc.disable()
            self.items.execute(self.var.start)
        else:
            raise ItemDoesNotExist(self.var.start)
        oslogger.info(u"experiment finished")
        self.end()

    def pause(self):
        """Pauses the experiment, sends the Python workspace to the GUI, and
        waits for the GUI to send a resume signal. This requires an output
        channel.
        """
        if self.paused:
            return

        from openexp.canvas import Canvas
        from openexp.canvas_elements import Text
        from openexp.keyboard import Keyboard

        self.paused = True
        self.transmit_workspace(__pause__=True)
        pause_canvas = Canvas(self)
        pause_canvas['msg'] = Text(
            'The experiment has been paused<br /><br />'
            'Press spacebar to resume<br />'
            'Press Q to quit'
        ).construct(pause_canvas)
        pause_keyboard = Keyboard(
            self,
            keylist=['space', 'q', 'Q'],
            timeout=0
        )
        pause_keyboard.show_virtual_keyboard()
        pause_canvas.show()
        try:
            while True:
                key, _time = pause_keyboard.get_key()
                if key == 'q' or key == 'Q':
                    pause_keyboard.show_virtual_keyboard(False)
                    raise UserAborted('The experiment was aborted')
                if key == 'space':
                    break
                time.sleep(.25)
        finally:
            self.paused = False
            self.transmit_workspace(__pause__=False)
        pause_keyboard.show_virtual_keyboard(False)
        pause_canvas['msg'].text = 'Resuming ...'
        pause_canvas.show()

    def cleanup(self):
        """Calls all the cleanup functions."""
        while len(self.cleanup_functions) > 0:
            func = self.cleanup_functions.pop()
            oslogger.debug(u"calling cleanup function")
            func()

    def end(self):
        """Nicely ends the experiment."""
        from openexp import sampler, canvas
        self.running = False
        try:
            self._log.close()
        except AttributeError:
            oslogger.error('missing or invalid log object')
        sampler.close_sound(self)
        canvas.close_display(self)
        self.cleanup()
        if not gc.isenabled():
            oslogger.info('enabling garbage collection')
            gc.enable()
        self.transmit_workspace(__finished__=True)

    def to_string(self):
        """
        Encodes the experiment into a string.

        Returns:
        A Unicode definition string for the experiment.
        """
        s = self._syntax.generate_front_matter()
        for var in self.var:
            s += self.variable_to_string(var)
        s += '\n'
        for _item in sorted(self.items):
            s += self.items[_item].to_string() + '\n'
        return s

    def save(self, path, overwrite=False, update_path=True):
        """Saves the experiment to file.

        Parameters
        ----------
        path : str, unicode
            The target file to save to.
        overwrite : bool, optional
            Indicates if existing files should be overwritten.
        update_path : bool, optional
            Indicates if the experiment_path attribute should be updated.

        Returns
        -------
        unicode, bool
            The path on successful saving or False otherwise.
        """
        path = safe_decode(path, enc=self.encoding)
        if os.path.exists(path) and not overwrite:
            return False
        from libopensesame.osexpfile import osexpwriter
        w = osexpwriter(self, path)
        if update_path:
            self.experiment_path = w.experiment_path
        return path

    def open(self, src):
        """Opens an experiment. The source can be any of the following:

        - An
        OpenSesame script (ie. not a file)
        - The full path to a .osexp
        experiment file.

        Parameters
        ----------
        src : str
            The source.

        Returns
        -------
        str
            An OpenSesame script.
        """
        from libopensesame.osexpfile import osexpreader
        f = osexpreader(self, src)
        self.experiment_path = f.experiment_path
        return f.script

    def reset_feedback(self):
        """Resets the feedback variables (acc, avg_rt, etc.)."""
        self.responses.reset_feedback()

    def var_info(self):
        """Returns a list of (name, value) tuples with variable descriptions
        for the main experiment.

        Returns:
        A list of tuples.
        """
        l = []
        for var in self.var:
            val = self.var.get(var, _eval=False)
            if self.var.is_default_loggable(var, val):
                l.append((var, val))
        return l

    def init_heartbeat(self):
        """Initializes heartbeat."""
        if self.heartbeat_interval <= 0 or self.var.fullscreen == 'yes' or \
                self.output_channel is None:
            self.heartbeat = None
            return
        from libopensesame.heartbeat import heartbeat
        self.heartbeat = heartbeat(self, interval=self.heartbeat_interval)
        self.heartbeat.start()

    def init_random(self):
        """Initializes the random number generators. For some reason, the numpy
        random seed is not re-initialized when the experiment is started
        again with the multiprocess runner, resulting in identical random
        runs. The standard random module doesn't suffer from this problem.
        But to be on the safe side, we now explicitly re-initialize the
        random seed.

        See also:

        - <http://forum.cogsci.nl/index.php?p=/discussion/1441/>
        """
        import random
        random.seed()
        try:
            # Don't assume that numpy is available
            import numpy
            numpy.random.seed()
        except:
            pass

    def init_sound(self):
        """Intializes the sound backend."""
        from openexp import sampler
        sampler.init_sound(self)

    def init_display(self):
        """Initializes the canvas backend."""
        from openexp import canvas
        canvas.init_display(self)
        self.python_workspace['win'] = self.window

    def init_clock(self):
        """Initializes the clock backend."""
        from openexp.clock import clock
        self._clock = clock(self)

    def init_log(self):
        """Initializes the log backend."""
        from openexp.log import log
        self._log = log(self, self.logfile)

# Alias for backwards compatibility
experiment = Experiment

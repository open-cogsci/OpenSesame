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
from libopensesame.var_store import var_store
from libopensesame.item_store import item_store
from libopensesame.response_store import response_store
from libopensesame.file_pool_store import file_pool_store
from libopensesame.syntax import syntax
from libopensesame.exceptions import osexception
from libopensesame import misc, item, metadata
from libopensesame.item_stack import item_stack_singleton
from libopensesame.oslogging import oslogger
from libopensesame.py3compat import *
import os
import sys
import pickle
import time
import warnings
import gc


# In Python 2, sending old-style classes across the pipeline causes trouble. We
# need to define the classobj type here. This is only applicable to Python 2,
# because Python 3 had only new-style classes.
class OldStyle:
    pass


classobj = type(OldStyle)


class experiment(item.item):

    """
    desc:
            A special item that controls the flow of the experiment.
    """

    description = u'The main experiment item'

    def __init__(self, name=u'experiment', string=None, pool_folder=None,
                 experiment_path=None, fullscreen=False, auto_response=False,
                 logfile=u'defaultlog.csv', subject_nr=0, workspace=None, resources={},
                 heartbeat_interval=1):
        """
        desc:
                Constructor. The experiment is created automatically be OpenSesame
                and you will generally not need to create it yourself.

        keywords:
                name:
                        desc:	The name of the experiment.
                        type:	[str, unicode]
                string:
                        desc:	A string containing the experiment definition, the
                                        name of an OpenSesame experiment file, or `None` to
                                        create a blank experiment.
                        type:	[str, unicode, NoneType]
                pool_folder:
                        desc:	A specific folder to be used for the file pool, or
                                        `None` to use a new temporary folder.
                        type:	[str, unicode, NoneType]
                experiment_path:
                        desc:	The path of the experiment file. This is the folder that
                                        the experiment is in, not the path to the experiment
                                        file.
                        type:	str
                fullscreen:
                        desc:	Indicates whether the experiment should be executed in
                                        fullscreen.
                        type:	bool
                auto_response:
                        desc:	Indicates whether auto-response mode should be enabled.
                        type:	bool
                logfile:
                        desc:	The logfile path.
                        type:	[unicode, str]
                subject_nr:
                        desc:	The subject number.
                        type:	int
                workspace:
                        desc:	A `python_workspace` object to be used for executing
                                        custom Python code, or `None` to create a new workspace.
                        type:	[python_workspace, NoneType]
                resources:
                        desc:	A dictionary with names as keys and paths as values.
                                        This serves as a look-up table for resources.
                        type:	dict
                heartbeat_interval:
                        desc:	A heartbeat interval in seconds, or <= 0 to disable
                                        heartbeats.
                        type:	[int, float]
        """

        # Make sure the logger is started
        if not oslogger.started:
            oslogger.start()
            oslogger.debug('starting logger in experiment init')
        self.var = var_store(self)
        self.pool = file_pool_store(self, folder=pool_folder)
        self._responses = response_store(self)
        # The _syntax and items objects may already have been created by
        # libqtopensesame.experiment.
        if not hasattr(self, u'_syntax'):
            self._syntax = syntax(self)
        if not hasattr(self, u'items'):
            self.items = item_store(self)
        if workspace is None:
            from libopensesame.python_workspace import python_workspace
            self._python_workspace = python_workspace(self)
        else:
            self._python_workspace = workspace
        self.running = False
        self.auto_response = auto_response
        self.heartbeat_interval = heartbeat_interval
        self.plugin_folder = u'plugins'
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
        item.item.__init__(self, name, self, string)
        # Default subject info
        self.set_subject(subject_nr)
        # Fullscreen needs to be set after the experiment has been parsed from
        # script, otherwise it will be overridden by the script.
        self.var.fullscreen = u'yes' if fullscreen else u'no'
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
        if not py3 and backend.backend_guess(self, 'sampler') == u'psycho':
            self.var.sampler_backend = 'legacy'
            oslogger.warning(
                u'The psycho sampler backend is not compatible with Python 2. '
                u'Falling back to legacy sampler backend'
            )

    @property
    def pool_folder(self):
        """Deprecated."""

        warnings.warn(
            u'experiment.pool_folder is deprecated. Use file_pool_store instead.',
            DeprecationWarning)
        return self.pool.folder()

    @property
    def fallback_pool_folder(self):
        """Deprecated."""

        warnings.warn(
            u'experiment.fallback_pool_folder is deprecated. Use file_pool_store instead.',
            DeprecationWarning)
        return self.pool.fallback_folder()

    @property
    def default_title(self):
        return u'New experiment'

    def get_file(self, path):
        """Deprecated."""

        warnings.warn(
            u'experiment.get_file() is deprecated. Use file_pool_store instead.',
            DeprecationWarning)
        return self.pool[path]

    def reset(self):
        """See item."""

        # Set default variables
        self.var.start = u'experiment'
        self.var.title = self.default_title
        self.var.round_decimals = 2
        self.var.form_clicks = u'no'
        self.var.disable_garbage_collection = u'yes'
        # In version 2.9.X and before, the sketchpad used 0,0 for the screen
        # center, whereas scripting items used 0,0 for the top-left. By setting
        # uniform_coordinates to 'yes', 0,0 is used for the center in all cases.
        self.var.uniform_coordinates = u'no'
        # Sound parameters
        self.var.sound_freq = 48000
        self.var.sound_sample_size = -16  # Negative values mean signed
        self.var.sound_channels = 2
        self.var.sound_buf_size = 1024
        # Default backend
        self.var.canvas_backend = u'xpyriment'
        # Display parameters
        self.var.width = 1024
        self.var.height = 768
        self.var.background = u'black'
        self.var.foreground = u'white'
        # Font parameters
        self.var.font_size = 18
        self.var.font_family = u'mono'
        self.var.font_italic = u'no'
        self.var.font_bold = u'no'
        self.var.font_underline = u'no'

    def file_in_pool(self, path):
        """Deprecated."""

        warnings.warn(
            u'experiment.file_in_pool() is deprecated. Use file_pool_store instead.',
            DeprecationWarning)
        return path in self.pool

    def module_container(self):
        """Specify the module that contains the item modules"""

        return u'libopensesame'

    def item_prefix(self):
        """
        A prefix for the plug-in classes, so that [prefix][plugin] class is used
        instead of the [plugin] class.
        """

        return u''

    def set_subject(self, nr):
        """
        desc:
                Sets the subject number and parity (even/ odd). This function is
                called automatically when an experiment is started, so you do not
                generally need to call it yourself.

        arguments:
                nr:
                        desc:	The subject nr.
                        type:	int

        example: |
                exp.set_subject(1)
                print('Subject nr = %d' % exp.get('subject_nr'))
                print('Subject parity = %s' % exp.get('subject_parity'))
        """

        # Set the subject nr and parity
        self.var.subject_nr = nr
        if nr % 2 == 0:
            self.var.subject_parity = u'even'
        else:
            self.var.subject_parity = u'odd'

    def read_definition(self, s):
        """
        Extracts a the definition of a single item from the string.

        Arguments:
        s	--	The definition string.

        Returns:
        A (str, str) tuple with the full string minus the definition string
        and the definition string.
        """

        # Read the string until the end of the definition
        def_str = u''
        line = next(s, None)
        if line is None:
            return None, u''
        get_next = False
        while True:
            if len(line) > 0:
                if line[0] != u'\t':
                    break
                else:
                    def_str += line + u'\n'
            line = next(s, None)
            if line is None:
                break
        return line, def_str

    def from_string(self, string):
        """
        desc:
                Reads the entire experiment from a string.

        arguments:
                string:	The definition string.
        """

        self.var.clear(preserve=[u'experiment_path', u'experiment_file'])
        self.reset()
        self.comments = []
        oslogger.debug(u"building experiment")
        if string is None:
            return
        self.front_matter, string = self._syntax.parse_front_matter(string)
        if self.experiment.front_matter[u'API'].version[0] < 2:
            # Old experiment scripts were saved in ASCII, and require decoding
            # of U+XXXX unicode characters.
            string = self.syntax.from_ascii(string)
        s = iter(string.split(u'\n'))
        line = next(s, None)
        while line is not None:
            get_next = True
            try:
                l = self.syntax.split(line)
            except ValueError as e:
                raise osexception(
                    u'Failed to parse script. Maybe it contains '
                    u'illegal characters or unclosed quotes?',
                    exception=e
                )
            if l:
                self.parse_variable(line)
                # Parse definitions
                if l[0] == u"define":
                    if len(l) != 3:
                        raise osexception(
                            u'Failed to parse definition',
                            line=line
                        )
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
        """
        desc:
                Sends the current workspace through the output channel. If there is
                no output channel, this function does nothing.

        keyword-dict:
                extra:	Any extra items in the workspace dict to be sent.
        """

        if self.output_channel is None:
            return
        d = self.python_workspace._globals.copy()
        d.update(extra)
        for key, value in d.copy().items():
            if self._is_oldstyle(value):
                del d[key]
                continue
            try:
                pickle.dumps(value)
            except:
                del d[key]
        self.output_channel.put(d)

    def _is_oldstyle(self, obj):
        """
        desc:
                Checks if an object is an old-style class or an instance of an
                old-style class. This is important, because these objects cannot be
                pickled properly, and the workspace transmission chokes on them.
        """

        if py3:
            return False
        # old-style class
        if type(obj) == classobj:
            return True
        # instance of old-style class
        if hasattr(obj, u'__class__') and type(obj.__class__) == classobj:
            return True
        return False

    def set_output_channel(self, output_channel):
        """
        desc:
                Sets the output channel, which is used to communicate the workspace
                between the experiment and the launch process (typically the GUI).

        arguments:
                output_channel:
                        desc: 	The output object, which must support a `put` method.
        """

        if not hasattr(output_channel, u'put'):
            raise osexception(u'Invalid output_channel: %s' % output_channel)
        self.output_channel = output_channel

    def run(self):
        """Runs the experiment."""

        # Save the date and time, and the version of OpenSesame
        self.var.datetime = safe_decode(
            time.strftime(u'%c'),
            enc=self.encoding,
            errors=u'ignore'
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
        if self.var.uniform_coordinates != u'yes':
            oslogger.warning(
                u'Uniform coordinates are disabled. This is deprecated, and '
                u'will be removed in the future. Please enable uniform '
                u'coordinates in the script of your experiment.'
            )
        oslogger.info(u"experiment started")
        if self.var.start in self.items:
            item_stack_singleton.clear()
            if self.var.disable_garbage_collection == u'yes':
                oslogger.info('disabling garbage collection')
                gc.disable()
            self.items.execute(self.var.start)
        else:
            raise osexception(
                "Could not find item '%s', which is the entry point of the experiment"
                % self.var.start
            )
        oslogger.info(u"experiment finished")
        self.end()

    def pause(self):
        """
        desc:
                Pauses the experiment, sends the Python workspace to the GUI, and
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
            u'The experiment has been paused<br /><br />'
            u'Press spacebar to resume<br />'
            u'Press Q to quit'
        ).construct(pause_canvas)
        pause_keyboard = Keyboard(
            self,
            keylist=[u'space', u'q', u'Q'],
            timeout=0
        )
        pause_keyboard.show_virtual_keyboard()
        pause_canvas.show()
        try:
            while True:
                key, _time = pause_keyboard.get_key()
                if key == u'q' or key == u'Q':
                    pause_keyboard.show_virtual_keyboard(False)
                    raise osexception(
                        u'The experiment was aborted',
                        user_triggered=True
                    )
                if key == u'space':
                    break
                time.sleep(.25)
        finally:
            self.paused = False
            self.transmit_workspace(__pause__=False)
        pause_keyboard.show_virtual_keyboard(False)
        pause_canvas['msg'].text = u'Resuming ...'
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
        s += u'\n'
        for _item in sorted(self.items):
            s += self.items[_item].to_string() + u'\n'
        return s

    def resource(self, name):
        """
        Retrieves a file from the resources folder.

        Arguments:
        name	--	The file name.

        Returns:
        A Unicode string with the full path to the file in the resources
        folder.
        """

        name = safe_decode(name)
        if self is not None:
            if name in self.resources:
                return self.resources[name]
            if os.path.exists(self.pool[name]):
                return self.pool[name]
        path = misc.resource(name)
        if path is None:
            raise FileNotFoundError(
                u"The resource '%s' could not be found in libopensesame.experiment.resource()"
                % name
            )
        return path

    def save(self, path, overwrite=False, update_path=True):
        """
        desc:
                Saves the experiment to file.

        arguments:
                path:
                        desc:	The target file to save to.
                        type:	[str, unicode]

        keywords:
                overwrite:
                        desc:	Indicates if existing files should be overwritten.
                        type:	bool
                update_path:
                        desc:	Indicates if the experiment_path attribute should be
                                        updated.
                        type:	bool

        returns:
                desc:	The path on successful saving or False otherwise.
                type:	[unicode, bool]
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
        """
        desc: |
                Opens an experiment. The source can be any of the following:

                - An OpenSesame script (ie. not a file)
                - The full path to a .osexp experiment file.

        arguments:
                src:
                        desc:	The source.
                        type:	str

        returns:
                desc:	An OpenSesame script.
                type:	str
        """

        from libopensesame.osexpfile import osexpreader
        f = osexpreader(self, src)
        self.experiment_path = f.experiment_path
        return f.script

    def reset_feedback(self):
        """Resets the feedback variables (acc, avg_rt, etc.)."""

        self.responses.reset_feedback()

    def var_info(self):
        """
        Returns a list of (name, value) tuples with variable descriptions
        for the main experiment.

        Returns:
        A list of tuples.
        """

        l = []
        for var in self.var:
            l.append((var, self.var.get(var, _eval=False)))
        return l

    def init_heartbeat(self):
        """
        desc:
                Initializes heartbeat.
        """

        if self.heartbeat_interval <= 0 or self.var.fullscreen == u'yes' or \
                self.output_channel is None:
            self.heartbeat = None
            return
        from libopensesame.heartbeat import heartbeat
        self.heartbeat = heartbeat(self, interval=self.heartbeat_interval)
        self.heartbeat.start()

    def init_random(self):
        """
        desc:
                Initializes the random number generators. For some reason, the numpy
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
        self.python_workspace[u'win'] = self.window

    def init_clock(self):
        """Initializes the clock backend."""

        from openexp.clock import clock
        self._clock = clock(self)

    def init_log(self):
        """Initializes the log backend."""

        from openexp.log import log
        self._log = log(self, self.logfile)


def clean_up(verbose=False, keep=[]):

    warnings.warn(u'libopensesame.experiment.clean_up() is deprecated',
                  DeprecationWarning)

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
from qtpy import QtWidgets
from libopensesame import plugins
from libopensesame.exceptions import osexception
from libopensesame.oslogging import oslogger
from libqtopensesame.misc.base_subcomponent import BaseSubcomponent
from libqtopensesame.misc.translate import translation_context
_ = translation_context(u'extension_manager', category=u'core')


def suspend_events(fnc):
    r"""A decorator that causes all the extension manager to be suspended while
    the function is executed.
    """
    def inner(self, *args, **kwdict):

        self.extension_manager.suspend()
        retval = fnc(self, *args, **kwdict)
        self.extension_manager.resume()
        return retval

    return inner


class ExtensionManager(BaseSubcomponent):

    r"""Initializes GUI extensions, and distributes signals (fires) to the
    relevant extensions.
    """
    def __init__(self, main_window):
        r"""Constructor.

        Parameters
        ----------
        main_window
            The main-window object.
        """
        self.setup(main_window)
        self.main_window.set_busy()
        QtWidgets.QApplication.processEvents()
        self._extensions = []
        self.events = {}
        self.provides = {}
        self._suspended = False
        self._suspended_until = None
        def extension_filter(ext_name): return False
        for ext_name in plugins.list_plugins(
                _type=u'extensions',
                mode=self.main_window.mode
        ):
            if extension_filter(ext_name):
                oslogger.debug(u'filtering extension {}'.format(ext_name))
                continue
            try:
                if self.main_window.options.profile:
                    from datamatrix import functional as fnc
                    with fnc.profile('profile-loadext-{}.log'.format(ext_name)):
                        ext = plugins.load_extension(
                            ext_name, self.main_window)
                else:
                    ext = plugins.load_extension(ext_name, self.main_window)
            except Exception as e:
                if not isinstance(e, osexception):
                    e = osexception(msg=u'Extension error', exception=e)
                self.notify(
                    u'Failed to load extension %s (see debug window for stack trace)'
                    % ext_name
                )
                self.console.write(e)
            else:
                self._extensions.append(ext)
                self.register_extension(ext, ext_name)
                if ext.extension_filter is not None:
                    extension_filter = ext.extension_filter
        self.main_window.set_busy(False)

    def register_extension(self, ext, ext_name=None):

        if ext_name is None:
            ext_name = str(ext)
        oslogger.debug(u'installing extension {}'.format(ext_name))
        for event in ext.supported_events():
            if event not in self.events:
                self.events[event] = []
            self.events[event].append(ext)
        for provide in ext.supported_provides():
            if provide in self.provides:
                oslogger.warning(
                    u'multiple extensions provide {}'.format(provide)
                )
                continue
            self.provides[provide] = ext

    def __getitem__(self, extension_name):
        r"""Emulates a dict interface for retrieving extensions.

        Parameters
        ----------
        extension_name : str
            The extension name.

        Returns
        -------
        base_extension
        """
        for ext in self._extensions:
            if ext.name() == extension_name:
                return ext
        raise osexception(u'Extension %s does not exist' % extension_name)

    def __contains__(self, extension_name):
        """
        arguments:
                extension_name:
                        desc:    The extension name.
                        type:    str

        returns:
                True if the extension exists, False otherwise.
        """
        return any(ext.name() == extension_name for ext in self._extensions)

    def fire(self, event, **kwdict):
        r"""Fires an event to all extensions that support the event.

        Parameters
        ----------
        event
            The event name.
        **kwdict : dict
            A dictionary with keywords that are applicable to a particular
            event.
        """
        if self._suspended_until == event:
            self._suspended = False
            self._suspended_until = None
        if self._suspended:
            oslogger.debug('event suspended {}'.format(event))
            return
        oslogger.debug('firing {}'.format(event))
        if event == u'open_experiment':
            for ext in self._extensions:
                ext.register_ui_files()
        for ext in self.events.get(event, []):
            try:
                ext.fire(event, **kwdict)
            except Exception as e:
                if not isinstance(e, osexception):
                    e = osexception(msg=u'Extension error', exception=e)
                self.notify(
                    u'Extension %s misbehaved on event %s (see debug window for stack trace)'
                    % (ext.name(), event)
                )
                self.console.write(e)

    def provide(self, provide, **kwdict):

        if provide not in self.provides:
            oslogger.debug('cannot not provide {}'.format(provide))
            return None
        ext = self.provides[provide]
        oslogger.debug('{} provides {}'.format(ext, provide))
        try:
            return ext.provide(provide, **kwdict)
        except Exception as e:
            if not isinstance(e, osexception):
                e = osexception(msg=u'Extension error', exception=e)
            self.notify(
                u'Extension %s misbehaved on providing %s (see debug window for stack trace)'
                % (ext.name(), provide)
            )
            self.console.write(e)

    def activate(self, ext_name):

        try:
            ext = self[ext_name]
        except Exception:
            return
        ext.activate()

    def suspend(self):
        r"""Suspends all events."""
        self._suspended = True

    def suspend_until(self, event):
        r"""Suspends all events until a specific event is fired. This is useful
        for situations where you want to supress all events between a starting
        and ending event.
        """
        self._suspended = True
        self._suspended_until = event

    def resume(self):
        r"""Resumes all events."""
        self._suspended = False

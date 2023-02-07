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
import time
from libopensesame.oslogging import oslogger
from libqtopensesame.misc import drag_and_drop
from libqtopensesame.misc.base_component import BaseComponent


class BaseSubcomponent(BaseComponent):

    r"""A base class for all components that require an experiment and theme
    property.
    """
    def name(self):
        """
        returns:
            desc:    The name of the extension, i.e. the extension class name.
            type:    unicode
        """
        return safe_decode(self.__class__.__name__, enc=u'utf-8')

    def fire(self, event, **kwdict):
        r"""Calls an event function, if it exists.

        Parameters
        ----------
        event : str, unicode
            The event name, which is handled by a function called `event_[event
            name]`.
        **kwdict : dict
            A keyword dictionary with event-specific keywords.
        """
        if hasattr(self, u'event_%s' % event):
            getattr(self, u'event_%s' % event)(**kwdict)

    def _fire_and_time(self, event, **kwdict):
        r"""Similar to fire() but also keeps track of the duration of each
        event for benchmarking purposes. This function is used if the
        --performance-profile argument is passed.
        """
        if hasattr(self, u'event_%s' % event):
            t0 = time.time()
            getattr(self, u'event_%s' % event)(**kwdict)
            if event not in self._event_durations:
                self._event_durations[event] = []
            self._event_durations[event].append(time.time() - t0)

    def provide(self, provide, **kwdict):
        r"""Executing a providing function, if it exists.

        Parameters
        ----------
        provide : str, unicode
            The provide name, which is handled by a function called
            `provide_[event name]`.
        **kwdict : dict
            A keyword dictionary with provide-specific keywords.


        Returns
        -------
        The return value of the providing function.
        """
        if hasattr(self, u'provide_%s' % provide):
            return getattr(self, u'provide_%s' % provide)(**kwdict)

    def supported_events(self):
        r"""Gives the events that are supported by the extension. This is done
        by introspecting which `event_[event name]` functions exist.

        Returns
        -------
        list
            A list of supported events.
        """
        events = []
        for event in dir(self):
            if event.startswith(u'event_'):
                events.append(event[6:])
                oslogger.debug(
                    u'extension %s supports %s' % (self.name(), event)
                )
        return events

    def supported_provides(self):
        r"""Gives the provides that are supported by the extension. This is
        done by introspecting which `provide_[provide name]` functions exist.

        Returns
        -------
        list
            A list of supported provides.
        """
        provides = []
        for provide in dir(self):
            if provide.startswith(u'provide_'):
                provides.append(provide[8:])
                oslogger.debug(
                    u'extension %s provides %s' % (self.name(), provide)
                )
        return provides

    # These properties allow for cleaner programming, without dot references.

    @property
    def experiment(self):
        return self.main_window.experiment

    @property
    def tabwidget(self):
        return self.main_window.ui.tabwidget

    @property
    def theme(self):
        return self.main_window.theme

    @property
    def notify(self):
        return self.main_window.experiment.notify

    @property
    def text_input(self):
        return self.main_window.experiment.text_input

    @property
    def item_store(self):
        return self.experiment.items

    @property
    def extensions(self):
        return self.main_window.extension_manager._extensions

    @property
    def extension_manager(self):
        return self.main_window.extension_manager
    
    @property
    def unloaded_extension_manager(self):
        return self.main_window._unloaded_extension_manager
    
    @property
    def plugin_manager(self):
        return self.main_window.experiment._plugin_manager

    @property
    def overview_area(self):
        return self.main_window.ui.itemtree

    @property
    def console(self):
        return self.main_window.console

    @property
    def pool(self):
        return self.main_window.experiment.pool

    @property
    def locale(self):
        return self.main_window._locale

    @property
    def item_toolbar(self):
        return self.main_window.ui.toolbar_items

    @property
    def main_toolbar(self):
        return self.main_window.ui.toolbar_main


# Alias for backwards compatibility
base_subcomponent = BaseSubcomponent

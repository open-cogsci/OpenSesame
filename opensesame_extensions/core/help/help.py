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
from qtpy import QtWidgets, QtCore
import webbrowser
import yaml
from libopensesame import metadata
from libqtopensesame.extensions import BaseExtension
from libqtopensesame.misc.base_subcomponent import BaseSubcomponent
from libqtopensesame.misc.config import cfg
from libqtopensesame.misc.translate import translation_context
from urllib.request import urlopen
_ = translation_context(u'help', category=u'extension')


class ActionPage(QtWidgets.QAction, BaseSubcomponent):

    r"""A menu entry for a single help page."""
    def __init__(self, main_window, title, link, menu):
        r"""Constructor.

        Parameters
        ----------
        main_window
            The main-window object.
        title
            The menu title.
        link
            The URL to open.
        menu
            The menu for the action.
        """
        QtWidgets.QAction.__init__(
            self, main_window.theme.qicon(u'applications-internet'),
            title,
            menu
        )
        self.setup(main_window)
        self.title = title
        self.link = link
        self.triggered.connect(self.open_page)

    def open_page(self):
        r"""Opens the page URL."""
        webbrowser.open(self.link)


class GetSitemapThread(QtCore.QThread):

    r"""A thread that asynchronously retrieves the documentation sitemap."""
    def __init__(self, help, sitemap_url, local_sitemap):

        QtCore.QThread.__init__(self)
        self._help = help
        self._sitemap_url = sitemap_url
        self._local_sitemap = local_sitemap
        self.sitemap = None

    def run(self):

        try:
            fd = urlopen(self._sitemap_url)
            self.sitemap = fd.read()
        except Exception:
            if self._local_sitemap is None:
                return
            with safe_open(self._help.ext_resource(self._local_sitemap)) as fd:
                self.sitemap = fd.read()


class Help(BaseExtension):

    def event_startup(self):
        r"""Build the menu on startup."""
        self._urls = []
        self.menu = self.menubar.addMenu(_(u'Help'))
        self._wait_action = QtWidgets.QAction(
            self.theme.qicon(u'process-working'),
            _(u'Please wait …'),
            self.menu
        )
        self._wait_action.setEnabled(False)
        self.menu.addAction(self._wait_action)
        # It can take some time to download the sitemap from cogsci. Therefore,
        # we use threading.
        self._get_sitemap_thread = GetSitemapThread(
            self,
            sitemap_url=cfg.online_help_sitemap.replace(
                u'[version]',
                metadata.major_version
            ),
            local_sitemap=None
        )
        self._get_sitemap_thread.start()
        self._get_sitemap_thread.finished.connect(self.populate_help_menu)

    def populate_help_menu(self):
        r"""Is collected when the sitemap is done loading, and populates the
        menu.
        """
        if self._get_sitemap_thread.sitemap is None:
            return
        try:
            _dict = safe_yaml_load(self._get_sitemap_thread.sitemap)
        except yaml.scanner.ScannerError:
            # If the sitemap was loaded but was not a valid yaml string. This
            # can happen for example when a captive portal returns something
            # invalid
            return
        if not isinstance(_dict, dict):
            return
        self.menu.clear()
        menu = self.build_menu(
            self.menu,
            cfg.online_help_base_url,
            _(u'Online help'),
            _dict,
            sub_menu=cfg.online_help_psychopy
        )
        if menu is not None:
            self.action_online_help = self.menu.addMenu(menu)
        if cfg.online_help_psychopy:
            menu = self.psychopy_help_menu()
            if menu is not None:
                self.action_psychopy_help = self.menu.addMenu(menu)
        self.menu.addSeparator()

    def build_menu(self, parent_menu, base_url, title, _dict, sub_menu=True):
        r"""A helper function to build the online-help menu.

        Parameters
        ----------
        parent_menu
            A parent QMenu for a submenu.
        base_url
            A prefix for relative urls.
        title
            A menu title.
        _dict
            A dict extracted from the sitemap with page names and contents.

        Returns
        -------
        A QMenu.
        """
        if sub_menu:
            menu = parent_menu.addMenu(
                self.theme.qicon(u'applications-internet'),
                title
            )
        else:
            menu = parent_menu
        for name, link in _dict.items():
            if not isinstance(link, str):
                self.build_menu(menu, base_url, name, link)
                return
            if not self._is_url(link):
                link = base_url+link
            self._urls.append(link)
            menu.addAction(
                ActionPage(
                    self.main_window,
                    safe_decode(name, enc=u'utf-8'),
                    link,
                    menu
                )
            )
        return menu

    def psychopy_help_menu(self):
        r"""Builds a PsychoPy help menu.

        Returns
        -------
        A QMenu.
        """
        with safe_open(self.ext_resource(u'psychopy_sitemap.yaml')) as fd:
            sitemap = fd.read()
        _dict = safe_yaml_load(sitemap)
        menu = self.build_menu(self.menu, None, _(u'PsychoPy API'), _dict)
        return menu

    def _is_url(self, link):
        r"""Verifies whether a string corresponds to an http(s) url."""
        return link.startswith(u'http://') or link.startswith(u'https://')

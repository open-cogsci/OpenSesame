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
from openexp import resources
from libopensesame import metadata, misc
from libqtopensesame.misc.base_subcomponent import BaseSubcomponent
from libqtopensesame.misc.config import cfg
from libqtopensesame.widgets.tab_bar import TabBar
from qtpy import QtGui, QtWidgets, QtCore
from libqtopensesame.misc.translate import translation_context
_ = translation_context(u'tab_widget', category=u'core')

# Determines how many tabs are kept active and automatically switched back to
# when the current tab is closed.
MAX_TAB_STACK = 3


class TabWidget(BaseSubcomponent, QtWidgets.QTabWidget):

    """A custom tab widget with some extra functionality"""
    tab_removed = QtCore.Signal(int)
    tab_inserted = QtCore.Signal(int)

    def __init__(self, parent=None):
        r"""Constructor

        Parameters
        ----------
        parent, optional
            The parent QWidget
        """
        QtWidgets.QTabWidget.__init__(self, parent)
        self.setTabBar(TabBar(self))
        BaseSubcomponent.setup(self, parent)
        self.tabCloseRequested.connect(self.removeTab)
        self.currentChanged.connect(self.index_changed)
        self.setSizePolicy(
            QtWidgets.QSizePolicy.MinimumExpanding,
            QtWidgets.QSizePolicy.MinimumExpanding
        )
        self.shortcut_switch_left = QtWidgets.QShortcut(
            QtGui.QKeySequence.PreviousChild,
            self.main_window,
            self.switch_prev,
            self.switch_prev
        )
        self.shortcut_switch_right = QtWidgets.QShortcut(
            QtGui.QKeySequence.NextChild,
            self.main_window,
            self.switch_next,
            self.switch_next
        )
        self._tab_stack = []

    def switch_prev(self):
        r"""Switches to the previous tab."""
        i = self.currentIndex() - 1
        if i < 0:
            i = self.count() - 1
        self.setCurrentIndex(i)

    def switch_next(self):
        r"""Switches to the next tab."""
        i = self.currentIndex() + 1
        if i >= self.count():
            i = 0
        self.setCurrentIndex(i)

    def _update_actions(self):

        count = self.count()
        index = self.currentIndex()
        self.main_window.ui.action_close_other_tabs.setVisible(count > 1)
        self.main_window.ui.action_close_all_tabs.setVisible(count > 0)
        self.main_window.ui.action_close_current_tab.setVisible(count > 0)

    def tabRemoved(self, i):
        r"""Overridden to emit the tab_removed signal when a tab has been
        removed.
        """
        QtWidgets.QTabWidget.tabRemoved(self, i)
        self.tab_removed.emit(i)
        self._update_actions()

    def tabInserted(self, i):
        r"""Overridden to emit the tab_removed signal when a tab has been
        removed.
        """
        QtWidgets.QTabWidget.tabInserted(self, i)
        self.tab_inserted.emit(i)
        self._update_actions()

    def add(self, widget, icon, name, switch=True):
        r"""Open a tab, or switches to it if the tab already exists.

        Parameters
        ----------
        widget
            A QWidget for the tab
        icon
            The name of an icon or a QIcon
        name
            A name for the tab
        switch : bool, optional
            Indicates whether the tab should be switched to.
        """
        # If a widget is currently open, then we push it to the stack so that
        # we can go back to it later when the newly added widget is closed.
        current_index = self.currentIndex()
        current_widget = self.widget(current_index)
        if current_widget is not None:
            self._tab_stack.append((
                current_widget,
                self.tabIcon(current_index),
                self.tabText(current_index))
            )
            self._tab_stack = self._tab_stack[-MAX_TAB_STACK:]
        index = self.indexOf(widget)
        if index < 0:
            index = self.addTab(
                widget,
                self.main_window.theme.qicon(icon),
                name
            )
        if switch:
            self.setCurrentIndex(index)

    def remove(self, widget):
        r"""Removes the tab with a given widget in it.

        Parameters
        ----------
        widget : QWidget
            The widget in the tab.
        """
        index = self.indexOf(widget)
        if index >= 0:
            self.removeTab(index)

    def set_icon(self, widget, icon):
        r"""Sets the icon for a tab with a specific widget.

        Parameters
        ----------
        widget : QWidget
            A widget.
        icon : unicode
            An icon name.
        """
        index = self.indexOf(widget)
        if index >= 0:
            self.setTabIcon(index, self.theme.qicon(icon))

    def close_all(self, dummy=None, avoid_empty=True):
        r"""Closes all tabs.

        Parameters
        ----------
        avoid_empty : bool, optional
            Indicates whether the general tab should be automatically opened if
            all tabs are closed.
        """
        while self.count():
            self.removeTab(0)
        if avoid_empty and not self.count():
            self.open_general()

    def close_current(self, dummy=None, avoid_empty=True):
        r"""Closes the current tab.

        Parameters
        ----------
        avoid_empty : bool, optional
            Indicates whether the general tab should be automatically opened if
            all tabs are closed.
        """
        self.removeTab(self.currentIndex())
        if not avoid_empty or self.count():
            return
        if self._tab_stack:
            self.add(*self._tab_stack.pop())
        else:
            self.open_general()

    def close_other(self):
        """Close all tabs except for the currently opened one"""
        while self.count() > 0 and self.currentIndex() != 0:
            self.removeTab(0)
        while self.count() > 1:
            self.removeTab(1)

    def get_index(self, tab_name):
        """
        Return the index of a specific tab

        Arguments:
        tab_name -- the tab_name of the widget

        Returns:
        The index of the tab or None if the tab wasn't found
        """
        for i in range(self.count()):
            w = self.widget(i)
            if (hasattr(w, u"tab_name") and w.tab_name == tab_name) or \
                    (hasattr(w, tab_name)):
                return i
        return None

    def get_item(self, item):
        """
        Return the index of a specific item tab

        Arguments:
        item -- the name of the item

        Returns:
        The index of the tab or None if the tab wasn't found
        """
        for i in range(self.count()):
            w = self.widget(i)
            if (hasattr(w, u"__edit_item__") and w.__edit_item__ == item):
                return i
        return None

    def current_item(self):
        """
        returns:
                desc:	The name of the currently visible item, or None if no item
                                is currently visible.
                type:	[str, NoneType]
        """
        w = self.currentWidget()
        if hasattr(w, u'__item__'):
            return w.__item__
        return None

    def get_widget(self, tab_name):
        """
        Return a specific tab

        Arguments:
        tab_name -- the tab_name of the widget

        Returns:
        A QWidget or None if the tab wasn't found
        """
        i = self.get_index(tab_name)
        if i is None:
            return None
        return self.widget(i)

    def open_browser(self, url):
        """
        Open a browser tab to browse local or remote HTML files

        Argument:
        url -- a url
        """
        from libqtopensesame.widgets import webbrowser
        browser = webbrowser.webbrowser(self.main_window)
        browser.load(url)
        self.add(browser, u"applications-internet", _(u'Help'))

    def open_help(self, item):
        r"""Opens a help tab for the specified item. Looks for a file called
        [item].html or [item].md in the resources folder.

        Parameters
        ----------
        item
            The item for which help should be displayed.
        """
        import os
        try:
            path = resources[f'{item}.md']
        except FileNotFoundError:
            try:
                path = resources[f'{item}.html']
            except FileNotFoundError:
                path = resources[f'help/missing.md']
        self.open_browser(path)

    def open_backend_settings(self):
        """Opens the backend settings"""
        if self.switch(u'__backend_settings__'):
            return
        from libqtopensesame.widgets.backend_settings import backend_settings
        self.add(backend_settings(self.main_window), u'backend',
                 _(u'Back-end settings'))

    def open_forum(self):
        """Open osdoc.cogsci.nl"""
        self.open_browser(u'http://forum.cogsci.nl')

    def open_general(self):
        """Opens the general tab"""
        if self.switch(u'__general_properties__'):
            return
        from libqtopensesame.widgets.general_properties import general_properties
        w = general_properties(self.main_window)
        self.add(w, u'experiment', _(u'General properties'))

    def open_general_script(self):
        """Opens the general script editor"""
        if self.switch(u'__general_script__'):
            return
        from libqtopensesame.widgets.general_script_editor import \
            general_script_editor
        self.add(general_script_editor(self.main_window), u'utilities-terminal',
                 _(u'General script editor'))

    def open_osdoc(self, url=u''):
        r"""Open a page on osdoc.cogsci.nl."""
        misc.open_url(
            u'http://osdoc.cogsci.nl/%s/%s' % (metadata.main_version, url)
        )

    def open_stdout_help(self):
        """Open the debug window help tab"""
        self.open_osdoc(u'manual/interface')

    def open_unused(self):
        """Opens the unused tab"""
        if self.switch(u'__unused__'):
            return
        from libqtopensesame.widgets.unused_widget import unused_widget
        w = unused_widget(self.main_window)
        self.add(w, u'unused', _(u'Unused items'))

    def open_preferences(self):
        """Open the preferences tab"""
        from libqtopensesame.widgets import preferences_widget
        if not self.switch(u"__preferences__"):
            self.add(preferences_widget.preferences_widget(self.main_window),
                     u"options", _(u"Preferences"))

    def switch(self, tab_name):
        """
        Switch to a specific tab

        Returns:
        True if the tab exists, False otherwise
        """
        i = self.get_index(tab_name)
        if i is None:
            return False
        self.setCurrentIndex(i)
        return True

    def toggle_onetabmode(self):
        """Toggles onetabmode"""
        cfg.onetabmode = self.main_window.ui.action_onetabmode.isChecked()
        if cfg.onetabmode:
            self.close_other()
            self.tabBar().setVisible(False)
        else:
            self.tabBar().setVisible(True)
        self.setTabsClosable(not cfg.onetabmode)
        self.main_window.ui.action_close_all_tabs.setEnabled(
            not cfg.onetabmode)
        self.main_window.ui.action_close_current_tab.setEnabled(
            not cfg.onetabmode)
        self.main_window.ui.action_close_other_tabs.setEnabled(
            not cfg.onetabmode)

    def index_changed(self, index):
        """
        Monitors tab index changes, closing other tabs if onetabmode is enabled

        Arguments:
        index -- the index of the new tab
        """
        self.currentChanged.disconnect()
        if cfg.onetabmode:
            self.close_other()
        w = self.currentWidget()
        if hasattr(w, u'on_activate'):
            w.on_activate()
        self.currentChanged.connect(self.index_changed)
        self._update_actions()

    def open_markdown(self, md, icon=u'dialog-information',
                      title=u'Attention!', url=None, tmpl=None):
        r"""Opens a Markdown-formatted tab.

        Parameters
        ----------
        md : str
            If it ends with `.md`, this is interpreted as a file name.
            Otherwise, it is interpreted as markdown text.
        icon : str, optional
            The name of the tab icon.
        title : str, optional
            The tab title.
        url : str, optional
            A url to identify the page. This only applies when the markdown is
            provided as text; otherwise the markdown filename is used.
        """
        from libqtopensesame.widgets.webbrowser import webbrowser
        wb = webbrowser(self.main_window)
        if md.endswith(u'.md'):
            wb.load(md, tmpl=tmpl)
        else:
            wb.load_markdown(md, url=url, tmpl=tmpl)
        self.main_window.tabwidget.add(wb, icon, title)

    def focus(self):
        r"""Properly give focus to the current widget (if any)."""
        item = self.current_item()
        if item is None:
            return
        self.experiment.items[item].set_focus()


# Alias for backwards compatibility
tab_widget = TabWidget

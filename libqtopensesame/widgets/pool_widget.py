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
from libopensesame import misc
from libopensesame.oslogging import oslogger
from libqtopensesame.misc.config import cfg
from libqtopensesame.widgets.base_widget import BaseWidget
from libqtopensesame._input.popup_menu import PopupMenu
from libqtopensesame._input.confirmation import Confirmation
from qtpy import QtCore, QtWidgets
import os
import os.path
import shutil
from libqtopensesame.misc.translate import translation_context
_ = translation_context(u'pool_widget', category=u'core')


class PoolWidget(BaseWidget):

    r"""The file-pool widget."""
    def __init__(self, main_window):
        r"""Constructor.

        Parameters
        ----------
        main_window
            The main-window object.
        """
        self.max_len = 5
        super().__init__(main_window, ui=u'widgets.pool_widget')
        self.ui.button_pool_add.clicked.connect(self.select_and_add)
        self.ui.button_refresh.clicked.connect(self.refresh)
        self.ui.button_help_pool.clicked.connect(self.help)
        self.ui.button_browse_pool.clicked.connect(self.browse)
        self.ui.edit_pool_filter.textChanged.connect(self.refresh)
        self.ui.combobox_view.currentIndexChanged.connect(self.set_view)
        self.ui.list_pool.itemActivated.connect(self.activate_file)
        self.ui.list_pool.itemChanged.connect(self.rename_file)
        self.main_window.theme.apply_theme(self)
        self.ui.label_size_warning.setVisible(False)

    def help(self):
        r"""Opens the help tab."""
        self.tabwidget.open_osdoc(u'manual/interface')

    def set_view(self):
        r"""Sets the viewmode (list/ icons) based on the gui control."""
        if self.ui.combobox_view.currentIndex() == 0:
            self.ui.list_pool.setViewMode(QtWidgets.QListView.ListMode)
        else:
            self.ui.list_pool.setViewMode(QtWidgets.QListView.IconMode)

    def browse(self):
        r"""Opens the pool folder in the file manager in an OS specific way."""
        misc.open_url(self.experiment.pool.folder())

    def add(self, files, rename=False):
        r"""Adds a list of files to the pool.

        Parameters
        ----------
        files : list
            A list of paths.
        """
        if not files:
            return
        n_replace = sum(
            self.pool.in_folder(os.path.basename(path))
            for path in files
        )
        if not rename and n_replace:
            if n_replace == 1:
                msg = _(
                    u"The file pool already contains a file with the same name. Do you want to overwrite it?")
            else:
                msg = _(
                    u"The file pool already contains files with the same names. Do you want to overwrite {} files?")
            c = confirmation(self.main_window, msg.format(n_replace))
            if not c.show():
                return
        for path in files:
            basename = os.path.basename(path)
            if self.pool.in_folder(basename) and rename:
                while self.pool.in_folder(basename):
                    basename = u'_' + basename
            try:
                self.pool.add(path, new_name=basename)
            except (IOError, shutil.Error) as e:
                self.notify(_(u'Failed to copy %s to file pool') % path)
                self.console.write(safe_decode(e, errors=u'ignore'))
        self.refresh()
        self.select(basename)

    def select_and_add(self, dummy=None):
        r"""Adds one or more files to the pool."""
        path_list = QtWidgets.QFileDialog.getOpenFileNames(
            self.main_window.ui.centralwidget, _(u"Add files to pool"),
            directory=cfg.default_pool_folder)
        if not path_list:
            return
        # Qt5 puts the first element in another list, check for that here
        if isinstance(path_list[0], list):
            path_list = path_list[0]
        if not path_list:
            return
        cfg.default_pool_folder = os.path.dirname(path_list[0])
        self.add(path_list)

    def select(self, fname):
        r"""Selects a specific file in the file pool.

        Parameters
        ----------
        fname : str, unicode
            The file to be selected.
        """
        for i in range(self.ui.list_pool.count()):
            item = self.ui.list_pool.item(i)
            if item.text() == fname:
                self.ui.list_pool.setCurrentItem(item)

    def refresh(self):
        r"""Refreshes the contents of the pool widget."""
        try:
            path_iterator = iter(self.pool)
        except Exception as e:
            self.notify(_(u'Failed to refresh file pool'))
            self.console.write(safe_decode(e, errors=u'ignore'))
            return
        filt = self.ui.edit_pool_filter.text().lower()
        self.ui.list_pool.clear()
        for path in path_iterator:
            oslogger.debug(path)
            fname = os.path.basename(path)
            if filt in fname.lower():
                icon = self.theme.qfileicon(self.pool[path])
                item = QtWidgets.QListWidgetItem(icon, fname)
                item.setFlags(item.flags() | QtCore.Qt.ItemIsEditable)
                item.icon = icon
                item.path = path
                item.setToolTip(path)
                self.ui.list_pool.addItem(item)
        try:
            size = self.pool.size()
        except:
            size = -1
        oslogger.debug(u'pool is %d bytes' % size)
        if size > cfg.file_pool_size_warning:
            self.ui.label_size_warning.setText(_('Your file pool is larger '
                                                 'than usual (%d MB). This increases loading and saving time. '
                                                 'Consider moving files from the file pool to the experiment '
                                                 'folder.') % (size / 1048576))
            self.ui.label_size_warning.setVisible(True)
        else:
            self.ui.label_size_warning.setVisible(False)

    def open_file(self, path):
        r"""Opens a file in a platform specific way.

        Parameters
        ----------
        path : unicode, str
            The file to be opened.
        """
        misc.open_url(self.pool[path])

    def activate_file(self, item):
        r"""Is called when a file is double-clicked or otherwise activated and
        opens the file.

        Parameters
        ----------
        item : QListWidgetItem
        """
        self.open_file(item.path)

    def contextMenuEvent(self, event):
        r"""Presents a context menu.

        Parameters
        ----------
        event : QMouseClickEvent
        """
        item = self.ui.list_pool.itemAt(self.ui.list_pool.mapFromGlobal(
            event.globalPos()))
        if item is None:
            return
        path = item.path
        pm = PopupMenu(self, [
            (0, _(u'Open'), item.icon),
            (1, _(u'Remove from pool'), u'delete'),
            (2, _(u'Rename'), u'rename'),
        ])
        action = pm.show()
        if action == 0:
            self.open_file(path)
        elif action == 1:
            self.delete_selected_files()
        elif action == 2:
            self.ui.list_pool.editItem(item)

    def delete_selected_files(self):
        r"""Deletes all selected files from the pool. Asks for confimation\
        first.
        """
        # Prepare the confirmation dialog, which contains a limited nr of
        # filenames
        l = []
        suffix = u''
        for item in self.ui.list_pool.selectedItems()[:self.max_len]:
            l.append(self.pool[item.text()])
        if len(self.ui.list_pool.selectedItems()) > self.max_len:
            suffix = _('And %d more file(s)') % \
                (len(self.ui.list_pool.selectedItems())-self.max_len)
        msg = _(u"<p>Are you sure you want to remove the following files?</p>"
                u"<p>- %s</p> <p>%s</p>") % (u"<br /> - ".join(l), suffix)
        c = Confirmation(self.main_window, msg)
        if not c.show():
            return
        # Create a list of files to be removed
        dL = []
        for item in self.ui.list_pool.selectedItems():
            dL.append(item.path)
        # Remove the files
        try:
            for f in dL:
                del self.pool[f]
            oslogger.debug(u"removed '%s'" % f)
        except:
            oslogger.error(u"failed to remove '%s'" % f)
        self.refresh()
        self.main_window.set_unsaved()

    def rename_file(self, item):
        r"""Starts a rename action for an item.

        Parameters
        ----------
        item : QListWidgetItem
        """
        old_name = item.path
        new_name = item.text().strip()
        if new_name in self.pool:
            self.notify(
                _(u"There already is a file named '%s' in the file pool")
                % new_name)
            new_name = old_name
        elif new_name in (old_name, u''):
            new_name = old_name
        else:
            try:
                self.pool.rename(old_name, new_name)
            except:
                self.notify(_(u'Failed to rename "%s" to "%s".')
                            % (old_name, new_name))
        self.refresh()
        self.select(new_name)

    def dragEnterEvent(self, event):
        r"""Accepts an incoming drag that precedes a drop.

        Parameters
        ----------
        event : QDragEnterEvent
        """
        event.acceptProposedAction()

    def dropEvent(self, event):
        r"""Accepts an incoming drop.

        Parameters
        ----------
        event : QDropEnterEvent
        """
        files = []
        for url in event.mimeData().urls():
            files.append(url.toLocalFile())
        self.add(files)
        event.acceptProposedAction()

    def focusInEvent(self, e):
        r"""Focus the filter edit when the widget receives focus.

        Parameters
        ----------
        e : QFocusEvent
        """
        self.ui.edit_pool_filter.setFocus()


def select_from_pool(main_window, parent=None):
    r"""A static function that presents the select from pool dialog.

    Parameters
    ----------
    main_window
        The GUI main window
    parent, optional
        The parent QWidget or None to use main window's central widget.
    """
    if parent is None:
        parent = main_window.ui.centralwidget
    d = QtWidgets.QDialog(parent)
    widget = PoolWidget(main_window)
    widget.refresh()
    bbox = QtWidgets.QDialogButtonBox(d)
    bbox.addButton(_(u"Cancel"), QtWidgets.QDialogButtonBox.RejectRole)
    bbox.addButton(_(u"Select"), QtWidgets.QDialogButtonBox.AcceptRole)
    bbox.accepted.connect(d.accept)
    bbox.rejected.connect(d.reject)
    vbox = QtWidgets.QVBoxLayout()
    vbox.addWidget(widget)
    vbox.addWidget(bbox)
    d.setLayout(vbox)
    d.setWindowTitle(_(u"Select file from pool"))
    res = d.exec_()
    main_window.ui.pool_widget.refresh()
    if res == QtWidgets.QDialog.Rejected:
        return u""
    selected = widget.ui.list_pool.currentItem()
    if selected is None:
        return u""
    return selected.text()


# Alias for backwards compatibility
pool_widget = PoolWidget

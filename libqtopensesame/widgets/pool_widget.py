#-*- coding:utf-8 -*-

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

from libopensesame import debug, misc
from libqtopensesame.misc import _
from libqtopensesame.misc.config import cfg
from libqtopensesame.widgets.base_widget import base_widget
from PyQt4 import QtCore, QtGui
import os
import platform
import os.path
import shutil
import subprocess

class pool_widget(base_widget):

	"""The file pool widget"""

	def __init__(self, main_window):

		"""
		Constructur

		Arguments:
		main_window		--	The GUI main window.

		Keyword arguments:
		parent			--	A parent widget. (default=None)
		"""

		# Known image and sound extensions
		self.exts = {u"image" : (u".png", u".jpg", u".bmp", u".gif", \
			u".jpeg"), \
			u"sound" : (u".ogg", u".wav"), \
			u"text" : (u".txt", u".csv", u".tsv"), \
			u"python" : (u".py", u".pyc"), \
			u"video" : (u".avi", u".mpg", u".wmv", u".mpeg", u".mov", u".ogv", \
				u".mp4", u".flv"), \
			u"pdf" : (u".pdf"), \
			}

		self.max_len = 5
		super(pool_widget, self).__init__(main_window,
			ui=u'widgets.pool_widget')
		self.ui.button_pool_add.clicked.connect(self.select_and_add)
		self.ui.button_refresh.clicked.connect(self.refresh)
		self.ui.button_help_pool.clicked.connect(self.help)
		self.ui.button_browse_pool.clicked.connect(self.browse)
		self.ui.edit_pool_filter.textChanged.connect(self.refresh)
		self.ui.combobox_view.currentIndexChanged.connect(self.set_view)
		self.ui.list_pool.itemActivated.connect(self.activate_file)
		self.main_window.theme.apply_theme(self)

		self.ui.combobox_view.setItemIcon(0, self.main_window.theme.qicon( \
			u"view-list-details"))
		self.ui.combobox_view.setItemIcon(1, self.main_window.theme.qicon( \
			u"view-list-icons"))

	def help(self):

		"""Open the help tab"""

		self.main_window.ui.tabwidget.open_help(u"pool")

	def set_view(self):

		"""Set the viewmode (list/ icons) based on the gui control"""

		if self.ui.combobox_view.currentIndex() == 0:
			self.ui.list_pool.setViewMode(QtGui.QListView.ListMode)
		else:
			self.ui.list_pool.setViewMode(QtGui.QListView.IconMode)

	def browse(self):

		"""Open the pool folder in the file manager in an OS specific way"""

		misc.open_url(self.experiment.pool_folder)

	def add(self, files):

		"""
		Add a list of files to the pool.

		Arguments:
		files - A list of paths
		"""

		basename = ""
		for path in files:
			path = str(path)
			debug.msg(path)
			basename = os.path.basename(path)
			if not os.path.isfile(path):
				self.experiment.notify( \
					_(u"'%s' is not a regular file and could not be added to the file pool.") \
					% path)
			else:
				# If a similar file already exists in the pool, ask before overwriting
				if os.path.exists(os.path.join( \
					self.experiment.pool_folder, basename)):
					resp = QtGui.QMessageBox.question(self, _("Overwrite"), \
						_(u"A file named '%s' already exists in the pool. Do you want to overwrite this file?") \
						% basename, QtGui.QMessageBox.Yes, QtGui.QMessageBox.No)
					if resp == QtGui.QMessageBox.Yes:
						shutil.copyfile(path, os.path.join( \
							self.experiment.pool_folder, basename))
				else:
					shutil.copyfile(path, os.path.join( \
						self.experiment.pool_folder, basename))

		self.refresh()
		self.select(basename)

	def select_and_add(self, dummy = None):

		"""
		Add one or more files to the pool

		Keyword arguments:
		dummy -- a dummy argument passed py the signal handler (default=None)
		"""

		path_list = QtGui.QFileDialog.getOpenFileNames( \
			self.main_window.ui.centralwidget, _(u"Add files to pool"), \
			directory=cfg.default_pool_folder)
		if len(path_list) == 0:
			return
		cfg.default_pool_folder = os.path.dirname(str(path_list[0]))
		self.add(path_list)

	def select(self, fname):

		"""
		Select a specific file in the file pool

		Arguments:
		fname -- the file to be selected
		"""

		for i in range(self.ui.list_pool.count()):
			item = self.ui.list_pool.item(i)
			if str(item.text()) == fname:
				self.ui.list_pool.setCurrentItem(item)

	def file_type(self, fname):

		"""
		Determine the type of a file based on the extension

		Arguments:
		fname -- the file under investigation

		Returns:
		A string with the filetype or "unknown"
		"""

		ext = os.path.splitext(fname)[1].lower()
		for file_type in self.exts:
			if ext in self.exts[file_type]:
				return file_type
		return u"unknown"

	def refresh(self):

		"""Refresh the contents of the pool widget"""

		filt = str(self.ui.edit_pool_filter.text()).lower()
		self.ui.list_pool.clear()

		# This function can be called after the pool has been cleaned
		# up. This should not lead to a warning.
		if not os.path.exists(self.experiment.pool_folder):
			return

		file_list = os.listdir(self.experiment.pool_folder)
		if self.experiment.fallback_pool_folder is not None:
			file_list += os.listdir(self.experiment.fallback_pool_folder)
		for fname in file_list:
			debug.msg(fname)
			if filt in fname.lower():
				icon = self.experiment.icon(self.file_type(fname))
				item = QtGui.QListWidgetItem(icon, fname)
				item.icon = icon
				item.path = os.path.join( \
					self.experiment.pool_folder, fname)
				self.ui.list_pool.addItem(item)

	def open_file(self, path):

		"""
		Open a file in a platform specific way

		Arguments:
		path -- the full path to the file to be opened
		"""

		misc.open_url(path)

	def activate_file(self, item):

		"""
		Is called when a file is double-clicked or
		otherwise activated and opens the file.

		Arguments:
		item -- a listWidgetItem
		"""

		self.open_file(item.path)

	def contextMenuEvent(self, event):

		"""
		Presents a context menu

		Arguments:
		event -- a mouseClickEvent
		"""

		item = self.ui.list_pool.itemAt(self.ui.list_pool.mapFromGlobal( \
			event.globalPos()))
		if item is None:
			return
		menu = QtGui.QMenu()
		menu.addAction(item.icon, _(u"Open"))
		menu.addSeparator()
		menu.addAction(self.experiment.icon(u"delete"), \
			_(u"Remove from pool"))
		menu.addAction(self.experiment.icon(u"rename"), _(u"Rename"))
		menu.triggered.connect(self.context_action)
		self.context_target = str(item.text())
		menu.exec_(event.globalPos())

	def context_action(self, action):

		"""
		Perform a conext menu action

		Arguments:
		action -- the action to be performed
		"""

		a = str(action.text())
		f = os.path.join(self.experiment.pool_folder, \
			self.context_target)

		if a == _(u"Open"):
			self.open_file(f)

		elif a == _(u"Remove from pool"):

			# Prepare the confirmation dialog, which contains a limited nr of
			# filenames
			l = []
			suffix = ''
			for item in self.ui.list_pool.selectedItems()[:self.max_len]:
				l.append(str(item.text()))
			if len(self.ui.list_pool.selectedItems()) > self.max_len:
				suffix = _('And %d more file(s)') % \
					(len(self.ui.list_pool.selectedItems())-self.max_len)

			# Ask for confirmation
			resp = QtGui.QMessageBox.question(self, _(u"Remove"), \
				_(u"<p>Are you sure you want to remove the following files from the file pool? This operation will only affect the OpenSesame file pool, not the original files on your disk.</p><p><b> - %s</b></p><p>%s</p>") \
				% (u"<br /> - ".join(l), suffix), QtGui.QMessageBox.Yes, \
				QtGui.QMessageBox.No)
			if resp == QtGui.QMessageBox.No:
				return

			# Create a list of files to be removed
			dL = []
			for item in self.ui.list_pool.selectedItems():
				dL.append(str(item.text()))

			# Remove the files
			try:
				for f in dL:
					os.remove(os.path.join( \
						self.experiment.pool_folder, f))
				debug.msg(u"removed '%s'" % self.context_target)
			except:
				debug.msg(u"failed to remove '%s'" % self.context_target)
		else:

			# Rename the file
			new_name, ok = QtGui.QInputDialog.getText(self, _(u"Rename"), \
				_(u"Please enter a new name for '%s'") \
				% self.context_target, text = self.context_target)
			if ok:
				new_name = str(new_name)

				if os.path.exists(os.path.join( \
					self.experiment.pool_folder, new_name)):
					self.experiment.notify( \
						_(u"There already is a file named '%s' in the file pool") \
						% new_name)
					return

				try:
					os.rename(f, os.path.join( \
						self.experiment.pool_folder, new_name))
					debug.msg(u"renamed '%s' to '%s'" % (self.context_target, \
						new_name))
				except:
					debug.msg(u"failed to rename '%s' to '%s'" % \
						(self.context_target, new_name))

		self.main_window.set_unsaved()
		self.refresh()

	def dragEnterEvent(self, event):

		"""
		Accept an incoming drag that precedes a drop

		Arguments:
		event -- a drag event
		"""

		event.acceptProposedAction()

	def dropEvent(self, event):

		"""
		Accept an incoming drop

		Arguments:
		event -- a drop event
		"""

		files = []
		for url in event.mimeData().urls():
			files.append(url.toLocalFile())
		self.add(files)
		event.acceptProposedAction()

def select_from_pool(main_window, parent=None):

	"""
	desc:
		A static function that presents the select from pool dialog.

	arguments:
		main_window:	The GUI main window

	keywords:
		parent:		The parent QWidget or None to use main window's central
					widget.
	"""

	if parent is None:
		parent = main_window.ui.centralwidget
	d = QtGui.QDialog(parent)
	widget = pool_widget(main_window)
	widget.refresh()
	bbox = QtGui.QDialogButtonBox(d)
	bbox.addButton(_(u"Cancel"), QtGui.QDialogButtonBox.RejectRole)
	bbox.addButton(_(u"Select"), QtGui.QDialogButtonBox.AcceptRole)
	bbox.accepted.connect(d.accept)
	bbox.rejected.connect(d.reject)
	vbox = QtGui.QVBoxLayout()
	vbox.addWidget(widget)
	vbox.addWidget(bbox)
	d.setLayout(vbox)
	d.setWindowTitle(_(u"Select file from pool"))
	res = d.exec_()
	main_window.refresh_pool()

	if res == QtGui.QDialog.Rejected:
		return ""

	selected = widget.ui.list_pool.currentItem()
	if selected is None:
		return ""
	return str(selected.text())

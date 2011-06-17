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

from libqtopensesame import pool_widget_ui
from PyQt4 import QtCore, QtGui
import os
import platform
import os.path
import shutil
import subprocess

class pool_widget(QtGui.QWidget):

	"""The file pool widget"""

	def __init__(self, main_window, parent = None):
	
		"""
		Constructur

		Arguments:
		main_window -- the GUI main window

		Keyword arguments:
		parent -- a parent widget (default = None)
		"""
		
		# Known image and sound extensions
		self.exts = {"image" : (".png", ".jpg", ".bmp", ".gif", ".jpeg"), \
			"sound" : (".ogg", ".wav"), \
			"text" : (".txt", ".csv", ".tsv"), \
			"python" : (".py", ".pyc"), \
			"video" : (".avi", ".mpg", ".wmv", ".mpeg", ".mov", ".ogv"), \
			}
		
		self.main_window = main_window
			
		QtGui.QWidget.__init__(self, parent)												
		self.ui = pool_widget_ui.Ui_Form()
		self.ui.setupUi(self)
		
		self.ui.button_pool_add.clicked.connect(self.select_and_add)
		self.ui.button_refresh.clicked.connect(self.refresh)
		self.ui.button_help_pool.clicked.connect(self.help)
		self.ui.button_browse_pool.clicked.connect(self.browse)
		self.ui.edit_pool_filter.textChanged.connect(self.refresh)				
		self.ui.combobox_view.currentIndexChanged.connect(self.set_view)
		self.ui.list_pool.itemActivated.connect(self.activate_file)
		
	def help(self):
	
		"""Open the help tab"""
	
		self.main_window.open_help_tab("Help: File pool", "pool")
		
		
	def set_view(self):
	
		"""Set the viewmode (list/ icons) based on the gui control"""
	
		if self.ui.combobox_view.currentIndex() == 0:
			self.ui.list_pool.setViewMode(QtGui.QListView.ListMode)
		else:
			self.ui.list_pool.setViewMode(QtGui.QListView.IconMode)
		
	def browse(self):
	
		"""Open the pool folder in the file manager in an OS specific way"""
		
		if platform.system() == "Linux":
			pid = subprocess.Popen(["xdg-open", self.main_window.experiment.pool_folder]).pid
		elif platform.system() == "Darwin":
			pid = subprocess.Popen(["open", self.main_window.experiment.pool_folder]).pid		
		elif platform.system() == "Windows":
			os.startfile(self.main_window.experiment.pool_folder)
		else:
			self.main_window.experiment.notify("I'm sorry, but I don't know how to open the pool folder on your platform!")
			
		if self.main_window.experiment.debug:
			print "pool_widget.browse(): pool folder opened in file manager"
				
	def add(self, files):
	
		"""
		Add a list of files to the pool.
		
		Arguments:
		files - A list of paths
		"""

		basename = ""
		for path in files:
			path = unicode(path)
			basename = os.path.basename(path)
			if not os.path.isfile(path):
				self.main_window.experiment.notify("'%s' is not a regular file and could not be added to the file pool." % path)
			else:			
				# If a similar file already exists in the pool, ask before overwriting
				if os.path.exists(os.path.join(self.main_window.experiment.pool_folder, basename)):
					resp = QtGui.QMessageBox.question(self, "Overwrite", "A file named '%s' already exists in the pool. Do you want to overwrite this file?" % basename, QtGui.QMessageBox.Yes, QtGui.QMessageBox.No)
					if resp == QtGui.QMessageBox.Yes:
						shutil.copyfile(path, os.path.join(self.main_window.experiment.pool_folder, basename))				
				else:
					shutil.copyfile(path, os.path.join(self.main_window.experiment.pool_folder, basename))		
					
		self.refresh()		
		self.select(basename)

	def select_and_add(self, dummy = None):
	
		"""
		Add one or more files to the pool

		Keyword arguments:
		dummy -- a dummy argument passed py the signal handler (default == None)
		"""
		
		self.add(QtGui.QFileDialog.getOpenFileNames(self.main_window.ui.centralwidget, "Add files to pool"))
		
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
		
		return "unknown"
		
	def refresh(self):
	
		"""Refresh the contents of the pool widget"""
		
		filt = str(self.ui.edit_pool_filter.text()).lower()
		
		self.ui.list_pool.clear()
		
		# This function can be called after the pool has been cleaned
		# up. This should not lead to a warning.
		if not os.path.exists(self.main_window.experiment.pool_folder):
			return
		
		for fname in os.listdir(self.main_window.experiment.pool_folder):
			if filt in fname.lower():
				icon = self.main_window.experiment.icon(self.file_type(fname))
				item = QtGui.QListWidgetItem(icon, fname)
				item.icon = icon
				item.path = os.path.join(self.main_window.experiment.pool_folder, fname)
				self.ui.list_pool.addItem(item)
				
	def open_file(self, path):
	
		"""
		Open a file in a platform specific way

		Arguments:
		path -- the full path to the file to be opened
		"""
		
		if platform.system() == "Windows":
			os.startfile(path)
		elif platform.system() == "Linux":
			subprocess.Popen(["xdg-open", path]).pid		
		elif platform.system() == "Darwin":
			subprocess.Popen(["open", path]).pid			
				
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
		
		item = self.ui.list_pool.itemAt(self.ui.list_pool.mapFromGlobal(event.globalPos()))
		if item == None:
			return
			
			
		menu = QtGui.QMenu()		
		menu.addAction(item.icon, "Open")
		menu.addSeparator()
		menu.addAction(self.main_window.experiment.icon("delete"), "Remove from pool")
		menu.addAction(self.main_window.experiment.icon("rename"), "Rename")	
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
		f = os.path.join(self.main_window.experiment.pool_folder, self.context_target)
		
		if a == "Open":
		
			self.open_file(f)
	
		elif a == "Remove from pool":
		
			# Create a list of files to be removed
			l = []
			for item in self.ui.list_pool.selectedItems():
				l.append(str(item.text()))				
		
			# Ask for confirmation
			resp = QtGui.QMessageBox.question(self, "Remove", "<p>Are you sure you want to remove the following files from the file pool? This operation will only affect the OpenSesame file pool, not the original files on your disk.</p><p><b> - %s</b></p>" % ("<br /> - ".join(l)), QtGui.QMessageBox.Yes, QtGui.QMessageBox.No)
			if resp == QtGui.QMessageBox.No:
				return					
					
			# Remove the files
			try:
				for f in l:
					os.remove(os.path.join(self.main_window.experiment.pool_folder, f))
				if self.main_window.experiment.debug:
					print "pool_widget.context_action(): removed '%s'" % self.context_target				
			except:
				if self.main_window.experiment.debug:
					print "pool_widget.context_action(): failed to remove '%s'" % self.context_target
		else:
		
			# Rename the file
			new_name, ok = QtGui.QInputDialog.getText(self, "Rename", "Please enter a new name for '%s'" % self.context_target, text = self.context_target)
			if ok:
				new_name = str(new_name)
				
				if os.path.exists(os.path.join(self.main_window.experiment.pool_folder, new_name)):
					self.main_window.experiment.notify("There already is a file named '%s' in the file pool" % new_name)
					return
				
				try:
					os.rename(f, os.path.join(self.main_window.experiment.pool_folder, new_name))
					if self.main_window.experiment.debug:
						print "pool_widget.context_action(): renamed '%s' to '%s'" % (self.context_target, new_name)
				except:
					if self.main_window.experiment.debug:
						print "pool_widget.context_action(): failed to rename '%s' to '%s'" % (self.context_target, new_name)
			
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
		
def select_from_pool(main_window):

	"""
	A static function that presents the select from pool dialog

	Arguments:
	main_window -- the GUI main window
	"""
	
	d = QtGui.QDialog(main_window.ui.centralwidget)	
	
	widget = pool_widget(main_window)
	widget.refresh()
	bbox = QtGui.QDialogButtonBox(d)
	bbox.addButton("Cancel", QtGui.QDialogButtonBox.RejectRole)
	bbox.addButton("Select", QtGui.QDialogButtonBox.AcceptRole)
	bbox.accepted.connect(d.accept)
	bbox.rejected.connect(d.reject)

	vbox = QtGui.QVBoxLayout()
	vbox.addWidget(widget)
	vbox.addWidget(bbox)

	d.setLayout(vbox)
	d.setWindowTitle("Select file from pool")
	res = d.exec_()

	main_window.refresh_pool()
		
	if res == QtGui.QDialog.Rejected:
		return ""
		
	selected = widget.ui.list_pool.currentItem()
	if selected == None:
		return ""
	return str(selected.text())

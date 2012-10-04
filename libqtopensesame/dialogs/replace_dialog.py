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

from PyQt4 import QtGui, QtCore
from libqtopensesame.ui import replace_dialog_ui
from libqtopensesame.misc import config, _

class replace_dialog(QtGui.QDialog):

	"""A search/ replace dialog"""

	def __init__(self, parent=None):

		"""
		Constructor

		Keywords arguments:
		parent -- the parent QWidget
		"""

		QtGui.QDialog.__init__(self, parent)
		self.edit = parent.edit
		self.ui = replace_dialog_ui.Ui_replace_dialog()
		self.ui.setupUi(self)
		parent.experiment.main_window.theme.apply_theme(self)
		self.adjustSize()
		self.ui.edit_search.setText(parent.search.text())
		self.ui.button_search.clicked.connect(self.search)
		self.ui.button_replace.clicked.connect(self.replace)
		self.ui.button_replace_all.clicked.connect(self.replace_all)

	def search(self):

		"""
		Select text matching the search term

		Returns:
		True if the string was found, False otherwise
		"""

		return self.parent().perform_search(term=self.ui.edit_search.text())

	def replace(self):

		"""Replace the current selection with the replace term"""

		self.parent().edit.replace(self.ui.edit_replace.text())

	def replace_all(self):

		"""
		Iteratively replace all occurences of the search term with the
		replace term
		"""

		if self.ui.edit_search.text().toLower() in \
			self.ui.edit_replace.text().toLower():
			QtGui.QMessageBox.information(self, _("Oops!"), \
				_("The replacement string cannot contain the search string."))
			return
		i = 0
		while self.search():
			i += 1
			self.replace()
		QtGui.QMessageBox.information(self, _("Replace all"), \
			_("%d occurence(s) have been replaced" % i))
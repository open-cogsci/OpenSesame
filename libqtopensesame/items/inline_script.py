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

import random
import re
import sys
from libopensesame import debug, misc
from libopensesame.inline_script import inline_script as inline_script_runtime
from libqtopensesame.items.qtplugin import qtplugin
from libqtopensesame.misc import _
from libqtopensesame.misc.config import cfg
from libqtopensesame.widgets.tree_inline_script_item import \
	tree_inline_script_item
from PyQt4 import QtCore, QtGui

class inline_script(inline_script_runtime, qtplugin):

	"""The inline_script GUI controls"""

	def __init__(self, name, experiment, string=None):

		"""See item."""

		inline_script_runtime.__init__(self, name, experiment, string)
		qtplugin.__init__(self)

	def apply_edit_changes(self):

		"""See qtitem."""

		super(inline_script, self).apply_edit_changes(self)
		sp = self.qprogedit.text(index=0)
		sr = self.qprogedit.text(index=1)
		self.set(u'_prepare', sp)
		self.set(u'_run', sr)
		self.update_item_icon()

	def set_focus(self):

		"""
		desc:
			Allows the item to focus the most important widget.
		"""

		self.qprogedit.setFocus()

	def item_icon(self):

		"""
		desc:
			Determines the icon, based on whether the scripts are syntactically
			correct.

		returns:
			desc:	An icon name.
			type:	unicode
		"""

		if self.experiment.python_workspace.check_syntax(
			self.unistr(self.get(u'_prepare', _eval=False)))\
			and self.experiment.python_workspace.check_syntax(
			self.unistr(self.get(u'_run', _eval=False))):
			return u'os-inline_script'
		return u'os-inline_script-syntax-error'

	def build_item_tree(self, toplevel=None, items=[], max_depth=-1,
		extra_info=None):

		"""See qtitem."""

		widget = tree_inline_script_item(self, extra_info=extra_info,
			symbols=(max_depth < 0 or max_depth > 1))
		items.append(self.name)
		if toplevel != None:
			toplevel.addChild(widget)
		return widget

	def init_edit_widget(self):

		"""See qtitem."""

		from QProgEdit import QTabManager
		super(inline_script, self).init_edit_widget(stretch=False)
		self.qprogedit = QTabManager(cfg=cfg)
		self.qprogedit.handlerButtonClicked.connect(self.apply_edit_changes)
		self.qprogedit.focusLost.connect(self.apply_edit_changes)
		self.qprogedit.cursorRowChanged.connect(self.apply_edit_changes)
		self.qprogedit.addTab(u'Prepare').setLang(u'Python')
		self.qprogedit.addTab(u'Run').setLang(u'Python')
		# Switch to the run phase, unless there is only content for the prepare
		# phase.
		if self._run == u'' and self._prepare != u'':
			self.qprogedit.setCurrentIndex(0)
		else:
			self.qprogedit.setCurrentIndex(1)
		self.edit_vbox.addWidget(self.qprogedit)

	def edit_widget(self):

		"""See qtitem."""

		super(inline_script, self).edit_widget()
		self.qprogedit.tab(0).setText(self.unistr(self._prepare))
		self.qprogedit.tab(1).setText(self.unistr(self._run))

	def get_ready(self):

		"""See qtitem."""

		if self.qprogedit.isAnyModified():
			debug.msg(u'applying pending script changes')
			self.apply_edit_changes()
			return True
		return super(inline_script, self).get_ready()

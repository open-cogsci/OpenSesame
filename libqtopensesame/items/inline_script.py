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
from libopensesame.oslogging import oslogger
from libopensesame.inline_script import inline_script as inline_script_runtime
from libqtopensesame.items.qtplugin import qtplugin
from libqtopensesame.misc.config import cfg
from libqtopensesame.widgets.tree_inline_script_item import (
	tree_inline_script_item
)
from libqtopensesame.misc.translate import translation_context
_ = translation_context(u'inline_script', category=u'item')


class inline_script(inline_script_runtime, qtplugin):

	"""The inline_script GUI controls"""

	description = _(u'Executes Python code')
	help_url = u'manual/python/about'
	language = u'Python'

	def __init__(self, name, experiment, string=None):

		"""See item."""

		inline_script_runtime.__init__(self, name, experiment, string)
		qtplugin.__init__(self)

	def apply_edit_changes(self):

		"""See qtitem."""

		qtplugin.apply_edit_changes(self)
		sp = self.qprogedit.text(index=0)
		sr = self.qprogedit.text(index=1)
		self.var._prepare = sp
		self.var._run = sr
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

		status = max(
			self.experiment.python_workspace.check_syntax(
				self.var.get(u'_prepare', _eval=False)),
			self.experiment.python_workspace.check_syntax(
				self.var.get(u'_run', _eval=False)))
		if status == 2:
			return u'os-inline_script-syntax-error'
		if status == 1:
			return u'os-inline_script-syntax-warning'
		return u'os-inline_script'

	def build_item_tree(
		self,
		toplevel=None,
		items=[],
		max_depth=-1,
		extra_info=None
	):

		"""See qtitem."""

		widget = tree_inline_script_item(
			self,
			extra_info=extra_info,
			symbols=(max_depth < 0 or max_depth > 1)
		)
		items.append(self.name)
		if toplevel is not None:
			toplevel.addChild(widget)
		return widget

	def init_edit_widget(self):

		"""See qtitem."""

		from QProgEdit import QTabManager

		qtplugin.init_edit_widget(self, stretch=False)
		self.qprogedit = QTabManager(cfg=cfg, runButton=True)
		self.qprogedit.execute.connect(self.main_window.console.execute)
		self.qprogedit.handlerButtonClicked.connect(self.apply_edit_changes)
		self.qprogedit.focusLost.connect(self.apply_edit_changes)
		self.qprogedit.cursorRowChanged.connect(self.apply_edit_changes)
		self.qprogedit.addTab(_(u'Prepare')).setLang(self.language)
		self.qprogedit.addTab(_(u'Run')).setLang(self.language)
		# Switch to the run phase, unless there is only content for the prepare
		# phase.
		if self.var._run == u'' and self.var._prepare != u'':
			self.qprogedit.setCurrentIndex(0)
		else:
			self.qprogedit.setCurrentIndex(1)
		self.edit_vbox.addWidget(self.qprogedit)

	def edit_widget(self):

		"""See qtitem."""

		qtplugin.edit_widget(self)
		_prepare = safe_decode(self.var._prepare)
		if _prepare != self.qprogedit.tab(0).text():
			self.qprogedit.tab(0).setText(_prepare)
		_run = safe_decode(self.var._run)
		if _run != self.qprogedit.tab(1).text():
			self.qprogedit.tab(1).setText(_run)

	def get_ready(self):

		"""See qtitem."""

		if self.qprogedit.isAnyModified():
			oslogger.debug(u'applying pending script changes')
			self.apply_edit_changes()
			return True
		return qtplugin.get_ready(self)

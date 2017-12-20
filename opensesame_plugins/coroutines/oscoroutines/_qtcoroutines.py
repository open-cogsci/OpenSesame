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
import os
from libqtopensesame.items.sequence import sequence
from libqtopensesame.items.qtplugin import qtplugin
from libqtopensesame.items.qtstructure_item import qtstructure_item
from libopensesame.sequence import sequence as sequence_runtime
from libqtopensesame.widgets.tree_item_item import tree_item_item
from libqtopensesame.validators import duration_validator
from oscoroutines import coroutines, items_adapter, tree_overview_adapter
from libqtopensesame.misc.translate import translation_context
_ = translation_context(u'coroutines', category=u'plugins')


class qtcoroutines(coroutines, sequence):

	"""
	desc:
		The coroutines plugin GUI.
	"""

	description = _(u'Run items simultaneously')
	help_url = u'manual/structure/coroutines'

	def __init__(self, name, experiment, string=None):

		"""See item."""

		coroutines.__init__(self, name, experiment, string)
		# We don't call the sequence constructor, because it doesn't specify
		# the plugin_file to qtplugin, which we need to do. We therefore
		# explicitly need to call the qtplugin and qtstructure_item
		# constructors.
		sequence_runtime.__init__(self, name, experiment, string)
		qtstructure_item.__init__(self)
		qtplugin.__init__(self, plugin_file=os.path.dirname(__file__))
		self.last_removed_child = None, None

	def reset(self):

		"""See item."""

		coroutines.reset(self)
		# Recreate the items adapter when the schedule is re-initialized.
		self._items = items_adapter(self.schedule)

	@property
	def items(self):

		"""
		desc:
			A property that maps the schedule list to an items list as expected
			by sequence.
		"""

		return self._items

	@items.setter
	def items(self, val):

		"""
		desc:
			A setter that maps an items list to a schedule list.
		"""

		self.schedule = self.schedule[:len(val)]
		self._items = items_adapter(self.schedule)
		for i, (item_name, cond) in enumerate(val):
			start_time = self.schedule[i][1]
			end_time = self.schedule[i][2]
			self.schedule[i] = item_name, start_time, end_time, cond

	def init_edit_widget(self):

		"""See qtitem."""

		super(sequence, self).init_edit_widget(False)
		self.treewidget = tree_overview_adapter(self, self.main_window,
			overview_mode=False)
		self.treewidget.setup(self.main_window)
		self.treewidget.structure_change.connect(self.update)
		self.treewidget.text_change.connect(self.update_script)
		self.treewidget.setHeaderLabels([_(u'Item name'), (u'Run if'),
			_(u'Start time'), _(u'End time (if applicable)')])
		self.set_focus_widget(self.treewidget)
		self.edit_vbox.addWidget(self.treewidget)
		self.add_line_edit_control(u'duration', _(u'Duration'),
			validator=duration_validator(self.main_window, default=u'5000'))
		self._combobox_end_after_item = self.add_combobox_control(
			u'end_after_item', _(u'End after item (optional)'),
			options=[s[0] for s in self.schedule]
		)
		self.add_line_edit_control(u'function_name',
			_(u'Generator function name (optional)'))
		self.add_checkbox_control(u'flush_keyboard',
			_(u'Flush pending key presses at coroutines start'))

	def edit_widget(self):

		"""See qtitem."""

		sequence.edit_widget(self)
		self._refresh()

	def rename(self, from_name, to_name):

		"""See qtitem."""

		sequence.rename(self, from_name, to_name)
		if self.var.end_after_item == from_name:
			self.var.end_after_item = to_name
			self._refresh()

	def build_item_tree(self, toplevel=None, items=[], max_depth=-1,
		extra_info=None):

		"""See qtitem."""

		widget = tree_item_item(self, extra_info=extra_info)
		items.append(self.name)
		if max_depth < 0 or max_depth > 1:
			for item, start_time, end_time, cond in self.schedule:
				if item in self.experiment.items:
					self.experiment.items[item].build_item_tree(widget, items,
						max_depth=max_depth-1, extra_info=cond)
					child = widget.child(widget.childCount()-1)
					child.setText(2, safe_decode(start_time))
					if not self.is_oneshot_coroutine(item):
						child.setText(3, safe_decode(end_time))
		if toplevel is not None:
			toplevel.addChild(widget)
		else:
			widget.set_draggable(False)
		return widget

	def insert_child_item(self, item_name, index=0):

		"""See sequence."""

		if not self.is_coroutine(item_name):
			self.experiment.notify(
				_(u'"%s" does not support coroutines.') % item_name)
			return
		sequence.insert_child_item(self, item_name, index=index)
		self._refresh()

	def remove_child_item(self, item_name, index=0):

		"""See sequence."""

		sequence.remove_child_item(self, item_name, index=index)
		if item_name == self.var.end_after_item:
			self.var.end_after_item = u''
		self._refresh()

	def _refresh(self):

		"""
		desc:
			Refreshes the GUI, which currently means updating the combobox for
			end_after_item.
		"""

		# No refresh necessary if the combobox hasn't been initialized yet
		if not hasattr(self, u'_combobox_end_after_item'):
			return
		self._combobox_end_after_item.clear()
		self._combobox_end_after_item.addItem(u'')
		current_index = 0
		for i, (item_name, st, et, cond) in enumerate(self.schedule):
			if self.var.end_after_item == item_name:
				current_index = i+1
			self._combobox_end_after_item.addItem(
				self.theme.qicon(self.experiment.items[item_name].item_icon()),
				item_name
			)
		self._combobox_end_after_item.setCurrentIndex(current_index)

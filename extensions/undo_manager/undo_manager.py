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
from libqtopensesame.extensions import base_extension
from libqtopensesame.misc.config import cfg
import difflib

class undo_stack(object):

	def __init__(self):

		self.current = {}
		self.history = []

	def add(self, key, state):

		if key in self.current:
			if self.current[key] == state:
				return
			self.history.append( (key, self.current[key]) )
		self.current[key] = state
		if len(self.history) > cfg.max_undo_history:
			self.history[-cfg.max_undo_history:]

	def can_undo(self):

		return len(self.history) > 0

	def __len__(self):

		return len(self.history)

	def pop(self):

		if len(self.history) == 0:
			return None, None
		key, state = self.history.pop()
		self.current[key] = state
		return key, state

	def last(self):

		if len(self.history) == 0:
			return None, None
		return self.history[-1]

class undo_manager(base_extension):

	def event_startup(self):

		self.initialize()
		self.console.set_workspace_globals({u'undo_manager' : self})

	def event_open_experiment(self, path):

		self.initialize()

	def event_delete_item(self, name):

		self.initialize()

	def event_rename_item(self, from_name, to_name):

		self.initialize()

	def event_purge_unused_items(self):

		self.initialize()

	def event_change_item(self, name):

		if self.in_undo:
			return
		self.remember_item_state(name)

	def activate(self):

		self.undo()

	def initialize(self):

		self.stack = undo_stack()
		self.in_undo = False
		for item in self.experiment.items:
			self.remember_item_state(item)

	def remember_item_state(self, item):

		script = self.experiment.items[item].to_string()
		self.stack.add(item, script)
		self.set_enabled(self.stack.can_undo())

	def undo(self, n=1):

		n = min(n, len(self.stack))
		if n <= 0:
			return
		self.in_undo = True
		for i in range(n):
			item, script = self.stack.pop()
			if item not in self.experiment.items:
				break
			self.experiment.items[item].from_string(script)
		if item in self.experiment.items:
			self.experiment.items[item].update()
			self.experiment.items[item].open_tab()
		self.in_undo = False
		self.set_enabled(self.stack.can_undo())

	def show(self):

		item, old_script = self.stack.last()
		if item is None:
			print(u'\nThe undo stack is empty')
			return
		self.console.write(
			u'\nShowing most recent undo operation (of %d):\n\n' \
			% len(self.stack))
		self.console.write(u'item: %s\n\n' % item)
		new_script = self.stack.current[item]
		for line in difflib.ndiff(old_script.splitlines(),
			new_script.splitlines()):
			if line.startswith(u'+'):
				self.console.write(u'\x1b[32;1m')
			elif line.startswith(u'-'):
				self.console.write(u'\x1b[31;1m')
			else:
				continue
			self.console.write(line + u'\n')
		self.console.write(u'\x1b[0m')

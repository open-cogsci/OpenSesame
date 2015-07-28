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

from libopensesame import debug
from libqtopensesame.extensions import base_extension

class example(base_extension):

	"""
	desc:
		An example extension that lists all available events.
	"""

	def activate(self):

		"""
		desc:
			Is called when the extension is activated through the menu/ toolbar
			action.
		"""

		debug.msg(u'Example extension activated')

	# Below is a list of event handlers, which you can implement to have your
	# extension react to specific events.

	def event_startup(self):

		"""
		desc:
			Called at the end of the OpenSesame startup process.
		"""

		debug.msg(u'Event fired: startup')

	def event_regenerate(self):

		"""
		desc:
			Called after the experiment has been reparsed from script.
		"""

		debug.msg(u'Event fired: regenerate')

	def event_run_experiment(self, fullscreen):

		"""
		desc:
			Called just before the experiment is launched.

		arguments:
			fullscreen:
				desc:	Indicates whether experiment is launched fullscreen.
				type:	bool
		"""

		debug.msg(u'Event fired: run_experiment(fullscreen=%s)' % fullscreen)

	def event_end_experiment(self):

		"""
		desc:
			Called after the experiment has ended, regardless of whether an
			exception occurred or not.
		"""

		debug.msg(u'Event fired: end_experiment')

	def event_save_experiment(self, path):

		"""
		desc:
			Called just before the experiment is been saved.

		arguments:
			path:
				desc:	The full path of the experiment file.
				type:	unicode
		"""

		debug.msg(u'Event fired: save_experiment(path=%s)' % path)

	def event_open_experiment(self, path):

		"""
		desc:
			Called just after the experiment has been opened.

		arguments:
			path:
				desc:	The full path of the experiment file.
				type:	unicode
		"""

		debug.msg(u'Event fired: open_experiment(path=%s)' % path)

	def event_close(self):

		"""
		desc:
			Called when OpenSesame closes, just before the state is saved and
			clean up is done.
		"""

		debug.msg(u'Event fired: close')

	def event_rename_item(self, from_name, to_name):

		"""
		desc:
			Called after an item has been renamed.

		arguments:
			from_name:
				desc:	The old name.
				type:	unicode
			to_name:
				desc:	The new name.
				type:	unicode
		"""

		debug.msg(u'Event fired: rename_item(from_name=%s, to_name=%s)' \
			% (from_name, to_name))

	def event_new_item(self, name, _type):

		"""
		desc:
			Called after a new item has been created.

		arguments:
			name:
				desc:	The item name.
				type:	unicode
			_type:
				desc:	The item type.
				type:	unicode
		"""

		debug.msg(u'Event fired: new_item(name=%s, _type=%s)' % (name, _type))

	def event_change_item(self, name):

		debug.msg(u'Event fired: change_item(name=%s)' % name)

	def event_delete_item(self, name):

		debug.msg(u'Event fired: delete_item(name=%s)' % name)

	def event_purge_unused_items(self):

		"""
		desc:
			Called after unused items have been purged.
		"""

		debug.msg(u'Event fired: purge_unused_items')

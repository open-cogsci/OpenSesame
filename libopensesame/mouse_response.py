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

from libopensesame import item, generic_response
import openexp.mouse

class mouse_response(item.item, generic_response.generic_response):

	"""An item for collection keyboard responses"""	

	description = u'Collects mouse responses'

	def __init__(self, name, experiment, string=None):

		"""
		Constructor.

		Arguments:
		name 		--	The name of the item.
		experiment 	--	The experiment.

		Keyword arguments:
		string		-- 	The item definition string. (default=None)
		"""

		self.flush = u'yes'
		self.show_cursor = u'yes'
		self.timeout = u'infinite'
		self.auto_response = 1
		self.duration = u'mouseclick'
		self.process_feedback = True				

		self.resp_codes = {}
		self.resp_codes[None] = u'timeout'
		self.resp_codes[1] = u'left_button'
		self.resp_codes[2] = u'middle_button'
		self.resp_codes[3] = u'right_button'
		self.resp_codes[4] = u'scroll_up'
		self.resp_codes[5] = u'scroll_down'

		item.item.__init__(self, name, experiment, string)

	def prepare(self):

		"""Prepares the item."""

		item.item.prepare(self)
		generic_response.generic_response.prepare(self)
		self._flush = self.get(u'flush') == u'yes'
					
	def run(self):

		"""Runs the item."""

		# Record the onset of the current item
		self.set_item_onset()
		# Show cursor if necessary
		if self.show_cursor == u'yes':
			self._mouse.set_visible(True)
		# Flush responses, to make sure that earlier responses are not carried
		# over.
		if self._flush:
			self._mouse.flush()			
		self.set_sri()
		self.process_response()
		self._mouse.set_visible(False)

	def var_info(self):

		"""
		Gives a list of dictionaries with variable descriptions.

		Returns:
		A list of (name, description) tuples.
		"""

		l = item.item.var_info(self) + \
			generic_response.generic_response.var_info(self)
		l.append( (u'cursor_x', u'[Depends on response]') )
		l.append( (u'cursor_y', u'[Depends on response]') )
		return l


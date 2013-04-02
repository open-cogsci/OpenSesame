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

from libopensesame import item, exceptions, generic_response
import openexp.keyboard
import openexp.exceptions

class keyboard_response(item.item, generic_response.generic_response):

	"""An item for collection keyboard responses"""

	def __init__(self, name, experiment, string=None):

		"""
		Constructor

		Arguments:
		name -- the name of the item
		experiment -- the experiment

		Keyword arguments:
		string -- item definition string
		"""

		self.flush = "yes"
		self.item_type = "keyboard_response"
		self.description = "Collects keyboard responses"
		self.timeout = "infinite"
		self.auto_response = 97 # 'a'
		self.duration = "keypress"
		self.process_feedback = True
		item.item.__init__(self, name, experiment, string)

	def prepare(self):

		"""
		Prepare the item

		Returns:
		True on success, False on failure
		"""

		item.item.prepare(self)
		generic_response.generic_response.prepare(self)
		self._flush = self.get("flush") == "yes"
		return True

	def run(self):

		"""
		Runs the item

		Returns:
		True on success, False on failure
		"""

		# Record the onset of the current item
		self.set_item_onset()

		# Flush responses, to make sure that earlier responses
		# are not carried over
		if self._flush:
			self._keyboard.flush()

		self.set_sri()
		self.process_response()

		# Report success
		return True

	def var_info(self):
		
		"""
		Give a list of dictionaries with variable descriptions

		Returns:
		A list of (name, description) tuples
		"""		

		return item.item.var_info(self) + \
			generic_response.generic_response.var_info(self)

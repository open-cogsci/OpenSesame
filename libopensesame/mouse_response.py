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
import openexp.mouse
import openexp.exceptions

class mouse_response(item.item, generic_response.generic_response):

	"""An item for collection keyboard responses"""	

	def __init__(self, name, experiment, string = None):

		"""
		Constructor

		Arguments:
		name -- the name of the item
		experiment -- the experiment

		Keyword arguments:
		string -- item definition string
		"""

		self.flush = "yes"
		self.show_cursor = "yes"
		self.item_type = "mouse_response"
		self.timeout = "infinite"
		self.description = "Collects mouse responses"
		self.auto_response = 1
		self.duration = "mouseclick"

		self.resp_codes = {}
		self.resp_codes[None] = "timeout"
		self.resp_codes[1] = "left_button"
		self.resp_codes[2] = "middle_button"
		self.resp_codes[3] = "right_button"
		self.resp_codes[4] = "scroll_up"
		self.resp_codes[5] = "scroll_down"		

		item.item.__init__(self, name, experiment, string)

	def prepare(self):

		"""
		Prepare the item

		Returns:
		True on success, False on failure
		"""

		item.item.prepare(self)
		generic_response.generic_response.prepare(self)
		return True
					
	def run(self):

		"""
		Runs the item

		Returns:
		True on success, False on failure
		"""

		# Record the onset of the current item
		self.set_item_onset()

		if self.show_cursor == "yes":
			self._mouse.set_visible()

		# Flush responses, to make sure that earlier responses
		# are not carried over
		if self.get("flush") == "yes":
			self._mouse.flush()			

		self.set_sri()
		self.process_response()
		self._mouse.set_visible(False)

		# Report success
		return True

	def var_info(self):

		"""
		Give a list of dictionaries with variable descriptions

		Returns:
		A list of (name, description) tuples
		"""

		l = generic_response.generic_response.var_info(self)
		l.append( ("cursor_x", "<i>Depends on response</i>") )
		l.append( ("cursor_y", "<i>Depends on response</i>") )

		return l


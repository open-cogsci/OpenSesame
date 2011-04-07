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

	def __init__(self, name, experiment, string = None):
	
		"""
		Initialize the loop
		"""
		
		self.flush = "yes"
		self.item_type = "keyboard_response"		
		self.description = "Collects keyboard responses"
		self.timeout = "infinite"
		self.auto_response = 97 # 'a'
		
		item.item.__init__(self, name, experiment, string)
		
	def prepare(self):
	
		"""
		Prepare the keyboard response item
		"""
		
		item.item.prepare(self)		
		self._keyboard = openexp.keyboard.keyboard(self.experiment)		
				 
		if self.has("allowed_responses"):
			l = str(self.get("allowed_responses")).split(";")
			#self._allowed_responses = openexp.response.keys(l)
			self._allowed_responses = l
			if len(self._allowed_responses) == 0:
				raise exceptions.runtime_error("'%s' are not valid allowed responses in keyboard_response '%s'" % (self.get("allowed_responses"), self.name))
		else:
			self._allowed_responses = None
			
		if self.experiment.auto_response:
			self._resp_func = self.auto_responder
		else:
			self._resp_func = self._keyboard.get_key
			
		self.prepare_timeout()		
		self._keyboard.set_timeout(self._timeout)
		self._keyboard.set_keylist(self._allowed_responses)
			
		return True		
				
	def run(self):
	
		"""
		Run the keyboard response item
		"""
	
		# Record the onset of the current item
		self.set_item_onset()

		# Flush responses, to make sure that earlier responses
		# are not carried over
		if self.get("flush") == "yes":
			self._keyboard.flush()		
		
		# If no start response interval has been set, set it to the onset of
		# the current response item
		if self.experiment.start_response_interval == None:
			self.experiment.start_response_interval = self.get("time_%s" % self.name)

		# Get the response
		try:
			resp, self.experiment.end_response_interval = self._resp_func()
		except openexp.exceptions.response_error as e:
			raise exceptions.runtime_error("The 'escape' key was pressed.")
		
		# Do some bookkeeping
		self.experiment.response_time = self.experiment.end_response_interval - self.experiment.start_response_interval		
		self.experiment.total_response_time += self.experiment.response_time
		self.experiment.total_responses += 1
		self.experiment.response = self._keyboard.to_chr(resp)
						
		if self.has("correct_response"):
			correct_response = self.get("correct_response")
		else:
			correct_response = "undefined"
			
		print "response:", self.experiment.response
		print "correct:", correct_response
			
		self.process_response(correct_response)
				
		# Report success
		return True
				
	def to_string(self):
	
		"""
		Encode the keyboard_response as string
		"""
	
		s = item.item.to_string(self, "keyboard_response")
		return s
		
	def var_info(self):
	
		"""
		Give a list of dictionaries with variable descriptions
		"""
		
		l = item.item.var_info(self)
		l.append( ("response", "<i>Depends on response</i>") )
		l.append( ("correct", "<i>Depends on response</i>") )
		l.append( ("response_time", "<i>Depends on response</i>") )
		l.append( ("average_response_time", "<i>Depends on response</i>") )
		l.append( ("avg_rt", "<i>Depends on response</i>") )		
		l.append( ("accuracy", "<i>Depends on response</i>") )		
		l.append( ("acc", "<i>Depends on response</i>") )		
		
		return l			

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
import shlex
import openexp.sampler

class sampler(item.item, generic_response.generic_response):

	"""Sound playback item"""

	def __init__(self, name, experiment, string = None):
	
		"""
		Constructor

		Arguments:
		name -- the name of the item
		experiment -- the experiment

		Keyword arguments:
		string -- definition string for the item
		"""

		self.description = "Plays a sound file in .wav or .ogg format"		
		self.item_type = "sampler"
		self.sample = ""
		self.pan = 0
		self.pitch = 1
		self.fade_in = 0
		self.volume = 1.0
		self.stop_after = 0
		self.duration = "sound"
		self.block = False

		item.item.__init__(self, name, experiment, string)

	def prepare_duration_sound(self):

		"""Set the duration function for 'sound' duration"""

		self.block = True
		self._duration_func = self.dummy
		
	def prepare(self):
	
		"""
		Prepare for playback

		Returns:
		True on success, False on failure
		"""			
		
		item.item.prepare(self)
		
		if self.sample.strip() == "":
			raise exceptions.runtime_error("No sample has been specified in sampler '%s'" % self.name)		
		sample = self.experiment.get_file(self.eval_text(self.sample))		
		if self.experiment.debug:
			self.sampler = openexp.sampler.sampler(self.experiment, sample)	
		else:
			try:
				self.sampler = openexp.sampler.sampler(self.experiment, sample)
			except Exception as e:		
				raise exceptions.runtime_error("Failed to load sample in sampler '%s': %s" % (self.name, e))
			
		pan = self.get("pan")
		if pan == -20:
			pan = "left"
		elif pan == 20:
			pan = "right"
			
		self.sampler.pan(pan)
		self.sampler.volume(self.get("volume"))						
		self.sampler.pitch(self.get("pitch"))
		self.sampler.fade_in(self.get("fade_in"))
		self.sampler.stop_after(self.get("stop_after"))		
		generic_response.generic_response.prepare(self)
		
		return True						
				
	def run(self):
	
		"""
		Play the sample

		Returns:
		True on success, False on failure		
		"""
	
		self.set_item_onset(self.time())
		self.set_sri()		
		self.sampler.play(self.block)	
		self.process_response()			
		return True
	
	def var_info(self):

		return generic_response.generic_response.var_info(self)

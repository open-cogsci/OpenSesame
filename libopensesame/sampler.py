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

from libopensesame import item, exceptions
import shlex
import openexp.sampler

class sampler(item.item):

	def __init__(self, name, experiment, string = None):
	
		"""
		Initialize the sampler
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
		
	def prepare(self):
	
		"""
		Prepare the sampler
		"""			
		
		item.item.prepare(self)					
		sample = self.experiment.get_file(self.eval_text(self.sample))		
		if sample == "":
			raise exceptions.runtime_error("No sample has been specified in sampler '%s'" % self.name)

		if self.experiment.debug:
			self.sampler = openexp.sampler.sampler(self.experiment, sample)	
		else:
			try:
				self.sampler = openexp.sampler.sampler(self.experimentsample)
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
		
		dur = self.get("duration")
		if dur == "sound":
			self.block = True
			self._duration_func = self.dummy
		elif dur == "keypress":
			self._keyboard = openexp.keyboard.keyboard(self.experiment)
			self._duration_func = self._keyboard.get_key
		elif dur == "mouseclick":
			self._mouse = openexp.mouse.mouse(self.experiment)
			self._duration_func = self._mouse.get_click
		else:
			try:				
				self._duration = int(self.get("duration"))			
			except:
				raise exceptions.runtime_error("Invalid duration '%s' in sketchpad '%s'. Expecting a positive number or 'keypress'." % (self.get("duration"), self.name))					
			if self._duration == 0:
				self._duration_func = self.dummy
			else:
				self._duration_func = self.sleep_for_duration		
		
		return True						
				
	def run(self):
	
		"""
		Play the sample
		"""
	
		self.set_item_onset(self.time())
		self.sampler.play(self.block)
	
		# And wait
		self._duration_func()		
			
		return True
	


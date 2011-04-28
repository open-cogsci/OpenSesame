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
import openexp.synth

class synth(item.item):

	def __init__(self, name, experiment, string = None):
	
		"""
		Initialize the synth
		"""

		self.description = "A basic sound synthesizer"		
		self.item_type = "synth"
		self.freq = 440
		self.length = 100
		self.osc = "sine"
		self.pan = 0		
		self.attack = 0
		self.decay = 5
		self.volume = 1.0
		self.duration = "sound"
		self.block = False
		
		item.item.__init__(self, name, experiment, string)	
		
	def prepare(self):
	
		"""
		Prepare the synth
		"""

		item.item.prepare(self)		
		
		try:
			self.synth = openexp.synth.synth(self.experiment, self.get("osc"), self.get("freq"), self.get("length"), self.get("attack"), self.get("decay"))
		except Exception as e:
			raise exceptions.runtime_error("Failed to generate sound in synth '%s': %s" % (self.name, e))
			
		pan = self.get("pan")
		if pan == -20:
			pan = "left"
		elif pan == 20:
			pan = "right"
		self.synth.pan(pan)
		self.synth.volume(self.get("volume"))
		
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
		self.synth.play(self.block)
	
		# And wait
		self._duration_func()		
			
		return True
	
		


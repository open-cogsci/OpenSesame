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

from libopensesame import sampler, exceptions, item, generic_response
import shlex
import openexp.synth

class synth(sampler.sampler, item.item):

	"""Plays a synthesized sound"""

	def __init__(self, name, experiment, string = None):
	
		"""
		Constructor

		Arguments:
		name -- the name of the item
		experiment -- the experiment

		Keyword arguments:
		string -- definition string for the item
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
		Prepare for playback

		Returns:
		True on success, False on failure
		"""		

		item.item.prepare(self)		
		
		try:
			self.sampler = openexp.synth.synth(self.experiment, self.get("osc"), self.get("freq"), self.get("length"), self.get("attack"), self.get("decay"))
		except Exception as e:
			raise exceptions.runtime_error("Failed to generate sound in synth '%s': %s" % (self.name, e))
			
		pan = self.get("pan")
		if pan == -20:
			pan = "left"
		elif pan == 20:
			pan = "right"
			
		self.sampler.pan(pan)
		self.sampler.volume(self.get("volume"))		
		generic_response.generic_response.prepare(self)
								
		return True
		


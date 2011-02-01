"""
This file is part of openexp.

openexp is free software: you can redistribute it and/or modify
it under the terms of the GNU General Public License as published by
the Free Software Foundation, either version 3 of the License, or
(at your option) any later version.

openexp is distributed in the hope that it will be useful,
but WITHOUT ANY WARRANTY; without even the implied warranty of
MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
GNU General Public License for more details.

You should have received a copy of the GNU General Public License
along with openexp.  If not, see <http://www.gnu.org/licenses/>.
"""

class openexp_error(Exception):

	def __init__(self, value):
	
		self.value = value
		
	def __str__(self):
	
		return str(self.value)

class canvas_error(openexp_error):

	def __init__(self, value):
	
		self.value = value
				
class response_error(openexp_error):

	def __init__(self, value):
	
		self.value = value
			
class sample_error(openexp_error):

	def __init__(self, value):
	
		self.value = value
		
class synth_error(openexp_error):

	def __init__(self, value):
	
		self.value = value
		
	


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

import sys
import os.path

legacy = {
	"description" : "Default PyGame backend, a safe choice", \
	"authors" : ["Sebastiaan Mathot"], \
	"canvas" : "legacy", \
	"keyboard" : "legacy", \
	"mouse" : "legacy", \
	"sampler" : "legacy", \
	"synth" : "legacy" \
	}
	
opengl = {
	"description" : "Uses PyGame in OpenGL mode", \
	"authors" : ["Sebastiaan Mathot", "Per Sederberg"], \
	"canvas" : "opengl", \
	"keyboard" : "legacy", \
	"mouse" : "legacy", \
	"sampler" : "legacy", \
	"synth" : "legacy" \
	}	

psycho = {
	"description" : "Uses PsychoPy", \
	"authors" : ["Sebastiaan Mathot", "Jonathan Peirce"], \
	"canvas" : "psycho", \
	"keyboard" : "psycho", \
	"mouse" : "psycho", \
	"sampler" : "legacy", \
	"synth" : "legacy" \
	}
	
backend_list = {}
backend_list["legacy"] = legacy
backend_list["opengl"] = opengl

# So far, the psycho back-end doesn't work on Mac OS (darwin)
if sys.platform != "darwin":
	backend_list["psycho"] = psycho

def match(experiment):

	"""
	Returns the name of the backend that is currently used by
	the experiment or "custom" if no matching backend is found.
	
	Arguments:
	experiment -- an instance of libopensesame.experiment.experiment
	
	Returns:
	The name of the backend or "custom" if no matching backend is found
	"""
	
	for name in backend_list:	
		backend = backend_list[name]	
		if experiment.canvas_backend == backend["canvas"] and \
			experiment.keyboard_backend == backend["keyboard"] and \
			experiment.mouse_backend == backend["mouse"] and \
			experiment.sampler_backend == backend["sampler"] and \
			experiment.synth_backend == backend["synth"]:			
			return name
	return "custom"

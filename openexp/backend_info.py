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

from libopensesame.py3compat import *

legacy = {
	"description" : "uses PyGame, maximum stability", \
	"canvas" : "legacy", \
	"keyboard" : "legacy", \
	"mouse" : "legacy", \
	"sampler" : "legacy", \
	"synth" : "legacy", \
	"icon" : "os-pygame"
	}

opengl = {
	"description" : "uses PyGame and OpenGL", \
	"canvas" : "opengl", \
	"keyboard" : "legacy", \
	"mouse" : "legacy", \
	"sampler" : "legacy", \
	"synth" : "legacy", \
	"icon" : "os-pygame"
	}

psycho = {
	"description" : "uses PsychoPy, powerful stimulus generation", \
	"canvas" : "psycho", \
	"keyboard" : "psycho", \
	"mouse" : "psycho", \
	"sampler" : "legacy", \
	"synth" : "legacy", \
	"icon" : "os-psychopy"
	}

xpyriment = {
	"description" : "uses Expyriment", \
	"canvas" : "xpyriment", \
	"keyboard" : "legacy", \
	"mouse" : "xpyriment", \
	"sampler" : "legacy", \
	"synth" : "legacy", \
	"icon" : "os-expyriment"
	}

xpyriment_gst = {
	"description" : "uses Expyriment with Gstreamer for sound", \
	"canvas" : "xpyriment", \
	"keyboard" : "legacy", \
	"mouse" : "xpyriment", \
	"sampler" : "gstreamer", \
	"synth" : "legacy", \
	"icon" : "os-expyriment"
	}

droid = {
	"description" : "for Android devices", \
	"canvas" : "droid", \
	"keyboard" : "droid", \
	"mouse" : "droid", \
	"sampler" : "legacy", \
	"synth" : "droid", \
	"icon" : "os-android"
	}

backend_list = {}
backend_list["legacy"] = legacy
backend_list["xpyriment"] = xpyriment
backend_list["droid"] = droid
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
		if experiment.var.canvas_backend == backend["canvas"] and \
			experiment.var.keyboard_backend == backend["keyboard"] and \
			experiment.var.mouse_backend == backend["mouse"] and \
			experiment.var.sampler_backend == backend["sampler"] and \
			experiment.var.synth_backend == backend["synth"]:
			return name
	return "custom"

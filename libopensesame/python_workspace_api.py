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

---
desc:
	Functions that are globally accessible in `inline_script` items.
---
"""

from libopensesame.py3compat import *

# Factory functions

def canvas(auto_prepare=True, **style_args):

	"""
	desc: |
		Creates a new `canvas` object. For a list of arguments and keywords,
		see:

		- [/python/canvas/](/python/canvas/)

	returns:
		desc:	A `canvas` object.
		type:	canvas

	example: |
		my_canvas = canvas()
	"""

	from openexp.canvas import canvas
	return canvas(experiment, auto_prepare=auto_prepare, **style_args)

def keyboard(**resp_args):

	"""
	desc: |
		Creates a new `keyboard` object. For a list of arguments and keywords,
		see:

		- [/python/keyboard/](/python/keyboard/)

	returns:
		desc:	A `keyboard` object.
		type:	keyboard

	example: |
		my_keyboard = keyboard()
	"""

	from openexp.keyboard import keyboard
	return keyboard(experiment, **resp_args)

def mouse(**resp_args):

	"""
	desc: |
		Creates a new `mouse` object. For a list of arguments and keywords,
		see:

		- [/python/mouse/](/python/mouse/)

	returns:
		desc:	A `mouse` object.
		type:	mouse

	example: |
		my_mouse = mouse()
	"""

	from openexp.mouse import mouse
	return mouse(experiment, *arglist, **kwdict)

def sampler(src, **playback_args):

	"""
	desc: |
		Creates a new `sampler` object. For a list of arguments and keywords,
		see:

		- [/python/sampler/](/python/sampler/)

	returns:
		desc:	A `sampler` object.
		type:	sampler

	example: |
		my_sampler = sampler()
	"""

	from openexp.sampler import sampler
	return sampler(experiment, src, **playback_args)

# Miscellaneous API	functions

def synth(osc="sine", freq=440, length=100, attack=0, decay=5):

	"""
	desc:
		Synthesizes a sound and returns it as a `sampler` object.

	keywords:
		osc:
			desc:	Oscillator, can be "sine", "saw", "square" or
					"white_noise".
			type:	[str, unicode]
		freq:
			desc:	Frequency, either an integer value (value in hertz) or a
					string ("A1", "eb2", etc.).
			type:	[str, unicode, int, float]
		length:
			desc:	The length of the sound in milliseconds.
			type:	[int, float]
		attack:
			desc:	The attack (fade-in) time in milliseconds.
			type:	[int, float]
		decay:
			desc:	The decay (fade-out) time in milliseconds.
			type:	[int, float]

	returns:
		desc:	A `sampler` object.
		type:	sampler

	example: |
		my_sampler = synth(freq=u'b2', length=500)
	"""

	from openexp.synth import synth
	return synth(experiment, osc=osc, freq=freq, length=length, attack=attack,
		decay=decay)

def copy_sketchpad(name):

	"""
	desc:
		Returns a copy of a `sketchpad`'s canvas.

	arguments:
		name:
			desc:	The name of the `sketchpad`.
			type:	[str, unicode]

	returns:
		desc:	A copy of the `sketchpad`'s canvas.
		type:	canvas
	"""

	c = canvas()
	c.copy(experiment.items[name].canvas)
	return c

def flush_log():

	"""
	desc:
		Forces any pending write operations to the log file to be written to
		disk.

	example: |
		log('TRIAL FINISHED')
		flush_log()
	"""

	experiment.flush_log()

def set_response(response=None, response_time=None, correct=None):

	"""
	desc:
		Processes a response in such a way that feedback variables are updated
		as well.

	keywords:
		response:
			desc:	The response value.
		response_time:
			desc:	The response time, or `None`.
			type:	[int, float, NoneType]
		correct:
			desc:	The correctness value, which should be 0, 1, `True`,
					`False`, or `None`.
			type:	[int, bool, NoneType]

	example: |
		my_keyboard = keyboard()
		t1 = time()
		button, timestamp = my_keyboard.get_key()
		if button == 'left':
			correct = 1
		else:
			correct = 0
		rt = timestamp - t1
		set_response(response=button, response_time=rt, correct=correct)
	"""

	experiment.set_response(response=response, response_time=response_time,
		correct=correct)

def set_subject_nr(nr):

	"""
	desc:
		Sets the subject number and parity (even/ odd). This function is called
		automatically when an experiment is started, so you only need to call it
		yourself if you overwrite the subject number that was specified when the
		experiment was launcherd.

	arguments:
		nr:
			desc:	The subject nr.
			type:	int

	example: |
		set_subject_nr(1)
		print('Subject nr = %d' % var.subject_nr)
		print('Subject parity = %s' % var.subject_parity)
	"""

	experiment.set_subject(nr)

def pause():

	"""
	desc:
		Pauses the experiment.
	"""

	experiment.pause()

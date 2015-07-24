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
from libopensesame.exceptions import osexception
import random

# Factory functions

def canvas(auto_prepare=True, **style_args):

	"""
	desc: |
		A convenience function that creates a new `canvas` object. For a
		description of possible keywords, see:

		- [/python/canvas/](/python/canvas/)

	returns:
		desc:	A `canvas` object.
		type:	canvas

	example: |
		my_canvas = canvas(color=u'red', penwidth=2)
		my_canvas.line(-10, -10, 10, 10)
		my_canvas.line(-10, 10, 10, -10)
		my_canvas.show()
	"""

	from openexp.canvas import canvas
	return canvas(experiment, auto_prepare=auto_prepare, **style_args)

def keyboard(**resp_args):

	"""
	desc: |
		A convenience function that creates a new `keyboard` object. For a
		description of possible keywords, see:

		- [/python/keyboard/](/python/keyboard/)

	returns:
		desc:	A `keyboard` object.
		type:	keyboard

	example: |
		my_keyboard = keyboard(keylist=[u'a', u'b'], timeout=5000)
		key, time = my_keyboard.get_key()
	"""

	from openexp.keyboard import keyboard
	return keyboard(experiment, **resp_args)

def mouse(**resp_args):

	"""
	desc: |
		A convenience function that creates a new `mouse` object. For a
		description of possible keywords, see:

		- [/python/mouse/](/python/mouse/)

	returns:
		desc:	A `mouse` object.
		type:	mouse

	example: |
		my_mouse = mouse(keylist=[1,3], timeout=5000)
		button, time = my_mouse.get_button()
	"""

	from openexp.mouse import mouse
	return mouse(experiment, *arglist, **kwdict)

def sampler(src, **playback_args):

	"""
	desc: |
		A convenience function that creates a new `sampler` object. For a
		description of possible keywords, see:

		- [/python/sampler/](/python/sampler/)

	returns:
		desc:	A `sampler` object.
		type:	sampler

	example: |
		src = exp.pool['bark.ogg']
		my_sampler = sampler(src, volume=.5, pan='left')
		my_sampler.play()
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

	example: |
		my_canvas = copy_sketchpad('my_sketchpad')
		my_canvas.show()
	"""

	c = canvas()
	c.copy(experiment.items[name].canvas)
	return c

def reset_feedback():

	"""
	desc:
		Resets all feedback variables to their initial state.

	example: |
		reset_feedback()
	"""

	experiment.reset_feedback()

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

def sometimes(p=.5):

	"""
	desc: |
		Returns True with a certain probability. (For more advanced
		randomization, use the Python `random` module.)

	keywords:
		p:
			desc:	The probability of returning True.
			type:	float

	returns:
		desc:	True or False
		type:	bool

	example: |
		if sometimes():
			print('Sometimes you win')
		else:
			print('Sometimes you loose')
	"""

	if (not isinstance(p, float) and not isinstance(p, int)) or p < 0 or p > 1:
		raise osexception(
			u'p should be a numeric value between 0 and 1, not "%s"' % p)
	return random.random() < p

def pause():

	"""
	desc:
		Pauses the experiment.
	"""

	experiment.pause()

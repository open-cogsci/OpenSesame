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

def canvas(*arglist, **kwdict):

	"""
	desc:
		Creates a new `canvas` object. For a list of arguments and keywords,
		see the `canvas` documention.

	returns:
		desc:	A `canvas` object.
		type:	canvas

	example: |
		my_canvas = canvas()
	"""

	from openexp.canvas import canvas
	return canvas(experiment, *arglist, **kwdict)

def keyboard(*arglist, **kwdict):

	"""
	desc:
		Creates a new `keyboard` object. For a list of arguments and keywords,
		see the `keyboard` documention.

	returns:
		desc:	A `keyboard` object.
		type:	keyboard

	example: |
		my_keyboard = keyboard()
	"""

	from openexp.keyboard import keyboard
	return keyboard(experiment, *arglist, **kwdict)

def mouse(*arglist, **kwdict):

	"""
	desc:
		Creates a new `mouse` object. For a list of arguments and keywords,
		see the `mouse` documention.

	returns:
		desc:	A `mouse` object.
		type:	mouse

	example: |
		my_mouse = mouse()
	"""

	from openexp.mouse import mouse
	return mouse(experiment, *arglist, **kwdict)

def sampler(*arglist, **kwdict):

	"""
	desc:
		Creates a new `sampler` object. For a list of arguments and keywords,
		see the `sampler` documention.

	returns:
		desc:	A `sampler` object.
		type:	sampler

	example: |
		my_sampler = sampler()
	"""

	from openexp.sampler import sampler
	return sampler(experiment, *arglist, **kwdict)

def synth(*arglist, **kwdict):

	"""
	desc:
		Creates a new `synth` object. For a list of arguments and keywords,
		see the `synth` documention.

	returns:
		desc:	A `synth` object.
		type:	synth

	example: |
		my_synth = synth()
	"""

	from openexp.synth import synth
	return synth(experiment, *arglist, **kwdict)

# Miscellaneous API	functions

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

def log(msg):

	"""
	desc:
		Writes a message to the log file. Note that using the `log()` function
		in combination with a `logger` item is usually a bad idea, because it
		results in messy log files.

	arguments:
		msg:
			desc:	A message. This can be any type and will we be converted
					to a (unicode) string.

	example: |
		log('timestamp = %s' % time())
	"""

	experiment.log(msg)

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

def sleep(ms):

	"""
	desc:
		Waits (sleeps) for a specified duration.

	arguments:
		ms:
			desc:	An value specifying the duration in milliseconds.
			type:	[int, float]

	example: |
		sleep(1000) # Sleep one second
	"""

	experiment.sleep(ms)

def time():

	"""
	desc:
		Returns a timestamp for the current time. This timestamp only has
		a relative meaning, i.e. you can use it to determine the interval
		between two moments, but not the actual time.

	returns:
		desc:	A timestamp of the current time.
		type:	float

	example: |
		print('The time is %s' % time())
	"""

	return experiment.time()

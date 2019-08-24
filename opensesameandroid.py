#!/usr/bin/env python
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

import os
import sys
import pygame
import traceback
import yaml
from libopensesame.experiment import experiment, clean_up
try:
	import android
except:
	android = None

sdcard_folders = [
	'/sdcard/',
	'/mnt/sdcard/'
	]

class stdout_file(object):

	"""A class that redirects the standard output to a file"""

	def __init__(self, stdout):

		"""
		Constructor

		Arguments:
		stdout		--	the original standard output
		"""

		self.stdout = stdout

		# Try to auto-detect the sdcard location and create a text file there
		for path in sdcard_folders:
			if os.path.isdir(path):
				break
		try:
			self.fd = open(os.path.join(path, 'opensesame-debug.txt'), 'w')
		except:
			self.stdout.write('Failed to create %s' % path)
			self.fd = None

	def write(self, s):

		"""
		Write a message to the standard output

		Arguments:
		s			--	the message to write
		"""

		self.stdout.write(s+'\n')
		if self.fd is not None:
			self.fd.write(s)
			self.fd.flush()
			os.fsync(self.fd.fileno())

def main():

	"""The main routine, which is called automatically by pgs4a"""

	if android is not None:
		sys.stdout = stdout_file(sys.stdout)

	# First check if an autorun file has been specified. This is a yaml file
	# with the experiment path, subject nr, and logfile in it.
	for folder in sdcard_folders:
		path = os.path.join(folder, 'opensesame-autorun.yml')
		print(path)
		if os.path.exists(path):
			d = yaml.load(open(path))
			experiment_path = d['experiment']
			subject_nr = d['subject_nr']
			logfile = d['logfile']
			break
	# If no autorun file has been specified, we launch the menu experiment.
	else:
		src = 'opensesame_resources/android/menu.osexp'
		print('Launching %s' % src)
		menu = experiment('Experiment', src)
		menu.experiment_path = None
		menu.run()
		menu.end()
		clean_up(menu.debug)
		experiment_path = menu._experiment
		subject_nr = menu._subject_nr
		logfile = menu._logfile

	# Next run the actual experiment!
	try:
		exp = experiment(name='Experiment', string=experiment_path,
			experiment_path=os.path.dirname(experiment_path))
	except Exception as e:
		for s in traceback.format_exc(e).split("\n"):
			print(s)
	print('Launching %s' % experiment_path)
	exp.set_subject(subject_nr)
	exp.logfile = logfile

	# Capture exceptions and write them to the standard output so they can be
	# inspected
	try:
		exp.run()
	except Exception as e:
		for s in traceback.format_exc(e).split("\n"):
			print(s)
	try:
		exp.end()
	except Exception as e:
		for s in traceback.format_exc(e).split("\n"):
			print(s)

	clean_up(exp.debug)
	pygame.display.quit()

if __name__ == "__main__":

	# This is only necessary for testing on a regular PC. On Android, the main()
	# function is called automatically.
	main()

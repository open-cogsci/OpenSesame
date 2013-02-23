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

import sys
import pygame
import traceback
from libopensesame.experiment import experiment, clean_up
try:
	import android
except:
	android = None
	
class stdout_file(object):
	
	"""A class that redirects the standard output to a file"""
	
	def __init__(self, stdout, path='/storage/sdcard0/opensesame-debug.txt'):
		
		"""
		Constructor
		
		Arguments:
		stdout		--	the original standard output
		
		Keyword arguments:
		path		--	the path for the logfile (default=
						'/storage/sdcard0/opensesame-debug.txt')
		"""
		
		self.stdout = stdout
		try:
			self.fd = open(path, 'w')
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
		if self.fd != None:
			self.fd.write(s)
			self.fd.flush()		

def main():
	
	"""The main routine, which is called automatically by pgs4a"""

	sys.argv.append('--debug')	
	if android != None:		
		sys.stdout = stdout_file(sys.stdout)
		
	# First start the menu experiment	
	src = 'resources/android/menu.opensesame.tar.gz'
	print 'Launching %s' % src
	menu = experiment('Experiment', src)
	menu.run()
	menu.end()
	clean_up(menu.debug)	
	
	# Next run the actual experiment!
	exp = experiment('Experiment', menu._experiment)
	print 'Launching %s' % menu._experiment
	exp.subject_nr = menu._subject_nr
	exp.logfile = menu._logfile
	
	# Capture exceptions and write them to the standard output so they can be
	# inspected
	try:
		exp.run()		
	except Exception as e:
		for s in traceback.format_exc(e).split("\n"):
			print s		
	try:
		exp.end()
	except Exception as e:
		for s in traceback.format_exc(e).split("\n"):
			print s
	
	clean_up(exp.debug)		
	pygame.display.quit()
	
if __name__ == "__main__":

	# This is only necessary for testing on a regular PC. On Android, the main()
	# function is called automatically.
	main()
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

****

This is a Python implementation of the famous cowsay program, which
says funny things.
"""

import sys
import textwrap

def get_width(msg, maxlen = 40):

	"""
	Gets the width of the cowsay message
	"""

	w = 0
	for l in textwrap.wrap(msg, maxlen):
		l = l.replace("\t", "    ")
		w = max(w, len(l))			
	return min(w, maxlen)
	
def get_height(msg, maxlen = 40):

	"""
	Gets the height of the cowsay message
	"""
	
	i = 0	
	for l in textwrap.wrap(msg, maxlen):
		l = l.replace("\t", "    ")
		while len(l) > 0:
			l = l[maxlen:]	
			i += 1
	return i
	
def text_balloon(msg, maxlen = 40):

	"""
	Returns the textballoong
	"""
	
	w = get_width(msg, maxlen)
	h = get_height(msg, maxlen)
	
	s = " _" + "_" * w + "_\n"

	i = 0	
	for l in textwrap.wrap(msg, maxlen):

		l = l.replace("\t", "    ")
		while len(l) > 0:
			if h == 1:
				left = "<"
				right = ">"
			elif i == 0:
				left = "/"
				right = "\\ "				
			elif i == h - 1:
				left = "\\"
				right = "/"
			else:
				left = "|"
				right = "|"							
			
			s += "%s %s %s\n" % (left, l[:maxlen].ljust(w), right)
			l = l[maxlen:]	
			i += 1
			
	s += " -" + "-" * w + "-"
	
	return s	

def cowsay(msg, maxlen = 40):

	"""
	Prints the cowsay message
	"""
	
	s = text_balloon(msg, maxlen)
	s += """
        \\   ^__^
         \\  (oo)\_______
            (__)\       )\\/\\
                ||----w |
                ||     ||
		"""	
			
	return s
	
def tuxsay(msg, maxlen = 40):

	"""
	Prints the tuxsay message
	"""
	
	s = text_balloon(msg, maxlen)
	s += """
   \\
    \\
        .--.
       |o_o |
       |:_/ |
      //   \\ \\
     (|     | )
    /'\\_   _/`\\
    \___)=(___/
		"""	
			
	return s

if __name__ == "__main__":

	msg = sys.argv[:-1]

	if "--tux" in sys.argv:
		print tux_say(msg)
	else:
		print cow_say(msg)


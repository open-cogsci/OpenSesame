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

***

This file includes all kinds of things so that py2exe incorporates
them into the distribution. This is necessary, because items are
loaded at runtime, and therefore escape the detection of py2exe.
"""

import sys
import os

# Below is a quick hack to deal with pylinks quirky behavior.
# Pylink needs to be imported prior to pygame, otherwise it
# gives a DLL not found error. However, if we use a regular
# import statement, py2exe will include pylink with OpenSesame
# which is not allowed. This hack loads pylink if available,
# prior to pygame, without giving an error if pylink is not
# installed.

if "--pylink" in sys.argv:
	try:
		exec("import pylink") # This makes sure that py2exe doesn't try to include pylink
	except:
		print "includes: failed to import pylink module. You will not be able to use eyelink connectivity"

# Explicitly importing these modules ensures that Py2exe will
# bundle them. This is therefore only required for Windows.

if os.name == "nt":
		
	from libqtopensesame import\
		qtplugin,\
		pool_widget,\
		qtitem,\
		sketchpad,\
		feedback,\
		logger,\
		loop,\
		sequence,\
		keyboard_response,\
		mouse_response,\
		inline_script,\
		sampler
		
	try:
		import pyffmpeg
	except:
		print "includes: failed to import 'pyffmpeg'. You will not be able to use the media_player plug-in."
		
	try:
		import pyaudio
	except:
		print "includes: failed to import 'pyaudio'. You will not be able to use the media_player plug-in."		
		
	try:
		import serial
	except:
		print "includes: failed to import 'serial' modukle. You will not be able to use serial/ parallel port connectivity"

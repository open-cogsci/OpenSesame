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

# We don't need OpenSesame for standalone demo mode
if __name__ != "__main__":
	from libopensesame import exceptions
	
# Don't crash if we fail to load pylink, because we 
# may still use dummy mode.
try:
	import pylink
	import Image	
	custom_display = pylink.EyeLinkCustomDisplay
except:
	custom_display = object
	print "libeyelink: failed to import pylink"	
	
import os.path
import pygame
import array
import math

_eyelink = None
	
class libeyelink:

	def __init__(self, resolution, data_file = "default.edf", fg_color = (255, 255, 255), bg_color = (0, 0, 0), saccade_velocity_threshold = 35, saccade_acceleration_threshold = 9500):

		"""<DOC>
		Constructor. Initializes the connection to the Eyelink
	
		Arguments:
		resolution -- (width, height) tuple

		Keyword arguments:
		data_file -- the name of the EDF file (default.edf)
		fg_color -- the foreground color for the calibration screen (default = 255, 255, 255)
		bg_color -- the background color for the calibration screen (default = 0, 0, 0)
		saccade_velocity_threshold -- velocity threshold used for saccade detection (default = 35)
		saccade_acceleration_threshold -- acceleration threshold used for saccade detection (default = 9500)
	
		Returns:
		True on connection success and False on connection failure       
		</DOC>"""
		
		global _eyelink
	
		self.data_file = data_file
		self.resolution = resolution
		self.recording = False		
		
		self.saccade_velocity_treshold = saccade_velocity_threshold
		self.saccade_acceleration_treshold = saccade_acceleration_threshold
		self.eye_used = None
		self.left_eye = 0
		self.right_eye = 1
		self.binocular = 2
	
		# Only initialize the eyelink once		
		if _eyelink == None:
			try:
				_eyelink = pylink.EyeLink()
			except Exception as e:
				raise exceptions.runtime_error("Failed to connect to the tracker: %s" % e)
				
			graphics_env = eyelink_graphics(_eyelink)
			pylink.openGraphicsEx(graphics_env)	
					
		pylink.getEYELINK().openDataFile(self.data_file)		     
		pylink.flushGetkeyQueue()
		pylink.getEYELINK().setOfflineMode()
		
		# Notify the eyelink of the display resolution
		self.send_command("screen_pixel_coords =  0 0 %d %d" % (self.resolution[0], self.resolution[1]))

		# Determine the software version of the tracker
		self.tracker_software_ver = 0
		self.eyelink_ver = pylink.getEYELINK().getTrackerVersion()
		if self.eyelink_ver == 3:
			tvstr = pylink.getEYELINK().getTrackerVersionString()
			vindex = tvstr.find("EYELINK CL")
			self.tracker_software_ver = int(float(tvstr[(vindex + len("EYELINK CL")):].strip()))

		# Set some configuration stuff (not sure what the parser and gazemap mean)
		if self.eyelink_ver >= 2:
			self.send_command("select_parser_configuration 0")
			if self.eyelink_ver == 2: #turn off scenelink camera stuff
				self.send_command("scene_camera_gazemap = NO")
		else:
			self.send_command("saccade_velocity_threshold = %d" % self.saccade_velocity_threshold)
			self.send_command("saccade_acceleration_threshold = %s" % self.saccade_acceleration_threshold)
	
		# Set EDF file contents. This specifies which data is written to the EDF file.
		self.send_command("file_event_filter = LEFT,RIGHT,FIXATION,SACCADE,BLINK,MESSAGE,BUTTON")
		if self.tracker_software_ver >= 4:
			self.send_command("file_sample_data  = LEFT,RIGHT,GAZE,AREA,GAZERES,STATUS,HTARGET")
		else:
			self.send_command("file_sample_data  = LEFT,RIGHT,GAZE,AREA,GAZERES,STATUS")

		# Set link data. This specifies which data is sent through the link and thus can
		# be used in gaze contingent displays
		self.send_command("link_event_filter = LEFT,RIGHT,FIXATION,SACCADE,BLINK,BUTTON")
		if self.tracker_software_ver >= 4:
			self.send_command("link_sample_data  = LEFT,RIGHT,GAZE,GAZERES,AREA,STATUS,HTARGET")
		else:
			self.send_command("link_sample_data  = LEFT,RIGHT,GAZE,GAZERES,AREA,STATUS") 

		# Not sure what this means. Maybe the button that is used to end drift correction?
		self.send_command("button_function 5 'accept_target_fixation'")
					
		if not self.connected():
			raise exceptions.runtime_error("Failed to connect to the eyetracker")
			
	
	def send_command(self, cmd):

		"""<DOC>
		Sends a command to the eyelink
	
		Arguments:
		cmd -- the eyelink command to be executed
		</DOC>"""
	
		pylink.getEYELINK().sendCommand(cmd)
	
	def log(self, msg):

		"""<DOC>
		Writes a message to the eyelink data file
	
		Arguments:
		msg -- the message to be logged
		</DOC>"""

		pylink.getEYELINK().sendMessage(msg)
	
	def log_var(self, var, val):

		"""<DOC>
		Writes a variable to the eyelink data file. This is a shortcut for
		eyelink.log("var %s %s" % (var, val))
	
		Arguments:
		var -- the variable name
		val -- the value
		</DOC>"""

		pylink.getEYELINK().sendMessage("var %s %s" % (var, val))
	
	def status_msg(self, msg):

		"""<DOC>
		Sets the eyelink status message, which is displayed on the 
		eyelink experimenter pc
	
		Arguments:
		msg -- the status message
		</DOC>"""
	
		pylink.getEYELINK().sendCommand("record_status_message '%s'" % msg)
	
	def connected(self):

		"""<DOC>
		Returs the status of the eyelink connection
	
		Returns:
		True if connected, False otherwise
		</DOC>"""
	
		return pylink.getEYELINK().isConnected()
		
	def calibrate(self):

		"""<DOC>
		Starts eyelink calibration
	
		Exceptions:
		Raises an exceptions.runtime_error on failure		
		</DOC>"""
	
		if self.recording:
			raise exceptions.runtime_error("Trying to calibrate after recording has started")	
	
		pylink.getEYELINK().doTrackerSetup()
	
	def drift_correction(self, pos = None, fix_triggered = False):

		"""<DOC>
		Performs drift correction and falls back to the calibration screen if
		necessary
	
		Keyword arguments:
		pos -- the coordinate (x,y tuple) of the drift correction dot or None
			   for the display center (default = None)
		fix_triggered -- a boolean indicating whether drift correction should
						 be fixation triggered, rather than spacebar triggered
						 (default = False)

		Returns:
		True on success, False on failure
	
		Exceptions:
		Raises an exceptions.runtime_error on error
		</DOC>"""
		
		if self.recording:
			raise exceptions.runtime_error("Trying to do drift correction after recording has started")

		if fix_triggered:
			return self.fix_triggered_drift_correction(pos)

		if pos == None:
			pos = self.resolution[0] / 2, self.resolution[1] / 2
					
		while True:	
			if not self.connected():
				raise exceptions.runtime_error("The eyelink is not connected")	
			try:
				# Params: x, y, draw fix, allow_setup
				error = pylink.getEYELINK().doDriftCorrect(pos[0], pos[1], 0, 1)
				if error != 27:
					print "libeyelink.drift_correction(): success"
					return True
				else:
					print "libeyelink.drift_correction(): escape pressed"
					return False
			except:
				print "libeyelink.drift_correction(): try again"
				return False
			
	def prepare_drift_correction(self, pos):

		"""<DOC>
		Puts the tracker in drift correction mode
	
		Arguments:
		pos -- the reference point
	
		Exceptions:
		Raises an exceptions.runtime_error on error	
		</DOC>"""

		# Start collecting samples in drift correction mode
		self.send_command("heuristic_filter = ON")	
		self.send_command("drift_correction_targets = %d %d" % pos)	
		self.send_command("start_drift_correction data = 0 0 1 0")
		pylink.msecDelay(50);
	
		# Wait for a bit until samples start coming in (I think?)
		if not pylink.getEYELINK().waitForBlockStart(100, 1, 0):
			raise exceptions.runtime_error("Failed to perform drift correction (waitForBlockStart error)")	
			
	def fix_triggered_drift_correction(self, pos = None, min_samples = 30, max_dev = 60, reset_threshold = 10):

		"""<DOC>
		Performs fixation triggered drift correction and falls back to the
		calibration screen if necessary
	
		Keyword arguments:
		pos -- the coordinate (x,y tuple) of the drift correction dot or None
			   for the display center (default = None)
		min_samples -- the minimum nr of stable samples that should be acquired
					   (default = 30)
		max_dev -- the maximum allowed deviation (default = 60)
		reset_threshold -- the maximum allowed deviation from one sample to the
						   next (default = 10)
	
		Returns:
		True on success, False on failure
	
		Exceptions:
		Raises an exceptions.runtime_error on error
		</DOC>"""
	
		if self.recording:
			raise exceptions.runtime_error("Trying to do drift correction after recording has started")
		
		self.recording = True
	
		if pos == None:
			pos = self.resolution[0] / 2, self.resolution[1] / 2	
		
		self.prepare_drift_correction(pos)
		
		# Loop until we have sufficient samples
		lx = []
		ly = []
		while len(lx) < min_samples:
	
			# Pressing escape enters the calibration screen	
			for event in pygame.event.get():
				if event.type == pygame.KEYDOWN:
					if event.key == pygame.K_ESCAPE:
						self.recording = False
						print "libeyelink.fix_triggered_drift_correction(): escape pressed"
						return False
	
			# Collect a sample
			x, y = self.sample()
		
			if len(lx) == 0 or x != lx[-1] or y != ly[-1]:
						
				# If the current sample deviates too much from the previous one,
				# reset counting
				if len(lx) > 0 and (abs(x - lx[-1]) > reset_threshold or abs(y - ly[-1]) > reset_threshold):
			
					lx = []
					ly = []
			
				# Collect samples
				else:		
		
					lx.append(x)
					ly.append(y)			
			
	
			if len(lx) == min_samples:
	
				avg_x = sum(lx) / len(lx)
				avg_y = sum(ly) / len(ly)			
				d = math.sqrt( (avg_x - pos[0]) ** 2 + (avg_y - pos[1]) ** 2)
	
				# Emulate a spacebar press on success
				pylink.getEYELINK().sendKeybutton(32, 0, pylink.KB_PRESS)			
			
				# getCalibrationResult() returns 0 on success and an exception
				# or a non-zero value otherwise
				result = -1
				try:
					result = pylink.getEYELINK().getCalibrationResult()
				except:
					lx = []
					ly = []
					print "libeyelink.fix_triggered_drift_correction(): try again"
				if result != 0:
					lx = []
					ly = []
					print "libeyelink.fix_triggered_drift_correction(): try again"
							
		
		# Apply drift correction
		pylink.getEYELINK().applyDriftCorrect()	
		self.recording = False		
		
		print "libeyelink.fix_triggered_drift_correction(): success"
		
		return True
	
	def start_recording(self):

		"""<DOC>
		Starts recording of gaze samples
	
		Exceptions:
		Raises an exceptions.runtime_error on failure
		</DOC>"""
	
		self.recording = True

		# Params: write  samples, write event, send samples, send events
		error = pylink.getEYELINK().startRecording(1, 1, 1, 1)
		if error:
			raise exceptions.runtime_error("Failed to start recording (startRecording error)")
		
		# Don't know what this is
		pylink.pylink.beginRealTimeMode(100)

		# Wait for a bit until samples start coming in (I think?)
		if not pylink.getEYELINK().waitForBlockStart(100, 1, 0):
			raise exceptions.runtime_error("Failed to start recording (waitForBlockStart error)")
		
	def stop_recording(self):

		"""<DOC>
		Stop recording of gaze samples
		</DOC>"""
	
		self.recording = False	

		pylink.endRealTimeMode();
		pylink.getEYELINK().setOfflineMode();                          
		pylink.msecDelay(500);                 

	def close(self):

		"""<DOC>
		Close the connection with the eyelink
		</DOC>"""
	
		if self.recording:
			self.stop_recording()

		# Close the datafile and transfer it to the experimental pc
		print "libeyelink: closing data file"
		pylink.getEYELINK().closeDataFile()
		pylink.msecDelay(100)
		print "libeyelink: transferring data file"
		pylink.getEYELINK().receiveDataFile(self.data_file, self.data_file)
		pylink.msecDelay(100)		
		print "libeyelink: closing eyelink"
		pylink.getEYELINK().close();
		pylink.msecDelay(100)		
	
	def set_eye_used(self):

		"""<DOC>
		Sets the eye_used variable, based on the eyelink's report, which
		specifies which eye is being tracked. If both eyes are being tracked,
		the left eye is used.
	
		Exceptions:
		Raises an exceptions.runtime_error on failure	
		<DOC>"""

		self.eye_used = pylink.getEYELINK().eyeAvailable()
		if self.eye_used == self.right_eye:
			self.log_var("eye_used", "right")
		elif self.eye_used == self.left_eye or self.eye_used == self.binocular:
			self.log_var("eye_used", "left")
			self.eye_used = self.left_eye
		else:
			raise exceptions.runtime_error("Failed to determine which eye is being recorded")
	
	def sample(self):

		"""<DOC>
		Gets the most recent gaze sample from the eyelink
	
		Returns:
		A tuple (x, y) containing the coordinates of the sample
	
		Exceptions:
		Raises an exceptions.runtime_error on failure		
		</DOC>"""
	
		if not self.recording:
			raise exceptions.runtime_error("Please start recording before collecting eyelink data")
	
		if self.eye_used == None:
			self.set_eye_used()
		
		s = pylink.getEYELINK().getNewestSample()
		if s != None:
			if self.eye_used == self.right_eye and s.isRightSample():
				gaze = s.getRightEye().getGaze()
			elif self.eye_used == self.left_eye and s.isLeftSample():
				gaze = s.getLeftEye().getGaze()
		
		return gaze
	
	def wait_for_event(self, event):

		"""<DOC>
		Waits until an event has occurred
	
		Arguments:
		event -- eyelink event, like pylink.STARTSACC
	
		Exceptions:
		Raises an exceptions.runtime_error on failure			
		</DOC>"""

		if not self.recording:
			raise exceptions.runtime_error("Please start recording before collecting eyelink data")	
	
		if self.eye_used == None:
			self.set_eye_used()

		d = 0
		while d != event:
			d = pylink.getEYELINK().getNextData()
		
		return pylink.getEYELINK().getFloatData()
	
	def wait_for_saccade_start(self):

		"""<DOC>
		Waits for a saccade start
	
		Returns:
		timestamp, start_pos
		
		Exceptions:
		Raises an exceptions.runtime_error on failure			
		</DOC>"""
	
		d = self.wait_for_event(pylink.STARTSACC)
		return d.getTime(), d.getStartGaze()
	
	def wait_for_saccade_end(self):

		"""<DOC>
		Waits for a saccade end
	
		Returns:
		timestamp, start_pos, end_pos
		
		Exceptions:
		Raises an exceptions.runtime_error on failure			
		</DOC>"""
	
		d = self.wait_for_event(pylink.ENDSACC)
		return d.getTime(), d.getStartGaze(), d.getEndGaze()
	
	def wait_for_fixation_start(self):

		"""<DOC>
		Waits for a fixation start
	
		Returns:
		timestamp, start_pos
		
		Exceptions:
		Raises an exceptions.runtime_error on failure			
		</DOC>"""
	
		d = self.wait_for_event(pylink.STARTFIX)		
		return d.getTime(), d.getStartGaze()
	
	
	def wait_for_fixation_end(self):

		"""<DOC>
		Waits for a fixation end
	
		Returns:
		timestamp, start_pos, end_pos
		
		Exceptions:
		Raises an exceptions.runtime_error on failure			
		</DOC>"""
	
		d = self.wait_for_event(pylink.ENDFIX)	
		return d.getTime(), d.getStartGaze(), d.getEndGaze()
	
	def wait_for_blink_start(self):

		"""<DOC>
		Waits for a blink start
	
		Returns:
		timestamp
		
		Exceptions:
		Raises an exceptions.runtime_error on failure			
		</DOC>"""

		d = self.wait_for_event(pylink.STARTBLINK)	
		return d.getTime()
	
	def wait_for_blink_end(self):

		"""<DOC>
		Waits for a blink end
	
		Returns:
		timestamp
		
		Exceptions:
		Raises an exceptions.runtime_error on failure			
		</DOC>"""

		d = self.wait_for_event(pylink.ENDBLINK)	
		return d.getTime()
		
class libeyelink_dummy:

	"""
	A dummy class to keep things running if there is
	no tracker attached.
	"""

	def __init__(self):
		pass
	
	def send_command(self, cmd):
		pass
	
	def log(self, msg):
		pass	

	def log_var(self, var, val):
		pass	
		
	def status_msg(self, msg):
		pass
	
	def connected(self):
		pass
		
	def calibrate(self):
		pass
	
	def drift_correction(self, pos = None, fix_triggered = False):
		pygame.time.delay(200)
		return True

	def prepare_drift_correction(self, pos):
		pass
					
	def fix_triggered_drift_correction(self, pos = None, min_samples = 30, max_dev = 60, reset_threshold = 10):
		pygame.time.delay(200)
		return True
	
	def start_recording(self):
		pass
		
	def stop_recording(self):
		pass

	def close(self):
		pass

	def set_eye_used(self):
		pass

	def sample(self):
		pass

	def wait_for_event(self, event):
		pass
		
	def wait_for_saccade_start(self):
		pygame.time.delay(100)
		return pygame.time.get_ticks(), (0, 0)	

	def wait_for_saccade_end(self):
		pygame.time.delay(100)
		return pygame.time.get_ticks(), (0, 0)	

	def wait_for_fixation_start(self):
		pygame.time.delay(100)
		return pygame.time.get_ticks(), (0, 0)	
		
	def wait_for_fixation_end(self):
		pygame.time.delay(100)
		return pygame.time.get_ticks(), (0, 0)	
	
	def wait_for_blink_start(self):
		pygame.time.delay(100)
		return pygame.time.get_ticks(), (0, 0)	
	
	def wait_for_blink_end(self):
		pygame.time.delay(100)
		return pygame.time.get_ticks(), (0, 0)			
		
	
class eyelink_graphics(custom_display):

	"""
	A custom graphics environment to provide calibration
	functionality using PyGame, rather than PyLinks built-in
	system, which causes crashes in combination with PyGame.
	
	Derived from the examples provided with PyLink
	"""
	
	fgcolor = 255, 255, 255, 255
	bgcolor = 0, 0, 0, 255

	def __init__(self, tracker):
	
		"""
		Constructor
		"""
	
		pylink.EyeLinkCustomDisplay.__init__(self)
				
		self.__target_beep__ = pygame.mixer.Sound(os.path.join(os.path.dirname(__file__), "click.wav"))
		self.__target_beep__done__ = pygame.mixer.Sound(os.path.join(os.path.dirname(__file__), "success.wav"))
		self.__target_beep__error__ = pygame.mixer.Sound(os.path.join(os.path.dirname(__file__), "error.wav"))
		
		self.imagebuffer = array.array('l')
		self.pal = None	
		self.size = (0,0)
			
		self.fnt = pygame.font.Font(os.path.join(os.path.dirname(__file__), "mono.ttf"), 12)		
		#self.fnt.set_bold(1)
		
		self.set_tracker(tracker)
		self.last_mouse_state = -1			    
    
	def set_tracker(self, tracker):
	
		"""
		Connect the tracker to the graphics environment
		"""
	
		self.tracker = tracker
		self.tracker_version = tracker.getTrackerVersion()
		if(self.tracker_version >=3):
			self.tracker.sendCommand("enable_search_limits=YES")
			self.tracker.sendCommand("track_search_limits=YES")
			self.tracker.sendCommand("autothreshold_click=YES")
			self.tracker.sendCommand("autothreshold_repeat=YES")
			self.tracker.sendCommand("enable_camera_position_detect=YES")			

	def setup_cal_display (self):
	
		"""
		Setup the calibration display.
		"""
	
		self.clear_cal_display()
				
	def exit_cal_display(self): 
	
		"""
		Called when exiting the calibration display
		"""
	
		self.clear_cal_display()
		
	def record_abort_hide(self):
	
		"""
		Don't know what this does (nothing, obviously,
		but don't know what it may do).
		"""
	
		pass

	def clear_cal_display(self):
	
		"""
		Erase the calibration display with black
		"""
	
		surf = pygame.display.get_surface()
		surf.fill(self.bgcolor)
		pygame.display.flip()
		surf.fill(self.bgcolor) 
		
	def erase_cal_target(self):
	
		"""
		Erase the target
		"""
	
		surf = pygame.display.get_surface()
		surf.fill(self.bgcolor)
		
		
	def draw_cal_target(self, x, y): 
	
		"""
		Draw the calibration target
		"""
	
		outsz=10
		insz=4
		
		surf = pygame.display.get_surface()
		rect = pygame.Rect(x-outsz, y-outsz, outsz*2, outsz*2)
		pygame.draw.ellipse(surf, self.fgcolor, rect)	
		rect = pygame.Rect(x-insz, y-insz, insz*2, insz*2)
		pygame.draw.ellipse(surf, self.bgcolor, rect)	
		pygame.display.flip()
		
	def play_beep(self,beepid):
	
		"""
		Play a sound
		"""
	
		if beepid == pylink.DC_TARG_BEEP or beepid == pylink.CAL_TARG_BEEP:
			self.__target_beep__.play()
		elif beepid == pylink.CAL_ERR_BEEP or beepid == pylink.DC_ERR_BEEP:
			self.__target_beep__error__.play()
		else:#	CAL_GOOD_BEEP or DC_GOOD_BEEP
			self.__target_beep__done__.play()
			
	def getColorFromIndex(self,colorindex):
	
		"""
		Defines the colors for the eye video
		"""
	
		if colorindex   ==  pylink.CR_HAIR_COLOR:          return (255,255,255,255)
		elif colorindex ==  pylink.PUPIL_HAIR_COLOR:       return (255,255,255,255)
		elif colorindex ==  pylink.PUPIL_BOX_COLOR:        return (0,255,0,255)
		elif colorindex ==  pylink.SEARCH_LIMIT_BOX_COLOR: return (255,0,0,255)
		elif colorindex ==  pylink.MOUSE_CURSOR_COLOR:     return (255,0,0,255)
		else: return (0,0,0,0)		
		
	def draw_line(self, x1, y1, x2, y2, colorindex):
	
		"""
		Draws a line
		"""
	
		color = self.getColorFromIndex(colorindex)
		imr = self.__img__.get_rect()
				
		x1=int((float(x1)/float(self.size[0]))*imr.w)
		x2=int((float(x2)/float(self.size[0]))*imr.w)
		y1=int((float(y1)/float(self.size[1]))*imr.h)
		y2=int((float(y2)/float(self.size[1]))*imr.h)
		pygame.draw.line(self.__img__,color,(x1,y1),(x2,y2))
							
	def draw_lozenge(self,x,y,width,height,colorindex):
		
		ci = 100
		color = self.getColorFromIndex(colorindex)
		
		#guide
		#self.draw_line(x,y,x+width,y,ci) #hor
		#self.draw_line(x,y+height,x+width,y+height,ci) #hor
		#self.draw_line(x,y,x,y+height,ci) #ver
		#self.draw_line(x+width,y,x+width,y+height,ci) #ver
		
		
		imr = self.__img__.get_rect()
		x=int((float(x)/float(self.size[0]))*imr.w)
		width=int((float(width)/float(self.size[0]))*imr.w)
		y=int((float(y)/float(self.size[1]))*imr.h)
		height=int((float(height)/float(self.size[1]))*imr.h)
		
		 
		if width>height:
			rad = height/2
			
			#draw the lines
			pygame.draw.line(self.__img__,color,(x+rad,y),(x+width-rad,y))
			pygame.draw.line(self.__img__,color,(x+rad,y+height),(x+width-rad,y+height))
			
			#draw semicircles
			
			pos = (x+rad,y+rad)
			clip = (x,y,rad,rad*2)
			self.__img__.set_clip(clip)
			pygame.draw.circle(self.__img__,color,pos,rad,1)
			self.__img__.set_clip(imr)
			
			pos = ((x+width)-rad,y+rad)
			clip = ((x+width)-rad,y,rad,rad*2)
			self.__img__.set_clip(clip)
			pygame.draw.circle(self.__img__,color,pos,rad,1)
			self.__img__.set_clip(imr)
		else:
			rad = width/2

			#draw the lines
			pygame.draw.line(self.__img__,color,(x,y+rad),(x,y+height-rad))
			pygame.draw.line(self.__img__,color,(x+width,y+rad),(x+width,y+height-rad))

			#draw semicircles
			if rad ==0: 
				return #cannot draw sthe circle with 0 radius
			pos = (x+rad,y+rad)
			clip = (x,y,rad*2,rad)
			self.__img__.set_clip(clip)
			pygame.draw.circle(self.__img__,color,pos,rad,1)
			self.__img__.set_clip(imr)

			pos = (x+rad,y+height-rad)
			clip = (x,y+height-rad,rad*2,rad)
			self.__img__.set_clip(clip)
			pygame.draw.circle(self.__img__,color,pos,rad,1)
			self.__img__.set_clip(imr)

			

	def get_mouse_state(self):
	
		"""
		Return the position and press-state of the mouse
		"""
	
		pos = pygame.mouse.get_pos()
		state = pygame.mouse.get_pressed()
		return (pos,state[0])
		
		
	def get_input_key(self):
	
		"""
		Get an input key
		"""
		
		ky=[]
		
		try:
			v = pygame.event.get()
		except:
			return None
			
		for key in v:
			if key.type != pygame.KEYDOWN:
				continue
			keycode = key.key
			if keycode == pygame.K_F1:  keycode = pylink.F1_KEY
			elif keycode ==  pygame.K_F2:  keycode = pylink.F2_KEY
			elif keycode ==   pygame.K_F3:  keycode = pylink.F3_KEY
			elif keycode ==   pygame.K_F4:  keycode = pylink.F4_KEY
			elif keycode ==   pygame.K_F5:  keycode = pylink.F5_KEY
			elif keycode ==   pygame.K_F6:  keycode = pylink.F6_KEY
			elif keycode ==   pygame.K_F7:  keycode = pylink.F7_KEY
			elif keycode ==   pygame.K_F8:  keycode = pylink.F8_KEY
			elif keycode ==   pygame.K_F9:  keycode = pylink.F9_KEY
			elif keycode ==   pygame.K_F10: keycode = pylink.F10_KEY

			elif keycode ==   pygame.K_PAGEUP: keycode = pylink.PAGE_UP
			elif keycode ==   pygame.K_PAGEDOWN:  keycode = pylink.PAGE_DOWN
			elif keycode ==   pygame.K_UP:    keycode = pylink.CURS_UP
			elif keycode ==   pygame.K_DOWN:  keycode = pylink.CURS_DOWN
			elif keycode ==   pygame.K_LEFT:  keycode = pylink.CURS_LEFT
			elif keycode ==   pygame.K_RIGHT: keycode = pylink.CURS_RIGHT

			elif keycode ==   pygame.K_BACKSPACE:    keycode = ord('\b')
			elif keycode ==   pygame.K_RETURN:  keycode = pylink.ENTER_KEY
			elif keycode ==   pygame.K_ESCAPE:  keycode = pylink.ESC_KEY
			elif keycode ==   pygame.K_TAB:     keycode = ord('\t')
  			elif(keycode==pylink.JUNK_KEY): keycode= 0
  			
			ky.append(pylink.KeyInput(keycode,key.mod))
		return ky
		
	def exit_image_display(self):
	
		"""
		Exit the image display
		"""
	
		self.clear_cal_display()
		
	def alert_printf(self,msg):
		
		"""
		Print alert message		
		"""
	
		print "eyelink_graphics.alert_printf(): %s" % msg
							
	def setup_image_display(self, width, height):
	
		"""
		Setup the image
		"""
	
		self.size = (width,height)
		self.clear_cal_display()
		self.last_mouse_state = -1
		
	def image_title(self,  text): 
	
		"""
		Setup the title
		"""
	
		text = text 

		sz = self.fnt.size(text[0])
		txt = self.fnt.render(text,len(text),self.fgcolor, self.bgcolor)
		surf = pygame.display.get_surface()
		imgsz=(self.size[0]*3,self.size[1]*3)
		topleft = ((surf.get_rect().w-imgsz[0])/2,(surf.get_rect().h-imgsz[1])/2)
		imsz=(topleft[0],topleft[1]+imgsz[1]+10)
		surf.blit(txt, imsz)
		
		text = "OpenSesame Eyelink Integration"
		_txt = self.fnt.render(text, len(text), self.fgcolor, self.bgcolor)
		surf.blit(_txt, (10, 10))
		
		text = "C:calibrate, V:validate, ESC:quit, A:auto threshold, Up/Down:change threshold, Left/Right:change view"
		_txt2 = self.fnt.render(text, len(text), self.fgcolor, self.bgcolor)
		surf.blit(_txt2, (10, 30))	
		
		pygame.display.flip()
		surf.blit(txt, imsz)
		surf.blit(_txt, (10, 10))
		surf.blit(_txt2, (10, 30))
		    			
	def draw_image_line(self, width, line, totlines,buff):		
	
		"""
		Draw lines		
		"""
	
		i =0
		while i <width:
			self.imagebuffer.append(self.pal[buff[i]])
			i= i+1
						
		if line == totlines:
			imgsz = (self.size[0]*3,self.size[1]*3)
			bufferv = self.imagebuffer.tostring()
			img =Image.new("RGBX",self.size)
			img.fromstring(bufferv)
			img = img.resize(imgsz)
			
			
			img = pygame.image.fromstring(img.tostring(),imgsz,"RGBX");
			
			self.__img__ = img
			self.draw_cross_hair()
			self.__img__ = None
			surf = pygame.display.get_surface()
			surf.blit(img,((surf.get_rect().w-imgsz[0])/2,(surf.get_rect().h-imgsz[1])/2))
			pygame.display.flip()
			surf.blit(img,((surf.get_rect().w-imgsz[0])/2,(surf.get_rect().h-imgsz[1])/2)) # draw on the back buffer too
			self.imagebuffer = array.array('l')
										
	def set_image_palette(self, r,g,b): 
	
		"""
		Set the image palette
		"""
	
		self.imagebuffer = array.array('l')
		self.clear_cal_display()
		sz = len(r)
		i =0
		self.pal = []
		while i < sz:
			rf = int(b[i])
			gf = int(g[i])
			bf = int(r[i])
			self.pal.append((rf<<16) | (gf<<8) | (bf))
			i = i+1		
				
# If this library is called as standalone, it shows a demonstration
# of the eyelink	
if __name__ == "__main__":

	print "Initializing pygame"
	
	pygame.init()
	pygame.display.init()
	pygame.mixer.init()
	pygame.display.set_mode((800, 600), pygame.DOUBLEBUF | pygame.RLEACCEL,32)
	pygame.mouse.set_visible(False)
	
	print "Initializing pylink"		
	l = libeyelink( (800, 600) )
	
	print "Calibrate"
	l.calibrate()
	
	print "Closing"
	l.close()
	

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

# Will be inherited by video_player
from libopensesame import item

# Will be inherited by qtvideo_player
from libqtopensesame import qtplugin

# Used to access the file pool
from libqtopensesame import pool_widget

# Used to throw exceptions
from libopensesame import exceptions

import pyffmpeg
import pygame
from pygame.locals import *
import pyaudio
import os.path

class media_player(item.item):
	
	def __init__(self, name, experiment, string=None):
		"""
		Initialize module. Link to the video can already be specified but this is optional
		vfile: The path to the file to be played
		screensize: An optional tuple with the preferred (w,h) of the output frame. Otherwise, the video is played in its original size
		"""

		# The version of the plug-in
		self.version = 0.11
		
		self.mp = pyffmpeg.FFMpegReader(0,False)
		self.videoTrack = None
		self.audioTrack = None
		self.audioBuffer = []
		self.bufferedAudio = True
		self.file_loaded = False
		self.frameTime = 0
		self.paused = False

		self.item_type = "media_player"
		self.description = "Plays a video from file"		
		self.duration = "keypress"
		self.fullscreen = "yes"
		self.playaudio = "yes"
		self.audioCorrection = 150000
		self.video_src = ""
		self.sendInfoToEyelink = "yes"
		self.event_handler = ""

		# The parent handles the rest of the construction
		item.item.__init__(self, name, experiment, string)
		

	def prepare(self):     
		"""
		Opens the video file for playback
		"""
				
		# Pass the word on to the parent
		item.item.prepare(self)
		
		# Byte-compile the event handling code (if any)
		if self.event_handler.strip() != "":
			self._event_handler = compile(self.event_handler, "<string>", "exec")
		else:
			self._event_handler = None

		# Find the full path to the video file. This will point to some
		# temporary folder where the file pool has been placed
		path = self.experiment.get_file(str(self.get("video_src")))

		# Open the video file
		if not os.path.exists(path) or str(self.get("video_src")).strip() == "":
			raise exceptions.runtime_error("Video file '%s' was not found in video_player '%s' (or no video file was specified)." % (os.path.basename(path), self.name))
		self.load(path)

		# Report success
		return True
		
	def load(self,vfile):
		"""
		Load a videofile and make it ready for playback
		file: The path to the file to be played
		"""
		
		if self.fullscreen == "no":
			TS_VIDEO_RGB24={ 'video1':(0, -1, {'pixel_format':pyffmpeg.PixelFormats.RGB24}), 'audio1':(1,-1,{})}
		elif self.fullscreen == "yes":
			TS_VIDEO_RGB24={ 'video1':(0, -1, {'pixel_format':pyffmpeg.PixelFormats.RGB24,'dest_width':self.experiment.width, 'dest_height':self.experiment.height}), 'audio1':(1,-1,{})}
		else:
			raise ValueError #Will never happen, but just in case
   
		#Check if audio stream is present, if not only process the video
		try:        
			self.mp.open(vfile,TS_VIDEO_RGB24)               # will throw IOError if it doesn't find an audio stream
			(self.videoTrack,self.audioTrack) = self.mp.get_tracks()
			if self.playaudio == "yes":
				self.samplingFreq = self.audioTrack.get_samplerate()
				self.audioTrack.set_observer(self.handleAudioFrame)
				if self.experiment.debug:
					print "media_player.load(): Channels: %s" % self.audioTrack.get_channels()
				self.audiostream = pyaudio.PyAudio().open(rate=self.samplingFreq,
															channels=self.audioTrack.get_channels(),
															format=pyaudio.paInt16,
															output=True)
														
				self.hasSound = True
			else:
				self.hasSound = False
				self.audioTrack = None
		except:
			try:
				del TS_VIDEO_RGB24['audio1']
				self.mp.open(vfile)
			except Exception as e:
				raise exceptions.runtime_error("Error opening video file. Please make sure a video file is specified and that it is of a supported format.<br><br>Error: %s" % e)
			else:
				self.videoTrack = self.mp.get_tracks()[0]
				self.hasSound = False
				if self.experiment.debug:
					print "media_player.load(): No audio track found"

		self.videoTrack.set_observer(self.handleVideoFrame)
		self.frameTime = 1000/self.videoTrack.get_fps()

		if self.experiment.debug:
			print "media_player.load(): Calculated frametime: %s ms" % self.frameTime
			print "media_player.load(): FPS: %s" % self.videoTrack.get_fps()

		self.screen = self.experiment.surface
		self.file_loaded = True
				
	# The video and audio callback methods.
	def handleVideoFrame(self, f):
		"""
		Callback method called by the VideoTrack object for handling a video frame
		"""
		if self.fullscreen == "yes":
			pygame.surfarray.use_arraytype("numpy")
			f=f.swapaxes(0,1)
			pygame.surfarray.blit_array(self.screen,f) 
			pygame.display.flip()
		elif self.fullscreen == "no":
			img = pygame.image.frombuffer(f.tostring(),self.videoTrack.get_size(),"RGB")
			self.screen.blit(img,((self.experiment.width - img.get_width()) / 2, (self.experiment.height - img.get_height()) / 2))
			pygame.display.flip()
			
		   
	def handleAudioFrame(self, a):
		"""
		Callback method called by the AudioTrack object for handling an audio frame
		"""
		if self.bufferedAudio:
			if len(self.audioBuffer) and self.audioBuffer[0][1] <= (self.videoTrack.get_current_frame_pts()+(300000-self.audioCorrection)):
				audioFrame = self.audioBuffer.pop(0)
				self.audiostream.write(audioFrame[0])
			   
			# Store current audio frame in the buffer    
			self.audioBuffer.append( (a[0].data, self.audioTrack.get_cur_pts()) )
		else:
			self.audiostream.write(a[0].data)
		

	def pause(self):
		"""
		Pauses playback. Continue with unpause()
		"""
		self.paused = True

	def unpause(self):
		"""
		Continues playback
		"""
		self.paused = False

	def handleEvent(self, event):
		"""
		Allow the user to insert custom code
		"""
		video = self.videoTrack
		audio = self.audioTrack
		frame_no = self.videoTrack.get_current_frame_frameno()

		continue_playback = True
                
		try:
			exec(self._event_handler)
		except Exception as e:
			raise exceptions.runtime_error("Error while executing event handling code: %s" % e)
		
		if type(continue_playback) != bool:
			continue_playback = False
		
		return continue_playback

        def rewind(self):
                try:
                        self.videoTrack.seek_to_frame(1)    #To prevent reading before the first frame which happens occasionally with some files
                except IOError:
                        try:
                                self.videoTrack.seek_to_frame(10)
                        except IOError:
                                raise exceptions.runtime_error("Could not read the first frames of the video file")

	
	def run(self):
		"""
		Starts the playback of the video file. You can specify an optional callable object to handle events between frames (like keypresses)
		This function needs to return a boolean, because it determines if playback is continued or stopped. If no callable object is provided
		playback will stop when the ESC key is pressed
		"""
		# Log the onset time of the item
		self.set_item_onset()
		if self.experiment.debug:
			print "media_player.run(): Audio delay: %d" % (300000-self.audioCorrection)
		
		if self.file_loaded:
			self.rewind()   #Make sure pointer is at the beginning of the video file
			
			self.playing = True
			startTime = pygame.time.get_ticks()			
			while self.playing:
									
				self.frame_calc_start = pygame.time.get_ticks()
								
				# Process all events
				for event in pygame.event.get():		
					if event.type == pygame.KEYDOWN or event.type == pygame.MOUSEBUTTONDOWN:												
						if self._event_handler != None:
							self.playing = self.handleEvent(event)
						elif event.type == pygame.KEYDOWN and self.get("duration") == "keypress":
							self.playing = False
						elif event.type == pygame.MOUSEBUTTONDOWN and self.get("duration") == "mouseclick":
							self.playing = False
							
						# Catch escape presses
						if event.type == pygame.KEYDOWN and event.key == pygame.K_ESCAPE:							
							raise exceptions.runtime_error("The escape key was pressed")													
				
				# Advance to the next frame if the player isn't paused
				if not self.paused:				
					try:
						self.mp.step()
					except IOError as e:
						self.playing = False
						if self.experiment.debug:
							print "media_player.run(): an IOError was caught: %s" % e
							
					if self.sendInfoToEyelink == "yes" and hasattr(self.experiment,"eyelink") and self.experiment.eyelink.connected():
						frame_no = self.videoTrack.get_current_frame_frameno()
						self.experiment.eyelink.log("MSG videoframe %s" % frame_no)
						self.experiment.eyelink.status_msg("videoframe %s" % frame_no )
							
					# Check if max duration has been set, and exit if exceeded
					if type(self.get("duration")) == int:
						if pygame.time.get_ticks() - startTime > (self.get("duration")*1000):
							self.playing = False							
							
					#Sleep for remainder of a frame duration that's left after all the processing time. This is only necessary when there is no sound stream
					sleeptime = int(self.frameTime - pygame.time.get_ticks() + self.frame_calc_start)
					if sleeptime > 0:
						pygame.time.wait(sleeptime)                
                        
			self.rewind()  #Rewind, if it needs to be played again in a next trial/block
			
			return True
		else:
			raise exceptions.runtime_error("No video loaded")
			return False

class qtmedia_player(media_player, qtplugin.qtplugin):
	"""
	Handles the GUI aspects of the plug-in.
	"""

	def __init__(self, name, experiment, string = None):
	
		"""
		Constructor. This function doesn't do anything specific
		to this plugin. It simply calls its parents. Don't need to
		change, only make sure that the parent name matches the name
		of the actual parent.
		"""
				
		# Pass the word on to the parents		
		media_player.__init__(self, name, experiment, string)		
		qtplugin.qtplugin.__init__(self, __file__)	
			
	def init_edit_widget(self):

		"""
		This function creates the controls for the edit
		widget.
		"""
		
		# Lock the widget until we're doing creating it
		self.lock = True
		
		# Pass the word on to the parent		
		qtplugin.qtplugin.init_edit_widget(self, False)
		
		# We don't need to bother directly with Qt4, since the qtplugin class contains
		# a number of functions which directly create controls, which are automatically
		# applied etc. A list of functions can be found here:
		# http://files.cogsci.nl/software/opensesame/doc/libqtopensesame/libqtopensesame.qtplugin.html
		self.add_filepool_control("video_src", "Video file", self.browse_video, default = "", tooltip = "A video file")						
		self.add_combobox_control("fullscreen", "Resize to fit screen", ["yes", "no"], tooltip = "Resize the video to fit the full screen")
		self.add_combobox_control("playaudio", "Play audio", ["yes", "no"], tooltip = "Specifies if the video has to be played with audio, or in silence")
		if hasattr(self, "add_slider_control"):
			self.add_slider_control("audioCorrection","Audio delay", 0, 300000, default = 150000, left_label = "sooner" , right_label = "later",tooltip = "Specify audio delay relative to video")
		else:
			self.add_spinbox_control("audioCorrection", "Audio delay", 0, 300000, tooltip = "Specify audio delay relative to video")
		self.add_combobox_control("sendInfoToEyelink", "Send frame no. to EyeLink", ["yes", "no"], tooltip = "If an eyelink is connected, then it will receive the number of each displayed frame as a msg event.\r\nYou can also see this information in the eyelink's status message box.\r\nThis option requires the installation of the OpenSesame EyeLink plugin and an established connection to the EyeLink.")       		
		self.add_line_edit_control("duration", "Duration", tooltip = "Expecting a value in seconds, 'keypress' or 'mouseclick'")
		self.add_editor_control("event_handler", "Custom Python code for handling keypress and mouseclick events (See Help for more information)", syntax = True, tooltip = "Specify how you would like to handle events like mouse clicks or keypresses. When set, this overrides the Duration attribute")
		self.add_text("<small><b>Media Player OpenSesame Plugin v%.2f, Copyright (2011) Daniel Schreij</b></small>" % self.version)
		
		# Unlock
		self.lock = True
			
	def browse_video(self):
	
		"""
		This function is called when the browse button is clicked
		to select a video from the file pool. It displays a filepool
		dialog and changes the video_src field based on the selection.
		"""
		
		s = pool_widget.select_from_pool(self.experiment.main_window)
		if str(s) == "":
				return			
		self.auto_line_edit["video_src"].setText(s)			
		self.apply_edit_changes()	
			
	def apply_edit_changes(self):
	
		"""
		Set the variables based on the controls. The code below causes
		this to be handles automatically. Don't need to change.
		"""
		
		# Abort if the parent reports failure of if the controls are locked
		if not qtplugin.qtplugin.apply_edit_changes(self, False) or self.lock:
			return False
						
		# Refresh the main window, so that changes become visible everywhere
		self.experiment.main_window.refresh(self.name)		
		
		# Report success
		return True

	def edit_widget(self):
	
		"""
		Set the controls based on the variables. The code below causes
		this to be handled automatically. Don't need to change.
		"""
		
		# Lock the controls, otherwise a recursive loop might arise
		# in which updating the controls causes the variables to be
		# updated, which causes the controls to be updated, etc...
		self.lock = True
		
		# Let the parent handle everything
		qtplugin.qtplugin.edit_widget(self)				
		
		# Unlock
		self.lock = False
		
		# Return the _edit_widget
		return self._edit_widget


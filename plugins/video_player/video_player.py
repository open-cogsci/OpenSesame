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

# OpenCV is used to read the video file
import cv

# PyGame is used to control the display
import pygame
from pygame.locals import *

class video_player(item.item):

	"""
	Implements the plug-in
	"""

	def __init__(self, name, experiment, string = None):
	
		"""
		Constructor
		"""
		
		# The version of the plug-in
		self.version = 0.10
			
		# First we set the plug-ins properties
		self.item_type = "video_player"
		self.description = "Plays a video from file"		
		self.duration = "keypress"
		self.fullscreen = "yes"
		self.frame_dur = 50
		self.video_src = ""
				
		# The parent handles the rest of the construction
		item.item.__init__(self, name, experiment, string)
						
	def prepare(self):
	
		"""
		Opens the video file for playback
		"""
			
		# Pass the word on to the parent
		item.item.prepare(self)			

		# Find the full path to the video file. This will point to some
		# temporary folder where the file pool has been placed
		path = self.experiment.get_file(self.video_src)
		
		# Open the video file
		self.video = cv.CreateFileCapture(path)
		
		# Report success
		return True
				
	def run(self):
	
		"""
		Handles the actual video playback
		"""
		
		# Log the onset time of the item
		self.set_item_onset()
		
		t = pygame.time.get_ticks()
		start_t = t
				
		# Loop until a key is pressed
		go = True
		while go:
		
			# Getting the video from the file onto the PyGame canvas is a bit complicated:
			# http://opencv.willowgarage.com/documentation/python/cookbook.html#opencv-to-pygame
			src = cv.QueryFrame(self.video)
			src_rgb = cv.CreateMat(src.height, src.width, cv.CV_8UC3)
			cv.CvtColor(src, src_rgb, cv.CV_BGR2RGB)
			pg_img = pygame.image.frombuffer(src_rgb.tostring(), cv.GetSize(src_rgb), "RGB")
			
			# In fullscreen mode, the surface is converted to the pixel format of the display surface
			# and scaled directly onto the display surface
			if self.fullscreen == "yes":
				pg_img = pg_img.convert(self.experiment.surface)
				pygame.transform.scale(pg_img, (self.experiment.width, self.experiment.height), self.experiment.surface)

			# In unscaled mode, the surface is blitted onto the center of the display
			else:
				self.experiment.surface.blit(pg_img, ((self.experiment.width - pg_img.get_width()) / 2, (self.experiment.height - pg_img.get_height()) / 2))	
	
			# Show the changes
			pygame.display.flip()
		
			# Pause before jumping to the next frame
			pygame.time.wait(self.frame_dur - pygame.time.get_ticks() + t)
			t = pygame.time.get_ticks()

			if type(self.duration) == int:			
				# Wait for a specified duration
				if t - start_t >= self.duration:
					go = False
					
			# Catch escape presses
			for event in pygame.event.get():		
			
				if event.type == KEYDOWN:					
					if event.key == pygame.K_ESCAPE:
						raise exceptions.runtime_error("The escape key was pressed.")
					if self.duration == "keypress":	
						go = False
						
				if event.type == MOUSEBUTTONDOWN and self.duration == "mouseclick":
					go = False
					
		# Release the camera	
		# Note: This function appears to be missing. Perhaps it's ok
		# and Python will release it automatically?
		# cv.ReleaseCapture(self.video)		
				
		# Report success
		return True
					
class qtvideo_player(video_player, qtplugin.qtplugin):

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
		video_player.__init__(self, name, experiment, string)		
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
		self.add_line_edit_control("duration", "Duration", tooltip = "Expecting a value in milliseconds, 'keypress' or 'mouseclick'")
		self.add_spinbox_control("frame_dur", "Frame duration", 1, 500, suffix = "ms", tooltip = "Duration in milliseconds of a single frame")
		self.add_text("<small><b>Video Player OpenSesame Plugin v%.2f</b></small>" % self.version)
		
		# Add a stretch to the edit_vbox, so that the controls do not
		# stretch to the bottom of the window.
		self.edit_vbox.addStretch()		
		
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

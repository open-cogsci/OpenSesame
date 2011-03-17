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
import sys

class media_player(item.item):
    
    def __init__(self, name, experiment, string=None):
        """
        Initialize module. Link to the video can already be specified but this is optional
        vfile: The path to the file to be played
        screensize: An optional tuple with the preferred (w,h) of the output frame. Otherwise, the video is played in its original size
        """

        # The version of the plug-in
        self.version = 0.10
		
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
            raise ValueError
   
        #Check if audio stream is present, if not only process the video
        try:        
            self.mp.open(vfile,TS_VIDEO_RGB24)               # will throw IOError if it doesn't find an audio stream
            (self.videoTrack,self.audioTrack) = self.mp.get_tracks()
            if self.playaudio == "yes":
                self.samplingFreq = self.audioTrack.get_samplerate()
                self.audioTrack.set_observer(self.handleAudioFrame)
                print "Channels: %s" % self.audioTrack.get_channels()
                self.audiostream = pyaudio.PyAudio().open(rate=self.samplingFreq,
                                                            channels=self.audioTrack.get_channels(),
                                                            format=pyaudio.paInt16,
                                                            output=True)
                                                        
                self.hasSound = True
            else:
                self.hasSound = False
                self.audioTrack = None
        except:
            print "Error: %s:\n%s" % (sys.exc_info()[0],sys.exc_info()[1])
            try:
                del TS_VIDEO_RGB24['audio1']
                self.mp.open(vfile)
            except IOError:
                raise exceptions.runtime_error("Error opening video file. Please make sure a video file is specified and that it is of a supported format")              
            else:
                self.videoTrack = self.mp.get_tracks()[0]
                self.hasSound = False
                print "No audio track found"

        self.videoTrack.set_observer(self.handleVideoFrame)
        print "FPS: %s" % self.videoTrack.get_fps()
        self.frameTime = 1000/self.videoTrack.get_fps()
        print "Calculated frametime: %s ms" % self.frameTime

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
    
    def run(self, eventHandler=None):
        """
        Starts the playback of the video file. You can specify an optional callable object to handle events between frames (like keypresses)
        This function needs to return a boolean, because it determines if playback is continued or stopped. If no callable object is provided
        playback will stop when the ESC key is pressed
        """
        # Log the onset time of the item
        self.set_item_onset()
        startTime = pygame.time.get_ticks()
        print "Audio delay: %d" % (300000-self.audioCorrection)
        
        if self.file_loaded:
            self.playing = True
            while self.playing:
                self.frame_calc_start = pygame.time.get_ticks()
                try:
                    if self.paused == False:
                        self.mp.step()  # Retrieve the audio and video frame and handle them                  
                except IOError:
                    self.playing = False
                    print "Warning: %s: %s" % (sys.exc_info()[0],sys.exc_info()[1])
                    raise exceptions.runtime_error("Error playing back video file")
                else:
                    if callable(eventHandler):
                        result = eventHandler()
                        if type(result) == bool:
                            self.playing = result
                        else:
                            raise exceptions.runtime_error("Invalid return type of specified event handler: must be bool")
                            self.playing = False
                    else:                 
                        e = pygame.event.poll()
                        if e.type== pygame.KEYDOWN: 
                            if e.key== pygame.K_ESCAPE:
                                self.playing = False
                            if e.key== pygame.K_SPACE:
                                if self.paused == True:
                                    self.paused = False
                                else:
                                    self.paused = True
                        if self.sendInfoToEyelink == "yes" and hasattr(self.experiment,"eyelink") and self.experiment.eyelink.connected():
                            frame_no = self.videoTrack.get_current_frame_frameno()
                            self.experiment.eyelink.log("MSG videoframe %s" % frame_no)
                            self.experiment.eyelink.status_msg("videoframe %s" % frame_no )
                            
                    #Sleep for remainder of a frame duration that's left after all the processing time. This is only necessary when there is no sound stream
                    sleeptime = int(self.frameTime - pygame.time.get_ticks() + self.frame_calc_start)
                    if sleeptime > 0:
                        pygame.time.wait(sleeptime)                
                    # Check if max duration has been set, and exit if exceeded
                    if type(self.duration) == int:
                        if pygame.time.get_ticks() - startTime > (self.duration*1000):
                            self.playing = False
                        
                            
            # Clean up on aisle 4!
            if self.hasSound:
                if hasattr(self,"audiostream"):                
                    self.audiostream.close()
                    self.audioTrack.close()
            self.videoTrack.close()
            self.mp.close()
            return True
        else:
            print "No video loaded"
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
        self.add_slider_control("audioCorrection","Audio delay",0,300000,150000,"sooner","later",tooltip = "Specify audio delay relative to video")
        self.add_combobox_control("sendInfoToEyelink", "Send frame no. to EyeLink", ["yes", "no"], tooltip = "If an eyelink is connected, then it will receive the number of each displayed frame as a msg event.\r\nYou can also see this information in the eyelink's status message box.\r\nThis option requires the installation of the OpenSesame EyeLink plugin and an established connection to the EyeLink.")       
        self.add_line_edit_control("duration", "Duration", tooltip = "Expecting a value in seconds, 'keypress' or 'mouseclick'")
        
        #self.add_spinbox_control("frame_dur", "Frame duration", 1, 500, suffix = "ms", tooltip = "Duration in milliseconds of a single frame")
        self.add_text("<small><b>Media Player OpenSesame Plugin v%.2f</b></small>" % self.version)
        
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

    
if __name__ == "__main__":
    # File to test for now. Soon to be replaced by command line argument
    vfile = sys.argv[1]

    player = media_player(vfile)
    player.play()
    pygame.quit()


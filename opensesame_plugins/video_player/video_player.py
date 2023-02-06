# -*- coding:utf-8 -*-

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
from libopensesame.py3compat import *

# OpenCV is used to read the video file
import cv
# PyGame is used to control the display
import pygame
from pygame.locals import *

from libopensesame import item
from libqtopensesame.items.qtautoplugin import qtautoplugin
from libqtopensesame.widgets import pool_widget
from libopensesame.exceptions import osexception


class video_player(item.item):

    description = u'An OpenCV-based image-only video player'

    def __init__(self, name, experiment, script=None):
        """
        Constructor.

        Arguments:
        name		--	The item name.
        experiment	--	The experiment object.

        Keyword arguments:
        script		--	A definition script. (default=None)
        """
        self.duration = u"keypress"
        self.fullscreen = u"yes"
        self.frame_dur = 50
        self.video_src = u""
        item.item.__init__(self, name, experiment, script)

    def prepare(self):
        """Opens the video file for playback."""
        if self.experiment.var.get(u'canvas_backend') != u'legacy':
            raise osexception(
                u'The video_player plug-in requires the legacy back-end!')

        item.item.prepare(self)
        path = self.experiment.pool[self.var.get(u'video_src')]
        # Open the video file
        self.video = cv.CreateFileCapture(path)
        # Convert the string to a boolean, for slightly faster evaluations in
        # the run phase
        self._fullscreen = self.var.get(u'fullscreen') == u"yes"
        # The dimensions of the video
        self._w = int(cv.GetCaptureProperty(
            self.video, cv.CV_CAP_PROP_FRAME_WIDTH))
        self._h = int(cv.GetCaptureProperty(
            self.video, cv.CV_CAP_PROP_FRAME_HEIGHT))
        if self._fullscreen:
            # In fullscreen mode, the video is always shown in the top-left and the
            # temporary images need to be fullscreen size
            self._x = 0
            self._y = 0
            self.src_tmp = cv.CreateMat(self.experiment.var.height,
                                        self.experiment.var.width, cv.CV_8UC3)
            self.src_rgb = cv.CreateMat(self.experiment.var.height,
                                        self.experiment.var.width, cv.CV_8UC3)
        else:
            # Otherwise the location of the video depends on its dimensions and the
            # temporary image is the same size as the video
            self._x = max(0, (self.experiment.var.width - self._w) / 2)
            self._y = max(0, (self.experiment.var.height - self._h) / 2)
            self.src_rgb = cv.CreateMat(self._h, self._w, cv.CV_8UC3)

    def run(self):
        """Handles the actual video playback."""
        # Log the onset time of the item
        self.set_item_onset()

        t = pygame.time.get_ticks()
        start_t = t
        # Loop until a key is pressed
        go = True
        while go:
            # Get the frame
            self.src = cv.QueryFrame(self.video)
            # Check for the end of the video
            if self.src is None:
                break
            # Resize if requested and convert the resulting image to
            # RGB format, which is compatible with PyGame
            if self._fullscreen:
                cv.Resize(self.src, self.src_tmp)
                cv.CvtColor(self.src_tmp, self.src_rgb, cv.CV_BGR2RGB)
            else:
                cv.CvtColor(self.src, self.src_rgb, cv.CV_BGR2RGB)
            # Convert the image to PyGame format
            pg_img = pygame.image.frombuffer(self.src_rgb.tostring(),
                                             cv.GetSize(self.src_rgb), u"RGB")
            # Show the video frame!
            self.experiment.surface.blit(pg_img, (self._x, self._y))
            pygame.display.flip()
            # Pause before jumping to the next frame
            pygame.time.wait(
                self.var.get(u'frame_dur') - pygame.time.get_ticks() + t)
            t = pygame.time.get_ticks()
            if type(self.var.get(u'duration')) == int:
                # Wait for a specified duration
                if t - start_t >= self.var.get(u'duration'):
                    go = False
            # Catch escape presses
            for event in pygame.event.get():
                if event.type == KEYDOWN:
                    if event.key == pygame.K_ESCAPE:
                        self.experiment.pause()
                    if self.var.get(u'duration') == u"keypress":
                        go = False
                if event.type == MOUSEBUTTONDOWN and self.var.get(u'duration') == \
                        u"mouseclick":
                    go = False
        # Release the camera
        # Note: This function appears to be missing. Perhaps it's ok
        # and Python will release it automatically?
        # cv.ReleaseCapture(self.video)


class qtvideo_player(video_player, qtautoplugin):

    def __init__(self, name, experiment, script=None):

        video_player.__init__(self, name, experiment, script)
        qtautoplugin.__init__(self, __file__)

"""
This file is part of openexp.

openexp is free software: you can redistribute it and/or modify
it under the terms of the GNU General Public License as published by
the Free Software Foundation, either version 3 of the License, or
(at your option) any later version.

openexp is distributed in the hope that it will be useful,
but WITHOUT ANY WARRANTY; without even the implied warranty of
MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
GNU General Public License for more details.

You should have received a copy of the GNU General Public License
along with openexp.  If not, see <http://www.gnu.org/licenses/>.
"""

import pygame
from pygame.locals import *
from OpenGL.GL import *
try:
    from OpenGL.GLU import *
    GLU = 1
except:
    print "Warning: OpenGL.GLU did not import correctly."
    GLU = None

lastclearcolor = None
lastclearimage = None
def clearScreen(color):
    """
    Set the whole window to RGB 3-tuple color.
    """
    global lastclearcolor
    global lastclearimage
    try:
        alpha = color[3]
    except IndexError:
        alpha = 255
    if alpha == 255:
        glClearColor(color[0] / 255.0, color[1] / 255.0, color[2] / 255.0, alpha / 255.0)
        glClear(GL_COLOR_BUFFER_BIT)
    else:
        if lastclearcolor != color:
            x, y = pygame.display.get_surface().get_size()
            lastclearimage = LowImage(x + 1, y + 1)
            lastclearimage.fill(color[0], color[1], color[2], alpha)
            lastclearcolor = color
        lastclearimage.show(0, 0)

gl_version = None
def getGLVersion():
    # !!! You must have an active GL context to call this method !!!
    global gl_version
    if gl_version is None:
        # Determine the version. This kind of an ugly hack to make sure
        # that versions like 1.1.1 can be represented as a float (i.e., strip
        # the final digit
        v = glGetString(GL_VERSION)
        v = ".".join(v.split()[0].split(".")[:2])		
        gl_version = float(v)
    return gl_version

def doBlockingFlip():
    """
    Perform a flip and then write a pixel to the back buffer to pause
    the pipeline.  Inspired by PsychToolbox code.
    """

    # do the flip
    pygame.display.flip()
    
    # The following is taken from the PsychToolbox
    # Draw a single pixel in left-top area of back-buffer. This will wait/stall the rendering pipeline
    # until the buffer flip has happened, aka immediately after the VBL has started.
    # We need the pixel as "synchronization token", so the following glFinish() really
    # waits for VBL instead of just "falling through" due to the asynchronous nature of
    # OpenGL:
    glDrawBuffer(GL_BACK)
    # We draw our single pixel with an alpha-value of zero - so effectively it doesn't
    # change the color buffer - just the z-buffer if z-writes are enabled...
    glColor4f(0,0,0,0)
    glBegin(GL_POINTS)
    glVertex2i(10,10)
    glEnd()
    # This glFinish() will wait until point drawing is finished, ergo backbuffer was ready
    # for drawing, ergo buffer swap in sync with start of VBL has happened.
    glFinish()


class OGLSprite:
    """Implement the ugly details of "blitting" to OpenGL"""
    def __init__(self, surf, mipmap=None, interpolate=True):
        """OGLSprite(self, surf, mipmap=None) -> OGLSprite
        
        Create a drawable texture out of a given surface."""

        w, h = surf.get_width(), surf.get_height()
        if getGLVersion() >= 2.1:
            w2 = w
            h2 = h
            img = surf
        else:
            # must use power of 2
            w2, h2 = 1, 1
            while w2 < w: w2 <<= 1
            while h2 < h: h2 <<= 1
            img = pygame.Surface((w2, h2), SRCALPHA, 32)
            img.blit(surf, (0,0))

        rgba = pygame.image.tostring(img, "RGBA", 0)

        #assign a texture
        texid = glGenTextures(1)
        glBindTexture(GL_TEXTURE_2D, texid)

        if mipmap:
            if not GLU:
                raise NotImplementedError("OGLSprite mipmaps require OpenGL.GLU")
            #build MIPMAP levels. Ths is another slow bit            
            gluBuild2DMipmaps(GL_TEXTURE_2D, GL_RGBA, w2, h2, GL_RGBA, GL_UNSIGNED_BYTE, rgba)
            glTexParameterf(GL_TEXTURE_2D, GL_TEXTURE_WRAP_S, GL_REPEAT)
            glTexParameterf(GL_TEXTURE_2D, GL_TEXTURE_WRAP_T, GL_REPEAT)
        else:
            glTexImage2D(GL_TEXTURE_2D, 0, GL_RGBA, w2, h2, 0, GL_RGBA, GL_UNSIGNED_BYTE, rgba)

        if interpolate:
            smoothing = GL_LINEAR
            glEnable(GL_LINE_SMOOTH)
            glEnable(GL_POLYGON_SMOOTH)
        else:
            smoothing = GL_NEAREST
            glDisable(GL_LINE_SMOOTH)
            glDisable(GL_POLYGON_SMOOTH)
        glTexParameterf(GL_TEXTURE_2D, GL_TEXTURE_MAG_FILTER, smoothing)
        glTexParameterf(GL_TEXTURE_2D, GL_TEXTURE_MIN_FILTER, smoothing)
        #glTexParameterf(GL_TEXTURE_2D, GL_TEXTURE_MAG_FILTER, GL_LINEAR)
        #glTexParameterf(GL_TEXTURE_2D, GL_TEXTURE_MIN_FILTER, GL_LINEAR)

        self.mipmap = mipmap
        self.srcsize = w, h
        self.texsize = w2, h2
        self.coords = float(w)/w2, float(h)/h2
        self.texid = texid
    def __del__(self):
        """
        """
        try:
            glDeleteTextures([self.texid])
        except NameError:
            pyepl.exceptions.eplWarn("glDeleteTextures function not present.")
    def update(self, surf):
        """update(self, surf) -> None
        """
        if self.mipmap:
            raise TypeError("Cannot update a mipmap enabled OGLSprite")

        w, h = surf.get_width(), surf.get_height()
        if getGLVersion() >= 2.1:
            w2 = w
            h2 = h
            img = surf
        else:
            # must use power of 2
            w2, h2 = 1, 1
            while w2 < w: w2 <<= 1
            while h2 < h: h2 <<= 1
            img = pygame.Surface((w2, h2), SRCALPHA, 32)
            img.blit(surf, (0,0))

        rgba = pygame.image.tostring(img, "RGBA", 0)

        glBindTexture(GL_TEXTURE_2D, self.texid)
        if 'glTexSubImage2D' in dir() and w2 <= self.texsize[0] and h2 <= self.texsize[1]:

            # untested; i suspect it doesn't work
            w2, h2 = self.texsize
            glTexSubImage2D(GL_TEXTURE_RECTANGLE_EXT, 0,
                0, 0, w2, h2, GL_RGBA, GL_UNSIGNED_BYTE, rgba);
            if (w, h) != self.srcsize:
                self.coords = float(w)/w2, float(h)/h2
        else:
            glTexImage2D(GL_TEXTURE_2D, 0, GL_RGBA,
                w2, h2, 0, GL_RGBA, GL_UNSIGNED_BYTE, rgba)
            self.coords = float(w)/w2, float(h)/h2
            self.texsize = w2, h2

        self.srcsize = w, h

        #print "TEX", self.srcsize, self.texsize, self.coords
    def blit_at(self, *rects):
        """blit_at(self, *rects) -> self

        Draw the texture at the supplied position(s).  If a tuple and width and
        height are not specified, the original size is used (just like you'd
        expect).  Returns self so ogs.enter().blit().exit() works"""

        for rect in rects:
            x0, y0 = rect[0:2]
            try:
                x1, y1 = x0 + rect[2], y0 + rect[3]
            except IndexError:
                x1, y1 = x0 + self.srcsize[0] - 1, y0 + self.srcsize[1] - 1

            glBindTexture(GL_TEXTURE_2D, self.texid)
            glBegin(GL_TRIANGLE_STRIP)
            glTexCoord2f(0, 0); glVertex2f(x0, y0)
            glTexCoord2f(self.coords[0], 0); glVertex2f(x1, y0)
            glTexCoord2f(0, self.coords[1]); glVertex2f(x0, y1)
            glTexCoord2f(self.coords[0], self.coords[1]); glVertex2f(x1, y1)
            glEnd()

        return self
    def enter(self, xres, yres):
        """enter(self) -> self
        
        Set up OpenGL for drawing textures; do this once per batch of
        textures.  Returns self so ogs.enter().blit().exit() works"""

        glViewport(0, 0, xres, yres)
        glPushAttrib(GL_ENABLE_BIT)     # save old enables
        glDisable(GL_DEPTH_TEST)
        glDisable(GL_CULL_FACE)
        glColor4f(1,1,1,1)
        glEnable(GL_TEXTURE_2D)

        # XXX: in pre pygame1.5, there is no proper alpha, so this makes
        # the entire texture transparent.  in 1.5 and forward, it works.
        if pygame.version.ver >= '1.4.9':
            glEnable(GL_BLEND)
            glBlendFunc(GL_SRC_ALPHA, GL_ONE_MINUS_SRC_ALPHA)

        #glEnable(GL_ALPHA_TEST)
        #glAlphaFunc(GL_GREATER, 0.5)

        glMatrixMode(GL_PROJECTION)
        glPushMatrix()
        glLoadIdentity()
        glOrtho(0.0, xres, yres, 0.0, 0.0, 1.0)

        glMatrixMode(GL_MODELVIEW)
        glPushMatrix()
        glLoadIdentity()

        #glTexEnvf(GL_TEXTURE_ENV, GL_TEXTURE_ENV_MODE, GL_DECAL)

        return self
    def exit(self):
        """exit(self) -> None

        Return OpenGL to previous settings; do this once per batch."""
        glMatrixMode(GL_PROJECTION)
        glPopMatrix()
        glMatrixMode(GL_MODELVIEW)
        glPopMatrix()
        glPopAttrib()
    def get_width(self):
        """get_width(self) -> int"""
        return self.srcsize[0]
    def get_height(self):
        """get_height(self) -> int"""
        return self.srcsize[1]

class LowImage:
    """
    Low level representation of an image.
    """
    def __init__(self, *args, **kwargs):
        """
        Create LowImage.
        """
        if len(args) == 2:
            self.surf = pygame.Surface(args)
        elif len(args) == 1:
            param = args[0]
            if isinstance(param, pygame.Surface):
                self.surf = param
            elif isinstance(param, str):
                self.surf = pygame.image.load(param)
            else:
                raise ValueError, "Invalid type for LowImage constructor argument."
        else:
            raise ValueError, "Invalid number of arguments for LowImage constructor."
        if kwargs.has_key('interpolate'):
            interpolate = kwargs['interpolate']
        else:
            interpolate = True
        self.gl_texture = OGLSprite(self.surf, interpolate=interpolate)
        self.gl_texture_dirty = False

	# this next line supposedly breaks on OSX, set to none if this is the case
        self.surfarray = pygame.surfarray.pixels3d(self.surf)
        # fix for the mac (breaks other stuff)
        #self.surfarray = None
    def dataString(self):
        """
        Return an RGBA string of the image data.
        """
        return pygame.image.tostring(self.surf, "RGBA")
    def cleanGLTexture(self):
        """
        """
        if self.gl_texture_dirty:
            self.gl_texture.update(self.surf)
            self.gl_texture_dirty = False
    def show(self, x, y):
        """
        """
        self.cleanGLTexture()
        self.gl_texture.enter(*pygame.display.get_surface().get_size())
        self.gl_texture.blit_at((x, y))
        self.gl_texture.exit()
    def fill(self, r, g, b, a):
        """
        """
        self.surf = self.surf.convert_alpha()
        self.surf.fill((int(r), int(g), int(b), int(a)))
        self.gl_texture_dirty = True
    def __getitem__(self, index):
        """
        Two dimensional indexing and slicing.
        """
        return pygame.surfarray.make_surface(self.surfarray[index])
    def __setitem__(self, index, value):
        """
        Index and slice assignment.
        """
        if isinstance(value, LowImage):
            self.surfarray[index] = value.surfarray
        else:
            self.surfarray[index] = value
        self.gl_texture_dirty = True
    def __mul__(self, x):
        """
        Color multiplication.
        """
        if isinstance(x, LowImage):
            return pygame.surfarray.make_surface(self.surfarray * x.surfarray)
        else:
            return pygame.surfarray.make_surface(self.surfarray * x)
    def __div__(self, x):
        """
        Color division.
        """
        if isinstance(x, LowImage):
            return pygame.surfarray.make_surface(self.surfarray / x.surfarray)
        else:
            return pygame.surfarray.make_surface(self.surfarray / x)
    def __add__(self, x):
        """
        Color addition.
        """
        if isinstance(x, LowImage):
            return pygame.surfarray.make_surface(self.surfarray + x.surfarray)
        else:
            return pygame.surfarray.make_surface(self.surfarray + x)
    def __sub__(self, x):
        """
        Color subtraction.
        """
        if isinstance(x, LowImage):
            return pygame.surfarray.make_surface(self.surfarray - x.surfarray)
        else:
            return pygame.surfarray.make_surface(self.surfarray - x)
    def __neg__(self):
        """
        Color inversion.
        """
        return pygame.surfarray.make_surface(-self.surfarray)
    def scale(self, x, y):
        """
        Get scaled image.
        """
        return LowImage(pygame.transform.scale(self.surf, (x, y)))
    def getSize(self):
        """
        Return an x, y tuple for image dimensions.
        """
        return self.surf.get_size()

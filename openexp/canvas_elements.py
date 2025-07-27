from openexp import backend


class ElementFactory:

    def __init__(self, *args, **kwargs):
        self._args = args
        self._kwargs = kwargs

    def construct(self, canvas):
        bck = backend.backend_guess(canvas.experiment, 'canvas')
        mod = __import__(f'openexp._canvas._{self.mod}.{bck}',
                         fromlist=['dummy'])
        cls = getattr(mod, bck.capitalize())
        return cls(canvas, *self._args, **self._kwargs)


def Line(sx, sy, ex, ey, **properties):
    class LineFactory(ElementFactory):
        mod = 'line'
    return LineFactory(sx, sy, ex, ey, **properties)


def Rect(x, y, w, h, **properties):
    class RectFactory(ElementFactory):
        mod = 'rect'
    return RectFactory(x, y, w, h, **properties)


def Ellipse(x, y, w, h, **properties):
    class EllipseFactory(ElementFactory):
        mod = 'ellipse'
    return EllipseFactory(x, y, w, h, **properties)


def Circle(x, y, r, **properties):
    class CircleFactory(ElementFactory):
        mod = 'circle'
    return CircleFactory(x, y, r, **properties)


def FixDot(x=None, y=None, style='default', **properties):
    class FixDotFactory(ElementFactory):
        mod = 'fixdot'
    return FixDotFactory(x, y, style, **properties)


def Polygon(vertices, **properties):
    class PolygonFactory(ElementFactory):
        mod = 'polygon'
    return PolygonFactory(vertices, **properties)


def Image(fname, center=True, x=None, y=None, scale=None, rotation=None,
          **properties):
    class ImageFactory(ElementFactory):
        mod = 'image'
    return ImageFactory(fname, center, x, y, scale, rotation, **properties)


def Gabor(x=0, y=0, orient=0, freq=.05, env='gaussian', size=96, stdev=12,
          phase=0, col1='white', col2='black', bgmode='avg'):
    class GaborFactory(ElementFactory):
        mod = 'gabor'
    return GaborFactory(x, y, orient, freq, env, size, stdev, phase, col1, col2,
                        bgmode)


def NoisePatch(x=0, y=0, env="gaussian", size=96, stdev=12, col1="white",
               col2="black", bgmode="avg"):
    class NoisePatchFactory(ElementFactory):
        mod = 'noise_patch'
    return NoisePatchFactory(x, y, env, size, stdev, col1, col2, bgmode)


def RichText(text, center=True, x=None, y=None, max_width=None, **properties):
    class RichTextFactory(ElementFactory):
        mod = 'richtext'
    return RichTextFactory(text, center, x, y, max_width, **properties)


def Arrow(sx, sy, ex, ey, body_length=0.8, body_width=.5, head_width=30,
          **properties):
    class ArrowFactory(ElementFactory):
        mod = 'arrow'
    return ArrowFactory(sx, sy, ex, ey, body_length, body_width, head_width,
                        **properties)


Text = RichText

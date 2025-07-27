class WidgetFactory:
    
    def __init__(self, *args, **kwargs):
        self._args = args
        self._kwargs = kwargs

    def construct(self, form):
        mod = __import__(f'libopensesame.widgets._{self.mod}',
                         fromlist=['dummy'])
        cls = getattr(mod, self.class_name)
        return cls(form, *self._args, **self._kwargs)


def Label(text='label', frame=False, center=True):
    class LabelFactory(WidgetFactory):
        mod = 'label'
        class_name = 'Label'
    return LabelFactory(text, frame, center) 


def Button(text='button', frame=True, center=True, var=None):
    class ButtonFactory(WidgetFactory):
        mod = 'button'
        class_name = 'Button'
    return ButtonFactory(text, frame, center, var)


def ImageButton(path=None, adjust=True, frame=False, image_id=None, var=None):
    class ImageButtonFactory(WidgetFactory):
        mod = 'image_button'
        class_name = 'ImageButton'
    return ImageButtonFactory(path, adjust, frame, image_id, var)


# The corresponding class is actually called Image, rather than ImageWidget. The
# factory should be called ImageWidget though, to avoid clashing with an existing
# image class
def ImageWidget(path=None, adjust=True, frame=False):
    class ImageWidgetFactory(WidgetFactory):
        mod = 'image'
        class_name = 'ImageWidget'
    return ImageWidgetFactory(path, adjust, frame)


def RatingScale(nodes=5, click_accepts=False, orientation='horizontal',
                var=None, default=None):
    class RatingScaleFactory(WidgetFactory):
        mod = 'rating_scale'
        class_name = 'RatingScale'
    return RatingScaleFactory(nodes, click_accepts, orientation, var, default)


def TextInput(text='', frame=True, center=False, stub='Type here ...',
              return_accepts=False, var=None, key_filter=None):
    class TextInputFactory(WidgetFactory):
        mod = 'text_input'
        class_name = 'TextInput'
    return TextInputFactory(text, frame, center, stub, return_accepts, var,
                            key_filter)


def Checkbox(text='checkbox', frame=False, group=None, checked=False,
             click_accepts=False, var=None):
    class CheckboxFactory(WidgetFactory):
        mod = 'checkbox'
        class_name = 'Checkbox'
    return CheckboxFactory(text, frame, group, checked, click_accepts, var)

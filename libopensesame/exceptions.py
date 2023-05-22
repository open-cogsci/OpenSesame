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
import re
import sys
from libopensesame.oslogging import oslogger
from libopensesame.item_stack import item_stack_singleton
from libopensesame.py3compat import *
import traceback
import time
import markdown


class AbortCoroutines(Exception):
    r"""A messaging Exception to indicate that coroutines should be aborted.
    That is, if a task raises an AbortCoroutines, then the currently running
    coroutines should abort.
    """
    
    pass


class OSException(Exception):
    """An OSException is raised when an error occurs that is not covered by
    any of the other Exception classes.
    """

    def __init__(self, msg):
        """Constructor.

        Parameters
        ----------
        msg : str, unicode
            An error message.
        """
        super().__init__(msg)
        self._msg = msg
        try:
            self.item, self.phase = item_stack_singleton[-1]
        except IndexError:
            # This may happen when the item stack is empty
            self.item = self.phase = 'unknown'
        self._read_more = f'''
<div id="more-information"
style="display:none;">{markdown.markdown(self.__doc__)}</div>

<a id="read-more" class="button"
onclick='document.getElementById("more-information").style.display = "block";document.getElementById("read-more").style.display = "none"'>
Learn more about this error</a>
'''

    def __str__(self):
        return f'''
{self.title()}\n\n{self._msg}

This error occurred in the {self.phase} phase of item {self.item}.
'''

    def markdown(self):
        return f'''
# {self.title()}

{self._msg}

This error occurred in the __{self.phase}__ phase of item 
<u><a href="opensesame://item.{self.item}.{self.phase}">
{self.item}</a></u>.

{self._read_more}
'''
    
    def title(self):
        return f'Error: {self.__class__.__name__}'


class BackendNotSupported(OSException):
    """This exception is raised when functionality is not supported backend.
    """
    pass

    
class InvalidKeyName(OSException):
    """An `InvalidKeyName` is raised when the name of a key has been
    incorrectly specified.
    """
    def __init__(self, key):
        super().__init__(f'Invalid key name: {key}')
        
        
class InvalidValue(OSException):
    """An `InvalidValue` is raised when an invalid value has been assigned to a
    variable. This can occur in many situations and generally indicates a
    mistake in the experiment. For example, you will get an `InvalidValue` if
    you specify a negative `sketchpad` duration.
    """
    pass


class InvalidColor(OSException):
    """An `InvalidColor` is raised when you have specified a color with an
    incorrect. This generally indicates a mistake in the experiment, such as a
    typo. For example, you will get an `InvalidColor` if you specify the color
    'bleu' (as opposed to 'blue'). For a list of valid color specifications,
    please visit see the documentation site.
    """
    def __init__(self, color):
        super().__init__(f'Invalid color specification: {color}')
        
        
class InvalidSketchpadElementScript(OSException):
    """An `InvalidSketchpadElementScript` is raised when there is a mistake in
    the script that defines a sketchpad element. This can happen when you
    manually modify a `sketchpad` script.
    """
    pass


class InvalidFormScript(OSException):
    """An `InvalidFormScript` is raised when there is a mistake in a form
    script. This can happen when you make a mistake while manually buidling a
    form using the `form_base` item, or while modifying the script of other
    form items.
    """
    pass


class InvalidOpenSesameScript(OSException):
    """An `InvalidOpenSesameScript` is raised when there is an error in the 
    OpenSesame script that defines the experiment and the items. This can 
    happen when you make a mistake while modifying the experiment script.
    """
    pass


class InvalidFormGeometry(OSException):
    """An `InvalidFormGeometry` is raised when a form has an impossible 
    geometry. This can happen for different reasons. For example, you will get
    an `InvalidFormGeometry` when a form is too small to fit
    all of its widgets.
    """
    pass


class UnsupportedImageFormat(OSException):
    """An `UnsupportedImageFormat` is raised when an image file does not have
    a format that is supported by OpenSesame. It can also occur when a file
    is not an image file at all. To solve this issue, make sure that the
    indicated file is indeed an image, and if necessary convert it to a
    standard format, such as `.png` or `.jpg`.
    """
    def __init__(self, path):
        super().__init__(f'{path} is not a supported image file')
        
        
class ImageDoesNotExist(OSException):
    """An `ImageDoesNotExist` is raised when you have specified an image file
    that does not exist. This commonly reflects a mistake in the experiment,
    such as a typo in a file name.
    """
    def __init__(self, path):
        super().__init__(f'Cannot find image file {path}')
        

class UnsupportedSoundFileFormat(OSException):
    """An `UnsupportedSoundFileFormat` is raised when a sound file does not
    have a format that is supported by OpenSesame. It can also occur when a
    file is not a sound image file at all. To solve this issue, make sure that
    the indicated file is indeed a sound file, and if necessary convert it to a
    standard format, such as `.wav` or `.mp3`.
    """
    def __init__(self, path):
        super().__init__(f'{path} is not a supported sound file')
        
        
class SoundFileDoesNotExist(OSException):
    """A `SoundFileDoesNotExist` is raised when you have specified a sound file
    that does not exist. This commonly reflects a mistake in the experiment,
    such as a typo in a file name.
    """
    def __init__(self, path):
        super().__init__(f'Cannot find sound file {path}')
        
        
class LoopSourceFileDoesNotExist(OSException):
    """A `LoopSourceFileDoesNotExist` is raised when you have specified a
    non-existent source file for a loop item. This commonly reflects  mistake
    in the experiment, such as a typo in a file name.
    """
    def __init__(self, path):
        super().__init__(f'Cannot find loop source file {path}')
        

class UnsupportedLoopSourceFile(OSException):
    """An `UnsupportedLoopSourceFile` is raised when you have specified a 
    source file for a loop item that is not a `.csv` or `.xlsx` file.
    """
    def __init__(self, path):
        super().__init__(f'{path} is not a supported loop source file')


class UserAborted(OSException):
    """This exception is raised when a user aborts an experiment."""
    def __str__(self):
        return self._msg
        

class UserKilled(UserAborted):
    """This exception is raised when a user kills an experiment."""
    pass

        
class MissingDependency(OSException):
    """A `MissingDependency` is raised when some functionality requires a
    package that is not available.
    """
    pass


class ItemDoesNotExist(OSException):
    """An `ItemDoesNotExist` is raised when the experiment refers to an item
    that does not exist. This can occur for different reasons.
    """
    def __init__(self, item_name):
        super().__init__(f'Item {item_name} does not exist')
        
        
class VariableDoesNotExist(OSException):
    """A `VariableDoesNotExist` is raised when the experiment refers to a
    variable that does not, or not yet, exist. This commonly reflects a mistake
    in the experiment, such as a typo in the name of a variable, or referring
    to a variable before it has been created. Note that variable names are case
    sensitive.
    """
    def __init__(self, var_name):
        super().__init__(f'Variable {var_name} does not exist')
        
        
class DeviceError(OSException):
    """A `DeviceError` is raised when an error occurs while connecting to, or
    interacting with, an external device. This can occur for different reasons.
    """
    pass


class PythonError(OSException):
    """A `PythonError` is raised when an error occurs during execution of 
    Python code, typically in an `inline_script` item.
    """
    def __init__(self, msg):
        super().__init__(msg)
        tb_lines = traceback.format_exc().splitlines()
        # Get the line number of most recent stack from the traceback. If no
        # traceback exists, fall back to line number 1
        tb = sys.exc_info()[2]
        if tb is None:
            self.line_nr = 1
        else:
            while tb.tb_next is not None:
                tb = tb.tb_next
            self.line_nr = tb.tb_lineno
        self._traceback = self.clean_traceback(tb_lines)

    def clean_traceback(self, tb_lines):
        # The __ignore_traceback__ comment serves as a marker to indicate which
        # parts of the error message should be hidden from the user because
        # they relate to the insides of OpenSesame, rather than to the user
        # error.
        for line_nr, tb_line in enumerate(tb_lines):
            if '# __ignore_traceback__' in tb_line:
                tb_lines = tb_lines[:1] + tb_lines[line_nr + 1:]
                break
        return '\n'.join(tb_lines).replace('<string>',
                                           f'<{self.item}.{self.phase}>')
        
    def __str__(self):
        return f'''
{self.title()}

{self._msg}

This error occurred on line {self.line_nr} in the {self.phase} phase of item {self.item}.

{self._traceback}
'''
        
    def markdown(self):
        
        return f'''
# {self.title()}

{self._msg}

This error occurred on __line {self.line_nr}__ in the
__{self.phase}__ phase of item
<u><a href="opensesame://item.{self.item}.{self.phase}.{self.line_nr - 1}">{self.item}</a></u>.

~~~ .traceback
{self._traceback}
~~~

{self._read_more}
'''


class PythonSyntaxError(PythonError):
    """A `PythonSyntaxError` is raised when a Python script, typically in an
    `inline_script` item, is not syntactically correct.
    """
    def __init__(self, msg, line_nr=1):
        super().__init__(msg)
        tb_lines = traceback.format_exc().splitlines()
        self.line_nr = line_nr
        self._traceback = self.clean_traceback(tb_lines)


class InvalidConditionalExpression(PythonSyntaxError):
    """An `InvalidConditionalExpression` is raised when a conditional 
    expresssion, such as a run-if, break-if, or show-if expression, is
    syntactically incorrect. This generally reflects a mistake in the 
    experiment, such as a typo in a conditional expression that renders it
    invalid.
    """
    def markdown(self):
        
        return f'''
# {self.title()}

{self._msg}

This error occurred in the
__{self.phase}__ phase of item
<u><a href="opensesame://item.{self.item}.{self.phase}.{self.line_nr - 1}">{self.item}</a></u>.

~~~ .traceback
{self._traceback}
~~~

{self._read_more}
'''


class ConditionalExpressionError(PythonError):
    """A `ConditionalExpressionError` is raised when an error occurs during the
    evaluation of a conditional expression, such as run-if, break-if, or
    show-if expression.
    """
    def markdown(self):
        
        return f'''
# {self.title()}

{self._msg}

This error occurred in the
__{self.phase}__ phase of item
<u><a href="opensesame://item.{self.item}.{self.phase}.{self.line_nr - 1}">{self.item}</a></u>.

~~~ .traceback
{self._traceback}
~~~

{self._read_more}
'''


class BaseFStringError:


    def __str__(self):
        return f'''
{self.title()}

{self._msg}

This error occurred in the {self.phase} phase of item {self.item}.

{self._traceback}
'''
        
    def markdown(self):
        return f'''
# {self.title()}

{self._msg}

This error occurred in the __{self.phase}__ phase of item
<u><a href="opensesame://item.{self.item}">{self.item}</a></u>.

~~~ .traceback
{self._traceback}
~~~

{self._read_more}
'''


class FStringError(BaseFStringError, PythonError):
    """An `FStringError` is raised when an error occurs during the evaluation
    of an f-string.
    """
    pass


class FStringSyntaxError(BaseFStringError, PythonSyntaxError):
    """An `FStringSyntaxError` is raised when text contains an f-string 
    expression that is not syntactically valid Python.
    """
    pass


class ExperimentProcessDied(OSException):
    """An `ExperimentProcessDied` is raised when the experiment process died.
    This is  generally the result of a bug in one of the underlying libraries 
    that causes Python to crash. This should not happen! If you experinence 
    this error often, please report it on the support forum.
    """
    pass


class UnexpectedError(OSException):
    """An `UnexpectedError` is raised when an error occurred that OpenSesame 
    does not recognize. This can happen when there is a bug in a plugin, one of
    the underlying Python libraries, or in OpenSesame itself. This should not
    happen! If you experinence this error often, please report it on the
    support forum.
    """
    def __init__(self, msg):
        super().__init__(msg)
        self._traceback = traceback.format_exc()
        
    def __str__(self):
        return f'{self.title()}\n\n{self._msg}\n\n{self._traceback}'
        
    def markdown(self):
        return f'# {self.title()}\n\n{self._msg}\n\n' \
               f'~~~ .traceback\n{self._traceback}\n~~~\n\n{self._read_more}'


# For backwards compatibility, we should also define the old Exception classes
osexception = OSException

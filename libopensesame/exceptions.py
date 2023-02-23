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
from libopensesame.oslogging import oslogger
from libopensesame.item_stack import item_stack_singleton
from libopensesame.py3compat import *
import traceback
import time


class AbortCoroutines(Exception):
    r"""A messaging Exception to indicate that coroutines should be aborted.
    That is, if a task raises an AbortCoroutines, then the currently running
    coroutines should abort.
    """
    
    pass


class OSException(Exception):
    """A general Exception class for exceptions that occur within OpenSesame.
    Ideally, only `osexception`s should occur, all other exceptions indicate a
    (usually harmless) bug somewhere.
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

    def __str__(self):
        return f'{self.title()}\n\n{self._msg}' \
               f'\n\nThis error occurred in the {self.phase} phase of item ' \
               f'{self.item}.'

    def markdown(self):
        return f'# {self.title()}\n\n{self._msg}' \
               f'\n\nThis error occurred in the __{self.phase}__ phase of ' \
               f'item __{self.item}__.'
    
    def title(self):
        return f'Error: {self.__class__.__name__}'


class BackendNotSupported(OSException):
    """This exception is raised when functionality is not supported backend.
    """
    pass

    
class InvalidKeyName(OSException):
    """This exception is raised when the name of a key has been incorrectly
    specified.
    """
    def __init__(self, key):
        super().__init__(f'Invalid key name: {key}')
        
        
class InvalidValue(OSException):
    """This exception is raised when a variable has an incorrect value or type.
    """
    pass


class InvalidColor(OSException):
    """This exception is raised when a color has been incorrectly specified.
    """
    def __init__(self, color):
        super().__init__(f'Invalid color specification: {color}')
        
        
class InvalidSketchpadElementScript(OSException):
    """This exception is raised when a sketchpad element has been incorrectly
    defined.
    """
    pass


class InvalidFormScript(OSException):
    """This exception is raised when a form has been incorrectly defined."""
    pass


class InvalidOpenSesameScript(OSException):
    """This exception is raised when there is an error in the OpenSesame script
    that defines the experiment and the items.
    """
    pass


class InvalidConditionalExpression(OSException):
    """This exception is raised when a conditional statement, such as a run-if,
    break-if, or show-if statement, is incorrectly defined.
    """
    pass


class InvalidFormGeormetry(OSException):
    """This exception is raised when a form has an invalid geometry."""
    pass


class UnsupportedImageFormat(OSException):
    """This exception is raised when an image file has an unsupported format.
    """
    def __init__(self, path):
        super().__init__(f'{path} is not a supported image file')
        
        
class ImageDoesNotExist(OSException):
    """This exception is raised when an image file does not exist."""
    def __init__(self, path):
        super().__init__(f'Cannot find image file {path}')
        

class UnsupportedSoundFileFormat(OSException):
    """This exception is raised when a sound file has an unsupported format.
    """
    def __init__(self, path):
        super().__init__(f'{path} is not a supported sound file')
        
        
class SoundFileDoesNotExist(OSException):
    """This exception is raised when an sound file does not exist."""
    def __init__(self, path):
        super().__init__(f'Cannot find sound file {path}')
        
        
class LoopSourceFileDoesNotExist(OSException):
    """This exception is raised when an loop source file does not exist."""
    def __init__(self, path):
        super().__init__(f'Cannot find loop source file {path}')
        

class UnsupportedLoopSourceFile(OSException):
    """This exception is raised when a loop source file has an unsupported
    format.
    """
    def __init__(self, path):
        super().__init__(f'{path} is not a supported loop source file')


class UserAborted(OSException):
    """This exception is raised when a user aborts an experiment."""
    def title(self):
        return 'Aborted'
        
    def __str__(self):
        return 'The experiment was aborted'
        
    def markdown(self):
        return '# Aborted\n\nThe experiment was aborted'
        

class UserKilled(UserAborted):
    """This exception is raised when a user aborts an experiment."""
    def title(self):
        return 'Aborted'
        
    def __str__(self):
        return 'The experiment process was killed'
        
    def markdown(self):
        return '# Aborted\n\nThe experiment process was killed'

        
class MissingDependency(OSException):
    """This exception is raised when some functionality requires a package
    that is not available.
    """
    pass


class ItemDoesNotExist(OSException):
    """This exception is raised when an item that does not exist is referred
    to.
    """
    def __init__(self, item_name):
        super().__init__(f'Item {item_name} does not exist')
        
        
class VariableDoesNotExist(OSException):
    """This exception is raised when a variable that does not exist is referred
    to.
    """
    def __init__(self, var_name):
        super().__init__(f'Variable {var_name} does not exist')
        
        
class DeviceError(OSException):
    """This exception is raised when an error occurs while connecting to, or
    interacting with, an external device.
    """
    pass


class PythonError(OSException):
    """This exception is raised when an error occurs during execution of Python
    code.
    """
    def __init__(self, msg):
        super().__init__(msg)
        tb = traceback.format_exc().splitlines()
        tb = tb[:1] + tb[5:]
        tb = '\n'.join(tb).replace('<string>', f'<{self.item}.{self.phase}>')
        self._traceback = tb
        
    def __str__(self):
        return f'{super()}\n\n{self._traceback}'
        
    def markdown(self):
        return f'{super().markdown()}\n\n' \
               f'~~~ .traceback\n{self._traceback}\n~~~'


class PythonSyntaxError(PythonError):
    """This exception is raised when there is a syntax error in Python code.
    """
    pass


class ConditionalExpressionError(PythonError):
    """This exception is raised when an error occurs during evaluation of a
    conditional expression.
    """
    pass


class ExperimentProcessDied(OSException):
    """This exception is raised when the experiment process died. This is 
    generally the result of a bug in one of the underlying libraries that
    causes Python to crash. This should not happen! If you experinence this
    error often, please report it on the support forum.
    """
    pass

# For backwards compatibility, we should also define the old Exception classes
osexception = OSException

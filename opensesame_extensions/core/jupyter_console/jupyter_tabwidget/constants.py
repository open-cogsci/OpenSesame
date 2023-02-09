# coding=utf-8

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

KERNEL_NAMES = {
    u'python': u'Python',
    u'python2': u'Python',
    u'python3': u'Python',
    u'ir': u'R',
    u'bash': u'Bash'
}
CHANGE_DIR_CMD = {
    u'ir': 'setwd("{path}")',
    u'bash': 'cd "{path}"'
}
LOGGING_LEVEL_CMD = {
    'python': {
        'Debug': 'import logging; logging.basicConfig(level=logging.DEBUG, force=True)',
        'Info': 'import logging; logging.basicConfig(level=logging.INFO, force=True)',
        'Warning': 'import logging; logging.basicConfig(level=logging.WARNING, force=True)',
        'Error': 'import logging; logging.basicConfig(level=logging.ERROR, force=True)',
        'Critical': 'import logging; logging.basicConfig(level=logging.CRITICAL, force=True)'
    }
}
DEFAULT_CHANGE_DIR_CMD = u'%cd "{path}"'
RUN_FILE_CMD = {
    u'ir': 'source("{path}")',
    u'bash': '"{path}"'
}
DEFAULT_RUN_FILE_CMD = u'%run "{path}"'
DEFAULT_RUN_DEBUG_CMD = None
RUN_SYSTEM_CMD = {
    u'ir': 'system("{cmd}")',
    u'bash': '{cmd}'
}
DEFAULT_RUN_SYSTEM_CMD = u'!{cmd}'
TRANSPARENT_KERNELS = [u'python', u'python2', u'python3']
PID_CMD = {
    u'python': u'os.getpid()',
    u'python2': u'os.getpid()',
    u'python3': u'os.getpid()'
}

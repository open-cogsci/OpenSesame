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
from libqtopensesame.runners.base_runner import BaseRunner
from libqtopensesame.runners.inprocess_runner import InprocessRunner
from libqtopensesame.runners.external_runner import ExternalRunner
from libqtopensesame.runners.multiprocess_runner import MultiprocessRunner

# This order has to match the order in the preferences combobox
RUNNER_LIST = 'inprocess', 'multiprocess', 'external'
DEFAULT_RUNNER = 'multiprocess'
# Alias for backwards compatibility
base_runner = BaseRunner
inprocess_runner = InprocessRunner
external_runner = ExternalRunner
multiprocess_runner = MultiprocessRunner

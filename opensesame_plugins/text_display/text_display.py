#-*- coding:utf-8 -*-

"""
This file is part of opensesame.

opensesame is free software: you can redistribute it and/or modify
it under the terms of the GNU General Public License as published by
the Free Software Foundation, either version 3 of the License, or
(at your option) any later version.

opensesame is distributed in the hope that it will be useful,
but WITHOUT ANY WARRANTY; without even the implied warranty of
MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
GNU General Public License for more details.

You should have received a copy of the GNU General Public License
along with opensesame.  If not, see <http://www.gnu.org/licenses/>.
"""

from libopensesame.py3compat import *
from libopensesame.exceptions import osexception
from libopensesame.generic_response import generic_response
from libopensesame.item import item
from libqtopensesame.items.qtautoplugin import qtautoplugin
import openexp.canvas
import os.path

class text_display(item, generic_response):

	pass

class qttext_display(text_display, qtautoplugin):

	"""Automatic GUI class."""

	def __init__(self, name, experiment, script=None):

		text_display.__init__(self, name, experiment, script)
		qtautoplugin.__init__(self, __file__)

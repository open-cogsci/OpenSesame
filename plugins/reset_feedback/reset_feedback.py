#-*- coding:utf-8 -*-

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
from libopensesame.item import item
from libqtopensesame.items.qtautoplugin import qtautoplugin
from qtpy import QtWidgets, QtCore

class reset_feedback(item):

	"""A very simple plug-in to reset feedback variables"""

	description = \
		u'Resets the feedback variables, such as \'avg_rt\' and \'acc\''

	def run(self):

		"""Resets the feedback variables."""

		self.experiment.reset_feedback()

class qtreset_feedback(reset_feedback, qtautoplugin):

	def __init__(self, name, experiment, script=None):

		reset_feedback.__init__(self, name, experiment, script)
		qtautoplugin.__init__(self, __file__)

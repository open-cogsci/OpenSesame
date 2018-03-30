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

from libopensesame.py3compat import *
from openexp import backend


class WidgetFactory(object):

	def __init__(self, *args, **kwargs):

		self._args = args
		self._kwargs = kwargs
		self._instance = None

	def construct(self, form):

		if self._instance is not None:
			return self._instance
		mod = __import__(
			'libopensesame.widgets._%s' % self.mod,
			fromlist=['dummy']
		)
		cls = getattr(mod, self.__class__.__name__)
		self._instance = cls(form, *self._args, **self._kwargs)
		return self._instance


class Label(WidgetFactory): mod = 'label'
class Button(WidgetFactory): mod = 'button'
class ImageButton(WidgetFactory): mod = 'image_button'
class ImageWidget(WidgetFactory): mod = 'image'
class RatingScale(WidgetFactory): mod = 'rating_scale'
class TextInput(WidgetFactory): mod = 'text_input'
class Checkbox(WidgetFactory): mod = 'checkbox'

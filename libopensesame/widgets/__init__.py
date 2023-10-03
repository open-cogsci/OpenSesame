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

from libopensesame.widgets._button import Button
from libopensesame.widgets._checkbox import Checkbox
from libopensesame.widgets._form import Form
from libopensesame.widgets._image import ImageWidget
from libopensesame.widgets._image_button import ImageButton
from libopensesame.widgets._label import Label
from libopensesame.widgets._rating_scale import RatingScale
from libopensesame.widgets._text_input import TextInput
from libopensesame.widgets._widget import Widget

# alias for backwards compatibility
button = Button
checkbox = Checkbox
form = Form
image = ImageWidget
image_button = ImageButton
label = Label
rating_scale = RatingScale
text_input = TextInput
widget = Widget

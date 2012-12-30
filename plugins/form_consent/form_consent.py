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

from libopensesame import item, exceptions, generic_response, widgets, plugins
from libqtopensesame import qtplugin
from openexp.canvas import canvas
import openexp.keyboard
import os.path
from PyQt4 import QtGui, QtCore

form_base = plugins.import_plugin('form_base')

default_script = """
__form_text__
You are about to participate in an experiment.

This experiment poses no known risks to your health and your name will not be associated with the findings.

Upon completion of your participation in this study you will be provided with a brief explanation of the question this study addresses.

If you have any questions not addressed by this consent form, please do not hesitate to ask.

You can stop at any time during experiment if you feel uncomfortable.
__end__
set form_title '<span size=24>Consent form</span>'
set checkbox_text 'I have read and understood the information shown above'
set accept_text 'Participate!'
set decline_text 'Do not participate'
set decline_message 'You need to accept the consent form to participate!'
set rows 1;4;1;1
widget 0 0 2 1 label text=[form_title]
widget 0 1 2 1 label text=[form_text] center=no
widget 0 2 2 1 checkbox text=[checkbox_text] var=checkbox_status
widget 0 3 1 1 button text=[accept_text] var=accept_status
widget 1 3 1 1 button text=[decline_text]
"""

class form_consent(form_base.form_base):

	def __init__(self, name, experiment, string=None):

		"""
		Constructor

		Arguments:
		name -- the name of the item
		experiment -- the experiment instance

		Keyword arguments:
		string -- a definition string
		"""

		if string == None:
			string = default_script
		super(form_consent, self).__init__(name, experiment, string, item_type= \
			'form_consent', description='A simple consent form')

	def from_string(self, script):

		"""
		Re-generate the form from a definition script

		Arguments:
		script -- the definition script
		"""

		self._widgets = []
		super(form_consent, self).from_string(script)

	def run(self):

		"""Execute the consent form"""

		while True:
			# In this case we cannot call super(form_consent, self), because
			# modules may have been reloaded. The exact nature of the bug is
			# unclear, but passing the __class__ property resolves it. See also
			# <http://thingspython.wordpress.com/2010/09/27/another-super-wrinkle-raising-typeerror/>

			super(self.__class__, self).run()
			if self.get('checkbox_status') == self.get('checkbox_text') and \
				self.get('accept_status') == 'yes':
				break
			c = canvas(self.experiment)
			c.text(self.get('decline_message'))
			c.show()
			self.sleep(5000)

class qtform_consent(form_consent, qtplugin.qtplugin):

	"""GUI controls"""

	def __init__(self, name, experiment, string=None):

		"""
		Constructor

		Arguments:
		name -- the name of the item
		experiment -- the experiment instance

		Keyword arguments:
		string -- a definition string
		"""

		form_consent.__init__(self, name, experiment, string)
		qtplugin.qtplugin.__init__(self, __file__)

	def init_edit_widget(self):

		"""Initialize the controls"""

		self.lock = True
		qtplugin.qtplugin.init_edit_widget(self, False)
		self.add_line_edit_control('form_title', 'Form title', tooltip= \
			'Form title')
		self.add_line_edit_control('checkbox_text', 'Checkbox text', \
			tooltip='Checbox text')
		self.add_line_edit_control('accept_text', 'Accept button text', \
			tooltip='Accept button text')
		self.add_line_edit_control('decline_text', 'Decline button text', \
			tooltip='Decline button text')
		self.add_line_edit_control('decline_message', 'Message on decline', \
			tooltip='Shown when the participant does not accept the consent form')
		self.add_editor_control('form_text', 'Consent form text', \
			tooltip='Consent form text')
		self.lock = False

	def apply_edit_changes(self):

		"""Apply the controls"""

		if not qtplugin.qtplugin.apply_edit_changes(self, False) or self.lock:
			return False
		return True

	def edit_widget(self):

		"""Update the controls"""

		self.lock = True
		qtplugin.qtplugin.edit_widget(self)
		self.lock = False
		return self._edit_widget


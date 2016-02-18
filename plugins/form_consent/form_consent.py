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
from libopensesame import plugins
from libqtopensesame.items.qtautoplugin import qtautoplugin
from openexp.canvas import canvas
form_base = plugins.import_plugin(u'form_base')

default_script = u"""
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

	initial_view = u'controls'

	def __init__(self, name, experiment, string=None):

		"""
		Constructor.

		Arguments:
		name		--	The name of the item.
		experiment	--	The experiment instance.

		Keyword arguments:
		string		--	A definition string. (default=None)
		"""

		if string is None or string.strip() == u'':
			string = default_script
		# Due to dynamic loading, we need to implement this super() hack. See
		# <http://thingspython.wordpress.com/2010/09/27/another-super-wrinkle-raising-typeerror/>
		self.super_form_consent = super(form_consent, self)
		self.super_form_consent.__init__(name, experiment, string, item_type= \
			u'form_consent', description=u'A simple consent form')

	def run(self):

		"""Executes the consent form."""

		while True:
			# In this case we cannot call super(form_consent, self), because
			# modules may have been reloaded. The exact nature of the bug is
			# unclear, but passing the __class__ property resolves it. See also
			# <http://thingspython.wordpress.com/2010/09/27/another-super-wrinkle-raising-typeerror/>
			self.super_form_consent.run()
			if self.var.get(u'checkbox_status') == self.var.get(u'checkbox_text') and \
				self.var.get(u'accept_status') == u'yes':
				break
			c = canvas(self.experiment)
			c.text(self.var.get(u'decline_message'))
			c.show()
			self.sleep(5000)

class qtform_consent(form_consent, qtautoplugin):

	def __init__(self, name, experiment, script=None):

		form_consent.__init__(self, name, experiment, script)
		qtautoplugin.__init__(self, __file__)

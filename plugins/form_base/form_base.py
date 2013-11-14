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

from libopensesame.exceptions import osexception
from libopensesame import item, widgets
from libqtopensesame.items.qtautoplugin import qtautoplugin
from libqtopensesame.misc import _
import openexp.canvas
import openexp.keyboard
import os.path
from PyQt4 import QtGui, QtCore

class form_base(item.item):

	"""A generic form plug-in"""
	
	def __init__(self, name, experiment, script=None, item_type=u'form_base', \
		description=u'A generic form plug-in'):

		"""
		Constructor

		Arguments:
		name		--	The item name.
		experiment	--	The experiment object.

		Keyword arguments:
		script		--	A definition script. (default=None)
		"""

		self.item_type = item_type
		self.description = description
		self.cols = u'2;2'
		self.rows = u'2;2'
		self.spacing = 10
		self.focus_widget = None
		self.theme = u'gray'
		self.only_render = u'no'
		self.margins = u'50;50;50;50'
		self._widgets = []

		item.item.__init__(self, name, experiment, script)

	def parse_line(self, line):

		"""
		Allows for arbitrary line parsing, for item-specific requirements.

		Arguments:
		line	--	A single definition line.
		"""

		l = self.split(line.strip())
		if len(l) < 6 or l[0] != u'widget':
			return

		# Verify that the position variables are integers
		try:
			col = int(l[1])
			row = int(l[2])
			colspan = int(l[3])
			rowspan = int(l[4])
		except:
			raise osexception( \
				_(u'Widget column and row should be numeric'))

		# Parse the widget into a dictionary and store it in the list of
		# widgets
		w = self.parse_keywords(line)
		w[u'type'] = l[5]
		w[u'col'] = col
		w[u'row'] = row
		w[u'colspan'] = colspan
		w[u'rowspan'] = rowspan
		self._widgets.append(w)

	def to_string(self):

		"""
		Parse the widgets back into a definition string

		Returns:
		A definition string
		"""

		s = item.item.to_string(self, self.item_type)
		for w in self._widgets:
			w = w.copy()
			_type = w[u'type']
			col = w[u'col']
			row = w[u'row']
			colspan = w[u'colspan']
			rowspan = w[u'rowspan']
			del w[u'type']
			del w[u'col']
			del w[u'row']
			del w[u'colspan']
			del w[u'rowspan']
			s += u'\twidget %s %s %s %s %s' % (col, row, colspan, rowspan, \
				_type)
			for keyword, value in w.items():
				s += ' %s="%s"' % (keyword, value)
			s += u'\n'
		s += u'\n'
		return s

	def run(self):

		"""
		Run the item

		Returns:
		True on success, False on failure
		"""

		self.set_item_onset()
		if self.get(u'only_render') == u'yes':
			self._form.render()
		else:
			self._form._exec(focus_widget=self.focus_widget)
		return True

	def prepare(self):

		"""Prepare for the run phase"""

		item.item.prepare(self)

		# Prepare the form
		try:
			cols = [float(i) for i in unicode(self.cols).split(';')]
			rows = [float(i) for i in unicode(self.rows).split(';')]
			margins = [float(i) for i in unicode(self.margins).split(';')]
		except:
			raise osexception( \
				_(u'cols, rows, and margins should be numeric values separated by a semi-colon'))
		self._form = widgets.form(self.experiment, cols=cols, rows=rows, \
			margins=margins, spacing=self.spacing, theme=self.theme, item=self)

		# Prepare the widgets
		for _w in self._widgets:

			# Evaluate all keyword arguments
			w = {}
			for var, val in _w.iteritems():
				w[var] = self.eval_text(val)

			_type = w[u'type']
			col = w[u'col']
			row = w[u'row']
			colspan = w[u'colspan']
			rowspan = w[u'rowspan']
			del w[u'type']
			del w[u'col']
			del w[u'row']
			del w[u'colspan']
			del w[u'rowspan']

			# Translate paths into full file names
			if u'path' in w:
				w[u'path'] = self.experiment.get_file(w[u'path'])

			# Process focus keyword
			focus = False
			if u'focus' in w:
				if w[u'focus'] == u'yes':
					focus = True
				del w[u'focus']

			# Create the widget and add it to the form
			try:
				_w = getattr(widgets, _type)(self._form, **w)
			except Exception as e:
				raise osexception( \
					u'Failed to create widget "%s": %s' % (_type, e))
			self._form.set_widget(_w, (col, row), colspan=colspan, \
					rowspan=rowspan)

			# Add as focus widget
			if focus:
				self.focus_widget = _w
		return True

class qtform_base(form_base, qtautoplugin):

	def __init__(self, name, experiment, script=None):

		form_base.__init__(self, name, experiment, script)
		qtautoplugin.__init__(self, __file__)

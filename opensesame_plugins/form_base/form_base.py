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
from libopensesame.exceptions import osexception
from libopensesame import item, widgets
from libqtopensesame.items.qtautoplugin import qtautoplugin
try:
	from libqtopensesame.misc.translate import translation_context
	_ = translation_context(u'form_base', category=u'plugin')
except ImportError:
	pass

class form_base(item.item):

	"""A generic form plug-in"""

	initial_view = u'script'

	def __init__(self, name, experiment, script=None, item_type=u'form_base',
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
		item.item.__init__(self, name, experiment, script)
		self.var.description = description

	def reset(self):

		"""
		desc:
			Resets plug-in to initial values.
		"""

		self.var.cols = u'2;2'
		self.var.rows = u'2;2'
		self.var.spacing = 10
		self.var._theme = u'gray'
		self.var.only_render = u'no'
		self.var.timeout = u'infinite'
		self.var.margins = u'50;50;50;50'
		self._widgets = []
		self._variables = []

	def set_validator(self):

		"""
		desc:
			See qtitem.
		"""

		self.validator = form_base

	def parse_line(self, line):

		"""
		Allows for arbitrary line parsing, for item-specific requirements.

		Arguments:
		line	--	A single definition line.
		"""

		cmd, arglist, kwdict = self.syntax.parse_cmd(line)
		if cmd != u'widget':
			return
		if len(arglist) != 5:
			raise osexception(_(u'Invalid widget specification: %s' % line))
		self._widgets.append((arglist, kwdict))
		if u'var' in kwdict:
			self._variables.append(kwdict[u'var'])

	def to_string(self):

		"""
		Parse the widgets back into a definition string

		Returns:
		A definition string
		"""

		s = item.item.to_string(self, self.item_type)
		for arglist, kwdict in self._widgets:
			s += u'\t%s\n' % self.syntax.create_cmd(u'widget', arglist, kwdict)
		s += u'\n'
		return s

	def run(self):

		"""Runs the item."""

		self.set_item_onset()
		if self.var.only_render == u'yes':
			self._form.render()
		else:
			self._form._exec(focus_widget=self.focus_widget)

	def prepare(self):

		"""Prepares the item."""

		item.item.prepare(self)

		# Prepare the form
		try:
			cols = [float(i) for i in str(self.var.cols).split(u';')]
			rows = [float(i) for i in str(self.var.rows).split(u';')]
			margins = [float(i) for i in str(self.var.margins).split(u';')]
		except:
			raise osexception(
				_(u'cols, rows, and margins should be numeric values separated by a semi-colon'))
		if self.var.timeout == u'infinite':
			timeout = None
		else:
			timeout = self.var.timeout
		self._form = widgets.form(self.experiment, cols=cols, rows=rows,
			margins=margins, spacing=self.var.spacing, theme=self.var._theme,
			item=self, timeout=timeout, clicks=self.var.form_clicks==u'yes')

		self.focus_widget = None
		for arglist, orig_kwdict in self._widgets:
			kwdict = orig_kwdict.copy()
			# Evaluate all values
			arglist = [self.syntax.eval_text(arg) for arg in arglist]
			for key, val in kwdict.items():
				kwdict[key] = self.syntax.eval_text(val, var=self.var)
			# Translate paths into full file names
			if u'path' in kwdict:
				kwdict[u'path'] = self.experiment.pool[kwdict[u'path']]
			# Process focus keyword
			focus = False
			if u'focus' in kwdict:
				if kwdict[u'focus'] == u'yes':
					focus = True
				del kwdict[u'focus']
			# Parse arguments
			_type = arglist[4]
			try:
				col = int(arglist[0])
				row = int(arglist[1])
				colspan = int(arglist[2])
				rowspan = int(arglist[3])
			except:
				raise osexception(
					_(u'In a form widget col, row, colspan, and rowspan should be integer'))
			# Create the widget and add it to the form
			try:
				_w = getattr(widgets, _type)(self._form, **kwdict)
			except Exception as e:
				raise osexception(
					u'Failed to create widget "%s": %s' % (_type, e))
			self._form.set_widget(_w, (col, row), colspan=colspan,
				rowspan=rowspan)
			# Add as focus widget
			if focus:
				if self.focus_widget is not None:
					raise osexception(
						_(u'You can only specify one focus widget'))
				self.focus_widget = _w

	def var_info(self):

		"""
		desc:
			Add response variables to var info list.

		returns:
			desc:	A list of (var_name, description) tuples.
			type:	list
		"""

		l = item.item.var_info(self)
		for var in self._variables:
			l.append( (var, u'[Response variable]') )
		return l

class qtform_base(form_base, qtautoplugin):

	def __init__(self, name, experiment, script=None):

		form_base.__init__(self, name, experiment, script)
		qtautoplugin.__init__(self, __file__)

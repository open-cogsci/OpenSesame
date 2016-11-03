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
import platform

# If OpenSesame is launched with pythonw.exe under Windows, the standard
# channels are not available. This will cause IPython to crash sometimes, so we
# need to explicitly create null channels. See also:
# - <https://github.com/smathot/OpenSesame/issues/363>
import sys
import os
if (sys.stderr is None or \
	(hasattr(sys.stderr, u'fileno') and sys.stderr.fileno() == -2)):
	sys.stdout = sys.stderr = open(os.devnull, u'w')
	sys.stdin = open(os.devnull, u'r')

from qtpy import QtWidgets, QtGui
try:
	# New-style Jupyter imports
	
	# When packaged on a mac, a check that qtconsole does to see if pyqt4 is available fails
	# Since PyQt4 is packaged with OpenSesame, we may assume it will be available and 
	# override the check to return True 
	if platform.system() == "Darwin" and hasattr(sys,"frozen"):
		import qtconsole.qt_loaders
		qtconsole.qt_loaders.has_binding = lambda api: api == u'pyqt'

	from qtconsole.rich_jupyter_widget import RichJupyterWidget \
		as RichIPythonWidget
	from qtconsole.inprocess import QtInProcessKernelManager
except:
	# Old-style IPython imports
	from IPython.qt.console.rich_ipython_widget import RichIPythonWidget
	from IPython.qt.inprocess import QtInProcessKernelManager
from libqtopensesame.console._base_console import base_console
from libqtopensesame.misc.config import cfg
from libopensesame import debug

def _style(cs, token):

	"""
	desc:
		Extracts the color from a QProgEdit style spec.

	arguments:
		cs:
			desc:	A QProgEdit colorscheme.
			type:	dict
		token:
			desc:	The style name.
			type:	[str, unicode]

	returns:
		desc:	A color string.
		type:	unicode
	"""

	color = cs.get(token, u'#000000')
	if isinstance(color, tuple):
		return color[0]
	return color

def pygments_style_factory(cs):

	"""
	arguments:
		cs:
			desc:	A QProgEdit colorscheme.
			type:	dict

	returns:
		desc:	A Pygments Style class that emulates the QProgEdit colorscheme.
		type:	Style
	"""

	from pygments.style import Style
	from pygments import token
	class my_style(Style):
		default_style = u''
		styles = {
			token.Comment 	: _style(cs, 'Comment'),
			token.Keyword	: _style(cs, 'Keyword'),
			token.Name		: _style(cs, 'Identifier'),
			token.String	: _style(cs, 'Double-quoted string'),
			token.Error		: _style(cs, 'Invalid'),
			token.Number	: _style(cs, 'Number'),
			token.Operator	: _style(cs, 'Operator'),
			token.Generic	: _style(cs, 'Default'),
		}
	return my_style

class ipython_console(base_console, QtWidgets.QWidget):

	"""
	desc:
		An IPython-based debug window.
	"""

	def __init__(self, main_window):

		"""
		desc:
			Constructor.

		arguments:
			main_window:	The main window object.
		"""

		super(ipython_console, self).__init__(main_window)
		kernel_manager = QtInProcessKernelManager()
		kernel_manager.start_kernel()
		self.kernel = kernel_manager.kernel
		self.kernel.gui = 'qt4'
		self.kernel.shell.banner1 = ''
		kernel_client = kernel_manager.client()
		kernel_client.start_channels()
		self.control = RichIPythonWidget()
		self.control.banner = self.banner()
		self.control.kernel_manager = kernel_manager
		self.control.kernel_client = kernel_client
		self.verticalLayout = QtWidgets.QVBoxLayout(self)
		self.verticalLayout.setContentsMargins(0,0,0,0)
		self.setLayout(self.verticalLayout)
		self.verticalLayout.addWidget(self.control)

	def clear(self):

		"""See base_console."""

		self.control.reset(clear=True)

	def focus(self):

		"""See base_console."""

		self.control._control.setFocus()

	def reset(self):

		"""See base_console."""

		self.kernel.shell.reset()
		self.kernel.shell.push(self.default_globals())
		self.clear()
		super(ipython_console, self).reset()

	def show_prompt(self):

		"""See base_console."""

		self.control._show_interpreter_prompt()

	def get_workspace_globals(self):

		"""See base_console."""

		return self.kernel.shell.user_global_ns.copy()

	def set_workspace_globals(self, _globals={}):

		"""See base_console."""

		self.kernel.shell.push(_globals)

	def validTheme(self, cs):

		"""
		returns:
			desc:	True if the colorscheme is valid, False otherwise.
			type:	bool
		"""

		for key in [
			u'Background',
			u'Default',
			u'Prompt in',
			u'Prompt out',
			u'Comment',
			u'Keyword',
			u'Identifier',
			u'Double-quoted string',
			u'Invalid',
			u'Number',
			u'Operator',
			]:
			if key not in cs:
				return False
		return True

	def setTheme(self):

		"""
		desc:
			Sets the theme, based on the QProgEdit settings.
		"""

		from QProgEdit import QColorScheme
		if not hasattr(QColorScheme, cfg.qProgEditColorScheme):
			debug.msg(u'Failed to set debug-output colorscheme')
			return u''
		cs = getattr(QColorScheme, cfg.qProgEditColorScheme)
		if not self.validTheme(cs):
			debug.msg(u'Invalid debug-output colorscheme')
			return u''
		self.control._highlighter.set_style(pygments_style_factory(cs))
		qss = u'''QPlainTextEdit, QTextEdit {
				background-color: %(Background)s;
				color: %(Default)s;
			}
			.in-prompt { color: %(Prompt in)s; }
			.in-prompt-number { font-weight: bold; }
			.out-prompt { color: %(Prompt out)s; }
			.out-prompt-number { font-weight: bold; }
			''' % cs
		self.control.style_sheet = qss
		self.control._control.setFont(QtGui.QFont(cfg.qProgEditFontFamily,
			cfg.qProgEditFontSize))

	def setup(self, main_window):

		"""See base_subcomponent."""

		super(ipython_console, self).setup(main_window)
		self.kernel.shell.push(self.default_globals())

	def write(self, s):

		"""See base_console."""

		self.control._append_plain_text(str(s))
		self.control._control.ensureCursorVisible()

	def execute(self, s):

		"""See base_console."""

		self.main_window.ui.dock_stdout.setVisible(True)
		self.control.execute(s)

	def focusInEvent(self, e):

		self.control.setFocus()
		e.accept()

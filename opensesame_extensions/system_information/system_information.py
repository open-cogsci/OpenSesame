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
from libqtopensesame.extensions import base_extension
from libqtopensesame.misc.translate import translation_context
_ = translation_context(u'system_information', category=u'extension')


class system_information(base_extension):

	"""
	desc:
		Shows a tab with system information and version numbers
	"""

	def activate(self):

		l = []
		for name, module, attr in [
			(u'OpenSesame', u'libopensesame.metadata', u'__version__'),
			(u'Python', u'sys', u'version'),
			(u'QProgEdit', u'QProgEdit', u'__version__'),
			(u'datamatrix', u'datamatrix', u'__version__'),
			(u'qdatamatrix', u'qdatamatrix', u'__version__'),
			(u'pseudorandom', u'pseudorandom', u'__version__'),
			(u'fileinspector', u'fileinspector', u'__version__'),
			(u'QNotifications', u'QNotifications', u'__version__'),
			(u'QOpenScienceFramework', u'QOpenScienceFramework', u'__version__'),
			(u'opencv', u'cv2', u'__version__'),
			(u'expyriment', u'expyriment', u'__version__'),
			(u'IPython', u'IPython', u'__version__'),
			(u'numpy', u'numpy', u'__version__'),
			(u'scipy', u'scipy', u'__version__'),
			(u'PIL/ PILLOW', u'PIL', u'VERSION'),
			(u'psychopy', u'psychopy', u'__version__'),
			(u'pygame', u'pygame', u'__version__'),
			(u'pygaze', u'pygaze', u'__version__'),
			(u'pyglet', u'pyglet', u'version'),
			(u'PyQt', u'qtpy', [u'QtCore', u'PYQT_VERSION_STR']),
			(u'serial', u'serial', u'VERSION'),
			(u'markdown', u'markdown', u'version'),
			(u'yaml', u'yaml', u'__version__'),
			]:
			try:
				mod = __import__(module)
			except ImportError:
				l.append(u'%s [not available]' % name)
				continue
			except Exception as e:
				l.append(
					u'%s [installed, but `%s` occured while importing]' \
					% (name, e.__class__.__name__))
				continue
			if isinstance(attr, basestring):
				attr = [attr]
			while len(attr) > 1:
				a = attr.pop(0)
				if hasattr(mod, a):
					mod = getattr(mod, a)
			a = attr.pop(0)
			if hasattr(mod, a):
				l.append(u'%s %s' % (name, getattr(mod, a)))
				continue
			l.append(u'%s [version unknown]' % name)

		# platform.architecture() does not seem to work correctly on Windows so a solution found on stackoverflow is used
		# http://stackoverflow.com/questions/2208828/detect-64bit-os-windows-in-python
		if(platform.platform().startswith('Windows') and platform.machine().endswith('64')):
			t = 'win64'
		elif(platform.platform().startswith('Windows') and not platform.machine().endswith('64')):
			t = 'win32'
		else:
			t = platform.architecture()[0]

		md = safe_read(self.ext_resource(u'system-information.md')) % {
			u'system' : platform.platform(),
			u'architecture' : t,
			u'modules' : u'- ' + u'\n- '.join(l)
			}
		self.tabwidget.open_markdown(md, icon=self.icon(),
			title=_(u'System information'))

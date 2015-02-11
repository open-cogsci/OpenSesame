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

from PyQt4 import QtGui
from libopensesame import debug
from libqtopensesame.misc import _
from libqtopensesame.extensions import base_extension
from libqtopensesame.misc.config import cfg

class update_checker(base_extension):
	
	def activate(self):

		self.check_for_updates()

	def event_startup(self):

		self.check_for_updates(always=False)

	def update_dialog(self, message):

		"""
		Presents an update dialog

		Arguments:
		message -- the message to be displayed
		"""

		from update_checker_dialog.update import update
		d = update(self.main_window, msg=message)
		d.exec_()

	def check_for_updates(self, always=True):

		import urllib

		if not always and not cfg.auto_update_check:
			debug.msg(u"skipping update check")
			return

		debug.msg(u"opening %s" % cfg.version_check_url)

		try:
			fd = urllib.urlopen(cfg.version_check_url)
			mrv = float(fd.read().strip())
		except Exception as e:
			if always:
				self.update_dialog( \
					_(u"... and is sorry to say that the attempt to check for updates has failed. Please make sure that you are connected to the internet and try again later. If this problem persists, please visit <a href='http://www.cogsci.nl/opensesame'>http://www.cogsci.nl/opensesame</a> for more information."))
			return

		# The most recent version as downloaded is always a float. Therefore, we
		# must convert the various possible version numbers to analogous floats.
		# We do this by dividing each subversion number by 100. The only
		# exception is that prereleases should be counted as older than stable
		# releases, so for pre-release we substract one bugfix version.
		# 0.27			->	0.27.0.0			->	0.27
		# 0.27.1 		-> 	0.27.1.0			->	0.2701
		# 0.27~pre1		->	0.27.0.1 - .0001	-> 	0.269901
		# 0.27.1~pre1	->	0.27.1.1 - .0001	-> 	0.270001
		v = self.main_window.version
		l = v.split(u"~pre")
		if len(l) == 2:
			lastSubVer = l[1]
			v = l[0]
			ver = -.0001
		else:
			lastSubVer = 0
			ver = .0
		lvl = 0
		fct = .01
		for subVer in v.split(u'.') + [lastSubVer]:
			try:
				_subVer = int(subVer)
			except:
				debug.msg(u'Failed to process version segment %s' % subVer, \
					reason=u'warning')
				return
			ver += fct**lvl * _subVer
			lvl += 1
		debug.msg(u'identifying as version %s' % ver)
		debug.msg(u'latest stable version is %s' % mrv)
		if mrv > ver:
			self.update_dialog( \
				_(u"... and is happy to report that a new version of OpenSesame (%s) is available at <a href='http://www.cogsci.nl/opensesame'>http://www.cogsci.nl/opensesame</a>!") % mrv)
		else:
			if always:
				self.update_dialog( \
					_(u" ... and is happy to report that you are running the most recent version of OpenSesame."))

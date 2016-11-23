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
from qtpy import QtWidgets
from libopensesame import debug
from libqtopensesame.extensions import base_extension
from libqtopensesame.misc.config import cfg
from libqtopensesame.misc.translate import translation_context
_ = translation_context(u'update_checker', category=u'extension')

class update_checker(base_extension):

	def activate(self):

		self.check_for_updates()

	def event_startup(self):

		self.check_for_updates(always=False)

	def check_for_updates(self, always=True):

		if py3:
			from urllib.request import urlopen
		else:
			from urllib2 import urlopen
		from distutils.version import StrictVersion
		from libopensesame import metadata
		import yaml

		if not always and not cfg.auto_update_check:
			debug.msg(u"skipping update check")
			return
		debug.msg(u"opening %s" % cfg.remote_metadata_url)
		success = True
		try:
			fd = urlopen(cfg.remote_metadata_url)
			s = fd.read()
			fd.close()
		except:
			debug.msg(u"failed to load remote metadata.yaml")
			success = False
		if success:
			try:
				remote_metadata = yaml.load(s)
			except:
				debug.msg(u"failed to load parse metadata.yaml")
				success = False
		if success:
			if u'stable_version' not in remote_metadata:
				debug.msg(u"no stable_version in metadata")
				success = False
			else:
				try:
					remote_strict_version = StrictVersion(
						remote_metadata[u'stable_version'])
				except:
					debug.msg(u"stable_version is not strict")
					success = False
		if not success:
			self.tabwidget.open_markdown(self.ext_resource(u'failed.md'))
			return
		if remote_strict_version > metadata.strict_version:
			debug.msg(u"new version available")
			s = safe_read(self.ext_resource(u'update-available.md'))
			self.tabwidget.open_markdown(s % remote_metadata,
				title=u'Update available!')
		else:
			debug.msg(u"up to date")
			if always:
				self.tabwidget.open_markdown(
					self.ext_resource(u'up-to-date.md'),
					title=_(u'Up to date!'))

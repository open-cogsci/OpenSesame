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
import os
import tarfile
from libopensesame import misc
from libopensesame.osexpfile import osexpbase


class osexpreader(osexpbase):

	"""
	desc:
		A reader for osexp files of any format.
	"""

	def __init__(self, exp, src):

		"""
		desc:
			Constructor. A side effect of calling this constructor is that all
			files in the file pool of src are extracted to the file pool folder
			of the experiment.

		arguments:
			exp:
				desc:	An experiment object.
				type:	experiment
			src:
				desc:	An OpenSesame script, or the name of an OpenSesame
						experiment file.
				type:	str
		"""

		osexpbase.__init__(self, exp)
		self._src = safe_decode(src)
		if self.format == u'script':
			self._read_script()
		elif self.format == u'scriptfile':
			self._read_scriptfile()
		elif self.format == u'targz':
			self._read_tarfile(format=u'r:gz')
		elif self.format == u'tar':
			self._read_tarfile(format=u'r')
		else:
			raise TypeError(u'"%s" is not an OpenSesame experiment')

	@property
	def script(self):

		"""See osexpbase"""

		return self._script

	def _determine_format(self):

		"""See osexpbase"""

		try:
			# Checking whether a path exists can appartently trigger a
			# ValueError when src is too long. Therefore, we use this awkward
			# construction.
			if not os.path.exists(self._src):
				raise ValueError(u'Path doesn\'t exist)')
		except ValueError:
			return u'script'
		try:
			tarfile.open(self._src, u'r:gz')
			return 'targz'
		except tarfile.ReadError:
			pass
		try:
			tarfile.open(self._src, u'r')
			return 'tar'
		except tarfile.ReadError:
			return 'scriptfile'

	def _read_script(self):

		"""
		visible: False

		desc:
			Reads a script (ie. not a file)
		"""

		self._script = self._src
		self._experiment_path = None

	def _read_scriptfile(self):

		"""
		visible: False

		desc:
			Reads a plain-text script file.
		"""

		self._experiment_path = os.path.dirname(self._src)
		with safe_open(self._src, universal_newline_mode) as fd:
			self._script = fd.read()

	def _read_tarfile(self, format):

		"""
		visible: False

		desc:
			Reads a tar or targz archive.

		arguments:
			format:
				desc:	The format to be used for tarfile.open().
				type:	str
		"""

		self._experiment_path = os.path.dirname(self._src)
		tar = tarfile.open(self._src, format)
		for name in tar.getnames():
			# Tar doesn't return unicode in Python 2
			uname = safe_decode(name)
			folder, fname = os.path.split(uname)
			# Ignore everything except the pool folder
			if folder != u'pool':
				continue
			# Filenames are encoded with U+XXXX notation in the archive. This is
			# necessary to deal with absence of good unicode support in .tar.gz.
			fname = self._syntax.from_ascii(fname)
			pool_folder = safe_str(
				self._pool.folder(),
				enc=misc.filesystem_encoding()
			)
			tar.extract(name, pool_folder)
			from_name = os.path.join(self._pool.folder(), uname)
			to_name = os.path.join(self._pool.folder(), fname)
			os.rename(from_name, to_name)
			os.rmdir(os.path.join(self._pool.folder(), folder))
		# Temporarily extract the script file to the file pool, and remove it
		# right away
		script_path = os.path.join(self._pool.folder(), u'script.opensesame')
		tar.extract(u'script.opensesame', self._pool.folder())
		with safe_open(script_path, universal_newline_mode) as fd:
			self._script = fd.read()
		os.remove(script_path)

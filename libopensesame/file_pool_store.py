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
from libopensesame import misc, debug
from libopensesame.exceptions import osexception
import tempfile
import os
import shutil

pool_folders = []

class file_pool_store(object):

	"""
	desc: |
		Provides a dictionary-like interface to the file pool.
	"""

	def __init__(self, experiment, folder=None):

		global pool_folders

		self.experiment = experiment
		if folder is None:
			# On some systems tempfile.mkdtemp() triggers a UnicodeDecodeError.
			# This is resolved by passing the dir explicitly as a Unicode
			# string. This fix has been adapted from:
			# - <http://bugs.python.org/issue1681974>
			self.__folder__ = tempfile.mkdtemp(suffix=u'.opensesame_pool',
				dir=safe_decode(tempfile.gettempdir(),
				enc=misc.filesystem_encoding()))
			pool_folders.append(self.__folder__)
			debug.msg(u'creating new pool folder')
		else:
			debug.msg(u'reusing existing pool folder')
			self.__folder__ = folder
		debug.msg(u'pool folder is \'%s\'' % self.__folder__)

	def __contains__(self, path):

		"""
		desc:
			Checks if a file is in the file pool.

		returns:
			desc:	A bool indicating if the file is in the pool.
			type:	bool

		example: |
			if not exp.file_in_pool('my_image.png'):
				print('my_image.png could not be found!')
			else:
				image_path = exp.get_file('my_image.png')
				my_canvas = exp.offline_canvas()
				my_canvas.image(image_path)
		"""

		return os.path.exists(self[path])

	def __delitem__(self, path):

		os.remove(self[path])

	def __getitem__(self, path):

		"""
		desc: |
			Returns the full path to a file. The logic is as follows:

			1. First checks if `path` is a file in the file pool.
			2. If not, check if `path` is a file in the folder of the current
			   experiment (if any).
			3. If not, check if `path` is a file in the `__pool__` subfolder of
			   the current experiment.
			4. If not, simply return `path`.

		arguments:
			path:
				desc:	A filename. This can be any type, but will be coerced
						to `unicode` if it is not `unicode`.

		returns:
			desc:	The full path to the file.
			type:	unicode

		example: |
			image_path = exp.get_file('my_image.png')
			my_canvas = exp.offline_canvas()
			my_canvas.image(image_path)
		"""

		path = self.experiment.unistr(path)
		if path.strip() == u'':
			raise osexception(u'Cannot get empty filename from file pool.')
		for folder in self.folders(include_experiment_path=True):
			_path = os.path.join(folder, path)
			if os.path.exists(_path):
				return _path
		return path

	def __iter__(self):

		pass

	def __len__(self):

		return len(self.files())

	def add(self, path):

		shutil.copyfile(external_path, os.path.join(self.__folder__,
			os.path.basename(path)))

	def files(self):

		_files = []
		for _folder in self.folder():
			for _file in os.listdir(_folder):
				if os.path.isfile(os.path.join(_folder, _file)):
					_files.append(_file)
		return _files

	def fallback_folder(self):

		_folders = self.folders()
		if len(_folders) < 2:
			return None
		return _folders[-1]

	def folder(self):

		return self.__folder__

	def folders(self, include_experiment_path=False):

		_folders = [self.__folder__]
		if self.experiment.experiment_path is None or \
			not os.path.exists(self.experiment.experiment_path):
				return _folders
		fallback_folder = os.path.join(self.experiment.experiment_path,
			u'__pool__')
		if os.path.exists(fallback_folder):
			_folders.append(fallback_folder)
		if include_experiment_path:
			_folders.append(self.experiment.experiment_path)
		return _folders

	def rename(self, old_path, new_path):

		pass

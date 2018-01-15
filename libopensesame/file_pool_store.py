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

class file_pool_store(object):

	"""
	desc: |
		The `pool` object provides dict-like access to the file pool. When
		checking whether a file is in the file pool, several folders are
		searched. For more details, see [folders].

		A `pool` object is created automatically when the experiment starts.

		In addition to the functions listed below, the following semantics are
		supported:

		__Example 1__:

		~~~ .python
		# Get the full path to a file in the file pool
		print(u'The full path to img.png is %s' %  pool[u'img.png'])
		# Check if a file is in the file pool
		if u'img.png' in pool:
			print(u'img.png is in the file pool')
		# Delete a file from the file pool
		del pool[u'img.png']
		# Walk through all files in the file pool. This retrieves the full
		# paths.
		for path in pool:
			print(path)
		# Check the number of files in the file pool
		print(u'There are %d files in the file pool' % len(pool))
		~~~

		__Example 2__:

		~~~ .python
		# Get the full path to an image from the file pool and show it
		if u'img.png' in pool:
			print(u'img.png could not be found!')
		else:
			image_path = pool[u'img.png']
			my_canvas = Canvas()
			my_canvas.image(image_path)
			my_canvas.show()
		~~~

		[TOC]
	"""

	def __init__(self, experiment, folder=None):

		"""
		visible: False

		desc:
			Constructor.

		arguments:
			experiment:
				desc:	The experiment object.
				type:	experiment

		keywords:
			folder:
				desc:	The folder to use for the file pool, or `None` to create
						a new temporary folder.
				type:	[str, unicode, NoneType]
		"""

		self.experiment = experiment
		if folder is None:
			# On some systems tempfile.mkdtemp() triggers a UnicodeDecodeError.
			# This is resolved by passing the dir explicitly as a Unicode
			# string. This fix has been adapted from:
			# - <http://bugs.python.org/issue1681974>
			self.__folder__ = tempfile.mkdtemp(suffix=u'.opensesame_pool',
				dir=safe_decode(tempfile.gettempdir(),
				enc=misc.filesystem_encoding()))
			debug.msg(u'creating new pool folder')
		else:
			debug.msg(u'reusing existing pool folder')
			self.__folder__ = folder
		debug.msg(u'pool folder is \'%s\'' % self.__folder__)

	def clean_up(self):

		"""
		visible: False

		desc:
			Removes the pool folder.
		"""

		try:
			shutil.rmtree(self.__folder__)
		except:
			debug.msg(u'Failed to remove %s' % self.__folder__)

	def __contains__(self, path):

		"""
		visible: False

		desc:
			Checks if a file is in the file pool.

		returns:
			desc:	A bool indicating if the file is in the pool.
			type:	bool
		"""

		if path == u'':
			return False
		return os.path.exists(self[path])

	def __delitem__(self, path):

		"""
		visible: False

		desc:
			Deletes a file from the file pool.

		arguments:
			path:
				desc:	The name of the file.
				type:	[str, unicode]
		"""

		os.remove(self[path])

	def __getitem__(self, path):

		"""
		visible: False

		desc: |
			Returns the full path to a file.

		arguments:
			path:
				desc:	A filename. This can be any type, but will be coerced
						to `unicode` if it is not `unicode`.

		returns:
			desc:	The full path to the file.
			type:	unicode
		"""

		path = safe_decode(path)
		if path.strip() == u'':
			raise osexception(u'Cannot get empty filename from file pool.')
		for folder in self.folders(include_experiment_path=True):
			_path = os.path.normpath(os.path.join(folder, path))
			if os.path.exists(safe_str(_path, enc=misc.filesystem_encoding())):
				return _path
		return os.path.normpath(path)

	def __iter__(self):

		"""
		visible: False

		returns:
			type:	file_pool_store_iterator
		"""

		return file_pool_store_iterator(self)

	def __len__(self):

		"""
		visible: False

		returns:
			desc:	The number of files in the file pool.
			type:	int
		"""

		return len(self.files())

	def count_included(self):

		"""
		visible: False

		returns:
			desc:	The number of files that are in the main pool folder, i.e.
					the folder that is included with the experiment.
			type:	int
		"""

		return len(os.listdir(self.folder()))

	def add(self, path, new_name=None):

		"""
		desc:
			Copies a file to the file pool.

		arguments:
			path:
				desc:	The full path to the file on disk.
				type:	[str, unicode]

		keywords:
			new_name:
				desc:	A new name for the file in the pool, or None to use the
						file's original name.
				type:	[str, NoneType]

		example: |
			pool.add(u'/home/username/Pictures/my_ing.png')
		"""

		if new_name is None:
			new_name = os.path.basename(path)
		shutil.copyfile(path, os.path.join(self.__folder__, new_name))

	def files(self):

		"""
		desc:
			Returns all files in the file pool.

		returns:
			desc:	A list of full paths.
			type:	list

		example: |
			for path in pool.files():
				print(path)
			# Equivalent to:
			for path in pool:
				print(path)
		"""

		_files = []
		for _folder in self.folders():
			for _file in os.listdir(_folder):
				if os.path.isfile(os.path.join(_folder, _file)):
					_files.append(_file)
		return sorted(_files)

	def fallback_folder(self):

		"""
		returns:
			desc:	The full path to the fallback pool folder, which is the
					`__pool__` subfolder of the current experiment folder, or
					`None` if this folder does not exist. The fallback pool
					folder is mostly useful in combination with a versioning
					system, such as git, because it allows you to save the
					experiment as a plain-text file, even when having files
					in the file pool.
			type:	[unicode, NoneType]

		example: |
			if pool.fallback_folder() is not None:
				print(u'There is a fallback pool folder!')
		"""

		_folders = self.folders()
		if len(_folders) < 2:
			return None
		return _folders[-1]

	def folder(self):

		"""
		desc:
			Gives the full path to the (main) pool folder. This is typically a
			temporary folder that is deleted when the experiment is finished.

		returns:
			desc:	The full path to the main pool folder.
			type:	unicode

		example: |
			print(u'The pool folder is here: ' % pool.folder())
		"""

		return self.__folder__

	def in_folder(self, path):

		"""
		desc:
			Checks whether path is in the pool folder. This is different from
			the `path in pool` syntax in that it only checks the main pool
			folder, and not the fallback pool folder and experiment folder.

		arguments:
			path:
				desc:	A file basename to check.
				type:	str

		returns:
			type:	bool

		example: |
			print(pool.in_folder('cue.png'))
		"""

		return os.path.exists(os.path.join(self.__folder__, path))

	def folders(self, include_fallback_folder=True,
		include_experiment_path=False):

		"""
		desc: |
			Gives a list of all folders that are searched when retrieving the
			full path to a file. These are (in order):

			1. The file pool folder itself, as returned by [folder].
			2. The folder of the current experiment (if it exists)
			3. The fallback pool folder, as returned by [fallback_folder]
			   (if it exists)

		keywords:
			include_fallback_folder:
				desc:	Indicates whether the fallback pool folder should be
						included if it exists.
				type:	bool
			include_experiment_path:
				desc:	Indicates whether the experiment folder should be
						included if it exists.
				type:	bool

		returns:
			desc:	A list of all folders.
			type:	list

		example: |
			print(u'The following folders are searched for files:')
			for folder in pool.folders():
				print(folder)
		"""

		_folders = [self.__folder__]
		if self.experiment.experiment_path is None or \
			not os.path.exists(self.experiment.experiment_path):
				return _folders
		fallback_folder = os.path.join(self.experiment.experiment_path,
			u'__pool__')
		if include_fallback_folder and os.path.exists(fallback_folder):
			_folders.append(fallback_folder)
		if include_experiment_path:
			_folders.append(self.experiment.experiment_path)
		return _folders

	def rename(self, old_path, new_path):

		"""
		desc:
			Renames a file in the pool folder.

		arguments:
			old_path:
				desc:	The old file name.
				type:	[str, unicode]
			new_path:
				desc:	The new file name.
				type:	[str, unicode]

		example: |
			pool.rename(u'my_old_img.png', u'my_new_img.png')
		"""

		path = self[old_path]
		dirname, basename = os.path.split(path)
		os.rename(path, os.path.join(dirname, new_path))

	def size(self):

		"""
		returns:
			desc:	The combined size in bytes of all files in the file pool.
			type:	int

		example:
			print(u'The size of the file pool is %d bytes' % pool.size())
		"""

		return sum([os.path.getsize(self[path]) for path in self])

class file_pool_store_iterator(object):

	def __init__(self, pool):

		self.pool = pool
		self.files = pool.files()

	def __iter__(self):

		return self

	def __next__(self):

		# For Python 3
		return self.next()

	def next(self):

		if len(self.files) == 0:
			raise StopIteration
		return self.files.pop()

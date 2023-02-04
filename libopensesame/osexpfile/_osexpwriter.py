# -*- coding:utf-8 -*-

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
import tempfile
import shutil
from libopensesame.osexpfile import OSExpBase
from libopensesame.oslogging import oslogger


class OSExpWriter(OSExpBase):

    """
    desc:
            A writer of osexp files. The format (plain text or tar.gz) depends on
            whether the file pool contains files.
    """

    def __init__(self, exp, path):
        """
        desc:
                Constructor.

        arguments:
                exp:
                        desc:	An experiment object.
                        type:	experiment
                path:
                        desc:	A path to the experiment file.
                        type:	str
        """

        super().__init__(exp)
        self._path = path
        self._experiment_path = os.path.dirname(path)
        if self.format == 'scriptfile':
            self._write_scriptfile()
        elif self.format == 'tarfile':
            self._write_tarfile()
        else:
            raise TypeError(u'Invalid format')

    @property
    def script(self):
        """See osexpbase"""

        return self._exp.to_string()

    def _determine_format(self):
        """See osexpbase"""

        return 'scriptfile' if not self._pool.count_included() else 'tarfile'

    def _write_scriptfile(self):
        """
        visible: False

        desc:
                Writes a plain-text file.
        """

        with safe_open(self._path, u'w') as fd:
            fd.write(self.script)

    def _write_tarfile(self):
        """
        visible: False

        desc:
                Writes a .tar.gz file.
        """

        # Write the script to a text file in the file pool
        script_path = os.path.join(self._pool.folder(), u'script.opensesame')
        with safe_open(script_path, u'w') as fd:
            fd.write(self.script)
        # Create the archive in a a temporary folder and move it afterwards.
        # This hack is needed, because tarfile fails on a Unicode path.
        tmp_path = tempfile.mktemp(suffix=u'.osexp')
        tar = tarfile.open(tmp_path, u'w:gz')
        tar.add(script_path, u'script.opensesame')
        os.remove(script_path)
        # We also create a temporary pool folder, where all the filenames are
        # Unicode sanitized to ASCII format. Again, this is necessary to deal
        # with poor Unicode support in .tar.gz.
        tmp_pool = tempfile.mkdtemp(suffix=u'.opensesame.pool')
        for fname in os.listdir(self._pool.folder()):
            src = os.path.join(self._pool.folder(), fname)
            if not os.path.isfile(src):
                oslogger.warning('{} is not a file'.format(src))
                continue
            dst = os.path.join(tmp_pool, self._syntax.to_ascii(fname))
            shutil.copyfile(src, dst)
        tar.add(tmp_pool, u'pool', True)
        tar.close()
        # Move the file to the intended location
        shutil.move(tmp_path, self._path)
        # Clean up the temporary pool folder
        try:
            shutil.rmtree(tmp_pool)
        except:
            pass

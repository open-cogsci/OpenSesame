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
from libqtopensesame.extensions import base_extension
from libqtopensesame.misc.config import cfg
from libopensesame import metadata
from qtpy import QtCore
import sys
import yaml
import os
import traceback
from libqtopensesame.misc.translate import translation_context
_ = translation_context(u'bug_report', category=u'extension')


class bug_report(base_extension):

    """
    desc:
            Captures the stderr and submits bug reports based on it.
    """

    def event_startup(self):
        """
        desc:
                Start capturing.
        """
        sys.excepthook = self.captured_err

    def indent(self, s):
        """
        desc:
                Tab-indent a piece of text so that it's code for Markdown.

        arguments:
                s:	The text to indent.

        returns:
                Indented text.
        """

        return u'\t' + s.replace(u'\n', u'\n\t').replace(os.linesep, u'\n\t')

    def event_bug_report_send(self):
        """
        desc:
                Sends a bug report for the latest stacktrace. Also closes the
                current tab, which is the report tab, and shows a results tab.
        """

        self.main_window.tabwidget.close_current()
        from urllib.request import urlopen
        from urllib.parse import urlencode
        if self.traceback is None:
            return
        q = urlencode({
            u'traceback': safe_str(self.traceback, errors=u'ignore'),
            u'version': safe_str(metadata.__version__, errors=u'ignore'),
            u'python_version': safe_str(metadata.python_version,
                                        errors=u'ignore'),
            u'platform': safe_str(metadata.platform, errors=u'ignore'),
        })
        url = cfg.bug_report_url + u'?' + q
        try:
            fd = urlopen(url)
            resp = safe_decode(fd.read(), errors=u'ignore')
            fd.close()
        except:
            self.tabwidget.open_markdown(self.ext_resource(u'failure.md'),
                                         title=_(u'Bug report not sent'))
            return
        if resp == u'OK':
            self.tabwidget.open_markdown(self.ext_resource(u'success.md'),
                                         title=_(u'Bug report sent'))
        else:
            self.tabwidget.open_markdown(self.ext_resource(u'failure.md'),
                                         title=_(u'Bug report not sent'))

    def captured_err(self, exception_type, value, tb):
        """
        desc:
                Shows a report tab when an error message has been captured.
        """

        error_list = traceback.format_exception(exception_type, value, tb)
        self.traceback = u"".join([safe_decode(tb_line)
                                  for tb_line in error_list])
        self.traceback_md = u'~~~ .traceback\n%s\n~~~\n' % self.traceback
        md = safe_read(self.ext_resource(u'report.md')) % {
            # u'traceback' : self.indent(self.stderr.buffer),
            u'traceback': self.traceback_md,
            u'version': metadata.__version__,
            u'python_version': safe_str(metadata.python_version,
                                        errors=u'ignore'),
            u'platform': metadata.platform,
        }
        self.tabwidget.open_markdown(md, title=_(u'Oops ...'))
        sys.stderr.write(self.traceback)

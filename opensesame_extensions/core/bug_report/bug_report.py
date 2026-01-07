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
from libqtopensesame.extensions import BaseExtension
from libqtopensesame.misc.config import cfg
from libopensesame import metadata
import sys
import os
import traceback
from libqtopensesame.misc.translate import translation_context
_ = translation_context('bug_report', category='extension')


class BugReport(BaseExtension):

    def event_startup(self):
        sys.excepthook = self.captured_err

    def indent(self, s):
        """Tab-indent a piece of text so that it's code for Markdown.

        Parameters
        ----------
        s
            The text to indent.

        Returns
        -------
        Indented text.
        """
        return '\t' + s.replace('\n', '\n\t').replace(os.linesep, '\n\t')

    def event_bug_report_send(self):
        """Sends a bug report for the latest stacktrace. Also closes the
        current tab, which is the report tab, and shows a results tab.
        """
        self.main_window.tabwidget.close_current()
        from urllib.request import urlopen
        from urllib.parse import urlencode
        if self.traceback is None:
            return
        q = urlencode({
            'traceback': safe_str(self.traceback, errors='ignore'),
            'version': safe_str(metadata.__version__, errors='ignore'),
            'python_version': safe_str(metadata.python_version,
                                       errors='ignore'),
            'platform': safe_str(metadata.platform, errors='ignore'),
        })
        url = cfg.bug_report_url + '?' + q
        try:
            fd = urlopen(url)
            resp = safe_decode(fd.read(), errors='ignore')
            fd.close()
        except:
            self.tabwidget.open_markdown(self.ext_resource('failure.md'),
                                         title=_('Bug report not sent'))
            return
        if resp == 'OK':
            self.tabwidget.open_markdown(self.ext_resource('success.md'),
                                         title=_('Bug report sent'))
        else:
            self.tabwidget.open_markdown(self.ext_resource('failure.md'),
                                         title=_('Bug report not sent'))

    def captured_err(self, exception_type, value, tb):
        r"""Shows a report tab when an error message has been captured."""
        error_list = traceback.format_exception(exception_type, value, tb)
        self.traceback = u"".join([safe_decode(tb_line)
                                  for tb_line in error_list])
        self.traceback_md = '~~~ .traceback\n%s\n~~~\n' % self.traceback
        md = safe_read(self.ext_resource('report.md')) % {
            # 'traceback' : self.indent(self.stderr.buffer),
            'traceback': self.traceback_md,
            'version': metadata.__version__,
            'python_version': safe_str(metadata.python_version,
                                        errors='ignore'),
            'platform': metadata.platform,
        }
        self.tabwidget.open_markdown(md, title=_('Oops ...'))
        sys.stderr.write(self.traceback)
        self.main_window.enable()

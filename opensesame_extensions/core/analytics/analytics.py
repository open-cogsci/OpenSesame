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
from qtpy import QtCore, QtNetwork
from libopensesame import metadata
from libqtopensesame.misc.config import cfg
from libqtopensesame.widgets.webbrowser import WebView
from libqtopensesame.extensions import BaseExtension
from libqtopensesame.misc.translate import translation_context
from libqtopensesame.misc import template_info
_ = translation_context(u'analytics', category=u'extension')


HTML = u'''<!DOCTYPE html>
<html>
<head>
<script>
<!-- Google tag (gtag.js) -->
<script async src="https://www.googletagmanager.com/gtag/js?id=G-TPL6TXE7KL">
</script>
<script>
  window.dataLayer = window.dataLayer || [];
  function gtag(){dataLayer.push(arguments);}
  gtag('js', new Date());

  gtag('config', 'G-TPL6TXE7KL');
</script>
</head>
</body>DUMMY BODY</body>
</html>
'''


class Analytics(BaseExtension):

    r"""Sends a ping to Google Analytics when OpenSesame is started."""
    def event_startup(self):

        wv = WebView(self.main_window)
        wv.setHtml(
            HTML,
            QtCore.QUrl(
                u'http://opensesame.app.cogsci.nl/{}/{}'.format(
                    self.main_window.mode,
                    metadata.__version__)
            )
        )
        wv.hide()
        if not QtNetwork.QNetworkConfigurationManager().isOnline() or \
                not cfg.analytics_show_notification:
            return
        self.extension_manager.fire(
            u'notify',
            message=_('Anonymous usage data is collected. You can disable '
                      'this by disabling the <i>analytics</i> extension.'),
            category=u'info', timeout=10000, buttontext=_(u'Got it!'))
        cfg.analytics_show_notification = False

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
from libqtopensesame.misc.translate import translation_context
_ = translation_context(u'quick_switcher', category=u'extension')


class quick_switcher(base_extension):

    """
    desc:
            The quick-switcher allows you to quickly navigate to items.
    """

    def activate(self):

        haystack = []
        for item in self.experiment.items.values():
            haystack.append((
                u'{} ({})'.format(item.name, item.item_type),
                item,
                item.open_tab
            ))
        self.extension_manager.fire(
            u'quick_select',
            haystack=haystack,
            placeholder_text=_(u'Search items …')
        )

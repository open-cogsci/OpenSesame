#!/usr/bin/env python
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
import os
from academicmarkdown import build
from libopensesame import misc

md = u"""
<div class='page-notification'>This page is generated automatically from item-specific help pages. These pages can be viewed in OpenSesame by clicking on the help icon in the top-right of the tab area.</div>

## Overview

%%--
toc:
 mindepth: 2
 exclude: [Overview]
--%%

## Commonly used items

%s

## Plug-ins

%s

"""
plugin_msg = u"\n<div class='page-notification'>This is a plug-in and may not be installed by default. For plug-in installation instructions, see <a href='/plug-ins/installation'>here</a>.</div>\n"

exclude_list = [u'general.md', u'variables.md', u'stdout.md', u'missing.md',
                u'auto_example.md', u'remote_logger.md', u'pool.md', u'video_player.md']


def collect(folder):
    """
    Recursively collects a list of Markdown help files from a specified folder.

    Arguments:
    folder		--	The source folder.

    Returns:
    A list of path names of help files.
    """
    src = []
    for fname in os.listdir(folder):
        path = os.path.join(folder, fname)
        if os.path.isdir(path):
            print('Entering %s' % path)
            src += collect(path)
            continue
        if fname in exclude_list or not fname.endswith(u'.md'):
            continue
        print('Adding %s' % path)
        src.append(path)
    return sorted(src)


def helpify(folder, msg=u''):
    """
    Recursively builds a help page from Markdown help files in a source folder.

    Arguments:
    folder		--	The source folder.

    Keyword arguments:
    msg			--	An informative message to include after each help file.

    Returns:
    A help page.
    """
    src = collect(folder)
    md = u''
    for path in src:
        _md = u'\n' + msg + open(path).read().decode(u'utf-8') + u'\n<hr />\n'
        _md = _md.replace(u'\n#', u'\n###')
        md += _md
    return md


md = md % (helpify(u'help'), helpify(u'plugins', plugin_msg))
html = build.HTML(md, standalone=False)
open('../osdoc/content/_includes/item-help', 'w').write(html.encode('utf-8'))

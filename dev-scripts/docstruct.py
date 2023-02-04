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

from academicmarkdown import build
import sys
import os
import imp
import re
import subprocess
import inspect

tmpl_doc = u"""

## Overview

%%--
toc:
 mindepth: 2
 maxdepth: 10
 exclude: [Overview]
--%%

%(openexp)s

%(libopensesame)s

%(libqtopensesame)s

"""

obj_doc = u"""
%(header)s %(name)s

%(doc)s

%(contains)s

More info:

- Type: %(type)s
- Full name: `%(full_name)s`
- Source: <%(src)s>

"""


def ingit(path):
    """
    Checks whether a given path is part of the Git repository.

    Returns:
    True if the file is in Git, False otherwise.
    """

    cmd = u'git ls-files %s --error-unmatch' % path
    try:
        subprocess.check_call(cmd.split())
    except:
        return False
    return True


def objcontains(obj):
    """
    Generates a description of an objects contents, i.e. functions and classes.

    Arguments:
    obj		--	An object.

    Returns:
    A documentation string.
    """

    l = []
    for i in dir(obj):
        o = getattr(obj, i)
        if inspect.isclass(o):
            l.append(u'class: `%s`' % i)
        elif inspect.isfunction(o):
            l.append(u'function: `%s()`' % i)
    if len(l) == 0:
        return u''
    return u'Provides (may include functions and classes imported from other modules):\n\n- ' + u'\n- '.join(sorted(l)) + '\n'


def docstr(obj):
    """
    Retrieves the docstring for an object.

    Arguments:
    obj		--	An object.

    Returns:
    A docstring.
    """

    doc = u''
    if obj.__doc__ is None:
        return u'Auto-generated object.'
    for r in re.finditer(u'<DOC>(.*?)</DOC>', obj.__doc__, re.M | re.S):
        doc += r.groups()[0]
    if len(doc) == 0:
        doc = u'No docstring specified.'
    return doc


def docmod(path, lvl=2):
    """
    Documents a module.

    Arguments:
    path 	--	The path to the module.

    Keyword arguments:
    lvl		--	The depth in the hierarchy. (default=2)

    Returns:
    A full documentation string.
    """

    name = os.path.basename(path)[:-3]
    full_name = path[:-3].replace(u'/', '.')
    header = u'#' * lvl
    src = u'https://github.com/smathot/OpenSesame/blob/master/%s' % path
    sys.path.append(os.path.abspath(os.path.dirname(path)))
    try:
        mod = imp.load_source(name, path)
        doc = docstr(mod)
        contains = objcontains(mod)
    except:
        doc = u'Failed to import module.'
        contains = u''
    sys.path.pop()
    md = obj_doc % {u'header': header, u'name': name, u'full_name':
                    full_name, u'doc': doc, u'src': src, u'type': u'module',
                    u'contains': contains}
    return md


def docpkg(folder, lvl=2):
    """
    Documents a package.

    Arguments:
    path 	--	The path to the package.

    Keyword arguments:
    lvl		--	The depth in the hierarchy. (default=2)

    Returns:
    A full documentation string.
    """

    md = u''

    path = os.path.join(folder, u'__init__.py')
    name = os.path.basename(folder)
    full_name = folder.replace(u'/', '.')
    header = u'#' * lvl
    src = u'https://github.com/smathot/OpenSesame/blob/master/%s' % path
    if not os.path.exists(path) or not ingit(path):
        return md
    sys.path.append(os.path.abspath(folder))
    pkg = imp.load_source(u'dummy', path)
    sys.path.pop()
    doc = docstr(pkg)
    contains = objcontains(pkg)
    md += obj_doc % {u'header': header, u'name': name, u'full_name':
                     full_name, u'doc': doc, u'src': src, u'type': u'package',
                     u'contains': contains}
    # Document modules
    for fname in sorted(os.listdir(folder)):
        path = os.path.join(folder, fname)
        if path.endswith(u'.py') and fname != u'__init__.py' and ingit(path):
            md += docmod(path, lvl+1)
    # Document packages
    for fname in sorted(os.listdir(folder)):
        path = os.path.join(folder, fname)
        if os.path.isdir(path):
            md += docpkg(path, lvl+1)
    return md


md = tmpl_doc % {
    u'openexp': docpkg(u'openexp'),
    u'libopensesame': docpkg(u'libopensesame'),
    u'libqtopensesame': docpkg(u'libqtopensesame'),
}

build.HTML(md, '../osdoc/content/_includes/source-code-structure',
           standalone=False)
build.PDF(md, 'docstruct.pdf')
build.MD(md, 'docstruct.md')

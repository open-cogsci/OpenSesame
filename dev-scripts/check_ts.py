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
import xml.etree.ElementTree as ET

for ts in os.listdir('resources/ts'):
    if not ts.endswith('.ts'):
        continue
    print 'Checking %s' % ts
    tree = ET.parse('resources/ts/%s' % ts)
    root = tree.getroot()
    nTotal = 0
    nObsolete = 0
    nUnfinished = 0
    for context in root:
        for msg in context:
            if len(msg) == 0:
                continue
            src = None
            tra = None
            for i in msg:
                if i.tag == u'source':
                    src = i.text
                    nTotal += 1
                elif i.tag == u'translation':
                    if u'type' in i.attrib:
                        if i.attrib[u'type'] == u'unfinished':
                            nUnfinished += 1
                        elif i.attrib[u'type'] == u'obsolete':
                            nObsolete += 1
                        else:
                            tra = i.text
            if tra is None:
                continue
            if src.count('%s') != tra.count('%s') or src.count('%d') != \
                    tra.count('%d') or src.count('%f') != tra.count('%f'):
                print '*** Wildcard mismatch!'
                print '\t', src
                print '\t', tra
    print 'Total: %d, Unfinished: %d, Obsolete: %d\n' % (nTotal, nUnfinished,
                                                         nObsolete)

#-*- coding:utf-8 -*-

"""
This file is part of openexp.

openexp is free software: you can redistribute it and/or modify
it under the terms of the GNU General Public License as published by
the Free Software Foundation, either version 3 of the License, or
(at your option) any later version.

openexp is distributed in the hope that it will be useful,
but WITHOUT ANY WARRANTY; without even the implied warranty of
MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
GNU General Public License for more details.

You should have received a copy of the GNU General Public License
along with openexp.  If not, see <http://www.gnu.org/licenses/>.
"""

import json
from PyQt4 import QtCore, QtGui
from libopensesame import debug

# For unknown mimetypes
invalid_data = {
	u'type':	u'invalid'
	}

def receive(drop_event):

	"""
	desc:
		Extracts data from a drop event. This data should be embedded in the
		mimedata as a json text string.

	arguments:
		drop_event:
			desc:	A drop event.
			type:	QDropEvent

	returns:
		desc:		A data dictionary. The 'type' key identifies the type of
					data that is being dropped.
		type:		dict
	"""

	mimedata = drop_event.mimeData()
	if not mimedata.hasText():
		debug.msg(u'No text data')
		return invalid_data
	text = unicode(mimedata.text())
	debug.msg(text)
	try:
		data = json.loads(text)
	except:
		debug.msg(u'Failed to load json mime data')
		return invalid_data
	if u'type' not in data:
		return invalid_data
	return data

def send(drag_src, data):

	"""
	desc:
		Starts a drag event, and embeds a data dictionary as json text in the
		mimedata.

	arguments:
		drag_src:
			desc:	The source widget.
			type:	QWidget
		data:
			desc:	A data dictionary. The 'type' key identifies the type of
					data that is being dropped.
			type:	dict

	returns:
		desc:		A drag object. The start function is called automatically.
		type:		QDrag
	"""

	text = json.dumps(data).decode('utf-8')
	mimedata = QtCore.QMimeData()
	mimedata.setText(text)
	drag = QtGui.QDrag(drag_src)
	drag.setMimeData(mimedata)
	drag.start()

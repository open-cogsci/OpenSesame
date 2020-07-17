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

---
desc:
	Drag-and-drop data is communicated by json-encoded dictionaries. The
	following drag types exist:

	-	type:			invalid

	-	type:			sketchpad-element-move

	-	type:			url-local
		url:			[url]

	-	type:			item-existing
		item-name:		[item name]
		QTreeWidgetItem	[representation of QTreeWidgetItem]

	-	type:		item-clone
		item:		[item name]

	-	type:		variable
		variable:	[variable name]

	-	type:			item-snippet
		main-item-name:	[suggested name]

		items:
			-	item-name:	[suggested name]
				item-type:	[item type]
				script:		[script]
			-	[...]
---
"""

import json
from qtpy import QtCore, QtGui
from libopensesame.oslogging import oslogger
from libopensesame.py3compat import *


# For unknown mimetypes
INVALID_DATA = {
	u'type' : u'invalid'
}


def matches(data, types):

	"""
	desc:
		Checks whether a data dictionary matches any of the specified drop
		types.

	arguments:
		data:
			desc:	A data dictionary. Non-dict types do not give an error, but
					return False.
		types:
			desc:	A list of types, matching the 'type' key in the data dict.
			type:	list

	returns:
		desc:		True if the data matches, False otherwise.
		type:		bool
	"""

	if not isinstance(data, dict):
		return False
	if u'type' not in data:
		return False
	if data[u'type'] not in types:
		return False
	return True

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
	# Reject unknown mimedata
	if not mimedata.hasText() and not mimedata.hasUrls():
		oslogger.warning(u'No text data')
		return INVALID_DATA
	# Process url mimedata
	if mimedata.hasUrls():
		urls = mimedata.urls()
		if len(urls) == 0:
			return INVALID_DATA
		url = urls[0]
		if not url.isLocalFile():
			return INVALID_DATA
		path = str(url.toLocalFile())
		data = {
			u'type': u'url-local',
			u'url': path
		}
		return data
	# Process JSON text data
	text = str(mimedata.text())
	try:
		data = json.loads(text)
	except:
		oslogger.warning(u'Failed to load json mime data')
		return INVALID_DATA
	if not isinstance(data, dict) or u'type' not in data:
		return INVALID_DATA
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

	text = safe_decode(json.dumps(data), enc=u'utf-8')
	mimedata = QtCore.QMimeData()
	mimedata.setText(text)
	drag = QtGui.QDrag(drag_src)
	drag.setMimeData(mimedata)
	drag.exec_()

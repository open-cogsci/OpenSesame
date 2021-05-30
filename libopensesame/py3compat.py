#-*- coding:utf-8 -*-

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

import functools
import sys
import io
import yaml

if sys.version_info >= (3,0,0):
	py3 = True
	basestring = str
	universal_newline_mode = u'r'
else:
	bytes = str
	str = unicode
	py3 = False
	universal_newline_mode = u'rU'
	RecursionError = RuntimeError
	PermissionError = IOError
	FileNotFoundError = OSError


def safe_decode(s, enc='utf-8', errors='strict'):
	if isinstance(s, str):
		return s
	if isinstance(s, bytes):
		return s.decode(enc, errors)
	# Numeric values are encoded right away
	if isinstance(s, (int, float)):
		return str(s)
	# Some types need to be converted to unicode, but require the encoding
	# and errors parameters. Notable examples are Exceptions, which have
	# strange characters under some locales, such as French. It even appears
	# that, at least in some cases, they have to be encodeed to str first.
	# Presumably, there is a better way to do this, but for now this at
	# least gives sensible results.
	if isinstance(s, Exception):
		try:
			return safe_decode(bytes(s), enc=enc, errors=errors)
		except:
			pass
	# For other types, the unicode representation doesn't require a specific
	# encoding. This mostly applies to non-stringy things, such as integers.
	try:
		return str(s)
	except Exception as e:
		from libopensesame.oslogging import oslogger
		oslogger.error(u'%s occurred, returning empty string' % type(e))
		return u''


def safe_encode(s, enc='utf-8', errors='strict'):
	if isinstance(s, bytes):
		return s
	if isinstance(s, str):
		return s.encode(enc, errors)
	try:
		return bytes(s)
	except Exception as e:
		from libopensesame.oslogging import oslogger
		oslogger.error(u'%s occurred, returning empty string' % type(e))
		return b''


def safe_read(path):
	with safe_open(path, u'r') as fd:
		try:
			s = fd.read()
		except UnicodeDecodeError:
			return u''
	return safe_decode(s, errors=u'ignore')


# Depending on the version of yaml, we should pass the Loader keyword or not
if hasattr(yaml, u'FullLoader'):
	def safe_yaml_load(s):
		return yaml.load(s, Loader=yaml.UnsafeLoader)
else:
	def safe_yaml_load(s):
		return yaml.load(s)


if py3:
	safe_str = safe_decode
	safe_open = functools.partial(open, encoding=u'utf-8')
else:
	safe_open = functools.partial(io.open, encoding=u'utf-8')
	safe_str = safe_encode

__all__ = [
	'py3',
	'safe_decode',
	'safe_encode',
	'safe_str',
	'universal_newline_mode',
	'safe_read',
	'safe_open',
	'safe_yaml_load'
]
if not py3:
	__all__ += [
		'str',
		'bytes',
		'RecursionError',
		'PermissionError',
		'FileNotFoundError'
	]
else:
	__all__ += ['basestring']

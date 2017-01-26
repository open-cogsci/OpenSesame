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

from libopensesame import metadata
from libopensesame.py3compat import *
from libqtopensesame.misc.base_subcomponent import base_subcomponent
import re
import os
try:
	import markdown
	from distutils.version import LooseVersion
	# TocExtension() doesn't support the title keyword in previous versions
	# This seems to have been added in 2.6 as part of the depraction of the 
	# HeaderID extension: 
	# https://github.com/waylan/Python-Markdown/releases/tag/2.6-final
	if LooseVersion(markdown.version) > LooseVersion(u'2.6'):
		from markdown.extensions import attr_list, extra, toc
	else:
		from libopensesame import debug
		debug.msg(u'Markdown disabled for markdown version: {}'.format(markdown.version))
		markdown = None
except:
	from libopensesame import debug
	debug.msg(u'Unable to import markdown, proceeding without markdown')
	markdown = None
try:
	from pygments import highlight
	if py3:
		from pygments.lexers import Python3TracebackLexer as TracebackLexer
		from pygments.lexers import Python3Lexer as PythonLexer
	else:
		from pygments.lexers import PythonTracebackLexer as TracebackLexer
		from pygments.lexers import PythonLexer as PythonLexer
	from pygments.formatters import HtmlFormatter
except:
	highlight = None
from libqtopensesame.misc.translate import translation_context
_ = translation_context(u'markdown', category=u'core')

class markdown_parser(base_subcomponent):

	"""
	desc:
		A Markdown parser with syntax highlighting.
	"""

	def __init__(self, main_window):

		"""
		desc:
			Constructor.

		arguments:
			main_window:	The main-window object.
		"""

		self.setup(main_window)
		self.css = u'<style type="text/css">'
		with safe_open(self.main_window.theme.resource(u'markdown.css')) as fd:
			self.css += fd.read() % {u'background_image' : \
				os.path.abspath(self.main_window.theme.resource(
				u'background.png'))}
		if highlight is not None:
			self.traceback_lexer = TracebackLexer()
			self.python_lexer = PythonLexer()
			self.html_formatter = HtmlFormatter()
			self.css += self.html_formatter.get_style_defs(u'.highlight')
			self.re_script = re.compile(
				r'^~~~\s*.(?P<syntax>\w+)(?P<script>.*?)^~~~', re.S | re.M)
		self.css += u'</style>'
		if markdown is not None:
			self.ext = [attr_list.AttrListExtension(), extra.ExtraExtension(),
				toc.TocExtension(title=u'Overview'),
				u'markdown.extensions.tables']
		self.footer = u'''
<p>
<a class="dismiss-button" href="opensesame://action.close_current_tab">%s</a>
</p>

<div class="footer">
OpenSesame %s %s —
Copyright <a href="http://www.cogsci.nl/smathot">Sebastiaan Mathôt</a> 2010-2016
</div>
''' % (_(u'Dismiss this message'), metadata.__version__, metadata.codename)

	def highlight(self, md):

		"""
		desc:
			Replaces ~~~ blocks with syntax-highlighted HTML code.

		arguments:
			md:
				desc:	A Markdown  string.
				type:	str

		returns:
			desc:	A Markdown  string.
			type:	str
		"""

		if highlight is None:
			return md
		while True:
			m = re.search(self.re_script, md)
			if m is None:
				break
			orig = m.group()
			syntax = m.group(u'syntax')
			script = m.group(u'script')
			if syntax == u'traceback':
				lexer = self.traceback_lexer
			elif syntax == u'python':
				lexer = self.python_lexer
			else:
				md = md.replace(orig, u'<code>%s</code>\n' % script)
				continue
			new = highlight(script, lexer, self.html_formatter)
			md = md.replace(orig, new)
		return md

	def to_html(self, md):

		"""
		desc:
			Converts Markdown to HTML.

		arguments:
			md:
				desc:	A Markdown  string.
				type:	str

		returns:
			desc:	A Markdown  string.
			type:	str
		"""

		md = self.highlight(md)
		if markdown is None:
			return u'<pre>%s</pre>' % md
		html = markdown.markdown(md, extensions=self.ext, errors=u'ignore') \
			+ self.css + self.footer
		if html.startswith(u'<p>title:'):
			title, body = tuple(html.split(u'\n', 1))
			html = u'<h1>%s</h1>\n\n%s' % (title[9:-4], body)
		return html

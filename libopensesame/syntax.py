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

import shlex
import re
import codecs
import os
import yaml
from distutils.version import StrictVersion
from libopensesame import metadata
from libopensesame.exceptions import osexception
from libopensesame.py3compat import *


class Syntax:

    """
    desc:
            The `syntax` class implement text operations, including those that are
            necessary for interpreting OpenSesame script.
    """

    def __init__(self, experiment):
        """
        desc:
                Constructor.

        arguments:
                experiment:	The experiment object.
        """

        self.experiment = experiment
        # A regular expression to match keywords, which are characterized by:
        # - Start with a letter or underscore
        # - Consists only of letters, numbers, or underscores, except for
        # - The last character, which is an equals sign
        self.re_cmd = re.compile(r'\A[_a-zA-Z]+[_a-zA-Z0-9]*=')
        # A regular expression to match [variables] in text. The first part
        # indictates that we don't match items preceded by a slash
        # (\[variables]). This introduces a problem in that the slash itself can
        # also be escaped. To deal with this we eat up any even number of
        # slashes (\\\\)* so that only sequences preceded by an odd number of
        # slashes are preserved.
        self.re_txt = re.compile(
            r'(?<!\\)(\\\\)*(\[[_a-zA-Z]+[_a-zA-Z0-9]*\])')
        # A regular expression to match inline Python statements, like so:
        # [=10*10]
        # [\[test\]]
        self.re_txt_py = re.compile(r'(?<!\\)(\\\\)*(\[=.*?[^\\]\])')
        # Catch single equals signs
        self.re_single_eq = re.compile(r'(?<![=!<>])(=)(?!=)')
        # Catch 'never' and 'always'
        self.re_never = re.compile(r'\bnever\b', re.I)
        self.re_always = re.compile(r'\balways\b', re.I)
        # Strict no-variables is used to remove all characters except
        # alphanumeric ones
        self.re_sanitize_strict_novars = re.compile(r'[^\w]')
        # Strict with variables is used to remove all characters except
        # alphanumeric ones and [] signs that indicate variables
        self.re_sanitize_strict_vars = re.compile(r'[^\w\[\]]')
        # Matches valid variable names
        self.re_valid_var_name = re.compile(r'\A[_a-zA-Z]+[_a-zA-Z0-9]*\Z')
        # Loose is used to remove double-quotes, slashes, and newlines
        self.re_sanitize_loose = re.compile(r'[\n\"\\]')
        # Unsanitization is used to replace U+XXXX unicode notation
        self.re_from_ascii = re.compile(r'U\+([A-F0-9]{4})')
        self.re_front_matter = re.compile(r'---(?P<info>.*?)---', re.S)

    def auto_type(self, val):
        """
        desc:
                Casts a value to its best-fitting type, i.e. float, int, or unicode.

        arguments:
                val:	A value of any type.

        returns:
                An auto-typed value.
        """

        try:
            f = float(val)
            # No flanking whitespace
            if isinstance(val, str):
                assert(val == val.strip())
        except:
            return safe_decode(val, errors=u'ignore')
        if int(f) == f:
            return int(f)
        return f

    def parse_front_matter(self, s):
        """
        desc:
                Parses the YAML front matter at the start of the script.

        arguments:
                s:
                        desc:	The script.
                        type:	str

        returns:
                desc:	A (d, s) tuple, where d is a dict with the front matter, and
                                and s is the script with the front matter stripped off.
                type:	dict
        """

        m = self.re_front_matter.match(s)
        try:
            d = safe_yaml_load(m.group(u'info'))
            s = s[len(m.group(0)):]
        except:
            d = {}
        # The API can be stored in a few ways:
        # - Not at all, which was the case in <= v2.9
        # - As a single value, in which the case the minor version becomes 0
        # - As a float, which is seen as a major.minor version
        if u'API' not in d:
            d['API'] = StrictVersion(u'1.0')
        elif isinstance(d['API'], int):
            d['API'] = StrictVersion(u'%d.0' % d['API'])
        elif isinstance(d['API'], float):
            d['API'] = StrictVersion(str(d['API']))
        return d, s

    def generate_front_matter(self):
        """
        desc:
                Generates YAML front matter. Any existing front matter is copied,
                except for the `OpenSesame`, `API`, and `Platform` fields, which are
                updated.

        returns:
                desc:	A front matter string.
                type:	str
        """

        self.experiment.front_matter.update({
            'OpenSesame': safe_str(metadata.__version__),
            'API': metadata.api,
            'Platform': os.name
        })
        front_matter = self.experiment.front_matter.copy()
        front_matter[u'API'] = metadata.api.version[0] \
            if metadata.api.version[1] == 0 \
            else float(str(metadata.api))
        return u'---\n%s---\n' % safe_decode(yaml.dump(
            front_matter, default_flow_style=False,
            allow_unicode=True))

    def split(self, s):
        """
        desc:
                A unicode-safe bash-style split function. This is a wrapper around
                shlex.split() which is not unicode-safe on Python 2.

        arguments:
                s:
                        desc:	The string to split.
                        type:	[str, unicode]

        returns:
                desc:	The string split into a list.
                type:	list
        """

        try:
            return shlex.split(s)
        except Exception as e:
            raise osexception(
                u'Failed to parse line "%s". Is there a closing quotation missing?'
                % s, exception=e)

    def parse_cmd(self, cmd):
        """
        desc:
                Parses OpenSesame command strings, which consist of a command,
                optionally followed by arguments, optionally followed by keywords.

                For example:

                        widget 0 0 1 1 label text="Demo text"

                Here, `widget` is the command, `0` through `label` are arguments,
                and `text` is a keyword.

        arguments:
                cmd:
                        desc:	The command string to parse.
                        type:	[str, unicode]

        returns:
                desc:	A (command, arglist, kwdict) tuple.
                type:	tuple
        """

        l = self.split(cmd)
        if len(l) == 0:
            return None, [], {}
        cmd = l[0]
        arglist = []
        kwdict = {}
        for s in l[1:]:
            m = self.re_cmd.match(s)
            if m is not None:
                arg = s[:m.end()-1]
                val = s[m.end():]
                kwdict[arg] = self.auto_type(val)
            else:
                arglist.append(self.auto_type(s))
        return cmd, arglist, kwdict

    def create_cmd(self, cmd, arglist=[], kwdict={}):
        """
        desc:
                Generates a command string.

        arguments:
                cmd:
                        desc:	The command.
                        type:	str

        keywords:
                arglist:
                        desc:	A list of compulsory order-specified arguments.
                        type:	list
                kwdict:
                        desc:	A dict of optional named keywords.
                        type:	dict
        """

        l = [cmd]
        for arg in arglist:
            l.append(self.safe_wrap(arg))
        for key, val in sorted(kwdict.items()):
            l.append(u'%s=%s' % (key, self.safe_wrap(val)))
        return u' '.join(l)

    def eval_text(self, txt, round_float=False, var=None):
        """
        desc:
                Evaluates variables and inline Python in a text string.

                Examples:

                        The resolution is [width] by [height] pixels
                        This evaluates to 100: [=10x10]

        arguments:
                txt:	The string to evaluate. If the input is not a string, then
                                the value will be returned unmodified.

        keywords:
                round_float:
                        desc:	Indicates whether floating point values should be
                                        rounded or not.
                        type:	bool

        returns:
                The evaluated string, or the input value for non-string input.
        """

        def get_escape_sequence(m):
            return u'' if m.group(1) is None \
                else m.group(1)[:len(m.group(1))//2]

        if not isinstance(txt, str):
            return txt
        txt = safe_decode(txt)
        if var is None:
            var = self.experiment.var
        if round_float:
            float_template = u'%%.%sf' % var.round_decimals
        while True:
            m = self.re_txt.search(txt)
            if m is None:
                break
            varname = m.group(2)[1:-1]
            val = var.get(varname)
            if round_float and isinstance(val, float):
                val = float_template % val
            else:
                val = safe_decode(val)
            txt = txt[:m.start(0)] + get_escape_sequence(m) + val \
                + txt[m.end(0):]
        # Detect Python inlines [=10*10]
        while True:
            m = self.re_txt_py.search(txt)
            if m is None:
                break
            py = self.unescape(m.group(2)[2:-1])
            val = self.experiment.python_workspace._eval(py)
            txt = txt[:m.start(0)] + get_escape_sequence(m) + safe_decode(val) \
                + txt[m.end(0):]
        return self.unescape(txt)

    def quotable_symbol(self, s):
        """
        returns:
                desc:	True if s is a symbol that should be quoted in a conditional
                                statement, and False otherwise.
                type:	bool
        """

        # Don't quote operators
        if s in [u'not', u'or', 'and']:
            return False
        # Don't quote special keywords
        if s.lower() in [u'always', u'never']:
            return False
        # Don't quote numeric values
        try:
            int(s)
            return False
        except:
            return True

    def compile_cond(self, cnd, bytecode=True):
        """
        desc:
                Compiles OpenSesame conditional statements.

                Examples:
                        [width] > 100
                        =var.width > 100

        arguments:
                cnd:
                        desc:	The conditional statement to compile.
                        type:	[str, unicode]

        keywords:
                bytecode:
                        desc:	Indicates whether the conditional statement should be
                                        returned as bytecode (True) or a Python string (False).
                        type:	bool

        returns:
                desc:	The conditional statement as a Python string or bytecode.
                type:	[str, bytecode]
        """

        # Python conditions `=True` don't have to be evaluated
        if cnd.startswith(u'='):
            cnd = cnd[1:]
        else:
            # Quote all non-quoted symbols. This can be probably be done through
            # a clever regular expression, but for now we use a simple loop.
            while True:
                in_quote = None
                in_var = False
                symbol_start = None
                for i, ch in enumerate(cnd):
                    # Don't scan within quoted strings
                    if in_quote is None:
                        if ch in u'"\'':
                            in_quote = ch
                            continue
                    elif ch == in_quote:
                        in_quote = None
                        continue
                    if in_quote:
                        continue
                    # Don't scan within variable definitions
                    if ch == u'[':
                        in_var = True
                        continue
                    elif ch == u']':
                        in_var = False
                        continue
                    if in_var:
                        continue
                    # Detect symbols starts, i.e. the first alphanumeric
                    # character or underscore
                    if ch.isalnum() or ch == u'_':
                        if symbol_start is None:
                            symbol_start = i
                    # Detect symbol ends, i.e. the first non-alphanumeric
                    # character after an alphanumeric character or an
                    # underscore.
                    elif symbol_start is not None:
                        symbol = cnd[symbol_start:i]
                        symbol_range = symbol_start, i
                        symbol_start = None
                        if not self.quotable_symbol(symbol):
                            continue
                        cnd = cnd[:symbol_range[0]] + u'"' + symbol + u'"' \
                            + cnd[symbol_range[1]:]
                        break
                else:
                    # The for-else clause happens when the for loop was not
                    # broken. If no break occurred, then nothing was quoted,
                    # and we don't need to restart the for loop, i.e. we can
                    # break the infinite while. We only need to check that there
                    # was no symbol still being processed, in which case it
                    # needs to be quoted.
                    if symbol_start is not None:
                        symbol = cnd[symbol_start:]
                        if self.quotable_symbol(symbol):
                            cnd = cnd[:symbol_start] + u'"' + symbol + u'"'
                    break
            # Replace [variables] by var.variables
            while True:
                m = self.re_txt.search(cnd)
                if m is None:
                    break
                cnd = cnd[:m.start()] + u'var.%s' % m.group()[1:-1] \
                    + cnd[m.end():]
            # Replace single equals signs (=) by doubles (==)
            cnd = self.re_single_eq.sub(u'==', cnd)
            # Replace always and never words by True or False
            cnd = self.re_never.sub(u'False', cnd)
            cnd = self.re_always.sub(u'True', cnd)
        if bytecode:
            try:
                return compile(cnd, u"<conditional statement>", u"eval")
            except:
                raise osexception(
                    u"'%s' is not a valid conditional statement" % cnd)
        return self.unescape(cnd)

    def unescape(self, s):
        """
        desc:
                Unescapes square brackets in text.

        arguments:
                s:
                        desc:	The text to unescape.
                        type:	str

        returns:
                desc:	The unescaped text.
                type:	str
        """

        s = safe_decode(s)
        return s.replace(u'\[', u'[').replace(u'\]', u']')

    def safe_wrap(self, s):
        """
        desc:
                Wraps and escapes a text so that it can safely be embedded in a
                command string. For example:

                He said: "hi"

                would become:

                "He said: \"hi\""

        arguments:
                s:
                        desc:	The text to wrap.
                        type:	str

        returns:
                desc:	The wrapped text.
                type:	str
        """

        s = safe_decode(s).replace(u'\\', u'\\\\')
        try:
            float(s)
            assert(s == s.strip())  # No flanking whitespace
        except:
            t = s.replace(u'_', u'')
            if not t.isalnum() or not t.isascii():
                return u'"%s"' % s.replace(u'"', u'\\"')
        return s

    def sanitize(self, s, strict=False, allow_vars=True):
        """
        desc:
                Removes invalid characters (notably quotes) from the string.

        arguments:
                s:
                        desc:	The string to be sanitized. This can be any type, but
                                        if it is not unicode, it will be coerced to unicode.

        keywords:
                strict:
                        desc:	If True, all except underscores and alphanumeric
                                        characters are stripped.
                        type:	bool
                allow_vars:
                        desc:	If True, square brackets are not sanitized, so you can
                                        use variables.
                        type:	bool

        returns:
                desc:	A sanitized string.
                type:	unicode

        example: |
                # Prints 'Universit Aix-Marseille'
                print(self.sanitize('\"Université Aix-Marseille\"'))
                # Prints 'UniversitAixMarseille'
                print(self.sanitize('\"Université Aix-Marseille\""', strict=True))
        """

        s = safe_decode(s)
        if strict:
            if allow_vars:
                return self.re_sanitize_strict_vars.sub(u'', s)
            return self.re_sanitize_strict_novars.sub(u'', s)
        return self.re_sanitize_loose.sub(u'', s)

    def to_ascii(self, s, strict=False):
        """
        desc:
                Converts all non-ASCII characters to U+XXXX notation, so that the
                resulting string can be treated as plain ASCII text.

        arguments:
                s:
                        desc:	A unicode string to be santized
                        type:	unicode

        keywords:
                strict:
                        desc:	If True, special characters are ignored rather than
                                        recoded.
                        type:	bool

        returns:
                desc:	A regular Python string with all special characters replaced
                                by U+XXXX notation or ignored (if strict).
                type:	str
        """

        if strict:
            _s = safe_encode(s, enc=u'ascii', errors=u'ignore')
        else:
            _s = codecs.encode(s, u'ascii', u'osreplace')
        _s = safe_decode(_s)
        return _s.replace(os.linesep, u'\n')

    def from_ascii(self, s):
        """
        desc:
                Converts an ascii str with U+XXXX notation to actual Unicode.

        arguments:
                s:
                        desc:	A plain-ascii string.
                        type:	str

        returns:
                desc:	A string with all U+XXXX characters converted to the corresponding
                                unicode characters.
                type:	unicode
        """

        if not isinstance(s, str):
            raise osexception(
                u'from_ascii() expects first argument to be unicode or str, not "%s"'
                % type(s))
        s = safe_decode(s)
        while True:
            m = self.re_from_ascii.search(s)
            if m is None:
                break
            s = s.replace(m.group(0), chr(int(m.group(1), 16)), 1)
        return s

    def valid_var_name(self, s):
        """
        desc:
                Checks whether a string is a valid variable name.

        arguments:
                s:
                        desc:	The string to check.
                        type:	str

        returns:
                type:	True if s is a variable valid name, False if not.
        """

        return re.match(self.re_valid_var_name, s)


def osreplace(exc):
    """
    desc:
            A replacement function to allow opensame-style replacement of unicode
            characters.

    arguments:
            exc:
                    type:	UnicodeEncodeError

    returns:
            desc:	A (replacement, end) tuple.
            type:	tuple
    """

    _s = u''
    for ch in exc.object[exc.start:exc.end]:
        _s += u'U+%.4X' % ord(ch)
    return _s, exc.end


codecs.register_error(u'osreplace', osreplace)
# Alias for backwards compatibility
syntax = Syntax

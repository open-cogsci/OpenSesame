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
from libqtopensesame.items.inline_script import InlineScript
from libopensesame.oslogging import oslogger
oslogger.start('unittest')


def test_extract_assignments():
    test_script = '''
def fnc():
    global d
    d = 1
    x = 1

a = 1
var.b = 1
while True:
    c = 1
for i in range(10):
    e = 1
'''    
    assignments = InlineScript._extract_assignments(test_script)
    assert sorted(assignments) == ['a', 'b', 'c', 'd', 'e']

def test_ensure_space_indent_pure_tabs():
    """Tabs should be converted to the default 4-space indent when no
    space-indented lines are available for autodetection.
    """
    script = 'def foo():\n\tif True:\n\t\tpass\n\treturn 1\n'
    expected = 'def foo():\n    if True:\n        pass\n    return 1'
    assert InlineScript._ensure_space_indent(script) == expected

def test_ensure_space_indent_autodetect_4():
    """Tabs should be converted using the indent width autodetected from
    existing space-indented lines (4 spaces in this case).
    """
    script = 'def foo():\n    if True:\n\t\tprint("hello")\n    return 1\n'
    expected = 'def foo():\n    if True:\n        print("hello")\n    return 1'
    assert InlineScript._ensure_space_indent(script) == expected

def test_ensure_space_indent_autodetect_2():
    """Autodetection should work for 2-space indentation styles.
    """
    script = 'def foo():\n  if True:\n\t\tprint("hello")\n  return 1\n'
    expected = 'def foo():\n  if True:\n    print("hello")\n  return 1'
    assert InlineScript._ensure_space_indent(script) == expected

def test_ensure_space_indent_no_tabs():
    """Scripts that already use space indentation should be returned
    unchanged.
    """
    script = 'def foo():\n    if True:\n        pass\n    return 1\n'
    expected = 'def foo():\n    if True:\n        pass\n    return 1'
    assert InlineScript._ensure_space_indent(script) == expected

def test_ensure_space_indent_empty():
    """An empty string should be returned unchanged.
    """
    assert InlineScript._ensure_space_indent('') == ''

def test_ensure_space_indent_mixed_tab_space():
    """Mixed tab and space leading whitespace on the same line should be
    handled correctly via expandtabs.
    """
    script = 'def foo():\n\t  if True:\n\t  \tprint("x")\n'
    expected = 'def foo():\n      if True:\n        print("x")'
    assert InlineScript._ensure_space_indent(script) == expected

def test_ensure_space_indent_no_trailing_newline():
    """Conversion should work correctly even when the input has no
    trailing newline.
    """
    script = 'def foo():\n\tpass'
    expected = 'def foo():\n    pass'
    assert InlineScript._ensure_space_indent(script) == expected

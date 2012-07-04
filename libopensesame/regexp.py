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

import re

# Strict no-variables is used to remove all characters except
# alphanumeric ones
sanitize_strict_novars = re.compile(r'[^\w]')		

# Strict with variables is used to remove all characters except
# alphanumeric ones and [] signs that indicate variables
sanitize_strict_vars = re.compile(r'[^\w\[\]]')		
# Loose is used to remove double-quotes, slashes, and newlines
sanitize_loose = re.compile(r'[\n\"\\]')		

# Unsanitization is used to replace U+XXXX unicode notation
unsanitize = re.compile( \
	r'U\+([A-F0-9]{4})')

# Used to find variables in a string
find_variable = re.compile(r'\[\w+\]')

# Used to convert arbitrary strings into valid Python variable names
sanitize_var_name = re.compile('\W|^(?=\d)')

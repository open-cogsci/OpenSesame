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

from libopensesame.py3compat import *
from libopensesame.exceptions import osexception
from libopensesame import item
from datamatrix import operations, DataMatrix
from pseudorandom import Enforce, MaxRep, MinDist, InvalidConstraint
import openexp.keyboard

class loop(item.item):

	"""A loop item runs a single other item multiple times"""

	description = u'Repeatedly runs another item'
	valid_orders = u'sequential', u'random'
	commands = [
		u'fullfactorial',
		u'shuffle',
		u'shuffle_horiz',
		u'slice',
		u'sort',
		u'sortby',
		u'reverse',
		u'roll',
		u'weight',
		]

	def reset(self):

		"""See item."""

		self.ef = None
		self.dm = DataMatrix(length=0)
		self.live_dm = None
		self.live_row = None
		self.operations = []
		self._item = u''

		self.var.repeat = 1
		self.var.continuous = u'no'
		self.var.order = u'random'
		self.var.break_if = u'never'
		self.var.break_if_on_first = u'yes'
		self.var.source = u'table' # file or table
		self.var.source_file = u''

	def from_string(self, string):

		"""See item."""

		self.var.clear()
		self.comments = []
		self.reset()
		if string is None:
			return
		for i in string.split(u'\n'):
			self.parse_variable(i)
			cmd, arglist, kwdict = self.syntax.parse_cmd(i)
			if cmd == u'run':
				if len(arglist) != 1 or kwdict:
					raise osexception(u'Invalid run command: %s' % i)
				self._item = arglist[0]
				continue
			if cmd == u'setcycle':
				if self.ef is not None or self.operations:
					raise osexception(
						u'setcycle must come before constraints and operations')
				if len(arglist) != 3 or kwdict:
					raise osexception(u'Invalid setcycle command: %s' % i)
				row, var, val = tuple(arglist)
				if row >= len(self.dm):
					self.dm.length = row+1
				if var not in self.dm:
					self.dm[var] = u''
				self.dm[row][var] = val
				continue
			if cmd == u'constrain':
				if self.operations:
					raise osexception(
						u'constraints must come before operations')
				if self.ef is None:
					self.ef = Enforce(self.dm)
				if len(arglist) != 1:
					raise osexception(u'Invalid constrain command: %s' % i)
				colname = arglist[0]
				try:
					col = self.dm[colname]
				except:
					raise osexception(u'Invalid column name: %s' % colname)
				for constraint, value in kwdict.items():
					try:
						if constraint == u'maxrep':
							self.ef.add_constraint(MaxRep, cols=[col],
								maxrep=value)
							continue
						if constraint == u'mindist':
							self.ef.add_constraint(MinDist, cols=[col],
								mindist=value)
							continue
					except InvalidConstraint as e:
						raise osexception(e)
					raise osexception(u'Invalid constrain command: %s' % i)
				continue
			if cmd in self.commands:
				self.operations.append( (cmd, arglist) )
		if len(self.dm) == 0:
			self.dm.length = 1
		if len(self.dm.columns) == 0:
			self.dm.empty_column = u''
		# Backwards compatibility: Older version of OpenSesame can specify the
		# number of cycles through the cycles variable. If the specified number
		# of cycles doesn't match the length of the datamatrix, we change the
		# length of the datamatrix.
		if u'cycles' in self.var and isinstance(self.var.cycles, int) \
				and self.var.cycles != len(self.dm):
			self.dm.length = self.var.cycles

	def to_string(self):

		"""See item."""

		# Older versions of OpenSesame use an explicit cycles variable, so we
		# set this here for backwards compatibility.
		self.var.cycles = len(self.dm)
		s = item.item.to_string(self)
		for i, row in enumerate(self.dm):
			for name, val in row:
				s += u'\t%s\n' % \
					self.syntax.create_cmd(u'setcycle', [i, name, val])
		if self.ef is not None:
			d = {}
			for constraint in self.ef.constraints:
				col = constraint.cols[0]
				if col not in d:
					d[col] = {}
				if isinstance(constraint, MaxRep):
					d[col][u'maxrep'] = constraint.maxrep
				elif isinstance(constraint, MinDist):
					d[col][u'mindist'] = constraint.mindist
			for col, kwdict in d.items():
				s += u'\t%s\n' % self.syntax.create_cmd(u'constrain', [col],
					kwdict)
		for cmd, arglist in self.operations:
			s += u'\t%s\n' % self.syntax.create_cmd(cmd, arglist)
		s += u'\t%s\n' % self.syntax.create_cmd(u'run', [self._item])
		return s

	def _require_arglist(self, cmd, arglist, minlen=1):

		"""
		desc:
			Checks whether a non-empty argument list has been specified, and
			raises an Exception otherwise.

		arguments:
			cmd:
				desc:	The command to check for.
				type:	str
			arglist:
				desc:	The argument list to check.
				type:	list
		"""

		if len(arglist) < minlen:
			raise osexception(u'Invalid argument list for %s' % cmd)

	def _create_live_datamatrix(self):

		"""
		desc:
			Builds a live DataMatrix. That is, it takes the orignal DataMatrix
			and applies all the operations as specified.

		returns:
			desc:	A live DataMatrix.
			type:	DataMatrix
		"""

		if self.var.source == u'table':
			src_dm = self.dm
		else:
			from datamatrix import io
			src = self.experiment.pool[self.var.source_file]
			if src.endswith(u'.xlsx'):
				try:
					src_dm = io.readxlsx(src)
				except Exception as e:
					raise osexception(u'Failed to read .xlsx file: %s' % src,
						exception=e)
			else:
				try:
					src_dm = io.readtxt(src)
				except Exception as e:
					raise osexception(u'Failed to read text file (perhaps it has the wrong format or it is not utf-8 encoded): %s' % src,
						exception=e)
		for column_name in src_dm.column_names:
			if not self.syntax.valid_var_name(column_name):
				raise osexception(
					'The loop table contains an invalid column name: 'u'\'%s\'' \
					% column_name)
		length = int(len(src_dm) * self.var.repeat)
		dm = DataMatrix(length=0)
		while len(dm) < length:
			i = min(length-len(dm), len(src_dm))
			if self.var.order == u'random':
				dm <<= operations.shuffle(src_dm)[:i]
			else:
				dm <<= src_dm[:i]
		if self.var.order == u'random':
			dm = operations.shuffle(dm)
		if self.ef is not None:
			self.ef.dm = dm
			dm = self.ef.enforce()
		for cmd, arglist in self.operations:
			# The column name is always specified last, or not at all
			if arglist:
				try:
					colname = arglist[-1]
					col = dm[colname]
				except:
					raise osexception(
						u'Column %s does not exist' % arglist[-1])
			if cmd == u'fullfactorial':
				dm = operations.fullfactorial(dm)
			elif cmd == u'shuffle':
				if not arglist:
					dm = operations.shuffle(dm)
				else:
					dm[colname] = operations.shuffle(col)
			elif cmd == u'shuffle_horiz':
				if not arglist:
					dm = operations.shuffle_horiz(dm)
				else:
					dm = operations.shuffle_horiz(
						*[dm[_colname] for _colname in arglist])
			elif cmd == u'slice':
				self._require_arglist(cmd, arglist, minlen=2)
				dm = dm[arglist[0]: arglist[1]]
			elif cmd == u'sort':
				self._require_arglist(cmd, arglist)
				dm[colname] = operations.sort(col)
			elif cmd == u'sortby':
				self._require_arglist(cmd, arglist)
				dm = operations.sort(dm, by=col)
			elif cmd == u'reverse':
				if not arglist:
					dm = dm[::-1]
				else:
					dm[colname] = col[::-1]
			elif cmd == u'roll':
				self._require_arglist(cmd, arglist)
				steps = arglist[0]
				if not isinstance(steps, int):
					raise osexception(u'roll steps should be numeric')
				if len(arglist) == 1:
					dm = dm[-steps:] << dm[:-steps]
				else:
					dm[colname] = list(col[-steps:]) + list(col[:-steps])
			elif cmd == u'weight':
				self._require_arglist(cmd, arglist)
				dm = operations.weight(col)
		return dm

	def prepare(self):

		"""See item."""

		item.item.prepare(self)
		# Deprecation errors. The direct reference to __vars__ prevents a lookup
		# in the parent var store.
		if (u'skip' in self.var.__vars__ and self.var.skip != 0) \
			or (u'offset' in self.var.__vars__ and self.var.offset != u'no'):
			raise osexception(
				u'The skip and offset options have been removed. Please refer to the documentation of the loop item for more information.')
		# Compile break-if statement
		break_if = self.var.get(u'break_if', _eval=False)
		if break_if not in (u'never', u''):
			self._break_if = self.syntax.compile_cond(break_if)
		else:
			self._break_if = None
		# Create a keyboard to flush responses between cycles
		self._keyboard = openexp.keyboard.keyboard(self.experiment)
		# Make sure the item to run exists
		if self._item not in self.experiment.items:
			raise osexception(
				u"Could not find item '%s', which is called by loop item '%s'" \
				% (self._item, self.name))

	def run(self):

		"""See item."""

		self.set_item_onset()
		if self.live_dm is None or self.var.continuous == u'no':
			self.live_dm = self._create_live_datamatrix()
			self.live_row = 0
		first = True
		while self.live_row < len(self.live_dm):
			self.experiment.var.repeat_cycle = 0
			self.experiment.var.live_row = self.live_row
			self.experiment.var.set('live_row_%s' % self.name, self.live_row)
			for name, val in self.live_dm[self.live_row]:
				if isinstance(val, basestring) and val.startswith(u'='):
					val = self.python_workspace._eval(val[1:])
				self.experiment.var.set(name, val)
			# Evaluate the run if statement
			if self._break_if is not None and \
				(not first or self.var.break_if_on_first == u'yes'):
				self.python_workspace[u'self'] = self
				if self.python_workspace._eval(self._break_if):
					break
			# Run the item!
			self.experiment.items.execute(self._item)
			# If the repeat_cycle flag was set, run the item again later
			if self.experiment.var.repeat_cycle:
				self.live_dm <<= self.live_dm[self.live_row:self.live_row+1]
				if self.var.order == u'random':
					self.live_dm = self.live_dm[:self.live_row+1] \
						<< operations.shuffle(self.live_dm[self.live_row+1:])
			self.live_row += 1
			first = False
		else:
			# If the loop finished without breaking, it needs to be reset on
			# the next run of the loop item
			self.live_row = None
			self.live_dm = None

	def var_info(self):

		"""See item."""

		return item.item.var_info(self) + [ (colname, safe_decode(col)) \
			for colname, col in self.dm.columns]

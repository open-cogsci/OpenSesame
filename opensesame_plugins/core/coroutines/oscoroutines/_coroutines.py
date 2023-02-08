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
from libopensesame.py3compat import *
from libopensesame.item import Item
from . import ItemTask, InlineTask


class Coroutines(Item):

    def reset(self):
        """See item."""
        self.var.duration = 5000
        self.var.flush_keyboard = u'yes'
        self.var.function_name = u''
        self.var.end_after_item = u''
        self.schedule = []
        self._events = []
        self.pre_cycle_functions = []
        self.post_cycle_functions = []

    def event(self, msg):

        self._events.append((self.clock.time(), msg))

    @property
    def event_log(self):

        return u'\n'.join([u'%d: %s' % (t, msg) for t, msg in self._events])

    def is_coroutine(self, item_name):
        return hasattr(self.experiment.items[item_name], u'coroutine')

    def is_oneshot_coroutine(self, item_name):
        try:
            return self.experiment.items[item_name].is_oneshot_coroutine
        except AttributeError:
            return False

    def from_string(self, string):
        self.var.clear()
        self.comments = []
        self.reset()
        if string is None:
            return
        for s in string.split(u'\n'):
            self.parse_variable(s)
            # run item_name start=1000 end=2000 runif="always"
            cmd, arglist, kwdict = self.syntax.parse_cmd(s)
            if cmd != u'run' or not len(arglist):
                continue
            item_name = arglist[0]
            start_time = kwdict.get(u'start', 0)
            end_time = kwdict.get(u'end', 0)
            cond = kwdict.get(u'runif', u'always')
            self.schedule.append((item_name, start_time, end_time, cond))

    def to_string(self):
        s = super().to_string()
        for item_name, start_time, end_time, cond in self.schedule:
            # If the item doesn't exist yet, then we simply go with the times
            # from the schedule. This happens during loading, if the
            # coroutines script is parsed before the scripts of the items that
            # are in it.
            if (
                    item_name in self.experiment.items and
                    self.is_oneshot_coroutine(item_name)
            ):
                end_time = start_time
            s += u'\t' + self.syntax.create_cmd(u'run', [item_name], {
                u'start': start_time,
                u'end': end_time,
                u'runif': cond
            }) + u'\n'
        return s

    def prepare(self):
        super().prepare()
        self.event('prepare coroutines')
        self._schedule = []
        for item_name, start_time, end_time, cond in self.schedule:
            if not self.python_workspace._eval(self.syntax.compile_cond(cond)):
                continue
            t = ItemTask(
                self, self.experiment.items[item_name],
                self.syntax.auto_type(self.syntax.eval_text(start_time)),
                self.syntax.auto_type(self.syntax.eval_text(end_time)),
                abort_on_end=item_name == self.var.end_after_item
            )
            self._schedule.append(t)
        if self.var.function_name != u"":
            t = InlineTask(self, self.var.function_name, self.python_workspace,
                           0, self.var.duration)
            self._schedule.append(t)

    def run(self):
        """See item."""
        # Launch all coroutines
        for task in self._schedule:
            task.launch()
        self._schedule.sort(key=lambda task: task.start_time)
        dt = 0
        active = []
        t0 = self.clock.time()
        i = 0
        running = True
        while running and dt < self.var.duration:
            # Activate coroutines by start time
            while self._schedule and self._schedule[0].started(dt):
                active.append(self._schedule.pop(0))
                active.sort(key=lambda task: task.end_time)
            for fnc in self.pre_cycle_functions:
                fnc()
            # Run all active coroutines. If a task returns alive, it should be
            # kept as an active task; if it returns DEAD, it should be removed
            # from the active tasks; if it returns ABORT, the whole coroutines
            # should be aborted.
            _active = []
            for task in active:
                status = task.step()
                if status == task.ALIVE:
                    _active.append(task)
                    continue
                if status == task.ABORT:
                    running = False
            active = _active
            for fnc in self.post_cycle_functions:
                fnc()
            # De-activate coroutines by end time
            while active and active[0].stopped(dt):
                active.pop(0)
            dt = self.clock.time()-t0
            i += 1
        self.event('killed after %d ms' % (self.clock.time()-t0))
        # Kill pending coroutines
        for task in active:
            task.kill()
        self.event('trampoline took %d ms' % (self.clock.time()-t0))
        self.experiment.var.coroutines_cycles = i
        self.experiment.var.coroutines_duration = dt
        self.experiment.var.coroutines_mean_cycle_duration = 1.*dt/i
        self.event('%d cycles with an average duration of %.4f ms' %
                   (
                       self.experiment.var.coroutines_cycles,
                       self.experiment.var.coroutines_mean_cycle_duration
                   )
                   )

    def var_info(self):
        l = []
        l.append((u"coroutines_cycles", u"[Determined at runtime]"))
        l.append((u"coroutines_duration", u"[Determined at runtime]"))
        l.append((u"coroutines_mean_cycle_duration",
                 u"[Determined at runtime]"))
        return l

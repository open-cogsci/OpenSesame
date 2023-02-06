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
from variable_inspector_cell import variable_inspector_cell
from libqtopensesame.widgets.base_widget import base_widget
from libqtopensesame.misc import drag_and_drop
from libqtopensesame.misc.translate import translation_context
_ = translation_context(u'variable_inspector', category=u'extension')


class variable_inspector_widget(base_widget):

    r"""The variable inspector widget, which includes the table, filter button,
    etc.
    """
    def __init__(self, main_window, ext):
        r"""Constructor.

        Parameters
        ----------
        main_window
            The main-window object.
        ext
            The variable_inspector-extension object.
        """
        super(variable_inspector_widget, self).__init__(
            main_window,
            ui=u'extensions.variable_inspector.variable_inspector'
        )
        self.ext = ext
        self.ui.edit_variable_filter.textChanged.connect(self.refresh)
        self.ui.button_help_variables.clicked.connect(self.ext.open_help)
        self.ui.button_reset.clicked.connect(self._reset)
        self.ui.table_variables.mousePressEvent = self.start_drag
        self._workspace_globals = {}
        self.refresh()

    def focus(self):
        r"""Sets the focus to the filter box."""
        self.ui.edit_variable_filter.setFocus()

    def _reset(self):
        r"""Resets the console, to reset the workspace."""
        self.set_workspace_globals({})
        self.refresh()

    def var(self):
        """
        returns:
                desc:	A (var_store, alive) tuple, where alive indicates whether
                                the var_store is from an active or finished experiment, or
                                from an inactive GUI experiment.
                type:	tuple
        """
        if (
                u'var' in self._workspace_globals and
                hasattr(self._workspace_globals[u'var'], u'inspect')
        ):
            return self._workspace_globals[u'var'], True
        return self.experiment.var, False

    def set_workspace_globals(self, global_dict):
        r"""Sets the workspace global dict.

        Parameters
        ----------
        global_dict
            The workspace global dict
        """
        self._workspace_globals = global_dict

    def start_drag(self, e):
        r"""Starts a variable drag operation.

        Parameters
        ----------
        e : QMousePressEvent
        """
        item = self.ui.table_variables.itemAt(e.pos())
        if item is None:
            return
        row = self.ui.table_variables.row(item)
        var = self.ui.table_variables.item(row, 0).text()
        drag_and_drop.send(
            self.ui.table_variables,
            {
                u'type': u'variable',
                u'variable': var
            }
        )

    def refresh(self):
        r"""Refreshes the table."""
        # Remember the view position
        scrollpos = self.ui.table_variables.verticalScrollBar().sliderPosition()
        col = self.ui.table_variables.currentColumn()
        row = self.ui.table_variables.currentRow()
        filt = str(self.ui.edit_variable_filter.text())
        var_store, alive = self.var()
        self.ui.label_no_heartbeat.setVisible(
            not self.main_window.runner_cls.has_heartbeat())
        self.ui.label_status.setText(
            _(u'Experiment status: <b>%s</b>') % self.main_window.run_status()
        )
        if alive and self.main_window.run_status() == u'finished':
            self.ui.widget_reset_message.show()
        else:
            self.ui.widget_reset_message.hide()
        # Filter the variables if necessary
        if len(filt) > 1:
            d = {
                var: info
                for var, info in var_store.inspect().items()
                if any(
                    q.strip() in var or
                    q.strip() in safe_decode(info[u'value'], errors=u'ignore') or
                    q.strip() in u' '.join(info[u'source'])
                    for q in filt.split(u'|')
                )
            }
        else:
            d = var_store.inspect()
        # Populate the table
        self.ui.table_variables.setRowCount(len(d))
        for i, var in enumerate(sorted(d.keys())):
            info = d[var]
            self.ui.table_variables.setItem(
                i,
                0,
                variable_inspector_cell(var, info)
            )
            self.ui.table_variables.setItem(
                i,
                1,
                variable_inspector_cell(info['value'], info)
            )
            self.ui.table_variables.setItem(
                i,
                2,
                variable_inspector_cell(info['source'], info)
            )
        # Restore the view position
        self.ui.table_variables.setCurrentCell(row, col)
        self.ui.table_variables.verticalScrollBar().setSliderPosition(scrollpos)

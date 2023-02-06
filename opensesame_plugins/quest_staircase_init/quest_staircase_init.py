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
from libopensesame.exceptions import osexception
from libopensesame import plugins
from libopensesame.oslogging import oslogger
from libopensesame.item import item
from libqtopensesame.items.qtautoplugin import qtautoplugin

Quest = None
try:
    import Quest
    oslogger.debug(u'Loading Quest module directly')
except:
    oslogger.debug(u'Failed to load Quest module directly')
if Quest is None:
    try:
        from psychopy.contrib import quest as Quest
        oslogger.debug(u'Loading Quest module from PsychoPy')
    except:
        oslogger.debug(u'Failed to load Quest module from PsychoPy')
if Quest is None:
    try:
        Quest = plugins.load_mod(__file__, u'Quest')
        oslogger.debug(u'Loading Quest module from plug-in folder')
    except:
        oslogger.debug(u'Failed to load Quest module from plug-in folder')
if Quest is None:
    raise osexception(u'Failed to load Quest module.')


class quest_staircase_init(item):

    r"""A plug-in that iniializes a Quest staircase."""
    description = u'Initializes a new Quest staircase procedure'

    def reset(self):
        r"""Initialize default variables."""
        self.var.t_guess = .5
        self.var.t_guess_sd = .25
        self.var.p_threshold = .75
        self.var.beta = 3.5
        self.var.delta = .01
        self.var.gamma = .5
        self.var.test_value_method = u'quantile'
        self.var.min_test_value = 0
        self.var.max_test_value = 1
        self.var.var_test_value = u'quest_test_value'

    def quest_set_next_test_value(self):
        r"""Sets the next test value for the Quest procedure."""
        if self.var.test_value_method == u'quantile':
            self.experiment.quest_test_value = self.experiment.quest.quantile
        elif self.var.test_value_method == u'mean':
            self.experiment.quest_test_value = self.experiment.quest.mean
        elif self.var.test_value_method == u'mode':
            self.experiment.quest_test_value = self.experiment.quest.mode
        else:
            raise osexception(
                u'Unknown test_value_method \'%s\' in quest_staircase_init'
                % self.var.test_value_method)
        test_value = max(self.var.min_test_value, min(
            self.var.max_test_value, self.experiment.quest_test_value()))
        oslogger.debug(u'quest_test_value = %s' % test_value)
        self.experiment.var.quest_test_value = test_value
        self.experiment.var.set(self.var.var_test_value, test_value)

    def prepare(self):
        r"""Prepares the plug-in."""
        self.experiment.quest = Quest.QuestObject(self.var.t_guess,
                                                  self.var.t_guess_sd, self.var.p_threshold, self.var.beta,
                                                  self.var.delta, self.var.gamma)
        self.experiment.quest_set_next_test_value = \
            self.quest_set_next_test_value
        self.experiment.quest_set_next_test_value()

    def var_info(self):
        r"""Gives a list of dictionaries with variable descriptions.

        Returns
        -------
        list
            A list of (name, description) tuples.
        """
        return item.var_info(self) + [(u'quest_test_value',
                                       u'(Determined by Quest procedure)')]


class qtquest_staircase_init(quest_staircase_init, qtautoplugin):

    r"""The GUI part of the plug-in. Controls are defined in info.json."""
    def __init__(self, name, experiment, script=None):
        r"""Constructor.

        Parameters
        ----------
        name
            The name of the plug-in.
        experiment
            The experiment object.
        script, optional
            A definition script.
        """
        quest_staircase_init.__init__(self, name, experiment, script)
        qtautoplugin.__init__(self, __file__)

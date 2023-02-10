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
import os
from libopensesame.experiment import Experiment as ExperimentRuntime
from libopensesame.base_python_workspace import BasePythonWorkspace
import opensesame_plugins
from libqtopensesame.misc.qtplugin_manager import QtPluginManager
from libqtopensesame.misc.qtitem_store import QtItemStore
from libqtopensesame.misc.qtsyntax import QtSyntax
from qtpy import QtCore, QtWidgets, QtGui
from libqtopensesame.misc.translate import translation_context
_ = translation_context(u'experiment', category=u'item')


class Experiment(ExperimentRuntime):

    """Contains various GUI controls for the experiment"""
    def __init__(self, main_window, name, string=None, pool_folder=None,
                 experiment_path=None, resources={}):
        r"""Constructor. The experiment is created automatically be OpenSesame
        and you will generally not need to create it yourself.

        Parameters
        ----------
        main_window : qtopensesame
            The main-window object.
        name : str, unicode
            The name of the experiment.
        string : str, unicode, NoneType, optional
            A string containing the experiment definition, the name of an
            OpenSesame experiment file, or `None` to create a blank experiment.
        pool_folder : str, unicode, NoneType, optional
            A specific folder to be used for the file pool, or `None` to use a
            new temporary folder.
        experiment_path : str, unicode, NoneType, optional
            The path of the experiment file. This will need to be specified
            even if a filename was passed using the `string` keyword.
        resources : dict, optional
            A dictionary with names as keys and paths as values. This serves as
            a look-up table for resources.
        """
        self.main_window = main_window
        self.ui = self.main_window.ui
        self.unused_items = []
        self.core_items = [
            u"loop", u"sequence", u"sketchpad", u"feedback", u"sampler",
            u"synth", u"keyboard_response", u"mouse_response", u"logger",
            u"inline_script"
        ]
        self.items = QtItemStore(self)
        self._syntax = QtSyntax(self)
        self._plugin_manager = QtPluginManager(opensesame_plugins)
        super().__init__(name, string, pool_folder,
                         experiment_path=experiment_path, resources=resources,
                         fullscreen=None,
                         workspace=BasePythonWorkspace(self))

    @property
    def overview_area(self):
        return self.main_window.ui.itemtree

    @property
    def default_title(self):
        return _(u'New experiment')

    @property
    def default_description(self):
        return _(u'Default description')

    def module_container(self):
        """
        Specifies the module that is used to get items from.

        Returns:
        u'libqtopensesame.items'
        """
        return u'libqtopensesame.items'
        
    def item_prefix(self):
        """
        A prefix for the plug-in classes, so that [prefix][plugin] class is used
        instead of the [plugin] class.
        """
        return u'qt'

    def build_item_tree(self, toplevel=None, items=[], max_depth=-1,
                        select=None):
        r"""Builds the overview area for the full experiment.

        Parameters
        ----------
        toplevel, optional
            The toplevel widget.
        items, optional
            A list of items that have already been added, to prevent recursion.
        max_depth, optional
            The maximum depth of the tree.
        select, optional
            The selected item.
        """
        if self.overview_area.locked:
            return
        from libqtopensesame.widgets.tree_unused_items_item import \
            tree_unused_items_item
        from libqtopensesame.widgets.tree_general_item import tree_general_item
        self.treeitem_general = tree_general_item(self)
        self.treeitem_unused = tree_unused_items_item(self.main_window)
        fold_state = self.overview_area.get_fold_state()
        self.overview_area.clear()
        self.overview_area.insertTopLevelItem(0, self.treeitem_general)
        self.overview_area.insertTopLevelItem(1, self.treeitem_unused)
        self.overview_area.set_fold_state(fold_state)
        self.overview_area.scrollToTop()
        if select is not None:
            self.ui.itemtree.select_item(select)

    def rename(self, from_name, to_name):
        """
        Renames an item.
    
        Parameters
        ----------
        from_name : str
            The old name.
        to_name : str
            The new name.
        """
        if self.var.start == from_name:
            self.var.start = to_name

    def check_name(self, name):
        """
        Checks whether a given name is valid. Reasons for not being valid
        are invalid characters or a conflict with an existing name..

        Arguments:
        name	--	The name to check.

        Returns:
        True if the name is allowed, False otherwise.
        """
        if name.strip() == u'':
            return u'Empty names are not allowed.'
        if name.lower() in [item.lower() for item in self.items.keys()]:
            return u'An item with that name already exists.'
        if name != self.syntax.sanitize(name, strict=True, allow_vars=False):
            return u'Name contains special characters. Only alphanumeric characters and underscores are allowed.'
        return True

    def delete(self, item_name, item_parent=None, index=None):
        """Deletes an item.

        Parameters
        ----------
        item_name: str
            The name of the item to be deleted.
        item_parent: str or None, optional
            The parent item. (default=None)
        index: int or None, optional
            The index of the item in the parent sequence, if
        """
        if self.var.start == item_name:
            self.notify(
                u'You cannot delete the entry point of the experiment!')
            return
        for item in self.items:
            self.items[item].delete(item_name, item_parent, index)
        self.main_window.close_item_tab(item_name)


# Alias for backwards compatibility
experiment = Experiment

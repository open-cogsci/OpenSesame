#!/bin/bash
pyuic4 resources/opensesame.ui > libqtopensesame/opensesame_ui.py
pyuic4 resources/opensesamerun.ui > libqtopensesame/opensesamerun_ui.py
pyuic4 resources/general_widget.ui > libqtopensesame/general_widget_ui.py
pyuic4 resources/sketchpad_widget.ui > libqtopensesame/sketchpad_widget_ui.py
pyuic4 resources/sampler_widget.ui > libqtopensesame/sampler_widget_ui.py
pyuic4 resources/synth_widget.ui > libqtopensesame/synth_widget_ui.py
pyuic4 resources/pool_widget.ui > libqtopensesame/pool_widget_ui.py
pyuic4 resources/notification_dialog.ui > libqtopensesame/notification_dialog_ui.py
pyuic4 resources/update_dialog.ui > libqtopensesame/update_dialog_ui.py
pyuic4 resources/tip_dialog.ui > libqtopensesame/tip_dialog_ui.py
pyuic4 resources/loop_wizard_dialog.ui > libqtopensesame/loop_wizard_dialog_ui.py
pyuic4 resources/gabor_dialog.ui > libqtopensesame/gabor_dialog_ui.py
pyuic4 resources/replace_dialog.ui > libqtopensesame/replace_dialog_ui.py
pyuic4 resources/noise_patch_dialog.ui > libqtopensesame/noise_patch_dialog_ui.py
pyuic4 resources/new_loop_sequence.ui > libqtopensesame/new_loop_sequence_ui.py
pyuic4 resources/preferences_widget.ui > libqtopensesame/preferences_widget_ui.py
pyuic4 resources/start_new_dialog.ui > libqtopensesame/start_new_dialog_ui.py
pyrcc4 resources/icons.qrc > libqtopensesame/icons_rc.py


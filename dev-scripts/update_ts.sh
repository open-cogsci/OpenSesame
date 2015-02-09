#!/bin/bash
for locale in translatables it_IT fr_FR zh_CN de_DE ru_RU
do
	echo "Updating $locale"
	pylupdate4 ~/git/QProgEdit/QProgEdit/ui/*.ui \
		resources/ui/dialogs/*.ui resources/ui/widgets/*.ui \
		resources/ui/misc/*.ui dev-scripts/translatables.py -ts \
		resources/ts/$locale.ts
done

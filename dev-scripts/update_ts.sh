#!/bin/bash
for locale in translatables it_IT fr_FR zh_CN de_DE ru_RU
do
	echo "Updating $locale"
	pylupdate4 ~/git/QProgEdit/resources/ui/*.ui \
		resources/ui/*.ui dev-scripts/translatables.py -ts \
		resources/ts/$locale.ts
done

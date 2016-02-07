#!/bin/bash
python3 translation_tools/build_ts.py
for locale in translatables fr_FR it_IT fr_FR zh_CN de_DE ru_RU
do
	echo "processing $locale"
	echo " update ts"
	pylupdate4 \
		resources/ui/dialogs/*.ui \
		resources/ui/widgets/*.ui \
		resources/ui/misc/*.ui \
		translatables-tmp.py -ts \
		resources/ts/$locale.ts
	echo " compile qm"
	lrelease-qt4 resources/ts/$locale.ts -qm resources/locale/$locale.qm
done
# rm translatables-tmp.py

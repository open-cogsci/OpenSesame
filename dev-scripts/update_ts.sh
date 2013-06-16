#!/bin/bash
for locale in translatables it_IT
do
	echo "Updating $locale"
	pylupdate4 resources/ui/*.ui dev-scripts/translatables.py -ts resources/ts/$locale.ts
done

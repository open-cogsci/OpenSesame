#!/bin/bash
for locale in translatables
do
	pylupdate4 resources/ui/*.ui dev-scripts/translatables.py -ts resources/ts/$locale.ts
done

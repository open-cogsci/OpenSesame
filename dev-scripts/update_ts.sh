#!/bin/bash
for locale in en_US en_GB nl_NL fr_FR de_DE es_ES
do
	pylupdate4 resources/ui/*.ui resources/ts/translatables.py -ts resources/ts/$locale.ts
done

#!/bin/bash
for locale in en_US en_GB nl_NL fr_FR de_DE es_ES
do
	lrelease resources/ts/$locale.ts -qm resources/locale/$locale.qm
done



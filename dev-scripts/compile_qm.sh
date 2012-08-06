#!/bin/bash
for locale in en_US en_GB nl_NL fr_FR de_DE es_ES it_IT
do
	lrelease resources/ts/$locale.ts -qm resources/locale/$locale.qm
done



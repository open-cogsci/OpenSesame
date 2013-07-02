#!/bin/bash
for locale in it_IT fr_FR
do
	lrelease resources/ts/$locale.ts -qm resources/locale/$locale.qm
done



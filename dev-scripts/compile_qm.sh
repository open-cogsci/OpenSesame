#!/bin/bash
for locale in it_IT fr_FR zh_CN de_DE
do
	lrelease-qt4 resources/ts/$locale.ts -qm resources/locale/$locale.qm
done



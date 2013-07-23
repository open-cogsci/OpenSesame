#!/bin/bash
for locale in it_IT fr_F zh_CN
do
	lrelease resources/ts/$locale.ts -qm resources/locale/$locale.qm
done



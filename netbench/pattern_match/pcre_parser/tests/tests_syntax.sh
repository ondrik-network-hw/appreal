#!/bin/bash

# Tests if parser can parsed - syntax test
# -i input file with expresions

SCRIPT=$(readlink -f $0)
SCRIPTPATH=`dirname $SCRIPT`

basic_tests=$SCRIPTPATH/../inputs/base.txt
BIN=$SCRIPTPATH/../tester

if [ ! -f $BIN ]; then
	echo "$BIN does not exists"
	exit 1
fi

# zpracuje volitelne vstupy
while [ "$#" -ne 0 ]; do
 case $1 in
	-i) shift; basic_tests=$1;;
esac; shift; done

IFS=$'\012' # novy radek
echo "Test for right patterns, [OK]=parsed, [ERROR]=not parsed"
echo "Tested file: $basic_tests"
for input_pattern in `cut -f1 < $basic_tests` ; do
	echo $input_pattern | $BIN 2>/dev/null 1>/dev/null
	RETURNED=$?
	if [ "x$RETURNED" == "x0" ]; then
		echo "[OK] $input_pattern"
	else
		echo "[ERROR] $input_pattern"
	fi
done

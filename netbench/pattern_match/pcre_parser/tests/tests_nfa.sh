#!/bin/bash

# Tests parser behavior on regexp
# - OK | SYNTAX_ERROR | NFA_ERROR | general ERROR
# - *.pattern file contains one pattern on single line
# -i file with regexps

SCRIPT=$(readlink -f $0)
SCRIPTPATH=`dirname $SCRIPT`

BIN=$SCRIPTPATH/../parser #parser program

if [ ! -f $BIN ]; then
	echo "$BIN does not exists"
	exit 1
fi

input_file=$SCRIPTPATH/../inputs/base.txt

# zpracuje volitelne vstupy
while [ "$#" -ne 0 ]; do
 case $1 in
	-i) shift; input_file=$1;
esac; shift; done

IFS=$'\012' # novy radek
#echo "Test for right patterns, [OK]=parsed, [ERROR]=not parsed"
echo "Tested file: $input_file"
for input_pattern in `cut -f1 < $input_file` ; do
	echo $input_pattern | tr '!' '\!' | $BIN 2>/dev/null 1>/dev/null
	RETURNED=$?
	if [ "x$RETURNED" == "x0" ]; then
		echo "[OK] $input_pattern"
	else if [ "x$RETURNED" == "x1" ]; then
		echo "[SYNTAX_ERROR] $input_pattern"
	else if [ "x$RETURNED" == "x3" ]; then
		echo "[NFA_ERROR] $input_pattern"
	else
		echo "[ERROR] $input_pattern"
	fi; fi; fi
done

exit 0

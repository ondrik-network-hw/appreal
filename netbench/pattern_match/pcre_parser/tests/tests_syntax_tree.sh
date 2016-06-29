#!/bin/bash

# Tests output of compile syntax tree to require output
# - diff *.pattern files to *.out files
# - *.pattern file contains one pattern on single line
# - *.out file contains right DEBUG output

SCRIPT=$(readlink -f $0)
SCRIPTPATH=`dirname $SCRIPT`

BIN=$SCRIPTPATH/../tester #parser program
DIR=$SCRIPTPATH #directory with tests files

if [ ! -f $BIN ]; then
	echo "$BIN does not exists"
	exit 1
fi

for i in $DIR/*.pattern; do

	PATTERN_FILE=$i
	OUT=`echo $i | sed 's/\(.*\)\.pattern/\1.out/g'`

	#echo "DIFF $i:"
	$BIN -d $i < $PATTERN_FILE | diff - $OUT > /dev/null
	RETURNED=$?
	if [ "x$RETURNED" == "x0" ]; then
		echo "[OK] $i"
	else
		echo "[ERROR] $i"
	fi

done;

exit 0

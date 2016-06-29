#!/bin/bash

# Diff output automata of parser to require output (MSFM format)
# - *.pattern file contains one pattern on single line

SCRIPT=$(readlink -f $0)
SCRIPTPATH=`dirname $SCRIPT`

BIN=$SCRIPTPATH/../parser #parser program
DIR=$SCRIPTPATH/ccsymbols #directory with tests files

if [ ! -f $BIN ]; then
	echo "$BIN does not exists"
	exit 1
fi

for i in $DIR/*.pattern; do

	PATTERN_FILE=$i
	OUT=`echo $i | sed 's/\(.*\)\.pattern/\1.msfm/g'`

	if [ -f $OUT ]; then

		#echo "DIFF $i:"
		$BIN -c -s $i < $PATTERN_FILE 1> nfa.msfm 2> /dev/null
		diff nfa.msfm $OUT > /dev/null
		RETURNED=$?
		if [ "x$RETURNED" == "x0" ]; then
			echo "[OK] $i: `cat $i`"
		else
			echo "[DIFF_ERROR] $i: `cat $i`"
		fi
	else
		echo "[OUTPUT_NOT_EXISTS] $i: `cat $i`"
	fi

done;

exit 0

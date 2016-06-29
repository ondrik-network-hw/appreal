#!/bin/bash

# Tests consistency of outputs on 10 same inputs
# - diff *.pattern files to *.out files
# - *.pattern file contains one pattern on single line
# - *.out file contains right DEBUG output

SCRIPT=$(readlink -f $0)
SCRIPTPATH=`dirname $SCRIPT`

BIN=$SCRIPTPATH/../parser #parser program
DIR=$SCRIPTPATH #directory with tests files

if [ ! -f $BIN ]; then
	echo "$BIN does not exists"
	exit 1
fi

PATTERN="/pc?[re]{1,4}[^not]*/"

rm -f diff.log

$BIN -o STDOUT -s $i <<< $PATTERN 1> msfm_ref.tmp 2> /dev/null

for i in {1..10}; do
	$BIN -o STDOUT -s $i <<< $PATTERN 1> msfm.tmp 2> /dev/null

	diff msfm.tmp msfm_ref.tmp >> diff.log
	RETURNED=$?
	if [ "x$RETURNED" == "x0" ]; then
		echo "[OK] $i"
	else
		echo "[DIFF_ERROR] $i"
	fi;
done;

rm msfm_ref.tmp
rm msfm.tmp
rm diff.log

exit 0

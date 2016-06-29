#!/bin/bash

# Make out file to each pattern file

SCRIPT=$(readlink -f $0)
SCRIPTPATH=`dirname $SCRIPT`

BIN=$SCRIPTPATH/../tester #test program
BIN_PARSER=$SCRIPTPATH/../parser #parser program
DIR=$SCRIPTPATH #directory with files

if [ ! -f $BIN ]; then
	echo "$BIN does not exists"
	exit 1
fi

if [ ! -f $BIN_PARSER ]; then
	echo "$BIN_PARSER does not exists"
	exit 1
fi

for i in $DIR/*.pattern; do

	PATTERN_FILE=$i
	OUT=`echo $i | sed 's/\(.*\)\.pattern/\1.out/g'`
	OUT_NFA=`echo $i | sed 's/\(.*\)\.pattern/\1.msfm/g'`

	$BIN -d < $PATTERN_FILE > $OUT 2> /dev/null

	rm -f $OUT_NFA
	$BIN_PARSER -o nfa.msfm < $PATTERN_FILE 1> /dev/null 2> /dev/null
	RETURNED=$?
echo $i
if [ "x$RETURNED" == "x0" ]; then
		mv nfa.msfm $OUT_NFA
	fi

done;

for i in $DIR/ccsymbols/*.pattern; do

	PATTERN_FILE=$i
	OUT_NFA=`echo $i | sed 's/\(.*\)\.pattern/\1.msfm/g'`

	rm -f $OUT_NFA
	$BIN_PARSER -c -o nfa.msfm < $PATTERN_FILE 1> /dev/null 2> /dev/null
	RETURNED=$?
echo $i
if [ "x$RETURNED" == "x0" ]; then
		mv nfa.msfm $OUT_NFA
	fi

done;

for i in $DIR/eof_free/*.pattern; do

	PATTERN_FILE=$i
	OUT_NFA=`echo $i | sed 's/\(.*\)\.pattern/\1.msfm/g'`

	rm -f $OUT_NFA
	$BIN_PARSER -c -o nfa.msfm -E < $PATTERN_FILE 1> /dev/null 2> /dev/null
	RETURNED=$?
echo $i
if [ "x$RETURNED" == "x0" ]; then
		mv nfa.msfm $OUT_NFA
	fi

done;

exit 0

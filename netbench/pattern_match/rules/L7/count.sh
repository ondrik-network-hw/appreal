#!/bin/sh
# Counts the number of input characters/character classes of a set of REs
# Author: Denis Matousek <imatousek@fit.vutbr.cz>

if [ $# -ne 2 ] ; then
	echo "Usage: $0 [PCRE] [PARSER]"
	exit
fi

LINE=1
TOTAL=0

while read -r PCRE ; do
	echo -n $LINE:
	echo $PCRE | $2 > /dev/null || echo "Error at line $LINE"
	COUNT=`grep '^[0-9][0-9]*$' nfa.msfm | tail -1`
	echo $COUNT
	TOTAL=`expr $TOTAL + $COUNT`
	rm -f nfa.msfm
	LINE=`expr $LINE + 1`
done < $1

echo total:$TOTAL

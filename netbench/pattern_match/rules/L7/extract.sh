#!/bin/sh

if [ $# -ne 2 ] ; then
	echo "Usage: $0 [FOLDER] [PARSER]"
	exit
fi

LINE=1

for FILE in $1/* ; do
	# | | | < extract RE | < substitute / with \/ | < add // | < copy to output file | < check with parser
	grep -v -e '^#' -e '^$' < $FILE | head -2 | tail -1 | sed 's/\//\\\//g' | sed 's/.*/\/&\//' | tee -a $1.pcre | $2 > /dev/null || echo "Error at line $LINE"
	LINE=`expr $LINE + 1`
done

rm -f nfa.msfm

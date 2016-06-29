############################################################################
#  Makefile: Particular Makefile in approach
#  Copyright (C) 2012 Brno University of Technology, ANT @ FIT
#  Author(s): Milan Pala, xpalam00@stud.fit.vutbr.cz
############################################################################

# Include base Makefile with common targets
include ../../Makefile.inc

# Name of approach used in his filenames
# e.g.: hybrid_fa.py -> hybrid_fa
APPROACH_NAME=ddfa
PM_BASE  = ../..
DOC_NAME = pattern_match.algorithms.delay_dfa.html
# binary C program
FILE=ddfa

CLEAN += $(FILE) data

# run searching in C program
$(FILE): $(FILE).c
	gcc -std=c99 -pedantic -Wall ${FILE}.c -o ${FILE}
runc: $(FILE)
	echo "POST xxxXXXxxx zblablablunk.kva" > data
	./${FILE} parse data


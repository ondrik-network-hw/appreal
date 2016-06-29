############################################################################
#  Makefile.inc: Base Makefile common for all approach
#  Copyright (C) 2012 Brno University of Technology, ANT @ FIT
#  Author(s): Milan Pala, xpalam00@stud.fit.vutbr.cz
############################################################################

# Python binary in shell path format
PYTHON_BIN=python

# Binary to open documentation in defaul viewer
DOC_OPEN_BIN=xdg-open

# Path from base of Pattern match part of Netbench to documentation root of 
# release
DOC_ROOT=../doc

# Path from algorithm, ... to base directory of pattern match part of Netbench
# Every approach must define this variable
PM_BASE?=.

# Name of documentation file
# Every approach must define this variable
DOC_NAME?=pattern_match.html


# Command to clean all mess in folder
RM=rm -rf
CLEAN=$(RM) *.pyc *.o *.dot *.o *.dot *.msfm *~

# Name of approach used in his filenames
# e.g.: /algorithms/hybrid_fa -> hybrid_fa
# Every approach redefine this variable if name is different then directory
APPROACH_NAME=$(shell basename `pwd`)

.PHONY: test clean run doc help

ifndef OVERRIDE
# Trigger unit tests of approach
test:
	$(PYTHON_BIN) test_$(APPROACH_NAME).py

# Clean current directory
clean:
	$(CLEAN)

# Run example of use of particular approach
run:
	$(PYTHON_BIN) example_of_use.py
endif

# Open Netbench documentation in defaul html viewer
doc:
	$(DOC_OPEN_BIN) $(PM_BASE)/$(DOC_ROOT)/$(DOC_NAME)


# Print help - all Makefile targets
help:
	@echo "Makefile targets:"
	@echo "run   - run example scripts. This target executes scripts example_of_use.py."
	@echo "        Those scripts demonstrate basic use of pattern match algorithm."
	@echo "test  - run unit tests. Use this target to test functionality of the "
	@echo "        pattern match part of Netbench package."
	@echo "doc   - open documentation in default html viewer."
	@echo "clean - clean generated files."
	@echo "help  - this help."
	@echo ""
	@echo "The make command can be executed in directory which contain pattern matching "
	@echo "algorithm, or in parent directories (pattern_match/algorithms/experimental). "
	@echo "If make is executed in parrent directory it will execute the target in all "
	@echo "subsidiary directories (only targets run, test and clean behave this way)."


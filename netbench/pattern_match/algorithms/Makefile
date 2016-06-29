############################################################################
#  Makefile: Makefile for approaches
#  Copyright (C) 2012 Brno University of Technology, ANT @ FIT
#  Author(s): Milan Pala, xpalam00@stud.fit.vutbr.cz
############################################################################
OVERRIDE = yes

# Include base Makefile with common targets
include ../Makefile.inc

# lists all directories in ./algorithms/ directory
APPROACHES = $(shell ls -p ./ | grep "/")

PM_BASE  = ..
DOC_NAME = pattern_match.algorithms.html

# Delegate all targets to each approach
test:
	@-for d in $(APPROACHES); do (cd $$d; $(MAKE) $@); done
run:
	@-for d in $(APPROACHES); do (cd $$d; $(MAKE) $@); done
clean:
	@-for d in $(APPROACHES); do (cd $$d; $(MAKE) $@); done

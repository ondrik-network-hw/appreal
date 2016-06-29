############################################################################
#  Makefile: Particular Makefile in root directory
#  Copyright (C) 2012 Brno University of Technology, ANT @ FIT
#  Author(s): Milan Pala, xpalam00@stud.fit.vutbr.cz
############################################################################
OVERRIDE = yes

# Include base Makefile with common targets
include ./Makefile.inc

APPROACHES_DIR = ./algorithms
TESTS_DIR      = ./tests
PARSER_DIR     = ./pcre_parser

PM_BASE  = .
DOC_NAME = pattern_match.html

.PHONY: test clean doc run help

# 1) test all approaches
# 2) test pattern_match
# 3) test parser
test:
	@-cd $(APPROACHES_DIR) && $(MAKE) test
	@-cd $(TESTS_DIR) && $(MAKE) test
	@-cd $(PARSER_DIR) && $(MAKE) test

# 1) clean approaches
# 2) clean parser
# 3) clean tests
# 4) clean pattern_match
clean:
	@-cd $(APPROACHES_DIR) && $(MAKE) clean
	@-cd $(PARSER_DIR) && $(MAKE) clean
	@-cd $(TESTS_DIR) && $(MAKE) clean
	$(CLEAN)

# Run all example_of_use.py scripts
run: 
	@-cd $(APPROACHES_DIR) && $(MAKE) run


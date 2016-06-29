#!/bin/bash

# Run all test scripts and hide OK message (ERROR messages are)

./tests_ccsymbols.sh | grep -v \[[]OK]
./tests_nfa_ex.sh | grep -v \[[]OK] | grep -v \[[]OUTPUT_NOT_EXISTS]
./tests_eof_free.sh | grep -v \[[]OK] | grep -v \[[]OUTPUT_NOT_EXISTS]
./tests_consistency.sh | grep -v \[[]OK]

exit 0

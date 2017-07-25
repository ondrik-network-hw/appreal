###############################################################################
#
#                          Makefile for PCAP Sanitizer
#
###############################################################################

CFLAGS=-std=c++11 \
  -pedantic-errors \
  -Wextra \
  -Wall \
  -Wfloat-equal \
  -Wctor-dtor-privacy \
  -Weffc++ \
  -Woverloaded-virtual \
  -fdiagnostics-show-option \
  -march=native \
	-g
	# -O2


INCLUDE=-I../../include

LIBS_ADD=-L../../build/src

LIBS=-lpcap


###############################################################################

.PHONY: all clean

all: $(patsubst %.cc,%,$(wildcard *.cc))

%: %.cc
	g++ $(CFLAGS) $(INCLUDE) $(LIBS_ADD) $< $(LIBS) -o $@

clean:
	rm -rf $(patsubst %.cc,%,$(wildcard *.cc))

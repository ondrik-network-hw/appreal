###############################################################################
#
#                          Makefile for PCAP Sanitizer
#
###############################################################################

# TODO: the Makefile is quite messy, someone might try to clean it

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


LIBS=-lpcap


###############################################################################

.PHONY: all clean

all: pcap-sane pcap-histo pcap-freq-extr pcap-enc-filter

pcap-sane: pcap-sane.o pcap-util.o
	g++ $< $(LIBS) pcap-util.o -o $@

pcap-histo: pcap-histo.o pcap-util.o
	g++ $< $(LIBS) pcap-util.o -o $@

pcap-freq-extr: pcap-freq-extr.o pcap-util.o
	g++ $< $(LIBS) pcap-util.o -o $@

pcap-enc-filter: pcap-enc-filter.o pcap-util.o
	g++ $< $(LIBS) random/randtest.o pcap-util.o -o $@

%.o: %.cc
	g++ $(CFLAGS) -c -o $@ $<

%: %.o pcap-util.o
	g++ $< $(LIBS) pcap-util.o -o $@

clean:
	rm -rf $(patsubst %.cc,%,$(wildcard *.cc)) pcap-util.o

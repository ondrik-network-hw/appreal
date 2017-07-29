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


LIBS=-lpcap


###############################################################################

.PHONY: all clean

all: pcap-sane pcap-histo

pcap-sane: pcap-sane.o pcap-util.o
	g++ $< $(LIBS) pcap-util.o -o $@

pcap-histo: pcap-histo.o pcap-util.o
	g++ $< $(LIBS) pcap-util.o -o $@

%.o: %.cc
	g++ $(CFLAGS) -c -o $@ $<

%: %.o pcap-util.o
	g++ $< $(LIBS) pcap-util.o -o $@

clean:
	rm -rf $(patsubst %.cc,%,$(wildcard *.cc)) pcap-util.o

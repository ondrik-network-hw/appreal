// pcap-ex-tractor - extracts payload from a PCAP file.  The output is a file
// where each line contains a payload of a packet in hexa, e.g.:
//
// 00 0A 10 69 FF 45 ...

#include <cassert>
#include <iomanip>
#include <iostream>
#include <fstream>
#include <vector>
#include <tuple>

#include "../pcap-util.hh"

// PCAP-related headers
#include <pcap.h>

size_t total_packets = 0;

// FUNCTION DECLARATIONS
void packetHandler(
	u_char*             userData,
	const pcap_pkthdr*  pkthdr,
	const u_char*       packet);


void print_usage(const char* prog_name)
{
	std::cout << "usage: " << prog_name << " <input.pcap>\n";
}

int main(int argc, char** argv)
{
	if (argc != 2)
	{
		print_usage(argv[0]);
		return EXIT_FAILURE;
	}

	std::string packets_file = argv[1];

	// open capture file for offline processing
	pcap_t *descr = pcap_util::pcap_open(packets_file);

	// start packet processing loop, just like live capture
	if (pcap_loop(descr, 0, packetHandler, nullptr) < 0)
	{
		std::cout << "pcap_loop() failed: " << pcap_geterr(descr);
		return EXIT_FAILURE;
	}

	return EXIT_SUCCESS;
}


void packetHandler(
	u_char* /* userData */,
	const pcap_pkthdr* pkthdr,
	const u_char* packet)
{
	assert(nullptr != pkthdr);
	assert(nullptr != packet);

	const u_char* payload;
	int len;
	std::tie(payload, len) = pcap_util::get_payload(pkthdr, packet);

	if (len < 0) { return; }

	for (size_t i = 0; i < static_cast<size_t>(len); ++i)
	{
		if (i != 0) { std::cout << " "; }
		std::cout << std::hex << std::setw(2) << std::setfill('0') <<
			std::uppercase << static_cast<unsigned>(payload[i]);
	}

	std::cout << "\n";

	++total_packets;
	if (total_packets % 1000 == 0)
	{
		std::cerr << "#";
		std::cerr.flush();
	}
}

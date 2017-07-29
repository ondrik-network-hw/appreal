// pcap-histo - creates a histogram of lengths of packets

#include <cassert>
#include <iostream>
#include <fstream>
#include <vector>
#include <tuple>

#include "pcap-util.hh"

// PCAP-related headers
#include <pcap.h>

const int MAX_LEN = 2047;

size_t total_packets = 0;
std::vector<size_t> packet_lengths(MAX_LEN+1);

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

	std::cout << "\n";
	std::cout << "Total processed packets in " << packets_file << ": " << total_packets << "\n";
	std::cout << "Histogram of lengths of payloads:\n";

	size_t sum = 0;
	for (size_t i = 0; i < 2048; ++i)
	{
		sum += packet_lengths[i];
		if (i % 40 == 0)
		{
			std::cout << i << " " << sum << "\n";
			sum = 0;
		}
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

	++total_packets;

	assert(len >= 0 && len <= MAX_LEN);
	packet_lengths[len] += 1;

	if (total_packets % 1000 == 0)
	{
		std::cout << "#";
		std::cout.flush();
	}
}


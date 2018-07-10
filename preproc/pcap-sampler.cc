// pcap-sampler - samples packets from PCAP file

#include <algorithm>
#include <cassert>
#include <cstring>
#include <iostream>
#include <iomanip>
#include <fstream>
#include <map>
#include <vector>
#include <tuple>
#include <unordered_map>
#include <unordered_set>

#include "pcap-util.hh"

// PCAP-related headers
#include <pcap.h>

// FUNCTION DECLARATIONS
void packetHandler(
	u_char*             userData,
	const pcap_pkthdr*  pkthdr,
	const u_char*       packet);

using Packet = std::pair<pcap_pkthdr, const u_char*>;

// GLOBAL VARIABLES
size_t total_packets = 0;
size_t sampled_packets = 0;
bool keep_encrypted = false;
pcap_dumper_t* dumper = nullptr;
unsigned freq = 0;


void print_usage(const char* prog_name)
{
	std::cout << "usage: " << prog_name << " FREQ <input.pcap> <output.pcap>\n";
}

int main(int argc, char** argv)
{
	if (argc != 4)
	{
		print_usage(argv[0]);
		return EXIT_FAILURE;
	}

	size_t param_start = 2;
	if (argc == 4)
	{
		try
		{
			freq = std::stoi(argv[1]);
			if (freq == 0)
			{
				throw std::runtime_error("0 not allowed!");
			}
		}
		catch (...)
		{
			print_usage(argv[0]);
			return EXIT_FAILURE;
		}
	}
	else
	{
		print_usage(argv[0]);
		return EXIT_FAILURE;
	}

	std::string packets_file = argv[param_start + 0];
	std::string dumper_file = argv[param_start + 1];

	// open capture file for offline processing
	pcap_t *descr = pcap_util::pcap_open(packets_file);

	dumper = pcap_dump_open(descr, dumper_file.c_str());
	if (nullptr == dumper)
	{
		std::cout << "pcap_dump_open() failed: " << pcap_geterr(descr);
		return EXIT_FAILURE;
	}

	// start packet processing loop, just like live capture
	if (pcap_loop(descr, 0, packetHandler, nullptr) < 0)
	{
		std::cout << "pcap_loop() failed: " << pcap_geterr(descr);
		return EXIT_FAILURE;
	}

	std::clog << "\n";
	std::cout << "Total processed packets in " << packets_file << ": " << total_packets << "\n";
	std::cout << "Sampled packets: " << sampled_packets << "\n";

	pcap_dump_close(dumper);

	return EXIT_SUCCESS;
}


void packetHandler(
	u_char* /* userData */,
	const pcap_pkthdr* pkthdr,
	const u_char* packet)
{
	assert(nullptr != pkthdr);
	assert(nullptr != packet);

	++total_packets;

	if (total_packets % freq == 0)
	{
		++sampled_packets;
		pcap_dump((u_char*)dumper, pkthdr, packet);
	}

	if (total_packets % 10000 == 0)
	{
		std::clog << "#";
		std::clog.flush();
	}
}

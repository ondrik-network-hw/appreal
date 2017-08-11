// pcap-enc-filter - filters encrypted traffic

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

extern "C"
{
#include "random/randtest.h"
}

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
size_t filtered_packets = 0;
bool keep_encrypted = false;
pcap_dumper_t* dumper = nullptr;

void print_usage(const char* prog_name)
{
	std::cout << "usage: " << prog_name << " (--in|--out) <input.pcap> <output.pcap>\n";
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
		if (argv[1] == std::string("--in"))
		{
			keep_encrypted = true;
		}
		else if (argv[1] == std::string("--out"))
		{
			keep_encrypted = false;
		}
		else
		{
			print_usage(argv[0]);
			return EXIT_FAILURE;
		}
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
	std::cout << "Filtered packets: " << filtered_packets << "\n";

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

	const u_char* payload;
	int len;
	std::tie(payload, len) = pcap_util::get_payload(pkthdr, packet);
	if (len < 0) { return; }

	// Maybe treat all packets shorter than some threshold unencrypted?
	bool too_short = len < 16;
	if (too_short)
	{
		return;
	}

	// Test statistical properties of the packet payload
	double ent, chisq, mean, montepi, scc;
	rt_init(0);
	rt_add(const_cast<u_char*>(payload), std::min(len,16));
	rt_end(&ent, &chisq, &mean, &montepi, &scc);

	if (!too_short && total_packets < 500)
	{
		std::clog << "Packet #" << total_packets << "\n";
		std::clog << "Length: " << len << "\n";
		std::clog << "Entropy: " << ent << "\n";
		std::clog << "Chi Square: " << chisq << "\n";
		std::clog << "Mean: " << mean << "\n";
		std::clog << "Monte Carlo Pi: " << montepi << "\n";
		std::clog << "Serial Correlation Coefficient: " << scc << "\n";
	}

	// bool matches_enc_test = ent > 6.0;
	bool matches_enc_test = scc < 0.1;

	if ((keep_encrypted && matches_enc_test) ||
		(!keep_encrypted && !matches_enc_test) ||
		(!keep_encrypted && too_short))
	{
		++filtered_packets;
		pcap_dump((u_char*)dumper, pkthdr, packet);
	}

	if (total_packets % 10000 == 0)
	{
		std::clog << "#";
		std::clog.flush();
	}
}

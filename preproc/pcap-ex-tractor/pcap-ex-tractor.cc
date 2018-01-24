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


enum class OutputFormat {TEXT, SPICE};
OutputFormat format = OutputFormat::TEXT;

// FUNCTION DECLARATIONS
void final_loop(
	u_char*             userData,
	const pcap_pkthdr*  pkthdr,
	const u_char*       packet);

void counting_loop(
	u_char*             userData,
	const pcap_pkthdr*  pkthdr,
	const u_char*       packet);


void print_usage(const char* prog_name)
{
	std::cout << "usage: " << prog_name << "[-t|-s] <input.pcap>\n";
	std::cout << "    -t   use text hexa format\n";
	std::cout << "    -s   use SPiCe competition format\n";
}

int main(int argc, char** argv)
{
	if (argc != 3)
	{
		print_usage(argv[0]);
		return EXIT_FAILURE;
	}

	std::string str_format   = argv[1];
	std::string packets_file = argv[2];
	if ("-t" == str_format) {
		format = OutputFormat::TEXT;
	} else if ("-s" == str_format) {
		format = OutputFormat::SPICE;
	} else {
		print_usage(argv[0]);
		return EXIT_FAILURE;
	}

	// open capture file for offline processing
	pcap_t *descr = pcap_util::pcap_open(packets_file);

	if (OutputFormat::SPICE == format) {
		std::cerr << "Initial pass: ";
		if (pcap_loop(descr, 0, counting_loop, nullptr) < 0) {
			std::cout << "pcap_loop() failed: " << pcap_geterr(descr);
			return EXIT_FAILURE;
		}

		std::cerr << "\n";
		std::cout << total_packets << " 256\n";
		total_packets = 0;

		pcap_close(descr);
		descr = nullptr;
		descr = pcap_util::pcap_open(packets_file);
	}

	std::cerr << "Final pass: ";
	// start packet processing loop, just like live capture
	if (pcap_loop(descr, 0, final_loop, nullptr) < 0) {
		std::cout << "pcap_loop() failed: " << pcap_geterr(descr);
		return EXIT_FAILURE;
	}
	std::cerr << "\n";

	return EXIT_SUCCESS;
}


void final_loop(
	u_char*             /* userData */,
	const pcap_pkthdr*  pkthdr,
	const u_char*       packet)
{
	assert(nullptr != pkthdr);
	assert(nullptr != packet);

	const u_char* payload;
	int len;
	std::tie(payload, len) = pcap_util::get_payload(pkthdr, packet);

	if (len < 0) { return; }

	if (OutputFormat::SPICE == format) {
		std::cout << len;

		for (size_t i = 0; i < static_cast<size_t>(len); ++i) {
			std::cout << " ";
			std::cout << static_cast<unsigned>(payload[i]);
		}
	} else {
		assert(OutputFormat::TEXT == format);
		for (size_t i = 0; i < static_cast<size_t>(len); ++i) {
			if (i != 0) { std::cout << " "; }
			std::cout << std::hex << std::setw(2) << std::setfill('0') <<
				std::uppercase << static_cast<unsigned>(payload[i]);
		}
	}

	std::cout << "\n";

	++total_packets;
	if (total_packets % 1000 == 0)
	{
		std::cerr << "#";
		std::cerr.flush();
	}
}

void counting_loop(
	u_char*             /* userData */,
	const pcap_pkthdr*  pkthdr,
	const u_char*       packet)
{
	assert(nullptr != pkthdr);
	assert(nullptr != packet);

	int len;
	std::tie(std::ignore, len) = pcap_util::get_payload(pkthdr, packet);
	if (len < 0) { return; }

	++total_packets;
	if (total_packets % 1000 == 0)
	{
		std::cerr << "#";
		std::cerr.flush();
	}
}

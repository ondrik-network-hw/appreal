// pcap-freq-extr - extracts most common packets from a PCAP file

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
void packetHandlerFirstPass(
	u_char*             userData,
	const pcap_pkthdr*  pkthdr,
	const u_char*       packet);

void packetHandlerSecondPass(
	u_char*             userData,
	const pcap_pkthdr*  pkthdr,
	const u_char*       packet);

using Packet = std::pair<pcap_pkthdr, const u_char*>;

// GLOBAL VARIABLES
const size_t NUM_PACKETS = 50;
size_t total_packets = 0;
std::unordered_map<size_t, size_t> hash_cnt = {};
std::unordered_map<size_t, size_t> hash_to_pick = {};
std::vector<Packet> arr_packets(NUM_PACKETS);

void print_usage(const char* prog_name)
{
	std::cout << "usage: " << prog_name << " <input.pcap> <output.pcap>\n";
}

int main(int argc, char** argv)
{
	if (argc != 3)
	{
		print_usage(argv[0]);
		return EXIT_FAILURE;
	}

	std::string packets_file = argv[1];
	std::string dumper_file = argv[2];

	// open capture file for offline processing
	pcap_t *descr = pcap_util::pcap_open(packets_file);

	std::clog << "First pass: ";
	// start packet processing loop, just like live capture
	if (pcap_loop(descr, 0, packetHandlerFirstPass, nullptr) < 0)
	{
		std::cout << "pcap_loop() failed: " << pcap_geterr(descr);
		return EXIT_FAILURE;
	}

	std::clog << "\n";
	std::cout << "Total processed packets in " << packets_file << ": " << total_packets << "\n";

	std::vector<std::pair<size_t, size_t>> hash_list(hash_cnt.begin(), hash_cnt.end());
	std::sort(hash_list.begin(), hash_list.end(),
		[](std::pair<size_t, size_t> lhs, std::pair<size_t, size_t> rhs){
			return lhs.second > rhs.second;
		});

	for (size_t i = 0; i < NUM_PACKETS; ++i)
	{
		std::cout << std::setfill('0') << std::setw(2) << i+1 << ": ";
		std::cout << std::hex << std::internal << "0x" << std::setfill('0') <<
			std::setw(16) << hash_list[i].first << std::dec;
		std::cout << " [" << hash_list[i].second << "]" << "\n";

		hash_to_pick.insert({hash_list[i].first, i});
	}

	std::clog << "Second pass: ";
	descr = pcap_util::pcap_open(packets_file);
	// start packet processing loop the second time
	if (pcap_loop(descr, 0, packetHandlerSecondPass, nullptr) < 0)
	{
		std::cout << "pcap_loop() failed: " << pcap_geterr(descr);
		return EXIT_FAILURE;
	}

	std::clog << "\n";

	pcap_dumper_t* dumper = pcap_dump_open(descr, dumper_file.c_str());
	if (nullptr == dumper)
	{
		std::cout << "pcap_dump_open() failed: " << pcap_geterr(descr);
		return EXIT_FAILURE;
	}

	for (auto i : arr_packets)
	{
		pcap_dump((u_char*)dumper, &i.first, i.second);
	}

	pcap_dump_close(dumper);

	return EXIT_SUCCESS;
}


void packetHandlerFirstPass(
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

	std::string str_payload = std::string(payload, payload + len);
	size_t hash_payload = std::hash<std::string>{}(str_payload);
	auto it_inserted_pair = hash_cnt.insert({hash_payload, 1});
	if (!it_inserted_pair.second)
	{ // if the hash is already in the map
		it_inserted_pair.first->second += 1;   // increment the counter
	}

	++total_packets;
	if (total_packets % 10000 == 0)
	{
		std::clog << "#";
		std::clog.flush();
	}
}

void packetHandlerSecondPass(
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

	std::string str_payload = std::string(payload, payload + len);
	size_t hash_payload = std::hash<std::string>{}(str_payload);
	auto it = hash_to_pick.find(hash_payload);
	if (it != hash_to_pick.end())
	{
		hash_to_pick.erase(hash_payload);
		u_char* packet_copy = new u_char[pkthdr->len];
		std::memcpy(packet_copy, packet, pkthdr->len);
		arr_packets[it->second] = {*pkthdr, packet_copy};
	}

	++total_packets;
	if (total_packets % 10000 == 0)
	{
		std::clog << "#";
		std::clog.flush();
	}
}

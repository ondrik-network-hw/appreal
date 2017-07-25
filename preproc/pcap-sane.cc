// pcap-sane - sanitizes packets in a PCAP file by filtering strange ones

#include <cassert>
#include <chrono>
#include <iostream>
#include <fstream>
#include <vector>

// PCAP-related headers
#include <pcap.h>
#include <net/ethernet.h>
#include <netinet/in.h>
#include <netinet/ip.h>
#include <netinet/ip_icmp.h>
#include <netinet/ip6.h>
#include <netinet/icmp6.h>
#include <netinet/tcp.h>
#include <netinet/udp.h>

// Ethernet 802.1Q header
// copied from
// https://stackoverflow.com/questions/13166094/build-vlan-header-in-c
struct vlan_ethhdr {
	u_int8_t  ether_dhost[ETH_ALEN];  /* destination eth addr */
	u_int8_t  ether_shost[ETH_ALEN];  /* source ether addr    */
	u_int16_t h_vlan_proto;
	u_int16_t h_vlan_TCI;
	u_int16_t ether_type;
} __attribute__ ((__packed__));

using TimePoint = std::chrono::time_point<std::chrono::high_resolution_clock>;

// GLOBAL VARIABLES
size_t total_packets = 0;
size_t payloaded_packets = 0;
size_t vlan_packets = 0;
size_t ipv4_packets = 0;
size_t ipv6_packets = 0;
size_t tcp_packets = 0;
size_t udp_packets = 0;
size_t pim_packets = 0;
size_t other_l3_packets = 0;
size_t other_l4_packets = 0;
size_t incons_packets = 0;
size_t accepted_aut1 = 0;
size_t accepted_aut2 = 0;

pcap_dumper_t* dumper = nullptr;

std::vector<size_t> packet_lengths(2048);

// FUNCTION DECLARATIONS
void packetHandler(u_char *userData, const pcap_pkthdr* pkthdr, const u_char* packet);


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

	char errbuf[PCAP_ERRBUF_SIZE];
	// open capture file for offline processing
	pcap_t *descr = pcap_open_offline(packets_file.c_str(), errbuf);
	if (nullptr == descr)
	{
		std::cout << "pcap_open_offline() failed: " << errbuf << "\n";
		return EXIT_FAILURE;
	}

	dumper = pcap_dump_open(descr, dumper_file.c_str());
	if (nullptr == dumper)
	{
		std::cout << "pcap_dump_open() failed: " << pcap_geterr(descr);
		return EXIT_FAILURE;
	}

	TimePoint startTime = std::chrono::high_resolution_clock::now();

	// start packet processing loop, just like live capture
	if (pcap_loop(descr, 0, packetHandler, nullptr) < 0)
	{
		std::cout << "pcap_loop() failed: " << pcap_geterr(descr);
		return EXIT_FAILURE;
	}

	pcap_dump_close(dumper);

	TimePoint finishTime = std::chrono::high_resolution_clock::now();
  std::chrono::duration<double> opTime = finishTime - startTime;

	std::cout << "\n";
	std::cout << "Total packets in " << packets_file << ": " << total_packets << "\n";
	std::cout << "Packets with VLAN: " << vlan_packets << "\n";
	std::cout << "Packets with IPv4: " << ipv4_packets << "\n";
	std::cout << "Packets with IPv6: " << ipv6_packets << "\n";
	std::cout << "Packets with other L3 (not processed): " << other_l3_packets << "\n";
	std::cout << "Packets with TCP: " << tcp_packets << "\n";
	std::cout << "Packets with UDP: " << udp_packets << "\n";
	std::cout << "Packets with other L4 (not processed): " << other_l4_packets << "\n";
	std::cout << "Packets with payload: " << payloaded_packets << "\n";
	std::cout << "Time: " <<
		std::chrono::duration_cast<std::chrono::nanoseconds>(opTime).count() * 1e-9
		<< "\n";

	for (size_t i = 0; i < 2048; ++i)
	{
		// std::cout << i << " " << packet_lengths[i] << "\n";
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
	assert(nullptr != dumper);

	// packet_lengths[pkthdr->len] += 1;

	++total_packets;

	// PROCESSING THE PACKET
	size_t offset = sizeof(ether_header);
	const ether_header* eth_hdr = reinterpret_cast<const ether_header*>(packet);
	uint16_t ether_type = ntohs(eth_hdr->ether_type);
	if (ETHERTYPE_VLAN == ether_type)
	{
		++vlan_packets;

		offset = sizeof(vlan_ethhdr);
		const vlan_ethhdr* vlan_hdr = reinterpret_cast<const vlan_ethhdr*>(packet);
		ether_type = ntohs(vlan_hdr->ether_type);
	}

	// Word pac(packet, packet + pkthdr->len);
	// std::cout << "Packet #" << total_packets-1 << ": ";
	// std::cout << std::to_string(pac) << "\n";

	unsigned l4_proto;

	// LAYER 3 PROTOCOL
	if (ETHERTYPE_IP == ether_type)
	{
		++ipv4_packets;

		const ip* ip_hdr = reinterpret_cast<const ip*>(packet + offset);
		offset += sizeof(ip);
		l4_proto = ip_hdr->ip_p;
	}
	else if (ETHERTYPE_IPV6 == ether_type)
	{
		++ipv6_packets;

		const ip6_hdr* ip_hdr = reinterpret_cast<const ip6_hdr*>(packet + offset);
		offset += sizeof(ip6_hdr);
		l4_proto = ip_hdr->ip6_nxt;
	}
	else
	{
		++other_l3_packets;
		return;
	}

	// LAYER 4 PROTOCOL
	if (IPPROTO_TCP == l4_proto)
	{
		++tcp_packets;
		offset += sizeof(tcphdr);
	}
	else if (IPPROTO_UDP == l4_proto)
	{
		++udp_packets;
		offset += sizeof(udphdr);
	}
	else
	{
		// std::cout << "L4 protocol over IPv4: " << l4_proto << "\n";
		++other_l4_packets;
		// std::cout << std::hex << static_cast<unsigned>(ip_hdr->ip_p) << std::dec << "\n";
		// std::cout << static_cast<unsigned>(ip_hdr->ip_p) << "\n";

		return;
	}

	++payloaded_packets;

	pcap_dump((u_char*)dumper, pkthdr, packet);



	// std::cout << std::to_string(payload);

	if (total_packets % 1000 == 0)
	{
		std::cout << "#";
		std::cout.flush();
	}
}

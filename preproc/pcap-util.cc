#include "pcap-util.hh"
#include <net/ethernet.h>
#include <netinet/in.h>
#include <netinet/ip.h>
#include <netinet/ip_icmp.h>
#include <netinet/ip6.h>
#include <netinet/icmp6.h>
#include <netinet/udp.h>

#include "tcp.h"

#include <cassert>
#include <stdexcept>
#include <string>
#include <sstream>

namespace {
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
}


std::pair<const u_char*, int> pcap_util::get_payload(
	const pcap_pkthdr*   pkthdr,
	const u_char*        packet)
{
	assert(nullptr != pkthdr);
	assert(nullptr != packet);

	size_t offset = sizeof(ether_header);
	const ether_header* eth_hdr = reinterpret_cast<const ether_header*>(packet);
	uint16_t ether_type = ntohs(eth_hdr->ether_type);
	if (ETHERTYPE_VLAN == ether_type)
	{
		offset = sizeof(vlan_ethhdr);
		const vlan_ethhdr* vlan_hdr = reinterpret_cast<const vlan_ethhdr*>(packet);
		ether_type = ntohs(vlan_hdr->ether_type);
	}

	// Word pac(packet, packet + pkthdr->len);
	// std::cout << "Packet #" << total_packets-1 << ": ";
	// std::cout << std::to_string(pac) << "\n";

	unsigned l4_proto;

	if (ETHERTYPE_IP == ether_type)
	{
		const ip* ip_hdr = reinterpret_cast<const ip*>(packet + offset);
		offset += sizeof(ip);
		l4_proto = ip_hdr->ip_p;
	}
	else if (ETHERTYPE_IPV6 == ether_type)
	{
		const ip6_hdr* ip_hdr = reinterpret_cast<const ip6_hdr*>(packet + offset);
		offset += sizeof(ip6_hdr);
		l4_proto = ip_hdr->ip6_nxt;
	}
	else
	{
		return {nullptr, -1};
	}

	bool ip_in_ip = false;

	bool processing = true;
	while (processing)
	{
		processing = false;
		if (IPPROTO_TCP == l4_proto)
		{
			const tcphdr* tcp_hdr = reinterpret_cast<const tcphdr*>(packet + offset);
			size_t tcp_hdr_size = tcp_hdr->th_off * 4;
			offset += tcp_hdr_size;
		}
		else if (IPPROTO_UDP == l4_proto)
		{
			offset += sizeof(udphdr);
		}
		else if (IPPROTO_IPIP == l4_proto)
		{
			if (ip_in_ip) { assert(false); }

			ip_in_ip = true;

			const ip* ip_hdr = reinterpret_cast<const ip*>(packet + offset);
			offset += sizeof(ip);
			l4_proto = ip_hdr->ip_p;

			processing = true;
		}
		else if (IPPROTO_ESP == l4_proto)
		{
			offset += 8;
		}
		else if (IPPROTO_ICMP == l4_proto)
		{
			offset += sizeof(icmphdr);
		}
		else if (IPPROTO_GRE == l4_proto)
		{
			return {nullptr, -1};
		}
		else if (IPPROTO_ICMPV6 == l4_proto)
		{
			offset += sizeof(icmp6_hdr);
		}
		else if (IPPROTO_FRAGMENT == l4_proto)
		{
			const ip6_frag* ip_hdr = reinterpret_cast<const ip6_frag*>(packet + offset);
			offset += sizeof(ip6_frag);
			l4_proto = ip_hdr->ip6f_nxt;

			processing = true;
		}
		else if (IPPROTO_IPV6 == l4_proto)
		{
			const ip6_hdr* ip_hdr = reinterpret_cast<const ip6_hdr*>(packet + offset);
			offset += sizeof(ip6_hdr);
			l4_proto = ip_hdr->ip6_nxt;
		}
		else if (IPPROTO_PIM == l4_proto)
		{
			return {nullptr, -1};
		}
		else
		{
			return {nullptr, -1};
		}
	}

	return {packet + offset, pkthdr->len - offset};
}

pcap_t* pcap_util::pcap_open(const std::string& filename)
{
	char errbuf[PCAP_ERRBUF_SIZE];
	pcap_t *descr = pcap_open_offline(filename.c_str(), errbuf);
	if (nullptr == descr)
	{
		std::ostringstream stream;
		stream << "pcap_open_offline() failed: ";
		stream << errbuf;
		throw std::runtime_error(stream.str());
	}

	return descr;
}


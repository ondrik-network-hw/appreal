#include <pcap.h>
#include <string>
#include <utility>

namespace pcap_util
{

std::pair<const u_char*, int> get_payload(
	const pcap_pkthdr*   pkthdr,
	const u_char*        packet);


pcap_t* pcap_open(
	const std::string&   filename);

}

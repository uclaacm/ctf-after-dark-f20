from scapy.all import *
from scapy.utils import *
import base64

import os

client_ip = "192.168.1.1"
client_port = 3102
server_ip = "172.0.0.4"
server_port = 4782
tcp_flow = []

# Convert string to base64
flag = "flag{base64_is_the_best!}"

flag_bytes = flag.encode('ascii')
base64_bytes = base64.b64encode(flag_bytes)
flag = base64_bytes.decode('ascii') 


#Handshake
#SYN - is used to establish the connection
## I copied this from Henry, thanks lol
client_syn_pkt = Ether()/IP(src=client_ip, dst=server_ip)/TCP(sport=client_port, dport=server_port)
tcp_flow.append(client_syn_pkt)

#SYN-ACK
server_syn_pkt = Ether()/IP(src=server_ip, dst=client_ip)/TCP(sport=server_port, dport=client_port, flags="SA")
server_syn_pkt[TCP].ack = 1
tcp_flow.append(server_syn_pkt)

client_syn_pkt = Ether()/IP(src=client_ip, dst=server_ip)/TCP(sport=client_port, dport=server_port, flags="A")
client_syn_pkt[TCP].seq = 1
client_syn_pkt[TCP].ack=1

tcp_flow.append(client_syn_pkt)

#Client is sending the data
#P means there is data accompannied

client_ack_pkt = Ether()/IP(src=client_ip, dst=server_ip)/TCP(sport=client_port, dport=server_port, flags="P")
client_ack_pkt[TCP].seq = 1
client_ack_pkt[TCP].ack=1

client_ack_pkt = client_syn_pkt/base64_bytes[0]
client_ack_pkt.show()
tcp_flow.append(client_ack_pkt)


#Server sends back an acknowledgement
server_ack_pkt = Ether()/IP(src=server_ip, dst=client_ip)/TCP(sport=server_port, dport=client_port, flags="A")
server_ack_pkt[TCP].seq = 1
server_ack_pkt[TCP].ack = 2
tcp_flow.append(server_ack_pkt)

# Send the rest of the packets
## packets have incorrect seq, ack numbers
for i in range(1,len(base64_bytes)):
    client_ack_pkt = Ether()/IP(src=client_ip, dst=server_ip)/TCP(sport=client_port, dport=server_port, flags="P")
    client_ack_pkt[TCP].seq = 1+i
    client_ack_pkt[TCP].ack=1

    client_ack_pkt = client_syn_pkt/base64_bytes[i]
    client_ack_pkt.show()
    tcp_flow.append(client_ack_pkt)


    #Server sends back an acknowledgement
    server_ack_pkt = Ether()/IP(src=server_ip, dst=client_ip)/TCP(sport=server_port, dport=client_port, flags="A")
    server_ack_pkt[TCP].seq = 1
    server_ack_pkt[TCP].ack = 2+i
    tcp_flow.append(server_ack_pkt)


wrpcap("scramble.pcap", tcp_flow)
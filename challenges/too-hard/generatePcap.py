from scapy.all import *
from scapy.utils import *

import os

client_ip = "10.1.1.1"
client_port = 5000
server_ip = "10.1.1.2"
server_port = 7000
tcp_flow = []
#generate the data
flag = "flag{shark_t1me_b4by}"
encrypted_flag = ""
def encrypt_flag(flag):
    encrypted_flag = []

    for ch in flag:
        encrypted_ch = (ord(ch) * 3).to_bytes(4,'little')
        encrypted_flag.append(encrypted_ch)
    return b''.join(encrypted_flag)

def decrypt_flag(encrypted_flag):
    formatted_flag = [encrypted_flag[i:i+4] for i in range(0, len(encrypted_flag), 4)]
    print(formatted_flag)
    decrypted_flag = []
    for ch in formatted_flag:
        decrypted_ch = int.from_bytes(ch, byteorder='little')
        decrypted_flag.append(chr(int(decrypted_ch/3)))

    return ''.join(decrypted_flag)

encrypted_flag = encrypt_flag(flag)
print(decrypt_flag(encrypted_flag))
#Handshake
#SYN - is used to establish the connection
client_syn_pkt = Ether()/IP(src=client_ip, dst=server_ip)/TCP(sport=client_port, dport=server_port)
tcp_flow.append(client_syn_pkt)

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

client_ack_pkt = client_syn_pkt/encrypted_flag
client_ack_pkt.show()
tcp_flow.append(client_ack_pkt)


#Server sends back an acknowledgement
server_ack_pkt = Ether()/IP(src=server_ip, dst=client_ip)/TCP(sport=server_port, dport=client_port, flags="A")
server_ack_pkt[TCP].seq = 1
server_ack_pkt[TCP].ack = 1 + len(encrypted_flag)
tcp_flow.append(server_ack_pkt)


#Ending the connection
client_fin_pkt = Ether()/IP(src=client_ip, dst=server_ip)/TCP(sport=client_port, dport=server_port, flags="F")
client_fin_pkt[TCP].seq = 1 + len(encrypted_flag)
tcp_flow.append(client_fin_pkt)

server_ack_pkt = Ether()/IP(src=server_ip, dst=client_ip)/TCP(sport=server_port, dport=client_port, flags="A")
server_ack_pkt[TCP].seq = 1
server_ack_pkt[TCP].ack = 2 + len(encrypted_flag)
tcp_flow.append(server_ack_pkt)

server_fin_pkt = Ether()/IP(src=server_ip, dst=client_ip)/TCP(sport=server_port, dport=client_port, flags="F")
server_fin_pkt[TCP].seq = 1
server_fin_pkt[TCP].ack = 3 + 2 + len(encrypted_flag)
tcp_flow.append(server_fin_pkt)

client_ack_pkt = Ether()/IP(src=client_ip, dst=server_ip)/TCP(sport=client_port, dport=server_port, flags="A")
client_ack_pkt[TCP].seq = 2 + len(encrypted_flag)
client_ack_pkt[TCP].ack = 2
tcp_flow.append(client_ack_pkt)

wrpcap("TooHard.pcap", tcp_flow)
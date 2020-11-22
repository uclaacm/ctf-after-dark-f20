from scapy.all import *
from scapy.utils import *

def decrypt_flag(encrypted_flag):
    formatted_flag = [encrypted_flag[i:i+4] for i in range(0, len(encrypted_flag), 4)]
    print(formatted_flag)
    decrypted_flag = []
    for ch in formatted_flag:
        decrypted_ch = int.from_bytes(ch, byteorder='little')
        decrypted_flag.append(chr(int(decrypted_ch/3)))

    return ''.join(decrypted_flag)

packets = rdpcap('./TooHard.pcap')

#Shows all packets
packets[TCP].show()

#specify the one we are interested in
payload_pkt = packets[TCP][3]

#find the payload

payload = payload_pkt[Raw].load
print(decrypt_flag(payload))

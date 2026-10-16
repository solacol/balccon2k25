from scapy.all import *
from scapy.contrib import coap
import time
from datetime import datetime

scapy_cap = rdpcap('constraints.pcap')
flag_enc = ''
flag = ''
pkt_0 = True
cur_pkt_time = 0
last_pkt_time = 0
cur_diff = 0
last_diff = 0

# Read in pcap and analyze
for pkt in scapy_cap:
    # We only want dst ip 127.1.33.7 (first connection)
    # The other IP would also work, but needs adjustments in diff timing below to filter out outliers etc.
    if pkt[IP].dst == "127.1.33.7":
        if pkt_0:
            pkt_0 = False
            cur_pkt_time = pkt.time
            last_pkt_time = pkt.time
        else:
            cur_pkt_time = pkt.time
            cur_diff = cur_pkt_time - last_pkt_time

            #print(cur_diff)

            real_diff = cur_diff - last_diff

            # Uncomment to see diffs
            #print(real_diff)

            last_diff = cur_diff

            # Diffs are around 0.8 to 0.8 and 0.3
            # ...
            # 0.312327
            # 0.259554
            # 0.852460
            # 0.331371
            # 0.866463
            # ...
            # Construct binary encoded flag from time diffs
            # A 50/50 if 0 or 1
            if real_diff < 0.8:
                flag_enc = flag_enc + '0'
            else:
                flag_enc = flag_enc + '1'
    else:
        continue

# Decode 
flag_enc_int = int(flag_enc, 2);
byte_num = flag_enc_int.bit_length() + 7 // 8
flag_enc_bin_arr = flag_enc_int.to_bytes(byte_num, "big")
flag = flag_enc_bin_arr.decode()

print("Encoded: " + flag_enc)
print("Decoded: " + flag)

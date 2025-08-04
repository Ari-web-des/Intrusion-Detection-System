import pyshark
import pandas as pd

def parse_full_pcap(pcap_file, packet_limit=1000):
    cap = pyshark.FileCapture(pcap_file, use_json=True)
    packets = []
    valid = 0

    for i, pkt in enumerate(cap):
        try:
            row = {
                'timestamp': pkt.sniff_time,
                'protocol': pkt.highest_layer,
                'length': int(pkt.length),
                'src_ip': pkt.ip.src if hasattr(pkt, 'ip') else 'N/A',
                'dst_ip': pkt.ip.dst if hasattr(pkt, 'ip') else 'N/A'
            }
            packets.append(row)
            valid += 1
        except Exception:
            continue

        if i >= packet_limit:
            break

    cap.close()
    print(f"Parsed {valid} valid packets.")
    return pd.DataFrame(packets)

if __name__ == "__main__":
    df = parse_full_pcap("data/capture.pcapng", packet_limit=2000)
    print(df.head())
    df.to_csv("data/parsed_packets.csv", index=False)

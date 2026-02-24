from scapy.all import TCP, UDP, ICMP, ARP, DNS
from tp1.utils.capture import Capture
from tp1.utils.config import logger
from tp1.utils.report import Report


def identify_protocol(pkt):
    if pkt.haslayer(TCP):
        return "TCP"
    elif pkt.haslayer(UDP):
        if pkt.haslayer(DNS):
            return "DNS"
        return "UDP"
    elif pkt.haslayer(ICMP):
        return "ICMP"
    elif pkt.haslayer(ARP):
        return "ARP"
    else:
        return "OTHER"


def count_protocols(packets):
    protocol_stats = {}
    for pkt in packets:
        proto = identify_protocol(pkt)
        if proto in protocol_stats:
            protocol_stats[proto] += 1
        else:
            protocol_stats[proto] = 1
    return protocol_stats


def print_stats(protocol_stats):
    print("Logger : stats protocoles :")
    for proto, count in protocol_stats.items():
        print(f"  {proto}: {count}")


def main():
    print("Logger : ids/ips demarre")
    logger.info("Starting TP1")
    print("Logger : pret pour la capture reseau")

    interface = "eth0"
    count = 10

    print(f"Logger : capture sur ma {interface} : {count} paquets")
    capture = Capture(interface, count)
    capture.capture_traffic()
    print(f"Logger: terminé : {len(capture.packets)} paquets captures")

    protocol_stats = count_protocols(capture.packets)
    print_stats(protocol_stats)

    capture.analyse("tcp")
    summary = capture.get_summary()

    filename = "report.pdf"
    report = Report(capture, filename, summary)
    report.generate("graph")
    report.generate("array")
    report.save(filename)

    print(f"Logger: terminé : rapport sauvegardé dans {filename}")


if __name__ == "__main__":
    main()

from scapy.all import TCP, UDP, ICMP, ARP, Raw
import argparse


SQL_PATTERNS = ["SELECT", "UNION", "DROP"]


def hello_world() -> str:
    """
    Hello world function

    :return: "hello world"
    """
    return "hello world"


def choose_interface() -> str:
    """
    Return network interface and input user choice

    :return: network interface
    """
    interface = ""
    return interface


def parse_args():
    """
    Parse les arguments de la ligne de commande
    """
    parser = argparse.ArgumentParser(description="ids/ips maison")
    parser.add_argument("-c", "--count", type=int, default=50, help="nombre de paquets")
    parser.add_argument("-i", "--interface", type=str, default="eth0", help="interface reseau")
    parser.add_argument("-o", "--output", type=str, default="rapport.pdf", help="fichier pdf")
    return parser.parse_args()


def identify_protocol(packet):
    """
    Identifie le protocole d'un paquet réseau
    """
    if packet.haslayer(TCP):
        return "TCP"
    elif packet.haslayer(UDP):
        return "UDP"
    elif packet.haslayer(ICMP):
        return "ICMP"
    elif packet.haslayer(ARP):
        return "ARP"
    else:
        return "OTHER"


def count_protocols(packets):
    """
    Compte le nombre de paquets par protocole
    """
    protocol_stats = {}
    for pkt in packets:
        proto = identify_protocol(pkt)
        if proto in protocol_stats:
            protocol_stats[proto] += 1
        else:
            protocol_stats[proto] = 1
    return protocol_stats


def print_stats(protocol_stats):
    """
    Affiche les statistiques des protocoles
    """
    print("Logger : stats protocoles :")
    for proto, count in protocol_stats.items():
        print(f"  {proto}: {count}")


def check_arp_response(packet):
    """
    Verifie si un paquet ARP est une reponse (potentiel spoofing)
    """
    if packet.haslayer(ARP):
        if packet[ARP].op == 2:
            src_ip = packet[ARP].psrc
            src_mac = packet[ARP].hwsrc
            print(f"Logger : arp reply detecte, ip: {src_ip} mac: {src_mac}")
            return {"type": "ARP_SPOOFING", "ip": src_ip, "mac": src_mac}
    return None


def check_sql_payload(packet):
    """
    Verifie si le payload contient une injection SQL
    """
    if packet.haslayer(Raw):
        try:
            payload = packet[Raw].load.decode("utf-8", errors="ignore")
            for pattern in SQL_PATTERNS:
                if pattern.lower() in payload.lower():
                    src_ip = packet[0][1].src if hasattr(packet[0], "src") else "unknown"
                    print(f"Logger : sql injection detecte, pattern: {pattern}")
                    return {"type": "SQL_INJECTION", "pattern": pattern, "ip": src_ip}
        except Exception:
            pass
    return None

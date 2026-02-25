from scapy.all import TCP, UDP, ICMP, ARP, DNS


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


def identify_protocol(pkt):
    """
    Identifie le protocole d'un paquet réseau
    """
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

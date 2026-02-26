from scapy.all import sniff
from tp1.utils.lib import choose_interface, count_protocols, check_arp_response, check_sql_payload
from tp1.utils.config import logger


class Capture:
    def __init__(self, interface: str = None, count: int = 10) -> None:
        self.interface = interface if interface else choose_interface()
        self.count = count
        self.packets = []
        self.summary = ""
        self.protocol_stats = {}
        self.attacks = []

    def capture_traffic(self) -> None:
        """
        Capture network traffic from an interface
        """
        interface = self.interface
        logger.info(f"Capture traffic from interface {interface}")
        print(f"Logger : capture sur ma {interface} : {self.count} paquets")
        self.packets = sniff(iface=interface, count=self.count)
        print(f"Logger : {len(self.packets)} paquets capturés")
        logger.info(f"{len(self.packets)} packets captured")

    def sort_network_protocols(self) -> dict:
        """
        Sort and return all captured network protocols
        """
        sorted_stats = dict(
            sorted(self.protocol_stats.items(), key=lambda x: x[1], reverse=True)
        )
        return sorted_stats

    def get_all_protocols(self) -> dict:
        """
        Return all protocols captured with total packets number
        """
        self.protocol_stats = count_protocols(self.packets)
        return self.protocol_stats

    def analyse(self, protocols: str) -> None:
        """
        Analyse all captured data and return statement
        Si un trafic est illégitime (exemple : Injection SQL, ARP
        Spoofing, etc)
        a) Noter la tentative d'attaque.
        b) Relever le protocole ainsi que l'adresse réseau/physique
        de l'attaquant.
        c) (FACULTATIF) Opérer le blocage de la machine
        attaquante.
        Sinon afficher que tout va bien
        """
        self.protocol_stats = self.get_all_protocols()
        sorted_protocols = self.sort_network_protocols()
        logger.debug(f"All protocols: {self.protocol_stats}")
        logger.debug(f"Sorted protocols: {sorted_protocols}")

        self.attacks = []
        for pkt in self.packets:
            arp_attack = check_arp_response(pkt)
            if arp_attack:
                self.attacks.append(arp_attack)
            sql_attack = check_sql_payload(pkt)
            if sql_attack:
                self.attacks.append(sql_attack)

        if self.attacks:
            print(f"Logger : {len(self.attacks)} attaques detectees")
        else:
            print("Logger : aucune attaque detectee")

        self.summary = self._gen_summary()

    def get_summary(self) -> str:
        """
        Return summary
        :return:
        """
        return self.summary

    def _gen_summary(self) -> str:
        """
        Generate summary
        """
        summary = "Rapport ids/ips\n"
        summary += f"Paquets captures: {len(self.packets)}\n"
        for proto, cnt in self.protocol_stats.items():
            summary += f"  {proto}: {cnt}\n"
        if self.attacks:
            summary += f"Attaques detectees: {len(self.attacks)}\n"
            for atk in self.attacks:
                summary += f"  {atk['type']} - {atk}\n"
        else:
            summary += "Aucune attaque detectee\n"
        return summary

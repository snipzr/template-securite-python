from tp1.utils.capture import Capture
from tp1.utils.config import logger
from tp1.utils.lib import count_protocols, print_stats
from tp1.utils.report import Report


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

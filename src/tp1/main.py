from tp1.utils.capture import Capture
from tp1.utils.config import logger
from tp1.utils.lib import parse_args, count_protocols, print_stats
from tp1.utils.report import Report


def main():
    args = parse_args()
    print("Logger : ids/ips demarre")
    logger.info("Starting TP1")
    print("Logger : pret pour la capture reseau")

    capture = Capture(args.interface, args.count)
    capture.capture_traffic()
    print(f"Logger: terminé : {len(capture.packets)} paquets captures")

    protocol_stats = count_protocols(capture.packets)
    print_stats(protocol_stats)

    capture.analyse("tcp")
    summary = capture.get_summary()

    report = Report(capture, args.output, summary)
    report.generate("graph")
    report.generate("array")
    report.save(args.output)

    print(f"Logger: terminé : rapport sauvegardé dans {args.output}")


if __name__ == "__main__":
    main()

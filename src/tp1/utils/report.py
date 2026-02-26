import pygal
from pygal.style import Style
from reportlab.lib.pagesizes import A4
from reportlab.platypus import SimpleDocTemplate, Table, TableStyle, Paragraph
from reportlab.lib.styles import getSampleStyleSheet
from reportlab.lib import colors

from tp1.utils.capture import Capture


class Report:
    def __init__(self, capture: Capture, filename: str, summary: str):
        self.capture = capture
        self.filename = filename
        self.title = "Rapport ids/ips"
        self.summary = summary
        self.array = None
        self.graph = None

    def generate(self, param: str) -> None:
        """
        Generate graph and array
        """
        if param == "graph":
            custom_style = Style(colors=("#3498db", "#2ecc71", "#9b59b6", "#e74c3c", "#f39c12"))
            chart = pygal.Bar(style=custom_style)
            chart.title = "Protocoles captures"
            for proto, count in self.capture.protocol_stats.items():
                chart.add(proto, count)
            chart.render_to_file("protocol_stats.svg")
            self.graph = "protocol_stats.svg"
            print("Logger : graphique protocol_stats.svg cree")
        elif param == "array":
            data = [["Protocole", "Quantite"]]
            for proto, count in self.capture.protocol_stats.items():
                data.append([proto, str(count)])
            self.array = data

    def save(self, filename: str) -> None:
        """
        Save report as PDF
        :param filename:
        :return:
        """
        doc = SimpleDocTemplate(filename, pagesize=A4)
        elements = []
        styles = getSampleStyleSheet()

        title = Paragraph(self.title, styles["Title"])
        elements.append(title)

        if self.array:
            table = Table(self.array)
            table.setStyle(
                TableStyle(
                    [
                        ("BACKGROUND", (0, 0), (-1, 0), colors.grey),
                        ("TEXTCOLOR", (0, 0), (-1, 0), colors.whitesmoke),
                        ("GRID", (0, 0), (-1, -1), 1, colors.black),
                    ]
                )
            )
            elements.append(table)

        if self.capture.attacks:
            elements.append(Paragraph("Menaces detectees", styles["Heading2"]))
            for attack in self.capture.attacks:
                attack_text = f"{attack['type']} - {attack}"
                elements.append(Paragraph(attack_text, styles["Normal"]))

        doc.build(elements)
        print(f"Logger : {filename} cree")

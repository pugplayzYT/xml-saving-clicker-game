import sys
from PyQt6.QtWidgets import (
    QApplication,
    QWidget,
    QVBoxLayout,
    QLabel,
    QPushButton,
)
import xml.etree.ElementTree as ET
import os

# Updated encryption multiplier
MULTIPLIER = (100000.55553 * 0.55555555555555555555555555555555555555555555555555555555555) / 8.56

# Updated encryption function
def encrypt_score(score):
    score = int(score)
    encrypted = ((score - 8 + 9) / 666) * MULTIPLIER
    return str(encrypted)  # Keep full decimal precision

# Updated decryption function
def decrypt_score(encrypted):
    try:
        encrypted = float(encrypted)
        original = ((encrypted / MULTIPLIER) * 666) - 9 + 8
        return int(original)  # Return as integer for game logic
    except:
        return 0  # If decryption fails, return 0

# Save score to an XML file with encryption
def save_score(score):
    encrypted_score = encrypt_score(score)
    root = ET.Element("data")
    score_element = ET.SubElement(root, "score")
    score_element.text = encrypted_score  # Keep full decimal in XML

    tree = ET.ElementTree(root)
    with open("score.xml", "wb") as file:
        tree.write(file)

# Load score from an XML file and decrypt
def load_score():
    if os.path.exists("score.xml"):
        tree = ET.parse("score.xml")
        root = tree.getroot()
        encrypted_score = root.find("score").text
        return decrypt_score(encrypted_score)
    return 0


# PyQt6 UI
class ClickerWindow(QWidget):
    def __init__(self):
        super().__init__()
        self.score = load_score()
        self.init_ui()

    def init_ui(self):
        self.setWindowTitle("Clicker Game")
        layout = QVBoxLayout()

        self.label = QLabel(f"Score: {self.score}")
        layout.addWidget(self.label)

        btn_click = QPushButton("Click!")
        btn_click.clicked.connect(self.increment_score)
        layout.addWidget(btn_click)

        btn_reset = QPushButton("Reset")
        btn_reset.clicked.connect(self.reset_score)
        layout.addWidget(btn_reset)

        self.setLayout(layout)

    def increment_score(self):
        self.score += 1
        self.label.setText(f"Score: {self.score}")
        save_score(self.score)

    def reset_score(self):
        self.score = 0
        self.label.setText(f"Score: {self.score}")
        save_score(self.score)


def main():
    app = QApplication(sys.argv)
    window = ClickerWindow()
    window.show()
    sys.exit(app.exec())


if __name__ == "__main__":
    main()

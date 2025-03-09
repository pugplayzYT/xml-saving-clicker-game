from kivy.app import App
from kivy.uix.boxlayout import BoxLayout
from kivy.uix.label import Label
from kivy.uix.button import Button
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


# Kivy UI
class ClickerApp(App):
    def build(self):
        self.score = load_score()

        layout = BoxLayout(orientation='vertical', padding=20, spacing=10)

        # Score Label
        self.label = Label(text=f"Score: {self.score}", font_size=30, bold=True)
        layout.add_widget(self.label)

        # Click Button
        btn_click = Button(text="Click!", font_size=24, size_hint=(None, None), size=(200, 60))
        btn_click.bind(on_press=self.increment_score)
        layout.add_widget(btn_click)

        # Reset Button
        btn_reset = Button(text="Reset", font_size=20, size_hint=(None, None), size=(150, 50))
        btn_reset.bind(on_press=self.reset_score)
        layout.add_widget(btn_reset)

        return layout

    # Increment score
    def increment_score(self, instance):
        self.score += 1
        self.label.text = f"Score: {self.score}"
        save_score(self.score)

    # Reset score
    def reset_score(self, instance):
        self.score = 0
        self.label.text = f"Score: {self.score}"
        save_score(self.score)


# Run the app
if __name__ == "__main__":
    ClickerApp().run()

import sys
import os
import time
import pyautogui
import keyboard
from PyQt5.QtWidgets import QApplication, QWidget, QVBoxLayout, QPushButton, QFileDialog, QLabel

class AutoApp(QWidget):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("Folder Automation Tool")
        self.setGeometry(300, 300, 400, 200)
        self.folder_path = ""
        self.actions = []

        layout = QVBoxLayout()

        self.label = QLabel("No folder selected")
        layout.addWidget(self.label)

        self.select_btn = QPushButton("Select Folder")
        self.select_btn.clicked.connect(self.select_folder)
        layout.addWidget(self.select_btn)

        self.record_btn = QPushButton("Start Recording (ESC to stop)")
        self.record_btn.clicked.connect(self.record_actions)
        layout.addWidget(self.record_btn)

        self.run_btn = QPushButton("Run Automation")
        self.run_btn.clicked.connect(self.run_automation)
        layout.addWidget(self.run_btn)

        self.setLayout(layout)

    def select_folder(self):
        folder = QFileDialog.getExistingDirectory(self, "Select Folder")
        if folder:
            self.folder_path = folder
            self.label.setText(f"Folder Selected: {folder}")

    def record_actions(self):
        self.actions = []
        print("Recording... Press ESC to stop.")
        start_time = time.time()
        while not keyboard.is_pressed("esc"):
            x, y = pyautogui.position()
            self.actions.append({
                "time": time.time() - start_time,
                "position": (x, y)
            })
            time.sleep(0.2)
        print("Recording stopped.")

    def run_automation(self):
        if not self.folder_path or not self.actions:
            print("Please select a folder and record actions first.")
            return

        for filename in os.listdir(self.folder_path):
            print(f"Automating: {filename}")
            for action in self.actions:
                x, y = action["position"]
                pyautogui.moveTo(x, y, duration=0.1)
                pyautogui.click()
                time.sleep(0.2)

if __name__ == "__main__":
    app = QApplication(sys.argv)
    window = AutoApp()
    window.show()
    sys.exit(app.exec_())

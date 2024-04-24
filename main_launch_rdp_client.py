import sys
from PyQt5.QtWidgets import QApplication, QWidget, QVBoxLayout, QPushButton, QFrame
import subprocess

class RemoteDesktopApp(QWidget):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("Remote Desktop Viewer")
        self.initUI()

    def initUI(self):
        layout = QVBoxLayout()

        # Button to launch RDP client application
        rdp_button = QPushButton("Launch RDP Client")
        rdp_button.clicked.connect(self.launch_rdp_client)
        layout.addWidget(rdp_button)

        # Frame to embed RDP client window
        self.rdp_frame = QFrame()
        layout.addWidget(self.rdp_frame)

        self.setLayout(layout)

    def launch_rdp_client(self):
        # Launch RDP client application (e.g., mstsc on Windows)
        subprocess.run(["mstsc"])

if __name__ == "__main__":
    app = QApplication(sys.argv)
    window = RemoteDesktopApp()
    window.show()
    sys.exit(app.exec())






import sys
from PyQt5.QtWidgets import QApplication, QWidget, QVBoxLayout, QLabel
from PyQt5.QtGui import QPixmap
import pyrdp


class RemoteDesktopApp(QWidget):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("Remote Desktop Viewer")
        self.initUI()

    def initUI(self):
        layout = QVBoxLayout()

        self.remote_label = QLabel()
        layout.addWidget(self.remote_label)

        self.setLayout(layout)

    def update_remote_desktop(self, pixmap):
        self.remote_label.setPixmap(pixmap)


if __name__ == "__main__":
    app = QApplication(sys.argv)
    window = RemoteDesktopApp()
    window.show()

    # RDP connection parameters
    host = "172.16.20.25"
    username = "ED-Desk-84"
    password = "Eminent@123"

    # Establish RDP connection
    with pyrdp.RDPClient(host, username, password) as client:
        client.connect()

        while True:
            try:
                # Capture remote desktop image
                image_bytes = client.capture()

                # Convert image bytes to QPixmap
                pixmap = QPixmap()
                pixmap.loadFromData(image_bytes)

                # Update GUI
                window.update_remote_desktop(pixmap)
                app.processEvents()
            except KeyboardInterrupt:
                break

    sys.exit(app.exec_())

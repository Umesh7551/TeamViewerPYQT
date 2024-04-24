import sys

from PyQt6 import QtCore
from PyQt6.QtGui import QPixmap
from PyQt6.QtWidgets import QApplication, QWidget, QPushButton, QVBoxLayout, QLabel
from pyvnc2swf import RFBClient

class VNCViewer(QWidget):
    def __init__(self):
        super().__init__()
        self.initUI()

    def initUI(self):
        self.setWindowTitle('VNC Viewer')
        self.connectButton = QPushButton('Connect to VNC', self)
        self.connectButton.clicked.connect(self.connectToVNC)

        self.screenLabel = QLabel(self)
        self.screenLabel.setAlignment(QtCore.Qt.AlignmentFlag.AlignCenter)

        layout = QVBoxLayout()
        layout.addWidget(self.connectButton)
        layout.addWidget(self.screenLabel)
        self.setLayout(layout)

    def connectToVNC(self):
        # Replace these values with your remote machine's details
        host = '172.16.20.25'
        port = 5900
        password = '1234'

        client = RFBClient(host, port)
        client.connect()
        client.authenticate(password)

        # Now you have a connected VNC client, you can use it to interact with the remote machine's screen
        # For example, you can capture the screen and display it in your PyQt6 application
        # Continuously capture and update the screen
        while True:
            frame = client.captureFrame()
            if frame:
                pixmap = QPixmap.fromImage(frame)
                self.screenLabel.setPixmap(pixmap)
                self.screenLabel.adjustSize()
                QApplication.processEvents()  # Update the GUI


def main():
    app = QApplication(sys.argv)
    vnc_viewer = VNCViewer()
    vnc_viewer.show()
    sys.exit(app.exec())

if __name__ == '__main__':
    main()

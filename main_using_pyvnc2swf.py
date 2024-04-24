import sys

from PyQt6.QtCore import QTimer
from PyQt6.QtGui import QPixmap
from PyQt6.QtWidgets import QApplication, QWidget, QPushButton, QMessageBox
from pyvnc2swf import RFBClient


class RemoteDesktopViewer(QWidget):
    def __init__(self):
        super().__init__()
        self.initUI()

    def initUI(self):
        self.setWindowTitle('Remote Desktop Viewer')
        self.setGeometry(100, 100, 400, 300)

        self.connectButton = QPushButton('Connect', self)
        self.connectButton.setGeometry(150, 150, 100, 30)
        self.connectButton.clicked.connect(self.connectToRemoteDesktop)

    def updateRemoteDesktop(self):
        # Get the remote desktop image data from the VNC client
        try:
            desktop_image = self.client.capture_frame().convert('RGBA')
            desktop_image = desktop_image.mirrored()  # Mirrored to match VNC coordinate system
            pixmap = QPixmap.fromImage(desktop_image)
            self.remoteDesktopLabel.setPixmap(pixmap)
        except Exception as e:
            print(f"Error updating remote desktop: {e}")

    def connectToRemoteDesktop(self):
        # Connect to the remote desktop
        host = '172.16.20.25'
        port = 5900  # Default VNC port

        try:
            client = RFBClient(host, port)
            # Set up timer to periodically update the remote desktop image
            self.timer = QTimer(self)
            self.timer.timeout.connect(self.updateRemoteDesktop)
            self.timer.start(100)  # Update every 100 milliseconds Update every 100 milliseconds
        except Exception as e:
            QMessageBox.critical(self, 'Connection Error', f'Failed to connect to remote desktop: {e}')


def main():
    app = QApplication(sys.argv)
    viewer = RemoteDesktopViewer()
    viewer.show()
    sys.exit(app.exec())


if __name__ == '__main__':
    main()

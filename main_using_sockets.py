import sys
import socket
from PyQt5.QtWidgets import QApplication, QLabel, QVBoxLayout, QWidget
from PyQt5.QtGui import QPixmap
from PyQt5.QtCore import QTimer

class ScreenViewer(QWidget):
    def __init__(self, host, port):
        super().__init__()
        self.host = host
        self.port = port

        self.label = QLabel(self)
        self.layout = QVBoxLayout(self)
        self.layout.addWidget(self.label)
        self.setLayout(self.layout)

        self.socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.socket.connect((self.host, self.port))

        self.timer = QTimer(self)
        self.timer.timeout.connect(self.update_screen)
        self.timer.start(100)  # Update screen every 100 milliseconds

    def update_screen(self):
        data = b''
        while b'\n' not in data:
            chunk = self.socket.recv(4096)
            if not chunk:
                break
            data += chunk
        if data:
            pixmap = QPixmap()
            pixmap.loadFromData(data)
            self.label.setPixmap(pixmap)

    def closeEvent(self, event):
        self.socket.close()
        event.accept()

if __name__ == '__main__':
    app = QApplication(sys.argv)
    host = '172.16.20.25'  # Change this to the IP address of the server
    port = 80  # Change this to the port number the server is listening on
    viewer = ScreenViewer(host, port)
    viewer.setWindowTitle('Screen Viewer')
    viewer.show()
    sys.exit(app.exec())

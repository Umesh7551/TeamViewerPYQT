import sys

from PyQt6.QtGui import QPixmap
from PyQt6.QtGui import QImage
from PyQt6.QtWidgets import QApplication, QMainWindow, QLabel, QVBoxLayout, QWidget
import pyrdp
class RemoteScreenViewer(QMainWindow):
    def __init__(self):
        super().__init__()
        self.initUI()
        self.rdp_client = pyrdp.RemoteDesktop()

    def initUI(self):
        central_widget = QWidget()
        layout = QVBoxLayout()

        self.screen_label = QLabel()
        layout.addWidget(self.screen_label)

        central_widget.setLayout(layout)
        self.setCentralWidget(central_widget)

    def connect_to_remote(self, host, username, password):
        self.rdp_client.connect(host, username, password)
        self.rdp_client.setCallback(self.update_screen)
        self.rdp_client.start()

    def update_screen(self, pixels, width, height, stride):
        qimage = QImage(pixels, width, height, stride, QImage.Format.Format_RGB32)
        pixmap = QPixmap.fromImage(qimage)
        self.screen_label.setPixmap(pixmap)

if __name__ == '__main__':
    app = QApplication(sys.argv)
    viewer = RemoteScreenViewer()
    viewer.connect_to_remote('172.16.20.25', 'ED-Desk-84', 'Eminent@123')
    viewer.show()
    sys.exit(app.exec())

import sys
from PyQt6.QtWidgets import QApplication, QMainWindow, QLabel, QVBoxLayout, QWidget
from vnc_viewer import VNCViewer

class RemoteScreenViewer(QMainWindow):
    def __init__(self):
        super().__init__()
        self.initUI()
        self.vnc_viewer = VNCViewer()

    def initUI(self):
        central_widget = QWidget()
        layout = QVBoxLayout()

        self.screen_label = QLabel()
        layout.addWidget(self.screen_label)

        central_widget.setLayout(layout)
        self.setCentralWidget(central_widget)

    def connect_to_remote(self, host, port):
        self.vnc_viewer.connect(host, port)
        self.vnc_viewer.set_pixmap_handler(self.update_screen)
        self.vnc_viewer.start()

    def update_screen(self, pixmap):
        self.screen_label.setPixmap(pixmap)

if __name__ == '__main__':
    app = QApplication(sys.argv)
    viewer = RemoteScreenViewer()
    viewer.connect_to_remote('172.16.20.25', 5500)  # Replace with the remote host and port
    viewer.show()
    sys.exit(app.exec())
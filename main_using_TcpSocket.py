import sys
from PyQt5.QtWidgets import QApplication, QMainWindow, QLabel, QVBoxLayout, QWidget, QPushButton
from PyQt5.QtNetwork import QTcpServer, QTcpSocket
from PyQt5.QtGui import QPixmap, QPainter
from PyQt5.QtCore import Qt, QBuffer, QByteArray, QIODevice, QTimer


class ScreenServer(QTcpServer):
    def __init__(self):
        super().__init__()
        self.tcp_socket = None
        self.image = None
        self.timer = QTimer()
        self.timer.timeout.connect(self.send_frame)
        self.timer.start(100)

    def incomingConnection(self, socketId):
        if self.tcp_socket is None:
            self.tcp_socket = self.nextPendingConnection()
            self.tcp_socket.readyRead.connect(self.read_frame)

    def read_frame(self):
        data = self.tcp_socket.readAll()
        pixmap = QPixmap()
        pixmap.loadFromData(data)
        self.image = pixmap.toImage()

    def send_frame(self):
        if self.image is not None and self.tcp_socket is not None:
            buffer = QBuffer(QByteArray())
            buffer.open(QIODevice.ReadWrite)
            self.image.save(buffer, "PNG")
            self.tcp_socket.write(buffer.data())


class RemoteDesktopClient(QMainWindow):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("Remote Desktop Client")
        self.label = QLabel()
        self.setCentralWidget(self.label)
        self.tcp_socket = QTcpSocket()
        self.tcp_socket.readyRead.connect(self.receive_frame)
        self.tcp_socket.connectToHost("172.16.20.25", 80)

    def receive_frame(self):
        data = self.tcp_socket.readAll()
        pixmap = QPixmap()
        pixmap.loadFromData(data)
        self.label.setPixmap(pixmap)


class RemoteDesktopServer(QMainWindow):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("Remote Desktop Server")
        self.start_button = QPushButton("Start Server")
        self.start_button.clicked.connect(self.start_server)
        self.setCentralWidget(self.start_button)
        self.server = ScreenServer()

    def start_server(self):
        self.server.listen("172.16.20.25", 80)
        self.start_button.setEnabled(False)


if __name__ == "__main__":
    app = QApplication(sys.argv)
    server_window = RemoteDesktopServer()
    server_window.show()
    client_window = RemoteDesktopClient()
    client_window.show()
    sys.exit(app.exec())




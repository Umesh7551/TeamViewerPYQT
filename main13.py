import sys
import socket
from PyQt6.QtWidgets import QApplication, QMainWindow, QLabel, QMessageBox
from PyQt6.QtGui import QPixmap
from PyQt6.QtCore import QCoreApplication, QByteArray

class RemoteDesktopApp(QMainWindow):
    def __init__(self):
        super().__init__()
        self.initUI()
        self.connectToRemoteDesktop()

    def initUI(self):
        self.setWindowTitle('Remote Desktop App')
        self.setGeometry(100, 100, 800, 600)

        self.remoteDesktopLabel = QLabel(self)
        self.remoteDesktopLabel.setGeometry(100, 100, 600, 400)

    def connectToRemoteDesktop(self):
        try:
            # Replace 'remote_ip' and 'remote_port' with the actual IP and port of the remote server
            remote_ip = '172.16.20.25'
            remote_port = 80

            # Create a socket object
            self.client_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

            # Connect to the remote server
            self.client_socket.connect((remote_ip, remote_port))

            # Connection successful
            QMessageBox.information(self, 'Connection Status', 'Connected to remote desktop!')

            # Start receiving screen data
            self.receiveScreenData()

        except Exception as e:
            # Connection failed
            QMessageBox.critical(self, 'Connection Error', f'Failed to connect to remote desktop: {e}')

    def receiveScreenData(self):
        try:
            while True:
                # Receive screen data from the server
                screen_data = self.client_socket.recv(4096)

                # Convert the received bytes to a QPixmap and display it in the QLabel
                pixmap = QPixmap()
                pixmap.loadFromData(QByteArray(screen_data))
                self.remoteDesktopLabel.setPixmap(pixmap)

        except Exception as e:
            # Handle error
            print(f"Error receiving screen data: {e}")
            self.client_socket.close()

def main():
    app = QApplication(sys.argv)
    ex = RemoteDesktopApp()
    ex.show()
    sys.exit(app.exec())

if __name__ == '__main__':
    main()

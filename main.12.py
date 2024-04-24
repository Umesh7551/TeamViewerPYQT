# import sys
# import socket
# from PyQt6.QtWidgets import QApplication, QMainWindow, QPushButton, QMessageBox
# from PyQt6.QtCore import QCoreApplication
#
#
# class RemoteDesktopApp(QMainWindow):
#     def __init__(self):
#         super().__init__()
#         self.initUI()
#
#     def initUI(self):
#         self.setWindowTitle('Remote Desktop App')
#         self.setGeometry(100, 100, 400, 300)
#
#         self.connectButton = QPushButton('Connect to Remote Desktop', self)
#         self.connectButton.setGeometry(100, 100, 200, 50)
#         self.connectButton.clicked.connect(self.connectToRemoteDesktop)
#
#         self.quitButton = QPushButton('Quit', self)
#         self.quitButton.setGeometry(100, 200, 200, 50)
#         self.quitButton.clicked.connect(QCoreApplication.instance().quit)
#
#     def connectToRemoteDesktop(self):
#         try:
#             # Replace 'remote_ip' and 'remote_port' with the actual IP and port of the remote server
#             remote_ip = '172.16.20.25'
#             remote_port = 80
#
#             # Create a socket object
#             client_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
#
#             # Connect to the remote server
#             client_socket.connect((remote_ip, remote_port))
#
#             # Connection successful
#             QMessageBox.information(self, 'Connection Status', 'Connected to remote desktop!')
#
#             # Here you can proceed with screen sharing or other functionalities
#
#             # Remember to close the socket when done
#             client_socket.close()
#
#         except Exception as e:
#             # Connection failed
#             QMessageBox.critical(self, 'Connection Error', f'Failed to connect to remote desktop: {e}')
#
#
# def main():
#     app = QApplication(sys.argv)
#     ex = RemoteDesktopApp()
#     ex.show()
#     sys.exit(app.exec())
#
#
# if __name__ == '__main__':
#     main()


import sys
import socket
from PyQt6.QtWidgets import QApplication, QMainWindow, QPushButton, QMessageBox, QLabel
from PyQt6.QtGui import QPixmap, QScreen
from PyQt6.QtCore import QCoreApplication, QTimer, QByteArray, QBuffer, QIODevice  # Add import here


class RemoteDesktopApp(QMainWindow):
    def __init__(self):
        super().__init__()
        self.initUI()

        # Initialize screen capture timer
        self.timer = QTimer(self)
        self.timer.timeout.connect(self.updateRemoteDesktop)
        self.timer.start(100)  # Update every 100 milliseconds

    def initUI(self):
        self.setWindowTitle('Remote Desktop App')
        self.setGeometry(100, 100, 800, 600)

        self.connectButton = QPushButton('Connect to Remote Desktop', self)
        self.connectButton.setGeometry(100, 100, 200, 50)
        self.connectButton.clicked.connect(self.connectToRemoteDesktop)

        self.quitButton = QPushButton('Quit', self)
        self.quitButton.setGeometry(100, 200, 200, 50)
        self.quitButton.clicked.connect(QCoreApplication.instance().quit)

        self.remoteDesktopLabel = QLabel(self)
        self.remoteDesktopLabel.setGeometry(100, 300, 600, 300)

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

        except Exception as e:
            # Connection failed
            QMessageBox.critical(self, 'Connection Error', f'Failed to connect to remote desktop: {e}')

    def updateRemoteDesktop(self):
        try:
            # Capture the screen
            screen = QApplication.primaryScreen()
            screenshot = screen.grabWindow(0)

            # Convert the screenshot to a QPixmap
            pixmap = QPixmap(screenshot)

            # Display the screenshot in the QLabel
            self.remoteDesktopLabel.setPixmap(pixmap)

            # If connected, send the screenshot to the remote client
            if hasattr(self, 'client_socket'):
                # Convert the screenshot to bytes
                screenshot_bytearray = QByteArray()
                buffer = QBuffer(screenshot_bytearray)
                buffer.open(QIODevice.OpenModeFlag.WriteOnly)
                pixmap.save(buffer, "PNG")  # Save the screenshot to the buffer as PNG
                buffer.close()

                # Send the screenshot to the client
                self.client_socket.sendall(screenshot_bytearray)

        except Exception as e:
            # Handle error
            print(f"Error updating remote desktop: {e}")


def main():
    app = QApplication(sys.argv)
    ex = RemoteDesktopApp()
    ex.show()
    sys.exit(app.exec())


if __name__ == '__main__':
    main()

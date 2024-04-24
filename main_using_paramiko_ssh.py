import sys
from datetime import time
from urllib import request

import requests
import win32api
import win32com
import win32con
import win32gui
import win32ui
from PIL.Image import Image
from PyQt6.QtWidgets import (
    QApplication, QMainWindow, QWidget, QVBoxLayout, QHBoxLayout,
    QLabel, QLineEdit, QPushButton, QMessageBox, QFileDialog
)
from PyQt6.QtCore import QThread, pyqtSignal  # For threading
import paramiko  # For remote connection
from paramiko import SFTPClient
import io
from PyQt6.QtGui import QPixmap, QGuiApplication
import mss
import pyautogui
import pywin
from pywinauto import Desktop


class RemoteCommandThread(QThread):
    def __init__(self, ssh_client):
        super().__init__()
        self.ssh_client = ssh_client
        self.command_output = None
        self.finished = pyqtSignal()  # Signal emitted when thread finishes

    def run(self):
        # Code to execute commands on the remote machine using self.ssh_client
        # (e.g., using stdin, stdout, stderr)
        # Store the output in self.command_output
        # ...

        self.finished.emit()  # Signal completion


class MainWindow(QMainWindow):
    def __init__(self):
        super().__init__()

        # Create widgets
        self.hostname_label = QLabel("Hostname/IP Address:")
        self.hostname_edit = QLineEdit()
        self.username_label = QLabel("Username:")
        self.username_edit = QLineEdit()
        self.password_label = QLabel("Password:")
        self.password_edit = QLineEdit()
        self.connect_button = QPushButton("Connect to Remote Machine")
        self.connect_button.clicked.connect(self.connect_to_remote)


        # Status label
        self.status_label = QLabel()

        # Layout widgets
        layout = QVBoxLayout()
        layout.addWidget(self.hostname_label)
        layout.addWidget(self.hostname_edit)
        layout.addWidget(self.username_label)
        layout.addWidget(self.username_edit)
        layout.addWidget(self.password_label)
        layout.addWidget(self.password_edit)
        layout.addWidget(self.connect_button)

        layout.addWidget(self.status_label)

        # Add VNC viewer widget
        self.vnc_viewer = QLabel("VNC Viewer")
        layout.addWidget(self.vnc_viewer)

        central_widget = QWidget()
        central_widget.setLayout(layout)
        self.setCentralWidget(central_widget)

        # Add SFTP controls
        self.sftp_label = QLabel("SFTP Operations:")
        self.sftp_button = QPushButton("List Remote Files")
        self.sftp_button.clicked.connect(self.list_remote_files)
        layout.addWidget(self.sftp_label)
        layout.addWidget(self.sftp_button)

        # Set window title
        self.setWindowTitle("Remote Machine Management")
        self.setGeometry(200, 200, 400, 300)
        # self.setMaximumSize(400, 300)
        # Create a thread for remote connection (optional)
        self.remote_thread = None

        # SSH and SFTP clients (initialized on connection)
        self.ssh_client = None
        self.sftp_client = None

    def connect_to_remote(self):
        hostname = self.hostname_edit.text()
        username = self.username_edit.text()
        password = self.password_edit.text()

        # Validation (optional, add checks for empty fields, etc.)
        if not all([hostname, username, password]):
        # if not all([hostname]):
            QMessageBox.critical(self, "Error", "Please fill in all fields.")
            return

        # Connect using Paramiko (consider error handling)
        try:
            self.ssh_client = paramiko.SSHClient()
            self.ssh_client.set_missing_host_key_policy(paramiko.AutoAddPolicy())
            self.ssh_client.connect(hostname=hostname, username=username, password=password)

            self.show_success_message()  # Optional message
            # Display VNC viewer
            # self.display_vnc_viewer(hostname, username, password=password)
            # Display screen of remote machine
            # self.display_remote_screen(hostname, username, password)

            # Display remote screen
            self.display_remote_screen()
            # Optionally, start a separate thread for remote command execution
            # self.remote_thread = RemoteCommandThread(self.ssh_client)
            # self.remote_thread.finished.connect(self.handle_remote_thread_finished)
            # self.remote_thread.start()
        except Exception as e:
            self.show_error_message(f"Connection failed: {e}")

    def show_success_message(self):
        QMessageBox.information(self, "Success", "Connected to remote machine.")

    def show_error_message(self, message):
        QMessageBox.critical(self, "Error", message)


    def display_remote_screen(self):
        # Capture remote screen using pyautogui
        try:
            # screenshot = pyautogui.screenshot()
            # screenshot.save('remote_screen.png')
            # pixmap = QPixmap('remote_screen.png')
            # self.vnc_viewer.setPixmap(pixmap)
            # Create a Desktop object
            desktop = Desktop()

            # Get the remote desktop window
            remote_desktop = desktop.window(title_re="Remote Desktop")

            # Capture the screenshot of the remote desktop
            screenshot = remote_desktop.capture_as_image()

            # Convert the screenshot to a QPixmap and display it
            pixmap = QPixmap.fromImage(screenshot)
            self.vnc_viewer.setPixmap(pixmap)

        except Exception as e:
            self.show_error_message(f"Error capturing remote screen: {e}")


    def list_remote_files(self):
        # List remote files using SFTP
        if self.ssh_client:
            try:
                self.sftp_client = self.ssh_client.open_sftp()
                files = self.sftp_client.listdir('.')
                QMessageBox.information(self, "Remote Files", "Remote Files:\n" + "\n".join(files))
            except Exception as e:
                self.show_error_message(f"SFTP error: {e}")
        else:
            self.show_error_message("Not connected to remote machine.")



if __name__ == '__main__':
    app = QApplication(sys.argv)
    window = MainWindow()
    window.show()
    sys.exit(app.exec())
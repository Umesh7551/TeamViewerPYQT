import sys
from PyQt5.QtWidgets import QApplication, QWidget, QVBoxLayout, QHBoxLayout, QPushButton, QLabel, QLineEdit
import paramiko


class RemoteControlApp(QWidget):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("Remote Control App")
        self.initUI()

    def initUI(self):
        # Layout
        layout = QVBoxLayout()

        # Connection section
        connection_layout = QHBoxLayout()
        self.host_label = QLabel("Host:")
        self.host_input = QLineEdit()
        self.host_input.setText("remote_host_ip")
        self.port_label = QLabel("Port:")
        self.port_input = QLineEdit()
        self.port_input.setText("22")
        self.connect_button = QPushButton("Connect")
        self.connect_button.clicked.connect(self.connect_to_remote)
        connection_layout.addWidget(self.host_label)
        connection_layout.addWidget(self.host_input)
        connection_layout.addWidget(self.port_label)
        connection_layout.addWidget(self.port_input)
        connection_layout.addWidget(self.connect_button)

        # Status label
        self.status_label = QLabel()

        layout.addLayout(connection_layout)
        layout.addWidget(self.status_label)

        self.setLayout(layout)

    def connect_to_remote(self):
        host = self.host_input.text()
        # port = int(self.port_input.text())
        try:
            # SSH connection
            ssh_client = paramiko.SSHClient()
            ssh_client.set_missing_host_key_policy(paramiko.AutoAddPolicy())
            ssh_client.connect(hostname=host, username='ED-Desk-84', password='Eminent@123')

            # Example: send a command
            stdin, stdout, stderr = ssh_client.exec_command('ls -l')

            # Read the output
            output = stdout.read().decode()

            # Do something with the output, like display it in the GUI
            self.status_label.setText(output)

            ssh_client.close()
        except Exception as e:
            self.status_label.setText(f"Error: {str(e)}")


if __name__ == "__main__":
    app = QApplication(sys.argv)
    window = RemoteControlApp()
    window.show()
    sys.exit(app.exec())

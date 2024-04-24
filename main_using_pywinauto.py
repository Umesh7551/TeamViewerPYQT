import sys
from PyQt6.QtWidgets import QApplication, QMainWindow, QPushButton
from pywinauto import Desktop

class MainWindow(QMainWindow):
    def __init__(self):
        super().__init__()
        self.initUI()

    def initUI(self):
        self.setWindowTitle('PyQt + PyWinAuto')
        self.setGeometry(100, 100, 300, 200)

        self.button = QPushButton('Click Me', self)
        self.button.setGeometry(100, 100, 100, 50)
        self.button.clicked.connect(self.clickButton)

    def clickButton(self):
        # Create a PyWinAuto Desktop object
        desktop = Desktop()

        # Find the Calculator application window
        calculator_window = desktop.window(title="Calculator")

        # Perform actions on the Calculator window
        calculator_window.type_keys('12345')

def main():
    app = QApplication(sys.argv)
    window = MainWindow()
    window.show()
    sys.exit(app.exec())

if __name__ == '__main__':
    main()

import sys

from controller.main import MainController
from PySide6.QtWidgets import QApplication, QMainWindow


class MainWindow(QMainWindow):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("Presenter")

        self.controller = MainController(self)

        self.showMaximized()  # Später zu Fullscreen ändern


if __name__ == "__main__":
    app = QApplication([])
    window = MainWindow()
    sys.exit(app.exec())

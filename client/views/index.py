from PySide6.QtCore import Qt
from PySide6.QtGui import QPixmap
from PySide6.QtWidgets import QLabel, QVBoxLayout, QWidget


class IndexView(QWidget):
    def __init__(self):
        super().__init__()
        self.setLayout(QVBoxLayout())
        self.layout().setAlignment(Qt.AlignmentFlag.AlignCenter)

        self.img = QLabel()
        self.img.setAlignment(Qt.AlignmentFlag.AlignCenter)
        self.layout().addWidget(self.img)

        title = QLabel("Willkommen")
        title.setStyleSheet("font-size: 64pt;")
        title.setAlignment(Qt.AlignmentFlag.AlignCenter)
        self.layout().addWidget(title)

        self.message = QLabel()
        self.message.setStyleSheet("font-size: 12pt;")
        self.message.setAlignment(Qt.AlignmentFlag.AlignCenter)
        self.layout().addWidget(self.message)

        self.set_image(QPixmap("./assets/presenter.png"))

    def set_image(self, pixmap: QPixmap, size=128):
        self.img.setPixmap(
            pixmap.scaledToHeight(size, Qt.TransformationMode.SmoothTransformation)
        )

    def set_message(self, message):
        self.message.setText(message)

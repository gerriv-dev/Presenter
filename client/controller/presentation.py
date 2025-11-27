import requests
from components.websocket import WebSocket
from PySide6.QtCore import QObject, Qt
from PySide6.QtGui import QPixmap
from PySide6.QtWidgets import QLabel, QStackedWidget
from utils.wifi import check_connection
from views.index import IndexView


class PresentationController(QObject):
    def __init__(self):
        super().__init__()
        self.root = QStackedWidget()

        self.index_view = IndexView()
        self.root.addWidget(self.index_view)

        self.index_view.set_message("Überprüfe Internetverbindung...")
        if not check_connection():
            self.index_view.set_message(
                "Keine Internetverbindung. Versuche einen Neustart."
            )

        self.index_view.set_message("Verbinde mit Server...")
        self.ws = WebSocket(
            "wss://presenter-nu.vercel.app/ws",
            self.handle_message,
            lambda: self.index_view.set_message("Verbunden."),
            lambda: self.index_view.set_message("Verbinde mit Server..."),
        )

        self.view = QLabel("test")
        self.view.setAlignment(Qt.AlignmentFlag.AlignCenter)
        self.root.addWidget(self.view)

        self.set_image("presenter.png")

    def set_image(self, name):
        pixmap = QPixmap()
        pixmap.loadFromData(
            requests.get("https://presenter-nu.vercel.app/pp/" + name).content
        )
        self.view.setPixmap(
            pixmap.scaledToHeight(
                self.root.height(), Qt.TransformationMode.SmoothTransformation
            )
        )

    def handle_message(self, message):
        if message == "stop":
            self.root.setCurrentWidget(self.index_view)
        elif len(message) > 5 and message[:5] == "start":
            self.set_image(message[6:])
            self.root.setCurrentWidget(self.view)

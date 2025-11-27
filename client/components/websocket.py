from PySide6.QtCore import QTimer
from PySide6.QtWebSockets import QWebSocket


class WebSocket(QWebSocket):
    def __init__(self, url, on_message, on_connect=None, on_disconnect=None):
        super().__init__()
        self.url = url
        self.disconnect = False
        self.reconnect_interval = 2000

        self.timer = QTimer()
        self.timer.timeout.connect(self.connect)

        self.textMessageReceived.connect(on_message)

        if on_connect is not None:
            self.connected.connect(on_connect)
        self.on_disconnect = on_disconnect

        self.errorOccurred.connect(self.handle_disconnect)
        self.disconnected.connect(self.handle_disconnect)

        self.connect()

    def connect(self):
        self.disconnect = False
        self.open(self.url)

    def disconnect(self):
        self.disconnect = True
        self.close()

    def handle_disconnect(self):
        if not self.disconnect:
            if self.on_disconnect is not None:
                self.on_disconnect()
            self.timer.start(self.reconnect_interval)

from PySide6.QtCore import QObject

from .presentation import PresentationController


class MainController(QObject):
    def __init__(self, parent):
        super().__init__(parent)
        self.controller = None
        self.set_controller(PresentationController)

    def set_controller(self, controller):
        self.controller = controller()
        self.parent().setCentralWidget(self.controller.root)

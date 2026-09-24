from PySide6.QtGui import QColor, QPalette
from PySide6.QtWidgets import QWidget


class Widget(QWidget):
    def __init__(self, parent: QWidget | None = None) -> None:
        super().__init__(parent)
        self.setAutoFillBackground(True)

    def setBackgroundColor(self, color: QColor) -> None:
        palette = self.palette()
        palette.setColor(QPalette.ColorRole.Window, color)
        self.setPalette(palette)

"""MainWindow module for the PySide6 widget tester app."""

from PySide6.QtGui import QColor
from PySide6.QtWidgets import QWidget

from widget import Widget


class MainWindow(Widget):
    def __init__(self, parent: QWidget | None = None) -> None:
        super().__init__(parent)
        self.setWindowTitle("PySide6 Widget Tester")
        self.setBackgroundColor(QColor(20, 20, 20))
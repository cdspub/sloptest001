from PySide6.QtCore import Qt, Signal

from PySide6.QtGui import (
    QColor
)

from PySide6.QtWidgets import (
    QWidget,
)
import os

from widget import Widget

class W(Widget):
    def __init__(self, parent: QWidget | None = None) -> None:
        super().__init__(parent=parent)
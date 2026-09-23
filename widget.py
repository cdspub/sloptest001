"""Widget module for the PySide6 widget tester app."""

from PySide6.QtGui import QColor, QPalette
from PySide6.QtWidgets import QWidget


class Widget(QWidget):
    """A basic custom widget with helper methods for styling."""

    def __init__(self, parent: QWidget | None = None) -> None:
        super().__init__(parent)

    def setBackgroundColor(self, color: QColor) -> None:
        """Set the widget's background color.

        Uses the widget palette so it works correctly under native styles
        (e.g. Windows), without needing to enable stylesheet-based painting.
        """
        palette = self.palette()
        palette.setColor(QPalette.ColorRole.Window, color)
        self.setPalette(palette)

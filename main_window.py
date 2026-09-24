from PySide6.QtGui import QColor
from PySide6.QtWidgets import QApplication, QVBoxLayout, QWidget
from widget import Widget


class MainWindow(Widget):
    def __init__(self, app: QApplication, parent: QWidget | None = None) -> None:
        super().__init__(parent)
        self._app = app
        self.setWindowTitle("PySide6 Widget Tester")
        self.setBackgroundColor(QColor(20, 20, 20))
        layout = QVBoxLayout(self)
        layout.addStretch()
        self._resize_to_screen()

    def _resize_to_screen(self) -> None:
        screen = self._app.primaryScreen()
        if screen is None:
            return
        available = screen.availableGeometry()
        self.resize(int(available.width() * 0.8), int(available.height() * 0.8))
        frame = screen.geometry()
        x = frame.x() + (frame.width() - self.width()) // 2
        y = frame.y() + (frame.height() - self.height()) // 2
        self.move(x, y)

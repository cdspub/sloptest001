from PySide6.QtCore import Qt
from PySide6.QtGui import QColor, QKeySequence, QShortcut
from PySide6.QtWidgets import (
    QApplication,
    QScrollArea,
    QSplitter,
    QVBoxLayout,
    QWidget,
)
from control_widget import ControlWidget
from widget import Widget


class MainWindow(Widget):
    def __init__(self, app: QApplication, parent: QWidget | None = None) -> None:
        super().__init__(parent)
        self._app = app
        self.setWindowTitle("Widget Tester")
        self.setBackgroundColor(QColor(20, 20, 20))
        layout = QVBoxLayout(self)
        layout.addWidget(self._create_splitter())
        shortcut = QShortcut(QKeySequence(Qt.Key.Key_Escape), self)
        shortcut.activated.connect(self._on_escape)
        self._resize_to_screen()

    def _create_splitter(self) -> QSplitter:
        splitter = QSplitter(Qt.Orientation.Horizontal, self)
        self.control_widget = ControlWidget()
        self.control_widget.new_button.clicked.connect(self._on_new_button_clicked)
        scroll_area = QScrollArea()
        scroll_area.setWidgetResizable(True)
        scroll_area.setWidget(self.control_widget)
        right_pane = QWidget()
        QVBoxLayout(right_pane)
        splitter.addWidget(scroll_area)
        splitter.addWidget(right_pane)
        self._splitter = splitter
        total_width = self.width() if self.width() > 0 else 800
        splitter.setSizes([int(total_width * 0.2), int(total_width * 0.8)])
        return splitter

    def _on_escape(self) -> None:
        self.close()
        self._app.quit()

    def _on_new_button_clicked(self) -> None:
        print("New button clicked")

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
        total_width = self.width()
        self._splitter.setSizes([int(total_width * 0.2), int(total_width * 0.8)])

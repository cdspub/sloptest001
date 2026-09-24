from PySide6.QtGui import QColor
from PySide6.QtWidgets import QApplication, QMenuBar, QMenu, QVBoxLayout, QWidget
from widget import Widget


class MainWindow(Widget):
    def __init__(self, app: QApplication, parent: QWidget | None = None) -> None:
        super().__init__(parent)
        self._app = app
        self.setWindowTitle("PySide6 Widget Tester")
        self.setBackgroundColor(QColor(20, 20, 20))
        self._create_menu()
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

    def _create_menu(self) -> None:
        menu_bar = QMenuBar(self)
        new_menu: QMenu = menu_bar.addMenu("New")
        new_widget_action = new_menu.addAction("Widget")
        new_widget_action.triggered.connect(self._on_new_widget)

        layout = QVBoxLayout(self)
        layout.setContentsMargins(0, 0, 0, 0)
        layout.addWidget(menu_bar)
        layout.addStretch()

    def _on_new_widget(self) -> None:
        print("New Widget action triggered")

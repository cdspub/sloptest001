"""MainWindow module for the PySide6 widget tester app."""


from PySide6.QtGui import QColor
from PySide6.QtWidgets import QMenuBar, QMenu, QVBoxLayout, QWidget
from widget import Widget


class MainWindow(Widget):
    def __init__(self, parent: QWidget | None = None) -> None:
        super().__init__(parent)
        self.setWindowTitle("PySide6 Widget Tester")
        self.setBackgroundColor(QColor(20, 20, 20))
        self._create_menu()

    def _create_menu(self) -> None:
        """Create a menu bar with a single ``New`` menu and ``Widget`` action.

        ``Widget`` is not a ``QMainWindow``, so the menu bar is added to the
        widget's own layout instead of using ``QMainWindow.menuBar()``.
        """
        menu_bar = QMenuBar(self)
        new_menu: QMenu = menu_bar.addMenu("New")
        new_widget_action = new_menu.addAction("Widget")
        new_widget_action.triggered.connect(self._on_new_widget)

        layout = QVBoxLayout(self)
        layout.setContentsMargins(0, 0, 0, 0)
        layout.addWidget(menu_bar)
        layout.addStretch()

    def _on_new_widget(self) -> None:
        """Handle the ``New -> Widget`` action (stub)."""
        print("New Widget action triggered")

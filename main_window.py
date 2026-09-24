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
        self._widget_on_pane: Widget | None = None
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
        self.control_widget.add_button.clicked.connect(
            self._on_add_button_clicked)
        self.control_widget.remove_button.clicked.connect(
            self._on_remove_button_clicked)
        self.control_widget.sizeChanged.connect(self._on_size_changed)
        self.control_widget.backgroundColorChanged.connect(
            self._on_background_color_changed
        )
        self.control_widget.widgetRenamed.connect(self._on_widget_renamed)
        scroll_area = QScrollArea()
        scroll_area.setWidgetResizable(True)
        scroll_area.setWidget(self.control_widget)
        self.right_pane = QWidget()
        right_layout = QVBoxLayout(self.right_pane)
        right_layout.setAlignment(Qt.AlignmentFlag.AlignCenter)
        splitter.addWidget(scroll_area)
        splitter.addWidget(self.right_pane)
        self._splitter = splitter
        total_width = self.width() if self.width() > 0 else 800
        splitter.setSizes([int(total_width * 0.2), int(total_width * 0.8)])
        return splitter

    def _on_escape(self) -> None:
        self.close()
        self._app.quit()

    def _on_add_button_clicked(self) -> None:
        widget = self._widget_on_pane
        if widget is not None:
            return
        widget = Widget()
        widget.setObjectName(self.control_widget.name_line_input.text())
        widget.resize(
            self.control_widget.current_width(),
            self.control_widget.current_height(),
        )
        widget.setBackgroundColor(self.control_widget.current_background_color())
        self._widget_on_pane = widget
        self._place_widget_center()

    def _on_remove_button_clicked(self) -> None:
        self._remove_current_widget()

    def _on_size_changed(self, width: int, height: int) -> None:
        widget = self._widget_on_pane
        if widget is None:
            return
        widget.resize(width, height)
        self._place_widget_center()

    def _on_background_color_changed(self, color: QColor) -> None:
        widget = self._widget_on_pane
        if widget is not None:
            widget.setBackgroundColor(color)

    def _on_widget_renamed(self, name: str) -> None:
        widget = self._widget_on_pane
        if widget is not None:
            widget.setObjectName(name)

    def _remove_current_widget(self) -> None:
        if self._widget_on_pane is not None:
            self._widget_on_pane.setParent(None)
            self._widget_on_pane.deleteLater()
            self._widget_on_pane = None

    def _place_widget_center(self) -> None:
        widget = self._widget_on_pane
        if widget is None:
            return
        widget.setParent(self.right_pane)
        pane_size = self.right_pane.size()
        x = max(0, (pane_size.width() - widget.width()) // 2)
        y = max(0, (pane_size.height() - widget.height()) // 2)
        widget.move(x, y)
        widget.show()

    def resizeEvent(self, event) -> None:
        super().resizeEvent(event)
        self._place_widget_center()

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

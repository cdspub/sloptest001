from PySide6.QtCore import Signal
from PySide6.QtGui import QColor
from PySide6.QtWidgets import (
    QColorDialog,
    QFormLayout,
    QGroupBox,
    QPushButton,
    QLineEdit,
    QSpinBox,
    QVBoxLayout,
    QWidget,
)

from widget import Widget


class ColorButton(QPushButton):
    colorChanged = Signal(QColor)

    def __init__(self, color: QColor, parent: QWidget | None = None) -> None:
        super().__init__(parent)
        self._color = QColor(color)
        self.setText(self._color.name())
        self.clicked.connect(self._on_clicked)
        self._update_style()

    def color(self) -> QColor:
        return QColor(self._color)

    def setColor(self, color: QColor) -> None:
        self._color = QColor(color)
        self.setText(self._color.name())
        self._update_style()
        self.colorChanged.emit(self._color)

    def _on_clicked(self) -> None:
        chosen = QColorDialog.getColor(self._color, self, "Select Background Color")
        if chosen.isValid():
            self.setColor(chosen)

    def _update_style(self) -> None:
        text_color = "white" if self._color.lightnessF() < 0.5 else "black"
        self.setStyleSheet(
            f"background-color: {self._color.name()}; color: {text_color};"
        )


class ControlWidget(Widget):
    widgetRenamed = Signal(str)
    sizeChanged = Signal(int, int)
    backgroundColorChanged = Signal(QColor)

    def __init__(self, parent: QWidget | None = None) -> None:
        super().__init__(parent)

        self.new_button = QPushButton("New", self)
        self.name_line_input = QLineEdit(self)
        self.width_spin_input = QSpinBox(self)
        self.width_spin_input.setRange(1, 100000)
        self.width_spin_input.setValue(500)
        self.height_spin_input = QSpinBox(self)
        self.height_spin_input.setRange(1, 100000)
        self.height_spin_input.setValue(500)
        self.background_color_input = ColorButton(QColor("#808080"), self)

        labeled_frame = QGroupBox("Widget", self)
        form_layout = QFormLayout(labeled_frame)
        form_layout.addRow("Name:", self.name_line_input)
        form_layout.addRow("Width:", self.width_spin_input)
        form_layout.addRow("Height:", self.height_spin_input)
        form_layout.addRow("Background color:", self.background_color_input)

        layout = QVBoxLayout(self)
        layout.addWidget(self.new_button)
        layout.addWidget(labeled_frame)
        layout.addStretch()

        self.name_line_input.textChanged.connect(self._on_name_changed)
        self.width_spin_input.valueChanged.connect(self._emit_size_changed)
        self.height_spin_input.valueChanged.connect(self._emit_size_changed)
        self.background_color_input.colorChanged.connect(self._on_bg_color_changed)

    def current_width(self) -> int:
        return self.width_spin_input.value()

    def current_height(self) -> int:
        return self.height_spin_input.value()

    def current_background_color(self) -> QColor:
        return self.background_color_input.color()

    def _emit_size_changed(self) -> None:
        self.sizeChanged.emit(self.current_width(), self.current_height())

    def _on_name_changed(self, name: str) -> None:
        self.widgetRenamed.emit(name)

    def _on_bg_color_changed(self, color: QColor) -> None:
        self.backgroundColorChanged.emit(color)

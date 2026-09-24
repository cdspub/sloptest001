from PySide6.QtCore import Qt, Signal
from PySide6.QtGui import QBrush, QColor, QIcon, QPainter, QPixmap
from PySide6.QtWidgets import (
    QColorDialog,
    QComboBox,
    QFormLayout,
    QGroupBox,
    QPushButton,
    QLineEdit,
    QSpinBox,
    QVBoxLayout,
    QWidget,
)

from widget import _BORDER_STYLES, _FILL_PATTERNS, Widget


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


class PatternButton(QPushButton):
    patternChanged = Signal(str)

    def __init__(self, pattern_name: str, color: QColor, parent: QWidget | None = None) -> None:
        super().__init__(parent)
        self._pattern_name = pattern_name
        self._color = QColor(color)
        self.setMinimumHeight(32)
        self.clicked.connect(self._on_clicked)
        self._update_display()

    def patternName(self) -> str:
        return self._pattern_name

    def setPattern(self, pattern_name: str) -> None:
        if pattern_name in _FILL_PATTERNS:
            self._pattern_name = pattern_name
            self._update_display()
            self.patternChanged.emit(self._pattern_name)

    def setColor(self, color: QColor) -> None:
        self._color = QColor(color)
        self._update_display()

    def _on_clicked(self) -> None:
        dialog = QComboBox(self)
        for name in _FILL_PATTERNS:
            dialog.addItem(self._pattern_pixmap(name), name)
        dialog.setCurrentIndex(dialog.findText(self._pattern_name))
        dialog.activated.connect(
            lambda index: self.setPattern(dialog.itemText(index))
        )
        popup_pos = dialog.mapToGlobal(dialog.rect().bottomLeft())
        dialog.view().setMinimumWidth(dialog.sizeHint().width())
        dialog.showPopup()
        dialog.move(popup_pos)

    def _pattern_pixmap(self, pattern_name: str) -> QPixmap:
        pixmap = QPixmap(64, 24)
        pixmap.fill(Qt.GlobalColor.transparent)
        painter = QPainter(pixmap)
        brush_color = QColor(self._color) if pattern_name == "Solid" else QColor("black")
        painter.fillRect(
            pixmap.rect(),
            QBrush(brush_color, _FILL_PATTERNS[pattern_name]),
        )
        painter.end()
        return pixmap

    def _update_display(self) -> None:
        self.setIcon(QIcon(self._pattern_pixmap(self._pattern_name)))
        self.setText(self._pattern_name)


class ControlWidget(Widget):
    widgetRenamed = Signal(str)
    sizeChanged = Signal(int, int)
    backgroundColorChanged = Signal(QColor)
    borderWidthChanged = Signal(int)
    borderStyleChanged = Signal(str)
    borderColorChanged = Signal(QColor)
    cornerRadiusChanged = Signal(int)
    fillPatternChanged = Signal(str)

    def __init__(self, parent: QWidget | None = None) -> None:
        super().__init__(parent)

        self.add_button = QPushButton("Add", self)
        self.remove_button = QPushButton("Remove", self)
        self.name_line_input = QLineEdit(self)
        self.width_spin_input = QSpinBox(self)
        self.width_spin_input.setRange(1, 100000)
        self.width_spin_input.setValue(500)
        self.height_spin_input = QSpinBox(self)
        self.height_spin_input.setRange(1, 100000)
        self.height_spin_input.setValue(500)
        self.background_color_input = ColorButton(QColor("#808080"), self)
        self.border_width_spin_input = QSpinBox(self)
        self.border_width_spin_input.setRange(0, 100)
        self.border_style_combo_input = QComboBox(self)
        self.border_style_combo_input.addItems(_BORDER_STYLES.keys())
        self.border_color_input = ColorButton(QColor("black"), self)
        self.corner_radius_spin_input = QSpinBox(self)
        self.corner_radius_spin_input.setRange(0, 1000)
        self.fill_pattern_input = PatternButton("Solid", QColor("#808080"), self)

        labeled_frame = QGroupBox("Widget", self)
        form_layout = QFormLayout(labeled_frame)
        form_layout.addRow("Name:", self.name_line_input)
        form_layout.addRow("Width:", self.width_spin_input)
        form_layout.addRow("Height:", self.height_spin_input)
        form_layout.addRow("Background color:", self.background_color_input)
        form_layout.addRow("Background fill pattern:", self.fill_pattern_input)
        form_layout.addRow("Border width:", self.border_width_spin_input)
        form_layout.addRow("Border style:", self.border_style_combo_input)
        form_layout.addRow("Border color:", self.border_color_input)
        form_layout.addRow("Corner radius:", self.corner_radius_spin_input)

        layout = QVBoxLayout(self)
        layout.addWidget(self.add_button)
        layout.addWidget(self.remove_button)
        layout.addWidget(labeled_frame)
        layout.addStretch()

        self.name_line_input.textChanged.connect(self._on_name_changed)
        self.width_spin_input.valueChanged.connect(self._emit_size_changed)
        self.height_spin_input.valueChanged.connect(self._emit_size_changed)
        self.background_color_input.colorChanged.connect(self._on_bg_color_changed)
        self.border_width_spin_input.valueChanged.connect(
            self.borderWidthChanged.emit
        )
        self.border_style_combo_input.currentTextChanged.connect(
            self.borderStyleChanged.emit
        )
        self.border_color_input.colorChanged.connect(self.borderColorChanged.emit)
        self.corner_radius_spin_input.valueChanged.connect(
            self.cornerRadiusChanged.emit
        )
        self.fill_pattern_input.patternChanged.connect(self.fillPatternChanged.emit)

    def current_width(self) -> int:
        return self.width_spin_input.value()

    def current_height(self) -> int:
        return self.height_spin_input.value()

    def current_background_color(self) -> QColor:
        return self.background_color_input.color()

    def current_border_width(self) -> int:
        return self.border_width_spin_input.value()

    def current_border_style(self) -> str:
        return self.border_style_combo_input.currentText()

    def current_border_color(self) -> QColor:
        return self.border_color_input.color()

    def current_corner_radius(self) -> int:
        return self.corner_radius_spin_input.value()

    def current_fill_pattern(self) -> str:
        return self.fill_pattern_input.patternName()

    def _emit_size_changed(self) -> None:
        self.sizeChanged.emit(self.current_width(), self.current_height())

    def _on_name_changed(self, name: str) -> None:
        self.widgetRenamed.emit(name)

    def _on_bg_color_changed(self, color: QColor) -> None:
        self.fill_pattern_input.setColor(color)
        self.backgroundColorChanged.emit(color)

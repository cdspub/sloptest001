from PySide6.QtWidgets import (
    QFormLayout,
    QGroupBox,
    QPushButton,
    QLineEdit,
    QSpinBox,
    QVBoxLayout,
    QWidget,
)

from widget import Widget


class ControlWidget(Widget):
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

        labeled_frame = QGroupBox("Widget", self)
        form_layout = QFormLayout(labeled_frame)
        form_layout.addRow("Name:", self.name_line_input)
        form_layout.addRow("Width:", self.width_spin_input)
        form_layout.addRow("Height:", self.height_spin_input)

        layout = QVBoxLayout(self)
        layout.addWidget(self.new_button)
        layout.addWidget(labeled_frame)
        layout.addStretch()

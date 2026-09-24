from PySide6.QtWidgets import (
    QFormLayout,
    QGroupBox,
    QPushButton,
    QLineEdit,
    QVBoxLayout,
    QWidget,
)

from widget import Widget


class ControlWidget(Widget):
    def __init__(self, parent: QWidget | None = None) -> None:
        super().__init__(parent)

        self.new_button = QPushButton("New", self)
        self.name_line_input = QLineEdit(self)

        labeled_frame = QGroupBox("Name", self)
        form_layout = QFormLayout(labeled_frame)
        form_layout.addRow("Name:", self.name_line_input)

        layout = QVBoxLayout(self)
        layout.addWidget(self.new_button)
        layout.addWidget(labeled_frame)
        layout.addStretch()

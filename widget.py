from PySide6.QtCore import Qt
from PySide6.QtGui import (
    QBrush,
    QColor,
    QPainter,
    QPaintEvent,
    QPalette,
    QPen,
)
from PySide6.QtWidgets import QWidget

_BORDER_STYLES = {
    "None": Qt.PenStyle.NoPen,
    "Solid": Qt.PenStyle.SolidLine,
    "Dash": Qt.PenStyle.DashLine,
    "Dot": Qt.PenStyle.DotLine,
    "Dash Dot": Qt.PenStyle.DashDotLine,
    "Dash Dot Dot": Qt.PenStyle.DashDotDotLine,
}

_FILL_PATTERNS = {
    "Solid": Qt.BrushStyle.SolidPattern,
    "Horizontal": Qt.BrushStyle.HorPattern,
    "Vertical": Qt.BrushStyle.VerPattern,
    "Reverse diagonal": Qt.BrushStyle.BDiagPattern,
    "Forward diagonal": Qt.BrushStyle.FDiagPattern,
    "Crossed diagonals": Qt.BrushStyle.DiagCrossPattern,
    "Dense 1": Qt.BrushStyle.Dense1Pattern,
    "Dense 2": Qt.BrushStyle.Dense2Pattern,
    "Dense 3": Qt.BrushStyle.Dense3Pattern,
    "Dense 4": Qt.BrushStyle.Dense4Pattern,
    "Dense 5": Qt.BrushStyle.Dense5Pattern,
    "Dense 6": Qt.BrushStyle.Dense6Pattern,
    "Dense 7": Qt.BrushStyle.Dense7Pattern,
    "Cross": Qt.BrushStyle.CrossPattern,
}


class Widget(QWidget):
    def __init__(self, parent: QWidget | None = None) -> None:
        super().__init__(parent)
        self.setAutoFillBackground(True)
        self._border_width = 0
        self._border_style_name = "None"
        self._border_color = QColor("black")
        self._corner_radius = 0
        self._fill_pattern_name = "Solid"

    def setBackgroundColor(self, color: QColor) -> None:
        self._background_color = QColor(color)
        palette = self.palette()
        palette.setColor(QPalette.ColorRole.Window, self._background_color)
        self.setPalette(palette)
        self.update()

    def setBorderWidth(self, width: int) -> None:
        self._border_width = max(0, width)
        self.update()

    def setBorderStyle(self, style_name: str) -> None:
        if style_name in _BORDER_STYLES:
            self._border_style_name = style_name
            self.update()

    def setBorderColor(self, color: QColor) -> None:
        self._border_color = QColor(color)
        self.update()

    def setCornerRadius(self, radius: int) -> None:
        self._corner_radius = max(0, radius)
        self.update()

    def setBackgroundFillPattern(self, pattern_name: str) -> None:
        if pattern_name in _FILL_PATTERNS:
            self._fill_pattern_name = pattern_name
            self.update()

    def paintEvent(self, event: QPaintEvent) -> None:
        super().paintEvent(event)
        painter = QPainter(self)
        painter.setRenderHint(QPainter.RenderHint.Antialiasing)
        background = QColor(self.palette().color(QPalette.ColorRole.Window))
        brush = QBrush(background, _FILL_PATTERNS[self._fill_pattern_name])
        pen = QPen(self._border_color, self._border_width)
        pen.setStyle(_BORDER_STYLES[self._border_style_name])
        painter.setPen(pen)
        painter.setBrush(brush)
        inset = self._border_width / 2.0 if self._border_width > 0 else 0.0
        rect = self.rect().adjusted(inset, inset, -inset, -inset)
        if self._corner_radius > 0:
            painter.drawRoundedRect(rect, self._corner_radius, self._corner_radius)
        else:
            painter.drawRect(rect)
        painter.end()

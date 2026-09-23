"""MainWindow module for the PySide6 widget tester app."""

from PySide6.QtWidgets import QWidget

from widget import Widget


class MainWindow(Widget):
    """The application's main window widget.

    Inherits from :class:`widget.Widget` so it gains the custom helper
    methods (e.g. ``setBackgroundColor``) defined there.
    """

    def __init__(self, parent: QWidget | None = None) -> None:
        super().__init__(parent)
        self.setWindowTitle("PySide6 Widget Tester")

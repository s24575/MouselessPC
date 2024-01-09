import sys

from PySide6.QtWidgets import QApplication

from ui_main_window import UiMainFrame


if __name__ == "__main__":
    app = QApplication(sys.argv)
    widget = UiMainFrame()
    widget.show()
    sys.exit(app.exec())

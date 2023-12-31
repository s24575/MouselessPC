import sys

from PySide6.QtWidgets import QApplication

from ui_mainWindow import Ui_main_frame


if __name__ == "__main__":
    app = QApplication(sys.argv)
    widget = Ui_main_frame()
    widget.show()
    sys.exit(app.exec())

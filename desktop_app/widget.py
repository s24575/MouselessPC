import sys

from PySide6.QtWidgets import QApplication, QWidget, QMainWindow
from ui_mainWindow import Ui_mainFrame


class Widget(QMainWindow):
    def __init__(self, parent=None):
        super().__init__(parent)
        self.ui = Ui_mainFrame()
        self.ui.setupUi(self)


if __name__ == "__main__":
    app = QApplication(sys.argv)
    widget = Widget()
    widget.show()
    sys.exit(app.exec())

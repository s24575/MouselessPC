from PySide6.QtWidgets import (QApplication, QFrame, QGraphicsView, QHBoxLayout,
                               QLabel, QListView, QPushButton, QSizePolicy,
                               QVBoxLayout, QWidget, QComboBox, QFormLayout, QDialog, QInputDialog, QLineEdit,
                               QMessageBox, QDialogButtonBox, QSpacerItem)
from PySide6.QtGui import *
from PySide6.QtCore import *
import re


class UiSettings(QDialog):
    def __init__(self, parent=None):
        super().__init__(parent)
        self.parent_window = parent
        self.setupUi()

    def setupUi(self):
        self.setGeometry(600, 450, 400, 150)
        self.cancel = QPushButton(self)
        self.cancel.setObjectName(u"cancel")
        self.cancel.setGeometry(QRect(300, 110, 80, 24))
        self.cancel.clicked.connect(self.cancel_clicked)

        self.horizontalLayoutWidget = QWidget(self)
        self.horizontalLayoutWidget.setObjectName(u"horizontalLayoutWidget")
        self.horizontalLayoutWidget.setGeometry(QRect(85, 0, 200, 160))
        self.horizontalLayout = QHBoxLayout(self.horizontalLayoutWidget)
        self.horizontalLayout.setObjectName(u"horizontalLayout")
        self.horizontalLayout.setContentsMargins(0, 0, 0, 0)
        self.webcam = QPushButton(self.horizontalLayoutWidget)
        self.webcam.setObjectName(u"webcam")
        self.webcam.clicked.connect(self.webcam_clicked)

        self.horizontalLayout.addWidget(self.webcam)

        self.smartphone = QPushButton(self.horizontalLayoutWidget)
        self.smartphone.setObjectName(u"smartphone")
        self.smartphone.clicked.connect(self.smartphone_clicked)

        self.horizontalLayout.addWidget(self.smartphone)

        self.label = QLabel(self)
        self.label.setObjectName(u"label")
        self.label.setGeometry(QRect(90, 10, 191, 41))
        font = QFont()
        font.setPointSize(12)
        self.label.setFont(font)

        self.retranslateUi(self)

        QMetaObject.connectSlotsByName(self)

    def retranslateUi(self, Dialog):
        Dialog.setWindowTitle(QCoreApplication.translate("Dialog", u"Dialog", None))
        self.cancel.setText(QCoreApplication.translate("Dialog", u"Cancel", None))
        self.webcam.setText(QCoreApplication.translate("Dialog", u"Webcam", None))
        self.smartphone.setText(QCoreApplication.translate("Dialog", u"Smartphone", None))
        self.label.setText(QCoreApplication.translate("Dialog", u"Chose video source:", None))

    def webcam_clicked(self):
        self.parent_window.change_video_source(0)
        self.hide()

    def smartphone_clicked(self):
        dialog = self.InputDialog(self)

        address, port, parameter = None, None, None
        if dialog.exec_():
            address, port, parameter = dialog.get_inputs()

        if address and port:
            pattern_address = re.compile("\d{1,3}\.\d{1,3}\.\d{1,3}\.\d{1,3}")
            if not re.fullmatch(pattern_address, address):
                QMessageBox.warning(self, "Error", "Invalid IP address")
                return None

            pattern_port = re.compile("\d{0,5}")
            if not re.fullmatch(pattern_port, port):
                QMessageBox.warning(self, "Error", "Invalid port number")
                return None

            url = f"http://{address}:{port}"

            if parameter:
                url = url + f"/{parameter}"

            self.parent_window.change_video_source(url)
            self.hide()

    def cancel_clicked(self):
        print("Cancel button clicked")
        self.hide()

    class InputDialog(QDialog):
        def __init__(self, parent=None):
            super().__init__(parent)

            self.address = QLineEdit(self)
            self.address.setPlaceholderText("192.168.1.1")
            self.port = QLineEdit(self)
            self.port.setPlaceholderText("4747")
            self.parameter = QLineEdit(self)
            self.parameter.setPlaceholderText("video")

            buttonBox = QDialogButtonBox(QDialogButtonBox.Ok | QDialogButtonBox.Cancel, self)

            layout = QFormLayout(self)
            layout.addRow("IP address:", self.address)
            layout.addRow("Port:", self.port)
            layout.addRow("Parameter:", self.parameter)
            layout.addWidget(buttonBox)

            buttonBox.accepted.connect(self.accept)
            buttonBox.rejected.connect(self.reject)

        def get_inputs(self):
            return self.address.text(), self.port.text(), self.parameter.text()

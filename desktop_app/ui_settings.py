import sys

from PySide6.QtUiTools import QUiLoader
from PySide6.QtWidgets import (QApplication, QFrame, QGraphicsView, QHBoxLayout,
                               QLabel, QListView, QPushButton, QSizePolicy,
                               QVBoxLayout, QWidget, QComboBox, QFormLayout, QDialog)
from PySide6.QtGui import *
from PySide6.QtCore import *

class Ui_settings(QWidget):
    def __init__(self, parent=None):
        super().__init__()
        # self.setParent(parent)
        layout = QVBoxLayout()
        self.title = QLabel("settings")
        self.title.setObjectName(u"title")
        self.title.setGeometry(QRect(110, 10, 49, 16))
        layout.addWidget(self.title)

        self.source_label = QLabel()
        self.source_label.setObjectName(u"sourc_label")
        self.source_label.setGeometry(QRect(100, 50, 101, 16))
        self.source_label.setTextFormat(Qt.PlainText)
        layout.addWidget(self.source_label)

        self.horizontalLayoutWidget = QWidget()
        self.horizontalLayoutWidget.setObjectName(u"horizontalLayoutWidget")
        self.horizontalLayoutWidget.setGeometry(QRect(50, 70, 168, 51))

        self.source_container = QHBoxLayout(self.horizontalLayoutWidget)
        self.source_container.setObjectName(u"source_container")
        self.source_container.setContentsMargins(0, 0, 0, 0)

        self.webcam = QPushButton(self.horizontalLayoutWidget)
        self.webcam.setObjectName(u"webcam")

        self.source_container.addWidget(self.webcam)

        self.pushButton_2 = QPushButton(self.horizontalLayoutWidget)
        self.pushButton_2.setObjectName(u"pushButton_2")
        self.pushButton_2.setEnabled(False)

        layout.addWidget(self.horizontalLayoutWidget)

        self.source_container.addWidget(self.pushButton_2)

        self.gesture_label = QLabel()
        self.gesture_label.setObjectName(u"gesture_label")
        self.gesture_label.setGeometry(QRect(100, 140, 49, 16))
        layout.addWidget(self.gesture_label)

        self.formLayoutWidget = QWidget()
        self.formLayoutWidget.setObjectName(u"formLayoutWidget")
        self.formLayoutWidget.setGeometry(QRect(50, 170, 171, 161))
        self.gestures_container = QFormLayout(self.formLayoutWidget)
        self.gestures_container.setObjectName(u"gestures_container")
        self.gestures_container.setHorizontalSpacing(15)
        self.gestures_container.setContentsMargins(5, 0, 0, 0)
        self.label_2 = QLabel(self.formLayoutWidget)
        self.label_2.setObjectName(u"label_2")

        self.gestures_container.setWidget(0, QFormLayout.LabelRole, self.label_2)

        self.label_3 = QLabel(self.formLayoutWidget)
        self.label_3.setObjectName(u"label_3")

        self.gestures_container.setWidget(2, QFormLayout.LabelRole, self.label_3)

        self.label_4 = QLabel(self.formLayoutWidget)
        self.label_4.setObjectName(u"label_4")

        self.gestures_container.setWidget(1, QFormLayout.LabelRole, self.label_4)

        self.label_5 = QLabel(self.formLayoutWidget)
        self.label_5.setObjectName(u"label_5")

        self.gestures_container.setWidget(3, QFormLayout.LabelRole, self.label_5)

        self.comboBox = QComboBox(self.formLayoutWidget)
        self.comboBox.setObjectName(u"comboBox")

        self.gestures_container.setWidget(0, QFormLayout.FieldRole, self.comboBox)

        self.comboBox_2 = QComboBox(self.formLayoutWidget)
        self.comboBox_2.setObjectName(u"comboBox_2")

        self.gestures_container.setWidget(1, QFormLayout.FieldRole, self.comboBox_2)

        self.comboBox_3 = QComboBox(self.formLayoutWidget)
        self.comboBox_3.setObjectName(u"comboBox_3")

        self.gestures_container.setWidget(2, QFormLayout.FieldRole, self.comboBox_3)

        self.comboBox_4 = QComboBox(self.formLayoutWidget)
        self.comboBox_4.setObjectName(u"comboBox_4")

        layout.addWidget(self.formLayoutWidget)

        self.gestures_container.setWidget(3, QFormLayout.FieldRole, self.comboBox_4)

        self.pushButton = QPushButton()
        self.pushButton.setObjectName(u"pushButton")
        self.pushButton.setGeometry(QRect(200, 350, 80, 24))
        layout.addWidget(self.pushButton)
        self.pushButton_3 = QPushButton()
        self.pushButton_3.setObjectName(u"pushButton_3")
        self.pushButton_3.setGeometry(QRect(110, 350, 80, 24))
        layout.addWidget(self.pushButton_3)
        self.pushButton_4 = QPushButton()
        self.pushButton_4.setObjectName(u"pushButton_4")
        self.pushButton_4.setGeometry(QRect(0, 350, 80, 24))
        layout.addWidget(self.pushButton_4)

        self.retranslateUi()
        self.setLayout(layout)
    # setupUi

    def retranslateUi(self):
        self.title.setText(QCoreApplication.translate("settings", u"Settings", None))
        self.source_label.setText(QCoreApplication.translate("settings", u"Video source", None))
        self.webcam.setText(QCoreApplication.translate("settings", u"Webcam", None))
        self.pushButton_2.setText(QCoreApplication.translate("settings", u"Smartphone", None))
        self.gesture_label.setText(QCoreApplication.translate("settings", u"Gestures", None))
        self.label_2.setText(QCoreApplication.translate("settings", u"TextLabel", None))
        self.label_3.setText(QCoreApplication.translate("settings", u"TextLabel", None))
        self.label_4.setText(QCoreApplication.translate("settings", u"TextLabel", None))
        self.label_5.setText(QCoreApplication.translate("settings", u"TextLabel", None))
        self.pushButton.setText(QCoreApplication.translate("settings", u"Submit", None))
        self.pushButton_3.setText(QCoreApplication.translate("settings", u"Default", None))
        self.pushButton_4.setText(QCoreApplication.translate("settings", u"Cancel", None))
    # retranslateUi


    def submit_clicked(self):
        print("Submit button clicked")

    def default_clicked(self):
        print("Default button clicked")

    def cancel_clicked(self):
        print("Cancel button clicked")

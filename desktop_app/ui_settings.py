from PySide6.QtWidgets import (QApplication, QFrame, QGraphicsView, QHBoxLayout,
                               QLabel, QListView, QPushButton, QSizePolicy,
                               QVBoxLayout, QWidget, QComboBox, QFormLayout, QDialog)
from PySide6.QtGui import *
from PySide6.QtCore import *


class UiSettings(QWidget):
    def __init__(self, parent=None):
        super().__init__()

        self.parent_window = parent
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

        self.smartphone = QPushButton(self.horizontalLayoutWidget)
        self.smartphone.setObjectName(u"smartphone")
        self.smartphone.setEnabled(False)

        layout.addWidget(self.horizontalLayoutWidget)

        self.source_container.addWidget(self.smartphone)

        self.gesture_label = QLabel()
        self.gesture_label.setObjectName(u"gesture_label")
        self.gesture_label.setGeometry(QRect(100, 140, 49, 16))
        layout.addWidget(self.gesture_label)

        self.form_layout_widget = QWidget()
        self.form_layout_widget.setObjectName(u"formLayoutWidget")
        self.form_layout_widget.setGeometry(QRect(50, 170, 171, 161))
        self.gestures_container = QFormLayout(self.form_layout_widget)
        self.gestures_container.setObjectName(u"gestures_container")
        self.gestures_container.setHorizontalSpacing(15)
        self.gestures_container.setContentsMargins(5, 0, 0, 0)
        self.label_2 = QLabel(self.form_layout_widget)
        self.label_2.setObjectName(u"label_2")

        self.gestures_container.setWidget(0, QFormLayout.LabelRole, self.label_2)

        self.label_3 = QLabel(self.form_layout_widget)
        self.label_3.setObjectName(u"label_3")

        self.gestures_container.setWidget(2, QFormLayout.LabelRole, self.label_3)

        self.label_4 = QLabel(self.form_layout_widget)
        self.label_4.setObjectName(u"label_4")

        self.gestures_container.setWidget(1, QFormLayout.LabelRole, self.label_4)

        self.label_5 = QLabel(self.form_layout_widget)
        self.label_5.setObjectName(u"label_5")

        self.gestures_container.setWidget(3, QFormLayout.LabelRole, self.label_5)

        self.combo_box = QComboBox(self.form_layout_widget)
        self.combo_box.setObjectName(u"comboBox")
        self.combo_box.addItem('action 1')

        self.gestures_container.setWidget(0, QFormLayout.FieldRole, self.combo_box)

        self.combo_box_2 = QComboBox(self.form_layout_widget)
        self.combo_box_2.setObjectName(u"comboBox_2")
        self.combo_box_2.addItem('action 2')

        self.gestures_container.setWidget(1, QFormLayout.FieldRole, self.combo_box_2)

        self.combo_box_3 = QComboBox(self.form_layout_widget)
        self.combo_box_3.setObjectName(u"comboBox_3")
        self.combo_box_3.addItem('action 3')

        self.gestures_container.setWidget(2, QFormLayout.FieldRole, self.combo_box_3)

        self.combo_box_4 = QComboBox(self.form_layout_widget)
        self.combo_box_4.setObjectName(u"comboBox_4")
        self.combo_box_4.addItem('action 3')

        layout.addWidget(self.form_layout_widget)

        self.gestures_container.setWidget(3, QFormLayout.FieldRole, self.combo_box_4)

        self.submit_btn = QPushButton()
        self.submit_btn.setObjectName(u"submit_btn")
        self.submit_btn.setGeometry(QRect(200, 350, 80, 24))
        self.submit_btn.clicked.connect(self.submit_clicked)
        layout.addWidget(self.submit_btn)
        self.default_btn = QPushButton()
        self.default_btn.setObjectName(u"default_btn")
        self.default_btn.setGeometry(QRect(110, 350, 80, 24))
        self.default_btn.clicked.connect(self.default_clicked)
        layout.addWidget(self.default_btn)
        self.cancel_btn = QPushButton()
        self.cancel_btn.setObjectName(u"cancel_btn")
        self.cancel_btn.setGeometry(QRect(0, 350, 80, 24))
        self.cancel_btn.clicked.connect(self.cancel_clicked)
        layout.addWidget(self.cancel_btn)

        self.retranslate_ui()
        self.setLayout(layout)
    # setupUi

    def retranslate_ui(self):
        self.title.setText(QCoreApplication.translate("settings", u"Settings", None))
        self.source_label.setText(QCoreApplication.translate("settings", u"Video source", None))
        self.webcam.setText(QCoreApplication.translate("settings", u"Webcam", None))
        self.smartphone.setText(QCoreApplication.translate("settings", u"Smartphone", None))
        self.gesture_label.setText(QCoreApplication.translate("settings", u"Gestures", None))
        self.label_2.setText(QCoreApplication.translate("settings", u"Gesture 1", None))
        self.label_3.setText(QCoreApplication.translate("settings", u"Gesture 2", None))
        self.label_4.setText(QCoreApplication.translate("settings", u"Gesture 3", None))
        self.label_5.setText(QCoreApplication.translate("settings", u"Gesture 4", None))
        self.submit_btn.setText(QCoreApplication.translate("settings", u"Submit", None))
        self.default_btn.setText(QCoreApplication.translate("settings", u"Default", None))
        self.cancel_btn.setText(QCoreApplication.translate("settings", u"Cancel", None))
    # retranslateUi

    def submit_clicked(self):
        print("Submit button clicked")
        self.show_main_window()

    def default_clicked(self):
        print("Default button clicked")
        self.show_main_window()

    def cancel_clicked(self):
        print("Cancel button clicked")
        self.show_main_window()

    def show_main_window(self):
        self.parent_window.show()
        self.close()

from PySide6.QtWidgets import (QApplication, QFrame, QGraphicsView, QHBoxLayout,
                               QLabel, QListView, QPushButton, QSizePolicy,
                               QVBoxLayout, QWidget, QMainWindow, QListWidget)
import numpy as np
import cv2
from PySide6.QtGui import *
from PySide6.QtCore import *

from desktop_app.log_thread import LogThread
from desktop_app.ui_settings import UiSettings
from desktop_app.video_thread import VideoThread


class UiMainFrame(QMainWindow):
    def __init__(self, model):
        super().__init__()
        self.model = model
        self.setup_ui()
        self.settings_window = None
        self.last_gesture = None

    def setup_ui(self):
        if not self.objectName():
            self.setObjectName(u"main_frame")
        self.setWindowModality(Qt.ApplicationModal)
        self.resize(761, 461)
        self.setSizeIncrement(QSize(1, 0))

        self.image_label = QLabel(self)
        qpixmap = QPixmap("desktop_app/camera_not_found.png")
        qpixmap = qpixmap.scaledToWidth(480)
        qpixmap = qpixmap.scaledToHeight(270)
        self.image_label.setPixmap(qpixmap)
        # self.text_label = QLabel('Webcam')
        vbox = QVBoxLayout()
        vbox.addWidget(self.image_label)
        # vbox.addWidget(self.text_label)

        self.vbox = vbox
        self.vbox.setGeometry(QRect(30, 30, 480, 270))

        self.video_thread = VideoThread()
        self.video_thread.change_pixmap_signal.connect(self.update_image)
        self.video_thread.start()

        self.settings = QPushButton(self)
        self.settings.clicked.connect(self.display_settings)

        self.settings.setObjectName(u"settings")
        self.settings.setGeometry(QRect(20, 420, 80, 24))
        self.list_view = QListWidget(self)
        self.list_view.setObjectName(u"list_view")
        self.list_view.setGeometry(QRect(550, 50, 180, 250))

        self.log_thread = LogThread(self.model)
        self.log_thread.gesture_signal.connect(self.add_to_log)
        self.log_thread.start()

        self.acions_log = QLabel(self)
        self.acions_log.setObjectName(u"acions_log")
        self.acions_log.setEnabled(True)
        self.acions_log.setGeometry(QRect(550, 30, 181, 21))
        self.start = QPushButton(self)
        self.start.setObjectName(u"start")
        self.start.setGeometry(QRect(250, 370, 107, 24))
        self.start.clicked.connect(self.start_clicked)
        self.stop = QPushButton(self)
        self.stop.setObjectName(u"stop")
        self.stop.setGeometry(QRect(370, 370, 101, 24))
        self.stop.clicked.connect(self.stop_clicked)

        self.processing_label = QLabel(self)
        self.processing_label.setObjectName(u"processing_label")
        self.processing_label.setGeometry(QRect(280, 340, 171, 16))

        self.retranslate_ui(self)

        QMetaObject.connectSlotsByName(self)

    # setupUi

    def retranslate_ui(self, main_frame):
        main_frame.setWindowTitle(QCoreApplication.translate("main_frame", u"Widget", None))
        self.settings.setText(QCoreApplication.translate("main_frame", u"Settings", None))
        self.acions_log.setText(QCoreApplication.translate("main_frame", u"Actions Log", None))
        self.start.setText(QCoreApplication.translate("main_frame", u"Start", None))
        self.stop.setText(QCoreApplication.translate("main_frame", u"Stop", None))
        self.processing_label.setText(QCoreApplication.translate("main_frame", u"Start/Stope gesture processing", None))

    # retranslateUi

    @Slot(np.ndarray, object, object)
    def update_image(self, cv_img, img_white, normalized_position):
        qt_image = self.convert_cv_qt(cv_img)
        self.image_label.setPixmap(qt_image)
        self.log_thread.update_image(img_white, normalized_position)

    def convert_cv_qt(self, cv_image):
        rgb_image = cv2.cvtColor(cv_image, cv2.COLOR_BGR2RGB)
        h, w, c = rgb_image.shape
        bytes_per_line = c * w
        convert_to_qt_format = QImage(rgb_image.data, w, h, bytes_per_line, QImage.Format_RGB888)
        p = convert_to_qt_format.scaled(480, 270)
        return QPixmap.fromImage(p)

    def closeEvent(self, event):
        self.video_thread.terminate()
        QThread.wait(self.video_thread)
        self.log_thread.terminate()
        QThread.wait(self.log_thread)
        event.accept()

    def display_settings(self):
        if self.settings_window is None:
            self.settings_window = UiSettings(self)
        self.settings_window.show()
        self.hide()

    @Slot(str)
    def add_to_log(self, gesture):
        if self.last_gesture == gesture:
            return None

        self.list_view.insertItem(0, gesture)
        self.list_view.scrollToTop()
        self.last_gesture = gesture

    def start_clicked(self):
        self.log_thread.is_stop_time = False
        self.log_thread.start()

    def stop_clicked(self):
        self.log_thread.is_stop_time = True
        self.log_thread.exit()

from PySide6.QtCore import (QCoreApplication, QDate, QDateTime, QLocale,
    QMetaObject, QObject, QPoint, QRect,
    QSize, QTime, QUrl, Qt)
from PySide6.QtGui import (QBrush, QColor, QConicalGradient, QCursor,
    QFont, QFontDatabase, QGradient, QIcon,
    QImage, QKeySequence, QLinearGradient, QPainter,
    QPalette, QPixmap, QRadialGradient, QTransform)
from PySide6.QtWidgets import (QApplication, QFrame, QGraphicsView, QHBoxLayout,
    QLabel, QListView, QPushButton, QSizePolicy,
    QVBoxLayout, QWidget)
import numpy as np
import cv2
from PySide6.QtGui import *
from PySide6.QtCore import *

class VideoThread(QThread):
    change_pixmap_signal = Signal(np.ndarray)

    def run(self):
        cap = cv2.VideoCapture(0)
        while True:
            ret, cv_imag = cap.read()
            if ret:
                self.change_pixmap_signal.emit(cv_imag)


class Ui_mainFrame(object):
    def setupUi(self, mainFrame):
        if not mainFrame.objectName():
            mainFrame.setObjectName(u"mainFrame")
        mainFrame.resize(738, 539)
        # self.webcamView = QGraphicsView(mainFrame)
        # self.webcamView.setObjectName(u"webcamView")
        # self.webcamView.setGeometry(QRect(30, 30, 431, 361))
        # set webcam view
        self.image_label = QLabel(mainFrame)
        self.text_label = QLabel('Webcam')
        vbox = QVBoxLayout()
        vbox.addWidget(self.image_label)
        vbox.addWidget(self.text_label)
        self.vbox = vbox
        self.vbox.setGeometry(QRect(30, 30, 400, 350))

        self.thread = VideoThread()
        self.thread.change_pixmap_signal.connect(self.update_image)
        self.thread.start()
        #

        self.settings = QPushButton(mainFrame)
        self.settings.setObjectName(u"settings")
        self.settings.setGeometry(QRect(20, 500, 80, 24))
        self.verticalLayoutWidget = QWidget(mainFrame)
        self.verticalLayoutWidget.setObjectName(u"verticalLayoutWidget")
        self.verticalLayoutWidget.setGeometry(QRect(510, 30, 141, 111))
        self.verticalLayout = QVBoxLayout(self.verticalLayoutWidget)
        self.verticalLayout.setObjectName(u"verticalLayout")
        self.verticalLayout.setContentsMargins(0, 0, 0, 0)
        self.label = QLabel(self.verticalLayoutWidget)
        self.label.setObjectName(u"label")

        self.verticalLayout.addWidget(self.label)

        self.webcam = QPushButton(self.verticalLayoutWidget)
        self.webcam.setObjectName(u"webcam")
        self.webcam.setEnabled(True)
        self.webcam.setChecked(False)

        self.verticalLayout.addWidget(self.webcam)

        self.phonecam = QPushButton(self.verticalLayoutWidget)
        self.phonecam.setObjectName(u"phonecam")

        self.verticalLayout.addWidget(self.phonecam)

        self.horizontalLayoutWidget = QWidget(mainFrame)
        self.horizontalLayoutWidget.setObjectName(u"horizontalLayoutWidget")
        self.horizontalLayoutWidget.setGeometry(QRect(130, 420, 221, 71))
        self.horizontalLayout = QHBoxLayout(self.horizontalLayoutWidget)
        self.horizontalLayout.setObjectName(u"horizontalLayout")
        self.horizontalLayout.setContentsMargins(0, 0, 0, 0)
        self.start = QPushButton(self.horizontalLayoutWidget)
        self.start.setObjectName(u"start")

        self.horizontalLayout.addWidget(self.start)

        self.stop = QPushButton(self.horizontalLayoutWidget)
        self.stop.setObjectName(u"stop")
        self.stop.setCursor(QCursor(Qt.ArrowCursor))
        self.stop.setMouseTracking(False)
        self.stop.setAcceptDrops(False)

        self.horizontalLayout.addWidget(self.stop)

        self.verticalLayoutWidget_2 = QWidget(mainFrame)
        self.verticalLayoutWidget_2.setObjectName(u"verticalLayoutWidget_2")
        self.verticalLayoutWidget_2.setGeometry(QRect(510, 190, 181, 311))
        self.verticalLayout_2 = QVBoxLayout(self.verticalLayoutWidget_2)
        self.verticalLayout_2.setObjectName(u"verticalLayout_2")
        self.verticalLayout_2.setContentsMargins(0, 0, 0, 0)
        self.label_2 = QLabel(self.verticalLayoutWidget_2)
        self.label_2.setObjectName(u"label_2")
        self.label_2.setEnabled(True)

        self.verticalLayout_2.addWidget(self.label_2)

        self.line = QFrame(self.verticalLayoutWidget_2)
        self.line.setObjectName(u"line")
        self.line.setFrameShape(QFrame.HLine)
        self.line.setFrameShadow(QFrame.Sunken)

        self.verticalLayout_2.addWidget(self.line)

        self.listView = QListView(self.verticalLayoutWidget_2)
        self.listView.setObjectName(u"listView")

        self.verticalLayout_2.addWidget(self.listView)


        self.retranslateUi(mainFrame)

        QMetaObject.connectSlotsByName(mainFrame)
    # setupUi

    def retranslateUi(self, mainFrame):
        mainFrame.setWindowTitle(QCoreApplication.translate("mainFrame", u"Widget", None))
        self.settings.setText(QCoreApplication.translate("mainFrame", u"Settings", None))
        self.label.setText(QCoreApplication.translate("mainFrame", u"Select video source", None))
        self.webcam.setText(QCoreApplication.translate("mainFrame", u"Webcam", None))
        self.phonecam.setText(QCoreApplication.translate("mainFrame", u"Phone camera", None))
        self.start.setText(QCoreApplication.translate("mainFrame", u"Start", None))
        self.stop.setText(QCoreApplication.translate("mainFrame", u"Stop", None))
        self.label_2.setText(QCoreApplication.translate("mainFrame", u"Logs", None))
    # retranslateUi

    @Slot(np.ndarray)
    def update_image(self, cv_img):
        qt_image = self.convert_cv_qt(cv_img)
        self.image_label.setPixmap(qt_image)

    def convert_cv_qt(self, cv_image):
        rgb_image = cv2.cvtColor(cv_image, cv2.COLOR_BGR2RGB)
        h, w, c = rgb_image.shape
        bytes_per_line = c * w
        convert_to_Qt_format = QImage(rgb_image.data, w, h, bytes_per_line, QImage.Format_RGB888)
        p = convert_to_Qt_format.scaled(400, 350)
        return QPixmap.fromImage(p)

    def closeEvent(self, event):
        self.thread.stop()
        event.accept()

import sys
from PyQt5.QtWidgets import QApplication, QWidget, QLabel, QMainWindow
from PyQt5.QtGui import QPainter, QColor, QPen
from PyQt5.QtCore import Qt, QRectF, QPoint, QTimer
from dronekit import connect
import math
from PyQt5 import QtCore, QtGui, QtWidgets

# DroneKit bağlantısı
connection_string = "127.0.0.1:14550"
vehicle = connect(connection_string, wait_ready=False)

class GPSspeedIndicator(QWidget):
    def __init__(self, vehicle):
        super().__init__()
        self.vehicle = vehicle
        self.gpsspeed = 0  # Başlangıçta hava hızı 0
        self.initUI()
        self.initTimer()

    def initUI(self):
        self.setGeometry(100, 100, 300, 300)
        self.setWindowTitle('GPS-SPEED Indicator')

    def initTimer(self):
        self.timer = QTimer(self)
        self.timer.timeout.connect(self.updateGPSspeed)
        self.timer.start(100)  # Her 100 milisaniyede bir güncelle

    def updateGPSspeed(self):
        self.gpsspeed = self.vehicle.groundspeed
        self.update()

    def paintEvent(self, event):
        painter = QPainter(self)
        painter.setRenderHint(QPainter.Antialiasing)

        # Dış çemberi çiz
        painter.setPen(QPen(Qt.black, 4))
        painter.setBrush(QColor(220, 220, 220))
        painter.drawEllipse(50, 50, 200, 200)

        # Hava hızı işaretlerini ve hız değerlerini çiz (5, 10, 15, ... 50 m/s aralıklarla)
        for i in range(5, 55, 5):
            angle = (i * 6.75) - 90  # Her 5 m/s için açıyı hesapla ve yukarıyı başlangıç noktası olarak ayarla
            radians = math.radians(angle)
            x_outer = 150 + int(100 * math.cos(radians))
            y_outer = 150 + int(100 * math.sin(radians))
            x_inner = 150 + int(80 * math.cos(radians))
            y_inner = 150 + int(80 * math.sin(radians))
            painter.setPen(QPen(Qt.black, 2))
            painter.drawLine(QPoint(x_outer, y_outer), QPoint(x_inner, y_inner))

            # Hız değerini yaz
            x_text = 150 + int(117 * math.cos(radians))
            y_text = 150 + int(117 * math.sin(radians))
            painter.drawText(QPoint(x_text - 10, y_text + 5), f"{i}")

        # Hava hızı ibresini çiz
        angle = int(self.gpsspeed * 6.75) - 90  # Hava hızını açısal dereceye çevir ve yukarı doğru hizala
        radians = math.radians(angle)
        painter.setPen(QPen(Qt.red, 4))
        painter.drawLine(QPoint(150, 150),
                         QPoint(150 + int(70 * math.cos(radians)),
                                150 + int(70 * math.sin(radians))))

        # Orta çemberi çiz
        painter.setPen(QPen(Qt.black, 2))
        painter.setBrush(Qt.black)
        painter.drawEllipse(140, 140, 20, 20)

        # Hava hızı etiketi
        painter.setPen(Qt.black)
        painter.setFont(painter.font())
        painter.drawText(QRectF(100, 260, 120, 30), Qt.AlignCenter, "GPS SPEED (m/s)")




class AirspeedIndicator(QWidget):
    def __init__(self, vehicle):
        super().__init__()
        self.vehicle = vehicle
        self.airspeed = 0  # Başlangıçta hava hızı 0
        self.initUI()
        self.initTimer()

    def initUI(self):
        self.setGeometry(100, 100, 300, 300)
        self.setWindowTitle('Airspeed Indicator')

    def initTimer(self):
        self.timer = QTimer(self)
        self.timer.timeout.connect(self.updateAirspeed)
        self.timer.start(100)  # Her 100 milisaniyede bir güncelle

    def updateAirspeed(self):
        self.airspeed = self.vehicle.airspeed
        self.update()

    def paintEvent(self, event):
        painter = QPainter(self)
        painter.setRenderHint(QPainter.Antialiasing)

        # Dış çemberi çiz
        painter.setPen(QPen(Qt.black, 4))
        painter.setBrush(QColor(220, 220, 220))
        painter.drawEllipse(50, 50, 200, 200)

        # Hava hızı işaretlerini ve hız değerlerini çiz (5, 10, 15, ... 50 m/s aralıklarla)
        for i in range(5, 55, 5):
            angle = (i * 6.75) - 90  # Her 5 m/s için açıyı hesapla ve yukarıyı başlangıç noktası olarak ayarla
            radians = math.radians(angle)
            x_outer = 150 + int(100 * math.cos(radians))
            y_outer = 150 + int(100 * math.sin(radians))
            x_inner = 150 + int(80 * math.cos(radians))
            y_inner = 150 + int(80 * math.sin(radians))
            painter.setPen(QPen(Qt.black, 2))
            painter.drawLine(QPoint(x_outer, y_outer), QPoint(x_inner, y_inner))

            # Hız değerini yaz
            x_text = 150 + int(117 * math.cos(radians))
            y_text = 150 + int(117 * math.sin(radians))
            painter.drawText(QPoint(x_text - 10, y_text + 5), f"{i}")

        # Hava hızı ibresini çiz
        angle = int(self.airspeed * 6.75) - 90  # Hava hızını açısal dereceye çevir ve yukarı doğru hizala
        radians = math.radians(angle)
        painter.setPen(QPen(Qt.red, 4))
        painter.drawLine(QPoint(150, 150),
                         QPoint(150 + int(70 * math.cos(radians)),
                                150 + int(70 * math.sin(radians))))

        # Orta çemberi çiz
        painter.setPen(QPen(Qt.black, 2))
        painter.setBrush(Qt.black)
        painter.drawEllipse(140, 140, 20, 20)

        # Hava hızı etiketi
        painter.setPen(Qt.black)
        painter.setFont(painter.font())
        painter.drawText(QRectF(100, 260, 100, 30), Qt.AlignCenter, "Airspeed (m/s)")

class Ui_MainWindow(object):

    def setupUi(self, MainWindow):
        MainWindow.setObjectName("MainWindow")
        MainWindow.resize(1275, 906)
        self.centralwidget = QtWidgets.QWidget(MainWindow)
        self.centralwidget.setObjectName("centralwidget")

        # AirspeedIndicator bileşenini ekliyoruz
        self.speedIndicator = AirspeedIndicator(vehicle)
        self.speedIndicator.setGeometry(QtCore.QRect(60, 50, 300, 300))
        self.speedIndicator.setParent(self.centralwidget)

        self.gpsspeedIndicator = GPSspeedIndicator(vehicle)
        self.gpsspeedIndicator.setGeometry(QtCore.QRect(670, 40, 281, 251))
        self.gpsspeedIndicator.setParent(self.centralwidget)

        # GPS etiketi örnek olarak bırakılıyor
        self.gps = QtWidgets.QLabel(self.centralwidget)
        self.gps.setGeometry(QtCore.QRect(670, 40, 281, 251))
        self.gps.setObjectName("gps")
        MainWindow.setCentralWidget(self.centralwidget)
        self.menubar = QtWidgets.QMenuBar(MainWindow)
        self.menubar.setGeometry(QtCore.QRect(0, 0, 1275, 22))
        self.menubar.setObjectName("menubar")
        MainWindow.setMenuBar(self.menubar)
        self.statusbar = QtWidgets.QStatusBar(MainWindow)
        self.statusbar.setObjectName("statusbar")
        MainWindow.setStatusBar(self.statusbar)

        self.retranslateUi(MainWindow)
        QtCore.QMetaObject.connectSlotsByName(MainWindow)

    def retranslateUi(self, MainWindow):
        _translate = QtCore.QCoreApplication.translate
        MainWindow.setWindowTitle(_translate("MainWindow", "MainWindow"))
        self.gps.setText(_translate("MainWindow", "GPS Data"))


if __name__ == "__main__":
    app = QtWidgets.QApplication(sys.argv)
    MainWindow = QtWidgets.QMainWindow()
    ui = Ui_MainWindow()
    ui.setupUi(MainWindow)
    MainWindow.show()
    sys.exit(app.exec_())

import sys
from PyQt5.QtWidgets import QApplication, QWidget
from PyQt5.QtGui import QPainter, QColor, QPen
from PyQt5.QtCore import Qt, QRectF, QPoint, QTimer
from dronekit import connect
import math

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

if __name__ == '__main__':
    # DroneKit ile bağlantı kurun
    connection_string = '127.0.0.1:14550'  # ArduPilot SITL veya gerçek drone bağlantısı
    vehicle = connect(connection_string, wait_ready=True)

    app = QApplication(sys.argv)
    ex = AirspeedIndicator(vehicle)
    ex.show()
    sys.exit(app.exec_())

import sys
from PyQt5.QtWidgets import QApplication, QMainWindow, QWidget
from PyQt5.QtGui import QPainter, QColor, QBrush, QPen
from PyQt5.QtCore import Qt, QRectF

class ShapesWindow(QMainWindow):
    def __init__(self):
        super().__init__()
        self.setWindowTitle('Dessiner des formes géométriques')
        self.setGeometry(50, 50, 900, 800)
        self.central_widget = QWidget()
        self.setCentralWidget(self.central_widget)

    def paintEvent(self, event):
        painter = QPainter(self)
        self.draw_shapes(painter)

    def draw_shapes(self, painter):
        # Dessiner un rectangle arrondi
        painter.setBrush(QBrush(QColor("#dddddd"), Qt.SolidPattern))
        rect = QRectF(50, 50, 800, 400)
        painter.drawRoundedRect(rect, 3, 3)

        for x in range(31):
            # Dessiner un demi-disque plein
            pen = QPen(QColor("#c0c0c0"), 0, Qt.SolidLine)
            painter.setPen(pen)            
            painter.setBrush(QBrush(QColor("#c0c0c0"), Qt.SolidPattern))
            half_circle_rect = QRectF(100+x*24, 100, 12, 12)
            painter.drawPie(half_circle_rect, 0 * 16, 180 * 16)
            pen.setColor(QColor("#e6e6e6"))
            painter.setPen(pen)
            painter.setBrush(QBrush(QColor("#e6e6e6"), Qt.SolidPattern))
            painter.drawPie(half_circle_rect, 180 * 16 , 180 * 16)

            # Dessiner un disque plein
            
            pen.setColor(QColor("#484848"))
            painter.setPen(pen)
            painter.setBrush(QBrush(QColor("#484848"), Qt.SolidPattern))
            full_circle_rect = QRectF(103+x*24, 103, 6, 6)
            painter.drawEllipse(full_circle_rect)

if __name__ == '__main__':
    app = QApplication(sys.argv)
    window = ShapesWindow()
    window.show()
    sys.exit(app.exec_())

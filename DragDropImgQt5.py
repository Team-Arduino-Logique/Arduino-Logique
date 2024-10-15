import sys
from PyQt5.QtWidgets import QApplication, QLabel, QMainWindow, QWidget, QVBoxLayout
from PyQt5.QtCore import Qt, QMimeData, QByteArray, QBuffer, QIODevice
from PyQt5.QtGui import QDrag, QPixmap, QPainter, QIcon

class DraggableImageLabel(QLabel):
    def __init__(self, pixmap, parent=None):
        super().__init__(parent)
        self.setPixmap(pixmap)
        self.setScaledContents(True)
        self.setFixedSize(pixmap.size())
        self.setAlignment(Qt.AlignCenter)

    def mousePressEvent(self, event):
        if event.button() == Qt.LeftButton:
            self.startDrag(event)

    def startDrag(self, event):
        mimeData = QMimeData()
        byteArray = QByteArray()
        buffer = QBuffer(byteArray)
        buffer.open(QIODevice.WriteOnly)
        self.pixmap().save(buffer, "PNG")
        mimeData.setData("application/x-qt-image", byteArray)

        drag = QDrag(self)
        drag.setMimeData(mimeData)
        drag.setPixmap(self.pixmap())
        drag.setHotSpot(event.pos())

        dropAction = drag.exec_(Qt.MoveAction)

class DropImageWidget(QWidget):
    def __init__(self):
        super().__init__()
        self.setAcceptDrops(True)
        self.layout = QVBoxLayout()
        self.setLayout(self.layout)

    def dragEnterEvent(self, event):
        if event.mimeData().hasFormat("application/x-qt-image"):
            event.acceptProposedAction()

    def dropEvent(self, event):
        data = event.mimeData().data("application/x-qt-image")
        image = QPixmap()
        image.loadFromData(data)
        label = DraggableImageLabel(image)
        self.layout.addWidget(label)
        event.acceptProposedAction()

class MainWindow(QMainWindow):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("Drag and Drop Image Example")
        self.setGeometry(100, 100, 600, 400)

        self.centralWidget = QWidget()
        self.setCentralWidget(self.centralWidget)

        self.layout = QVBoxLayout()
        self.centralWidget.setLayout(self.layout)

        initial_image = QPixmap("LedVerte.png")  # Replace with your image path
        self.draggableImageLabel = DraggableImageLabel(initial_image)
        self.layout.addWidget(self.draggableImageLabel)

        self.dropWidget = DropImageWidget()
        self.layout.addWidget(self.dropWidget)

if __name__ == '__main__':
    app = QApplication(sys.argv)
    window = MainWindow()
    window.show()
    sys.exit(app.exec_())

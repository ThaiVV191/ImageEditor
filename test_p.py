import sys
from PyQt5.QtGui import QPixmap, QImage, QPainter
from PyQt5.QtWidgets import QApplication, QMainWindow, QLabel, QGraphicsView, QGraphicsScene
from PyQt5.QtCore import Qt

class DrawOnImage(QMainWindow):
    def __init__(self):
        super().__init__()

        # Load image
        self.pixmap = QPixmap('output.jpg')
        self.image = QImage(self.pixmap)
        self.label = QLabel(self)
        self.label.setPixmap(self.pixmap)

        # Create QGraphicsScene and QGraphicsView
        self.scene = QGraphicsScene(self)
        self.view = QGraphicsView(self.scene, self)
        self.view.setGeometry(0, 0, self.pixmap.width(), self.pixmap.height())
        self.view.setRenderHint(QPainter.Antialiasing)
        self.view.setVerticalScrollBarPolicy(Qt.ScrollBarAlwaysOff)
        self.view.setHorizontalScrollBarPolicy(Qt.ScrollBarAlwaysOff)
        self.view.setDragMode(QGraphicsView.NoDrag)
        self.view.setInteractive(False)
        self.view.setWindowOpacity(0)

        # Connect events
        self.label.mousePressEvent = self.mousePressEvent
        self.label.mouseMoveEvent = self.mouseMoveEvent
        self.label.mouseReleaseEvent = self.mouseReleaseEvent

        # Set window properties
        self.setGeometry(100, 100, self.pixmap.width(), self.pixmap.height())
        self.setWindowTitle('Draw on Image')
        self.show()

    def mousePressEvent(self, event):
        self.start = event.pos()
        self.end = event.pos()
        self.update()

    def mouseMoveEvent(self, event):
        self.end = event.pos()
        self.update()

    def mouseReleaseEvent(self, event):
        painter = QPainter(self.pixmap)
        painter.drawLine(self.start, self.end)
        self.label.setPixmap(self.pixmap)
        self.update()

    def update(self):
        self.view.repaint()
        self.scene.clear()
        self.scene.addPixmap(self.pixmap)
        self.label.setGeometry(0, 0, self.pixmap.width(), self.pixmap.height())

if __name__ == '__main__':
    app = QApplication(sys.argv)
    window = DrawOnImage()
    sys.exit(app.exec_())

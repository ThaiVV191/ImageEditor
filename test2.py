from PyQt5.QtCore import *
from PyQt5.QtGui import *
from PyQt5.QtWidgets import *

import sys

class ImageViewer(QGraphicsView):
    def __init__(self, parent=None):
        super().__init__(parent)

        # Set up the QGraphicsView
        self.setRenderHint(QPainter.Antialiasing)
        self.setTransformationAnchor(QGraphicsView.AnchorUnderMouse)
        self.setResizeAnchor(QGraphicsView.AnchorUnderMouse)
        self.setVerticalScrollBarPolicy(Qt.ScrollBarAlwaysOff)
        self.setHorizontalScrollBarPolicy(Qt.ScrollBarAlwaysOff)
        self.setBackgroundBrush(QColor(30, 30, 30))
        self.setFrameShape(QGraphicsView.NoFrame)

        # Set up the QGraphicsScene and add an image to it
        self.scene = QGraphicsScene(self)
        self.image = QImage("samoyed_puppy_dog_pictures.jpg")
        self.item = QGraphicsPixmapItem(QPixmap.fromImage(self.image))
        self.scene.addItem(self.item)
        self.setScene(self.scene)

        # Variables to track the start and end points of the zoom operation
        self.start = None
        self.end = None

    def mousePressEvent(self, event):
        # Record the start point of the zoom operation
        self.start = self.mapToScene(event.pos())

    def mouseMoveEvent(self, event):
        # Update the end point of the zoom operation
        self.end = self.mapToScene(event.pos())

        # Redraw the zoom rectangle
        self.viewport().update()

    def mouseReleaseEvent(self, event):
        # Crop the image to
        self.cropImage()
        self.start = None
        self.end = None

    def paintEvent(self, event):
        super().paintEvent(event)

        # Draw the zoom rectangle if the user is currently zooming in
        if self.start is not None and self.end is not None:
            painter = QPainter(self.viewport())
            painter.setRenderHint(QPainter.Antialiasing)
            painter.setPen(QColor(255, 255, 255, 150))
            painter.drawRect(QRectF(self.start, self.end))

    def cropImage(self):
        # Calculate the top-left and bottom-right points of the zoomed-in region
        topLeft = QPointF(min(self.start.x(), self.end.x()), min(self.start.y(), self.end.y()))
        bottomRight = QPointF(max(self.start.x(), self.end.x()), max(self.start.y(), self.end.y()))

        # Calculate the width and height of the zoomed-in region
        width = abs(self.start.x() - self.end.x())
        height = abs(self.start.y() - self.end.y())

        # Create a QPixmap containing the zoomed-in region of the image
        zoomedImage = QPixmap(self.image).copy(topLeft.x(), topLeft.y(), width, height)

        # Update the QGraphicsView with the new zoomed-in image
        self.item.setPixmap(zoomedImage)
        self.fitInView(self.scene.itemsBoundingRect(), Qt.KeepAspectRatio)

class MainWindow(QMainWindow):
    def __init__(self):
        super().__init__()
        self.view = ImageViewer(self)
        
        self.setCentralWidget(self.view)
        self.showMaximized()
        self.log()

    def log(self):
        print(self.view.size())

if __name__ == '__main__':
    app = QApplication(sys.argv)
    win = MainWindow()
    win.show()
    sys.exit(app.exec_())



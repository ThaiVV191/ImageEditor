import sys
import cv2
from PyQt5.QtCore import *
from PyQt5.QtGui import *
from PyQt5.QtWidgets import *


class customQGraphicsView(QGraphicsView):
    def __init__(self):
        super().__init__()
        self.is_cropping = False
        self.crop_rect = None
        self.mouse_inside = False
        self.crop_start = None
        self.scene = QGraphicsScene()
        self.crop_end = None
        self.activate = False
    
    def enterEvent(self, event):
        self.mouse_inside = True

    def leaveEvent(self, event):
        self.mouse_inside = False

    def mousePressEvent(self, event):      
        if self.activate and event.button() == Qt.LeftButton:
            self.is_cropping = True
            self.crop_start = event.pos()
            self.crop_end = event.pos()
        else:
            event.ignore()
        
    def mouseMoveEvent(self, event):
       
        if self.activate and  self.mouse_inside and self.is_cropping:
            self.crop_end = event.pos()
            self.updateCropRect()
        else:
            event.ignore()
        
    def mouseReleaseEvent(self, event):
        if self.activate and  self.mouse_inside and event.button() == Qt.LeftButton:
            self.is_cropping = False
            
            
        
    def getResult(self):
        if self.crop_end == self.crop_start or abs(self.crop_end.x() - self.crop_start.x()) < 20 or abs(self.crop_end.y() - self.crop_start.y()) < 20 :
            return None, None
        else:
            return self.crop_start, self.crop_end
     
    def updateCropRect(self):
        if self.activate and self.mouse_inside:
            self.crop_rect = QRectF(self.crop_start, self.crop_end)
            self.viewport().update()
        
    def paintEvent(self, event):
        super().paintEvent(event)
        if self.crop_rect:
            painter = QPainter(self.viewport())
            painter.setRenderHint(QPainter.Antialiasing)
            painter.setPen(QPen(Qt.green, 2, Qt.SolidLine))
            painter.setBrush(QBrush(QColor(0, 0, 0, 100)))
            painter.drawRect(self.crop_rect)



class MainWindow(QMainWindow):
    def __init__(self):
        super().__init__()
        self.view = customQGraphicsView(self)
        self.image = QImage("samoyed_puppy_dog_pictures.jpg")  
        self.scene = QGraphicsScene(self)
        self.pixmap = QPixmap.fromImage(self.image)       
        self.scene.setSceneRect(0, 0, self.pixmap.width(), self.pixmap.height())
        self.scene.addPixmap(self.pixmap)
        self.view.setScene(self.scene)
        self.setCentralWidget(self.view)      
        self.editToolBarV = QToolBar(self)
        toolButton = QToolButton(self)
        toolButton.setIcon(QIcon('icons/crop.png'))
        toolButton.setIconSize(QSize(30, 30))
        toolButton.clicked.connect(self.open)  
        self.editToolBarV.addWidget(toolButton)
        self.showMaximized()


    def log(self):       
        print(self.view.size())
    def open(self):
        print(self.view.getResult())

if __name__ == '__main__':
    app = QApplication(sys.argv)
    win = MainWindow()
    win.show()
    sys.exit(app.exec_())

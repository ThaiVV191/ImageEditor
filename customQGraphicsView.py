import sys
import cv2
from PyQt5.QtCore import *
from PyQt5.QtGui import *
from PyQt5.QtWidgets import *


class customQGraphicsView(QGraphicsView):
    def __init__(self, parent=None):
        super().__init__(parent)
        self.is_cropping = False
        self.crop_rect = None
        self.mouse_inside = False
        self.crop_start = None
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

            # super().mousePressEvent(event)
        else:
            event.ignore()
        
    def mouseMoveEvent(self, event):
       
        if self.activate and  self.mouse_inside and self.is_cropping:
            self.crop_end = event.pos()
            self.updateCropRect()
            # super().mouseMoveEvent(event)
        else:
            event.ignore()
        
    def mouseReleaseEvent(self, event):
        if self.activate and  self.mouse_inside and event.button() == Qt.LeftButton:
            self.is_cropping = False
            e = self.crop_end
            # print(self.crop_end)
            # print(self.image.width(), self.image.height() )
            # x,y, x1, y1 = self.mapToScene(self.crop_start).x(), self.mapToScene(self.crop_start).y(), self.mapToScene(self.crop_end).x(), self.mapToScene(self.crop_end).y()
            # x = 0 if x < 0 else x
            # y = 0 if y < 0 else y
            # x1 = self.image.width() if x1 > self.image.width() else x1
            # y1  = self.image.height() if y1 > self.image.height() else y1
            # # print(x,x1)
            # # self.crop_rect = QRectF()
            # self.crop_rect = QRectF(x,y, x1 - x, y1 - y)
            # print(self.crop_rect)
            # print('image', self.image.size())
            # self.image = self.image.copy(self.crop_rect.toRect())

            # self.pixmap = QPixmap.fromImage(self.image)
            # self.scene.clear()  # Clear the scene
            # self.scene.setSceneRect(0, 0, self.pixmap.width(), self.pixmap.height())
            # self.scene.addPixmap(self.pixmap)
            # self.scene.update()
            # self.crop_rect = None
            # return {"button": e}
        
    def getResult(self):
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
        # self.view.mouseReleaseEvent

    # def _createToolBar(self, name, log, shortCut):
    #     window = QWidget()
    #     button = QVBoxLayout()
    #     toolButton = QToolButton(self)
    #     toolButton.setAutoRaise(True)
    #     toolButton.clicked.connect(log)       
    #     toolButton.setShortcut(QKeySequence(shortCut))
    #     toolButton.setIcon(QIcon(name))
    #     toolButton.setIconSize(QSize(30, 30))
    #     toolButton.setCheckable(True)
    #     button.addWidget(toolButton)
    #     spacer = QSpacerItem(10, 10, QSizePolicy.Fixed, QSizePolicy.Fixed)
    #     button.addItem(spacer)
    #     window.setLayout(button)
    #     self.editToolBarV.addWidget(window)
    #     return toolButton

    def log(self):
        
        print(self.view.size())
        # print(self.view.)

    def open(self):
        print(self.view.getResult())

if __name__ == '__main__':
    app = QApplication(sys.argv)
    win = MainWindow()
    win.show()
    sys.exit(app.exec_())

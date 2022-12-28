from PyQt5.QtWidgets import *
from PyQt5.QtGui import *
from PyQt5.QtCore import *

def open(parent):
        # print(1)
        file_name, _ = QFileDialog.getOpenFileName(
            parent, "Open file", ".", "Image Files (*.png *.jpg *.bmp)"
        )
        if not file_name:
            return
        pic = QGraphicsPixmapItem()
        parent.image_qt = QImage(file_name)
        pixmap = QPixmap.fromImage(parent.image_qt)
        pic.setPixmap(pixmap)
        parent.scene.setSceneRect(0, 0, pixmap.width(), pixmap.height())
        parent.scene.addItem(pic)
        # pass
        

def zoomIn(parent):
    
    # self.scale *= 1.15
    # self.resize_image()
    pass

def zoomOut(parent):
    # self.scale /=  1.15
    # self.resize_image()
    pass

def resize(parent):
    # size = self.pixmap.size()
    # scaled_pixmap = self.pixmap.scaled(self.scale * size)
    # self.pic.setPixmap(scaled_pixmap)
    # self.scene.setSceneRect(0, 0, scaled_pixmap.width(), scaled_pixmap.height())
    # self.scene.addItem(self.pic)
    # self.scene.update()
    pass

def save(parent):
    
    # self.scale *= 1.15
    # self.resize_image()
    pass

def crop(parent):
    
    # self.scale *= 1.15
    # self.resize_image()
    pass

def flip(parent):
    
    # self.scale *= 1.15
    # self.resize_image()
    pass

def rotate(parent):
    
    # self.scale *= 1.15
    # self.resize_image()
    pass

def text(parent):
    
    # self.scale *= 1.15
    # self.resize_image()
    pass



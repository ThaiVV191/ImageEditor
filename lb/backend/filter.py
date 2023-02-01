from PyQt5.QtWidgets import *
from PyQt5.QtGui import *
from PyQt5.QtCore import *
import qimage2ndarray
from PIL import Image, ImageFilter
import cv2
import numpy as np


def emboss(self, pixmap):
    image = converPixmapToCV(pixmap)
    image = cv2.cvtColor(image, cv2.COLOR_BGR2RGB)
    image = Image.fromarray(image)
    im_emboss = image.filter(ImageFilter.EMBOSS)
    pixmap_new =  convertPILtoPixmap(im_emboss)
    updateView(self, pixmap_new)

def boxBlur(self, pixmap):
    image = converPixmapToCV(pixmap)
    ksize = (self.blurBin.value(), self.blurBin.value())
    image = cv2.blur(image, ksize)
    pixmap_new =  convertCVtoPixmap(image)
    updateView(self, pixmap_new)

def medianBlur(self, pixmap):
    image = converPixmapToCV(pixmap)
    ksize =self.med.value()
    image = cv2.medianBlur(image, ksize)
    pixmap_new =  convertCVtoPixmap(image)
    updateView(self, pixmap_new)

def gaussianBlur(self, pixmap):
    image = converPixmapToCV(pixmap)
    ksize = (self.gaus.value(), self.gaus.value())
    image = cv2.GaussianBlur(image, ksize, 0)
    pixmap_new =  convertCVtoPixmap(image)
    updateView(self, pixmap_new)

def updateView(self, pixmap):
    self.scene.clear()
    self.scene.addPixmap(pixmap)
    self.pixmap = pixmap

def convertCVtoPixmap( rotated_image):
    return QPixmap.fromImage(QImage(rotated_image, rotated_image.shape[1], rotated_image.shape[0],rotated_image.shape[1] * rotated_image.shape[2], QImage.Format_RGB888).rgbSwapped())

def convertPILtoPixmap( rotated_image):
    np_image = np.array(rotated_image)
    qimage = qimage2ndarray.array2qimage(np_image)
    pixmap = QPixmap.fromImage(qimage)
    return pixmap

def converPixmapToCV(pixmap):
    image_data = qimage2ndarray.rgb_view(pixmap.toImage())
    image_data = cv2.cvtColor(image_data, cv2.COLOR_RGB2BGR)
    return image_data
    
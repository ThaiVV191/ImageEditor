from PyQt5.QtWidgets import *
from PyQt5.QtGui import *
from PyQt5.QtCore import *
import qimage2ndarray
from PIL import Image, ImageEnhance
import cv2
import numpy as np

def onBrightnessChanged(self, value, pixmap):
    if self.image is not None:
        self.temperature = ()
        self.contrast = ()
        self.saturation = ()
        self.sharpness = ()
        self.highlights = ()
        self.shadows = ()
        self.labelBrightness.setText('Brightness: {}'.format(value))
        image = converPixmapToCV(pixmap)
        image = cv2.cvtColor(image, cv2.COLOR_BGR2RGB)
        image = Image.fromarray(image)
        apha = 1 + abs(value) / 100       
        if len(self.brightness) > 0:
            pass
        else:
            self.brightness += (image,)
        enhancer = ImageEnhance.Brightness(self.brightness[0])
        im_output = enhancer.enhance(apha)
        pixmap_new =  convertPILtoPixmap(im_output)
        updateView(self, pixmap_new)

def onShadowsChanged(self, value, pixmap):
    if self.image is not None:
        self.temperature = ()
        self.contrast = ()
        self.saturation = ()
        self.sharpness = ()
        self.highlights = ()
        self.brightness = ()
        self.labelShadows.setText('Shadows: {}'.format(value))
        image = converPixmapToCV(pixmap)
        image = cv2.cvtColor(image, cv2.COLOR_BGR2RGB)
        image = Image.fromarray(image)
        apha = 1 - abs(value) / 100       
        if len(self.shadows) > 0:
            pass
        else:
            self.shadows += (image,)
        im_output = self.shadows[0].point(lambda x: x*apha)
        pixmap_new =  convertPILtoPixmap(im_output)
        updateView(self, pixmap_new)

def onHightlightsChanged(self, value, pixmap):
    if self.image is not None:
        self.temperature = ()
        self.contrast = ()
        self.saturation = ()
        self.sharpness = ()
        self.shadows = ()
        self.brightness = ()
        self.labelHightlights.setText('Hightlights: {}'.format(value))
        image = converPixmapToCV(pixmap)
        image = cv2.cvtColor(image, cv2.COLOR_BGR2RGB)
        image = Image.fromarray(image)
        apha = 1 + abs(value) / 100      
        if len(self.highlights) > 0:
            pass
        else:
            self.highlights += (image,)
        im_output = self.highlights[0].point(lambda x: x*apha)
        # im_output = enhancer.enhance(apha)
        pixmap_new =  convertPILtoPixmap(im_output)
        updateView(self, pixmap_new)

def onSharpnessChanged(self, value, pixmap):
    if self.image is not None:
        self.temperature = ()
        self.contrast = ()
        self.saturation = ()
        self.highlights = ()
        self.shadows = ()
        self.brightness = ()
        self.labelSharpness.setText('Sharpness: {}'.format(value))
        image = converPixmapToCV(pixmap)
        image = cv2.cvtColor(image, cv2.COLOR_BGR2RGB)
        image = Image.fromarray(image)
        apha = 1 + abs(value) / 100       
        if len(self.sharpness) > 0:
            pass
        else:
            self.sharpness += (image,)
        enhancer = ImageEnhance.Sharpness(self.sharpness[0])
        im_output = enhancer.enhance(apha)
        pixmap_new =  convertPILtoPixmap(im_output)
        updateView(self, pixmap_new)

def onSaturationChanged(self, value, pixmap):
    if self.image is not None:
        self.temperature = ()
        self.contrast = ()
        self.sharpness = ()
        self.highlights = ()
        self.shadows = ()
        self.brightness = ()
        self.labelSaturation.setText('Saturation: {}'.format(value))
        image = converPixmapToCV(pixmap)
        image = cv2.cvtColor(image, cv2.COLOR_BGR2RGB)
        image = Image.fromarray(image)
        apha = 1 + abs(value) / 100       
        if len(self.saturation) > 0:
            pass
        else:
            self.saturation += (image,)
        enhancer = ImageEnhance.Color(self.saturation[0])
        im_output = enhancer.enhance(apha)
        pixmap_new =  convertPILtoPixmap(im_output)
        updateView(self, pixmap_new)

def onContrastChanged(self, value, pixmap):
    if self.image is not None:
        self.temperature = ()
        self.saturation = ()
        self.sharpness = ()
        self.highlights = ()
        self.shadows = ()
        self.brightness = ()
        self.labelContrast.setText('Contrast: {}'.format(value))
        image = converPixmapToCV(pixmap)
        image = cv2.cvtColor(image, cv2.COLOR_BGR2RGB)
        image = Image.fromarray(image)
        apha = 1 + abs(value) / 100       
        if len(self.contrast) > 0:
            pass
        else:
            self.contrast += (image,)
        enhancer = ImageEnhance.Contrast(self.contrast[0])
        im_output = enhancer.enhance(apha)
        pixmap_new =  convertPILtoPixmap(im_output)
        updateView(self, pixmap_new)

def onTemperatureChanged(self, value, pixmap):
    if self.image is not None:
        self.contrast = ()
        self.saturation = ()
        self.sharpness = ()
        self.highlights = ()
        self.shadows = ()
        self.brightness = ()
        self.labelT.setText('Temperature: {}'.format(value))
        image = converPixmapToCV(pixmap)
        image = cv2.cvtColor(image, cv2.COLOR_BGR2RGB)
        apha = abs(value) / 100.0
        if len(self.temperature) > 0:
            pass
        else:
            self.temperature += (image[:, :, 0],)
            self.temperature += (image[:, :, 2],)
        image[:, :, 0] = self.temperature[0] * apha
        image[:, :, 2] = self.temperature[1] * ( 1 - apha)
        pixmap_new = convertCVtoPixmap(image)
        updateView(self, pixmap_new)


def updateView(self, pixmap):
    self.scene.clear()
    self.scene.addPixmap(pixmap)
    self.pixmap = pixmap

def convertCVtoPixmap( rotated_image):
    return QPixmap.fromImage(QImage(rotated_image, rotated_image.shape[1], rotated_image.shape[0],rotated_image.shape[1] * rotated_image.shape[2], QImage.Format_BGR888).rgbSwapped())

def convertPILtoPixmap( rotated_image):
    np_image = np.array(rotated_image)
    qimage = qimage2ndarray.array2qimage(np_image)
    pixmap = QPixmap.fromImage(qimage)
    return pixmap

def converPixmapToCV(pixmap):
    image_data = qimage2ndarray.rgb_view(pixmap.toImage())
    image_data = cv2.cvtColor(image_data, cv2.COLOR_RGB2BGR)
    return image_data
    
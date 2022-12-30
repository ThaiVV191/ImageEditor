from PyQt5.QtWidgets import *
from PyQt5.QtGui import *
from PyQt5.QtCore import *
import sys
from actions import *
import cv2
import numpy as np
import imutils
import qimage2ndarray
from customQGraphicsView import customQGraphicsView

from lb.backend.general.general import *

class ImageCropper(QMainWindow):
    def __init__(self):
        super().__init__()
        self.scale = 1
        self.image = None
        self.initUI()
        self.createToolBarV()


    def initUI(self):
        self.setWindowTitle("Python Menus & Toolbars")
        self.setGeometry(100, 100, 400, 300)
        self.centralWidget = QWidget()
        self.setCentralWidget(self.centralWidget)
        self.scene = QGraphicsScene()
        self.view = customQGraphicsView(self.scene)
        
        self.layout = QHBoxLayout()
        self.splitter = QSplitter(Qt.Vertical)
        self.splitter.addWidget(self.view)
        self.view.setSizePolicy(QSizePolicy.Expanding, QSizePolicy.Expanding)
        self.layout.addWidget(self.splitter, stretch = 6)
        self.editToolBarV = QToolBar(self)
        self.editToolBarH = QToolBar(self)
        self.addToolBar(Qt.LeftToolBarArea,self.editToolBarV)
        self.addToolBar(Qt.TopToolBarArea,self.editToolBarH)
        self.editToolBarH.setFixedHeight(50)
        self.note = QListWidget()
        self.layout.addWidget(self.note, stretch = 1)
        self.centralWidget.setLayout(self.layout)
        self.showMaximized()
    
    def createToolBarV(self):
        self.buttonOpen = self._createToolBar('icons/plus.png', self.open, "Ctrl+O")
        self.buttonSave = self._createToolBar('icons/save.png', self.save, "Ctrl+S")
        self.buttonZoomIn = self._createToolBar('icons/zoom-in.png', self.zoomIn, "Ctrl++")
        self.buttonZoomOut = self._createToolBar('icons/zoom-out.png', self.zoomOut,"Ctrl+-")
        self.buttonCrop = self._createToolBar('icons/crop.png', self.crop, "Ctrl+A")
        self.buttonFlipH = self._createToolBar('icons/flipH.png', self.flipH, "Ctrl+A")
        self.buttonFlipV = self._createToolBar('icons/filpV.png', self.flipV, "Ctrl+A")
        self.buttonResize = self._createToolBar('icons/resize.png', self.resize, "Ctrl+A")
        self.buttonRotate = self._createToolBar('icons/rotate.png', self.rotate , "Ctrl+A")
        self.buttonText = self._createToolBar('icons/text.png', self.text , "Ctrl+A")
        self.listTool = [self.buttonOpen, self.buttonSave, self.buttonZoomIn, self.buttonZoomOut, self.buttonCrop, self.buttonFlipH, self.buttonFlipV, \
             self.buttonResize,self.buttonRotate, self.buttonText ]
        for bt in self.listTool:
            bt.clicked.connect(self.button_clicked)

    def button_clicked(self):
        
        sender = self.sender()
        sender.setChecked(True)
        for button in self.listTool:
            if button != sender:
                button.setChecked(False)

    def _createToolBar(self, name, log, shortCut):
        window = QWidget()
        button = QVBoxLayout()
        toolButton = QToolButton(self)
        toolButton.setAutoRaise(True)
        toolButton.clicked.connect(log)       
        toolButton.setShortcut(QKeySequence(shortCut))
        toolButton.setIcon(QIcon(name))
        toolButton.setIconSize(QSize(25, 25))
        toolButton.setCheckable(True)
        button.addWidget(toolButton)
        spacer = QSpacerItem(10, 10, QSizePolicy.Fixed, QSizePolicy.Fixed)
        button.addItem(spacer)
        window.setLayout(button)
        self.editToolBarV.addWidget(window)
        return toolButton
        

    def open(self):
        self.editToolBarH.clear()
        self.view.activate = False
        file_name, _ = QFileDialog.getOpenFileName(
            self, "Open file", ".", "Image Files (*.png *.jpg *.bmp)"
        )
        if not file_name:
            return
        self.image = QImage(file_name)
        self.scene.clear()
        self.pixmap = QPixmap.fromImage(self.image)
        self.scene.setSceneRect(0, 0, self.image.width(), self.image.height())
        self.scene.addPixmap(self.pixmap)
        
        
    def zoomIn(self):
        self.editToolBarH.clear()
        self.view.activate = False
        self.scale = 1.05
        self.actionZoom()

    def zoomOut(self):
        self.editToolBarH.clear()
        self.view.activate = False
        self.scale *= 0.95
        self.actionZoom()
        
    def actionZoom(self):
        if self.image is not None:
            self.view.scale(self.scale, self.scale)

    def resize(self):
        if self.image is not None:
            self.editToolBarH.clear()
            self.view.activate = False
            window = QWidget()
            width = QLabel()
            width.setText('Width:')
            height = QLabel()
            height.setText('Height:')
            self.e1 = QLineEdit()
            validator = QIntValidator(100, 2000)
            self.e1.setValidator(validator)
            self.e1.setAlignment(Qt.AlignHCenter)
            self.e1.setMaxLength(4)
            self.e1.setFixedSize(100, 25)
            self.e2 = QLineEdit()
            validator = QIntValidator(100, 2000)
            self.e2.setValidator(validator)
            self.e2.setAlignment(Qt.AlignHCenter)
            self.e2.setMaxLength(4)
            self.e2.setFixedSize(100, 25)
            
            button_action = QAction( self)
            button_action.setShortcut(QKeySequence(Qt.Key_Enter))
            button_action.triggered.connect(self.buttonClickToResize)
            self.e1.returnPressed.connect(button_action.trigger)
            self.e2.returnPressed.connect(button_action.trigger)

            toolBarH = QHBoxLayout()
            toolBarH.addWidget(width)
            toolBarH.addWidget(self.e1)
            toolBarH.addWidget(height)
            toolBarH.addWidget(self.e2)
            window.setSizePolicy(QSizePolicy.Fixed, QSizePolicy.Fixed)
            window.setLayout(toolBarH)
            self.editToolBarH.addWidget(window)
            self.editToolBarH.addAction(button_action)
    
    def buttonClickToResize(self):
        if self.e1.text() != '' and self.e2.text() != '' and 2000 >= int(self.e1.text()) >= 200 and 2000>= int(self.e2.text()) >= 200:
            width = int(self.e1.text())
            height = int(self.e2.text())
            self.pixmap = self.pixmap.scaled(QSize(width,height), Qt.IgnoreAspectRatio,Qt.SmoothTransformation )
            self.scene.clear()  # Clear the scene
            self.scene.setSceneRect(0, 0, self.pixmap.width(), self.pixmap.height())
            self.scene.addPixmap(self.pixmap)
            self.scene.update()     

    def save(self):
        if self.image is not None:
            self.editToolBarH.clear()
            self.view.activate = False
            options = QFileDialog.Options()
            options |= QFileDialog.ReadOnly
            file_name, _ = QFileDialog.getSaveFileName(self, "Save Image", "", "Images (*.png *.xpm *.jpg);;All Files (*)", options=options)
            if file_name:
                self.pixmap.save(file_name)

    def crop(self):
        # self = crop(self)
        if self.buttonCrop.isChecked and self.image is not None:
            self.editToolBarH.clear()
            self.view.activate = True
            buttonCrop = QToolButton()
            buttonCrop.setText('OK')
            buttonCrop.setAutoRaise(True)
            buttonCrop.setIcon(QIcon('icons/check.png'))
            buttonCrop.clicked.connect(self.buttonClicked)
            left_spacer = QWidget()
            left_spacer.setSizePolicy(QSizePolicy.Expanding, QSizePolicy.Expanding)
            right_spacer = QWidget()
            right_spacer.setSizePolicy(QSizePolicy.Expanding, QSizePolicy.Expanding)
            self.editToolBarH.addWidget(left_spacer)
            self.editToolBarH.addWidget(buttonCrop)
            self.editToolBarH.addWidget(right_spacer)
        
    
    def buttonClicked(self):
        crop_start, crop_end = self.view.getResult()
        if crop_start is not None and crop_end is not None:
            x,y, x1, y1 = self.view.mapToScene(crop_start).x(), self.view.mapToScene(crop_start).y(), self.view.mapToScene(crop_end).x(), self.view.mapToScene(crop_end).y()
            x = 0 if x < 0 else x
            y = 0 if y < 0 else y
            x1 = self.pixmap.width() if x1 > self.pixmap.width() else x1
            y1  = self.pixmap.height() if y1 > self.pixmap.height() else y1
            crop_rect = QRectF(x,y, x1 - x, y1 - y)
            self.pixmap = self.pixmap.copy(crop_rect.toRect())
            self.view.crop_rect = None
            self.view.crop_start = None
            self.view.crop_end = None
            self.scene.clear()  # Clear the scene
            self.scene.setSceneRect(0, 0, self.pixmap.width(), self.pixmap.height())
            self.scene.addPixmap(self.pixmap)
            self.scene.update()
        
        

    def flipH(self):

        if self.image is not None:
            self.editToolBarH.clear()
            self.view.activate = False
            self.pixmap = self.pixmap.transformed(QTransform().scale(-1, 1))
            self.pixmap = self.pixmap.copy()
            self.scene.setSceneRect(0, 0, self.pixmap.width(), self.pixmap.height())
            self.scene.clear()
            self.scene.addPixmap(self.pixmap)
            self.scene.update()

    def flipV(self):

        if self.image is not None:
            self.editToolBarH.clear()
            self.view.activate = False
            self.pixmap = self.pixmap.transformed(QTransform().scale(1, -1))
            self.pixmap = self.pixmap.copy()
            self.scene.setSceneRect(0, 0, self.pixmap.width(), self.pixmap.height())
            self.scene.clear()
            self.scene.addPixmap(self.pixmap)
            self.scene.update()

    def rotate(self):
        if self.image is not None:
            self.pixmap_ = self.pixmap.copy()
            self.editToolBarH.clear()
            self.view.activate = False
            self.slider = QSlider(Qt.Horizontal, self)
            self.slider.setMinimum(0)
            self.slider.setMaximum(360)
            self.slider.setFixedWidth(self.view.width() // 2.5)
            self.editToolBarH.clear()
            buttonRotateL = QToolButton()
            buttonRotateL.clicked.connect(self.rotateImage90)      
            buttonRotateL.setIcon(QIcon('icons/rotateLeft.png'))
            buttonRotateR = QToolButton()
            buttonRotateR.clicked.connect(self.rotateImage_90)       
            buttonRotateR.setIcon(QIcon('icons/rotateRight.png'))
            self.slider.valueChanged.connect(self.rotateImage)
            window = QWidget()
            toolBarH = QHBoxLayout()
            toolBarH.setSizeConstraint(QLayout.SetFixedSize)
            toolBarH.addWidget(buttonRotateL)
            toolBarH.addWidget(buttonRotateR)
            toolBarH.addWidget(self.slider)
            window.setSizePolicy(QSizePolicy.Fixed, QSizePolicy.Fixed)
            window.setLayout(toolBarH)
            left_spacer = QWidget()
            left_spacer.setSizePolicy(QSizePolicy.Expanding, QSizePolicy.Expanding)
            right_spacer = QWidget()
            right_spacer.setSizePolicy(QSizePolicy.Expanding, QSizePolicy.Expanding)
            self.editToolBarH.addWidget(left_spacer)
            self.editToolBarH.addWidget(window)
            self.editToolBarH.addWidget(right_spacer)


    def rotateImage(self, angle):
        image = self.converPixmapToCV(self.pixmap_) 
        rotated_image = imutils.rotate_bound(image,angle)
        pixmap = QPixmap.fromImage(QImage(rotated_image, rotated_image.shape[1], rotated_image.shape[0], rotated_image.strides[0], QImage.Format_RGB888).rgbSwapped())
        self.pixmap = pixmap       
        self.scene.clear()
        self.scene.setSceneRect(0, 0, self.pixmap.width(), self.pixmap.height())       
        self.scene.addPixmap(self.pixmap)
        self.scene.update()

    def rotateImage90(self):
        image = self.converPixmapToCV(self.pixmap) 
        rotated_image = imutils.rotate_bound(image,-90)
        pixmap = QPixmap.fromImage(QImage(rotated_image, rotated_image.shape[1], rotated_image.shape[0], rotated_image.strides[0], QImage.Format_RGB888).rgbSwapped())
        self.pixmap = pixmap       
        self.scene.clear()
        self.scene.setSceneRect(0, 0, self.pixmap.width(), self.pixmap.height())       
        self.scene.addPixmap(self.pixmap)
        self.scene.update()

    def rotateImage_90(self):
        image = self.converPixmapToCV(self.pixmap) 
        rotated_image = imutils.rotate_bound(image,90)
        pixmap = QPixmap.fromImage(QImage(rotated_image, rotated_image.shape[1], rotated_image.shape[0], rotated_image.strides[0], QImage.Format_RGB888).rgbSwapped())
        self.pixmap = pixmap       
        self.scene.clear()
        self.scene.setSceneRect(0, 0, self.pixmap.width(), self.pixmap.height())       
        self.scene.addPixmap(self.pixmap)
        self.scene.update()


    def text(parent):
        
        # self.scale *= 1.15
        # self.resize_image()
        pass

    def updateView(self):
        matrix = QTransform().scale(self.view.viewport().width() / self.scene.width(), self.view.viewport().height() / self.scene.height())
        self.view.setTransform(matrix)

    def convertCVtoPixmap(self, image):
        return QPixmap.fromImage(QImage(self.image.data, self.image.shape[1], self.image.shape[0], 3*self.image.shape[1], QImage.Format_RGB888).rgbSwapped())

    def converPixmapToCV(self, pixmap):
        image_data = qimage2ndarray.rgb_view(pixmap.toImage())
        image_data = cv2.cvtColor(image_data, cv2.COLOR_RGB2BGR)
        # image_data = image_data.reshape(pixmap.height(), pixmap.width(), 3)
        return image_data




if __name__ == "__main__":
    app = QApplication(sys.argv)
    win = ImageCropper()
    win.show()
    sys.exit(app.exec_())
from PyQt5.QtWidgets import *
from PyQt5.QtGui import *
from PyQt5.QtCore import *
import sys
from actions import *
import cv2
# from PyQt5.QtGui import QMatrix
from customQGraphicsView import customQGraphicsView

from lb.backend.general.general import *

class ImageCropper(QMainWindow):
    def __init__(self):
        super().__init__()
        self.scale = 1
        self.image = None
        # self.scaled_pixmap = None
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
        self.buttonZoomIn = self._createToolBar('icons/zoom-in.png', self.zoomIn, "Ctrl+A")
        self.buttonZoomOut = self._createToolBar('icons/zoom-out.png', self.zoomOut,"Ctrl+A")
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
        toolButton.setIconSize(QSize(30, 30))
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
        pic = QGraphicsPixmapItem()
        # self.pixmap = QPixmap.fromImage(QImage(self.image.data, self.image.shape[1], self.image.shape[0], 3*self.image.shape[1], QImage.Format_RGB888).rgbSwapped())
        self.pixmap = QPixmap.fromImage(self.image)
        self.pixmapUpdate = self.pixmap.scaled(self.scale * self.pixmap.size())
        pic.setPixmap(self.pixmap)
        self.scene.setSceneRect(0, 0, self.image.width(), self.image.height())
        self.scene.addItem(pic)
        
        
    def zoomIn(self):
        self.editToolBarH.clear()
        self.view.activate = False
        self.scale *= 1.05
        self.actionZoom()
        
    def actionZoom(self):
        if self.image is not None:
            # self.pixmap = self.pixmapUpdate.copy()
            self.scaled_pixmap = self.pixmap.scaled(self.scale * self.pixmap.size(), Qt.KeepAspectRatio,Qt.SmoothTransformation )
            self.pixmapUpdate = self.scaled_pixmap.copy()
            pic = QGraphicsPixmapItem()
            pic.setPixmap(self.scaled_pixmap)
            self.scene.clear()
            self.scene.setSceneRect(0, 0, self.scaled_pixmap.width(), self.scaled_pixmap.height())
            self.scene.addItem(pic)
            self.scene.update()

    def zoomOut(self):
        self.editToolBarH.clear()
        self.view.activate = False
        self.scale /= 1.15
        self.actionZoom()

    def resize(self):
        self.editToolBarH.clear()
        self.view.activate = False
        window = QWidget()
        width = QLabel()
        width.setText('Width:')
        height = QLabel()
        height.setText('Height:')
        e1 = QLineEdit()
        e1.setFixedSize(100, 25)
        e2 = QLineEdit()
        e2.setFixedSize(100, 25)
        toolBarH = QHBoxLayout()
        toolBarH.addWidget(width)
        toolBarH.addWidget(e1)
        toolBarH.addWidget(height)
        toolBarH.addWidget(e2)
        window.setSizePolicy(QSizePolicy.Fixed, QSizePolicy.Fixed)
        window.setLayout(toolBarH)
        self.editToolBarH.addWidget(window)
        

    def save(self):
        if self.image is not None:
            self.editToolBarH.clear()
            self.view.activate = False
            options = QFileDialog.Options()
            options |= QFileDialog.ReadOnly
            file_name, _ = QFileDialog.getSaveFileName(self, "Save Image", "", "Images (*.png *.xpm *.jpg);;All Files (*)", options=options)
            if file_name:
                self.pixmapUpdate.save(file_name)

    def crop(self):
        self = crop(self)
        # if self.buttonCrop.isChecked and self.image is not None:
        #     self.editToolBarH.clear()
        #     self.view.activate = True
        #     button_action = QAction(QIcon("icons/check.png"), "OK", self)
        #     button_action.triggered.connect(self.buttonClicked)
        #     left_spacer = QWidget()
        #     left_spacer.setSizePolicy(QSizePolicy.Expanding, QSizePolicy.Expanding)
        #     right_spacer = QWidget()
        #     right_spacer.setSizePolicy(QSizePolicy.Expanding, QSizePolicy.Expanding)
        #     self.editToolBarH.addWidget(left_spacer)
        #     self.editToolBarH.addAction(button_action)
        #     self.editToolBarH.addWidget(right_spacer)
        
    
    def buttonClicked(self):
        crop_start, crop_end = self.view.getResult()
        if crop_start is not None and crop_end is not None:
            x,y, x1, y1 = self.view.mapToScene(crop_start).x(), self.view.mapToScene(crop_start).y(), self.view.mapToScene(crop_end).x(), self.view.mapToScene(crop_end).y()
            x = 0 if x < 0 else x
            y = 0 if y < 0 else y
            x1 = self.pixmapUpdate.width() if x1 > self.pixmapUpdate.width() else x1
            y1  = self.pixmapUpdate.height() if y1 > self.pixmapUpdate.height() else y1
            crop_rect = QRectF(x,y, x1 - x, y1 - y)
            self.pixmapUpdate = self.pixmapUpdate.copy(crop_rect.toRect())
            self.pixmap = self.pixmapUpdate.copy()
            self.view.crop_rect = None
            self.view.crop_start = None
            self.view.crop_end = None
            self.scene.clear()  # Clear the scene
            self.scene.setSceneRect(0, 0, self.pixmapUpdate.width(), self.pixmapUpdate.height())
            self.scene.addPixmap(self.pixmapUpdate)
            self.scene.update()
        
        

    def flipH(self):

        if self.image is not None:
            self.editToolBarH.clear()
            self.view.activate = False
            self.pixmapUpdate = self.pixmapUpdate.transformed(QTransform().scale(-1, 1))
            self.pixmap = self.pixmapUpdate.copy()
            self.scene.setSceneRect(0, 0, self.pixmapUpdate.width(), self.pixmapUpdate.height())
            self.scene.clear()
            self.scene.addPixmap(self.pixmapUpdate)
            self.scene.update()

    def flipV(self):

        if self.image is not None:
            self.editToolBarH.clear()
            self.view.activate = False
            self.pixmapUpdate = self.pixmapUpdate.transformed(QTransform().scale(1, -1))
            self.pixmap = self.pixmapUpdate.copy()
            self.scene.setSceneRect(0, 0, self.pixmapUpdate.width(), self.pixmapUpdate.height())
            self.scene.clear()
            self.scene.addPixmap(self.pixmapUpdate)
            self.scene.update()

    def rotate(parent):
        
        # self.scale *= 1.15
        # self.resize_image()
        pass

    def text(parent):
        
        # self.scale *= 1.15
        # self.resize_image()
        pass

    def updateView(self):
        matrix = QTransform().scale(self.view.viewport().width() / self.scene.width(), self.view.viewport().height() / self.scene.height())
        self.view.setTransform(matrix)




if __name__ == "__main__":
    app = QApplication(sys.argv)
    win = ImageCropper()
    win.show()
    sys.exit(app.exec_())
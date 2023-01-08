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
        self.tool()
        self.createToolBarV()


    def initUI(self):
        self.setWindowTitle("Python Menus & Toolbars")
        self.setGeometry(100, 100, 400, 300)
        self.centralWidget = QWidget()
        self.setCentralWidget(self.centralWidget)
        self.scene = QGraphicsScene()
        self.view = customQGraphicsView()
        self.view.setScene(self.scene)
        self.transform = self.view.transform()
        self.layout = QHBoxLayout()
        self.splitter = QSplitter(Qt.Vertical)
        self.splitter.addWidget(self.view)
        self.view.setSizePolicy(QSizePolicy.Expanding, QSizePolicy.Expanding)
        self.layout.addWidget(self.splitter, stretch = 4)
        self.editToolBarV = QToolBar(self)
        self.editToolBarH = QToolBar(self)
        self.addToolBar(Qt.LeftToolBarArea,self.editToolBarV)
        self.addToolBar(Qt.TopToolBarArea,self.editToolBarH)
        self.editToolBarH.setFixedHeight(50)
        self.tabs = QTabWidget()
        self.tabEdit = QWidget()
        self.tabFilter = QWidget()
        self.tabAI = QWidget()
        self.tabs.addTab(self.tabEdit, 'Edit Image')
        self.tabs.addTab(self.tabFilter, 'Filter')
        self.tabs.addTab(self.tabAI, 'AI tool')
        # self.setLayout(vbox)
        self.layout.addWidget(self.tabs, stretch = 1)
        self.centralWidget.setLayout(self.layout)
        self.showMaximized()

    def tool(self):
        self.hbox = QVBoxLayout()
        self.labelT = QLabel("Temperature: 0")
        self._tool(self.labelT, self.onTemperatureChanged)
        self.labelContrast = QLabel("Contrast: 0")
        self._tool(self.labelContrast, self.onContrastChanged)
        # Saturation
        self.labelSaturation = QLabel("Saturation: 0")
        self._tool(self.labelSaturation, self.onSaturationChanged)
        # Exposure
        self.labelSharpness = QLabel("Sharpness: 0")
        self._tool(self.labelSharpness, self.onSharpnessChanged)
        # Hightlights
        self.labelHightlights = QLabel("Hightlights: 0")
        self._tool(self.labelHightlights, self.onHightlightsChanged)
        #Shadows
        self.labelShadows = QLabel("Shadows: 0")
        self._tool(self.labelShadows, self.onShadowsChanged)
        #Brightness
        self.labelBrightness = QLabel("Brightness: 0")
        self._tool(self.labelBrightness, self.onBrightnessChanged)
        self.tabEdit.setLayout(self.hbox)

    def _tool(self, label, log):
        vbox = QVBoxLayout()
        widgetT = QWidget()
        widgetT.setFixedHeight(60)
        sliderTem = QSlider(Qt.Horizontal)
        # self.labelT = QLabel(name)
        sliderTem.setMinimum(-100)
        sliderTem.setMaximum(100)
        sliderTem.valueChanged.connect(log)
        vbox.addWidget(label)
        vbox.addWidget(sliderTem)

        widgetT.setLayout(vbox)
        self.hbox.addWidget(widgetT)
    
    def onBrightnessChanged(self, value):
        self.labelBrightness.setText('Brightness: {}'.format(value))

    def onShadowsChanged(self, value):
        self.labelShadows.setText('Shadows: {}'.format(value))

    def onHightlightsChanged(self, value):
        self.labelHightlights.setText('Hightlights: {}'.format(value))

    def onSharpnessChanged(self, value):
        self.labelSharpness.setText('Sharpness: {}'.format(value))

    def onSaturationChanged(self, value):
        self.labelSaturation.setText('Saturation: {}'.format(value))

    def onContrastChanged(self, value):
        self.labelContrast.setText('Contrast: {}'.format(value))

    def onTemperatureChanged(self, value):
        self.labelT.setText('Temperature: {}'.format(value))
        # self.slider.valueChanged.connect(self.rotateImage)
    
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
        self = open(self)   
        
    def zoomIn(self):
        self = zoomIn(self)

    def zoomOut(self):
        self = zoomOut(self)
        
    def actionZoom(self):
        self = actionZoom(self)

    def resize(self):
        self = resize(self)
    
    def buttonClickToResize(self):
            self = buttonClickToResize(self)

    def save(self):
        self = save(self)

    def crop(self):
        self = crop(self)
    
    def buttonClicked(self):
        self = buttonClicked(self)
        
    def flipH(self):
        self = flipH(self)

    def flipV(self):
        self = flipV(self)

    def rotate(self):
        self = rotate(self)

    def rotateImage(self, angle):
        self = rotateImage(self, angle)

    def rotateImage90(self):
        self = rotateImage90(self)

    def rotateImage_90(self):
        self = rotateImage_90(self)

    def text(self):
        self = text(self)

    def buttonClickToSetText(self):
        self = buttonClickToSetText(self)

    def buttonClickToSetTextPixmap(self):
        self = buttonClickToSetTextPixmap(self)          

    def fontColorChanged(self):
        self = fontColorChanged(self)
        
    def highlight(self):
       self = highlight(self)
        
    def bold(self):
        self = bold(self)
    
    def italic(self):
        self = italic(self)

    def underline(self):
        self = underline(self)

    def strike(self):
        self = strike(self)
        
    def alignLeft(self):
        self = alignLeft(self)

    def alignRight(self):
        self = alignRight(self)

    def alignCenter(self):
        self = alignCenter(self)
    
    def alignJustify(self):
        self = alignJustify(self)


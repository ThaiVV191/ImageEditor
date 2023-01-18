from PyQt5.QtWidgets import *
from PyQt5.QtGui import *
from PyQt5.QtCore import *
import imutils
import copy
import qimage2ndarray
from customQGraphicsView import customQGraphicsView
from lb.backend.edittool import *
from lb.backend.filter import *
from lb.backend.general.general import *

class ImageCropper(QMainWindow):
    def __init__(self):
        super().__init__()
        self.scale = 1
        self.image = None
        self.temperature = ()
        self.contrast = ()
        self.saturation = ()
        self.sharpness = ()
        self.highlights = ()
        self.shadows = ()
        self.brightness = ()
        self.initUI()
        self.toolFilter()
        self.toolEdit()    
        self.toolAI()   
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
        self.tabFilter.setFixedWidth(245)
        self.tabAI = QWidget()
        self.tabs.addTab(self.tabEdit, 'Edit Image')
        self.tabs.addTab(self.tabFilter, 'Filter')
        self.tabs.addTab(self.tabAI, 'AI tool')
        self.layout.addWidget(self.tabs, stretch = 1)
        self.centralWidget.setLayout(self.layout)
        self.showMaximized()

    def toolAI(self):       
        self.hboxTool = QVBoxLayout()
        self.blur, self.blurBin  = self.createtoolFilter('Box blur', self.boxBlur, False)
        self.blur1, self.gaus = self.createtoolFilter('Gaussian blur', self.gaussianBlur, False)
        self.blur2, self.med = self.createtoolFilter('Median blur', self.medianBlur, False)
        self.blur3, _ = self.createtoolFilter('Emboss', self.emboss, False)
        # self.blur.setAutoRaise(True)
        self.hboxTool.addWidget(self.blur)
        self.hboxTool.addWidget(self.blur1)
        self.hboxTool.addWidget(self.blur2)
        self.hboxTool.addWidget(self.blur3)
        self.tabAI.setLayout(self.hboxTool)

    def toolFilter(self):       
        self.hboxTool = QVBoxLayout()
        self.blur, self.blurBin  = self.createtoolFilter('Box blur', self.boxBlur, True)
        self.blur1, self.gaus = self.createtoolFilter('Gaussian blur', self.gaussianBlur, True)
        self.blur2, self.med = self.createtoolFilter('Median blur', self.medianBlur, True)
        self.blur3, _ = self.createtoolFilter('Emboss', self.emboss, False)
        # self.blur.setAutoRaise(True)
        self.hboxTool.addWidget(self.blur)
        self.hboxTool.addWidget(self.blur1)
        self.hboxTool.addWidget(self.blur2)
        self.hboxTool.addWidget(self.blur3)
        self.tabFilter.setLayout(self.hboxTool)
        

    def createtoolFilter(self, name, log, flag):
        hboxTool = QHBoxLayout()
        widgetFilter = QWidget()
        button_action = QPushButton(name)
        button_action.clicked.connect(log)
        # labelT = QLabel(name)
        spinBoxW = QSpinBox()
        spinBoxW.setMinimum(1)
        spinBoxW.setSingleStep(2)
        spinBoxW.setValue(3)
        # hboxTool.addWidget(labelT)
        if flag:
            hboxTool.addWidget(spinBoxW)    
        hboxTool.addWidget(button_action)   
        widgetFilter.setLayout(hboxTool)
        return widgetFilter, spinBoxW
        

    def toolEdit(self):      
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
        sliderTem.setMinimum(-100)
        sliderTem.setMaximum(100)
        sliderTem.valueChanged.connect(log)
        vbox.addWidget(label)
        vbox.addWidget(sliderTem)
        widgetT.setLayout(vbox)
        self.hbox.addWidget(widgetT)

    def emboss(self):
        emboss(self, self.pixmap)

    def boxBlur(self):
        boxBlur(self, self.pixmap)

    def gaussianBlur(self):
        gaussianBlur(self, self.pixmap)

    def medianBlur(self):
        medianBlur(self, self.pixmap)

    def onBrightnessChanged(self, value):
        if self.image is not None:
            onBrightnessChanged(self, value, self.pixmap)

    def onShadowsChanged(self, value):
        if self.image is not None:
            onShadowsChanged(self, value, self.pixmap)

    def onHightlightsChanged(self, value):
        if self.image is not None:
            onHightlightsChanged(self, value,self.pixmap)

    def onSharpnessChanged(self, value):
        if self.image is not None:
            onSharpnessChanged(self, value, self.pixmap)

    def onSaturationChanged(self, value):
        if self.image is not None:
            onSaturationChanged(self, value, self.pixmap)

    def onContrastChanged(self, value):
        if self.image is not None:
            onContrastChanged(self, value, self.pixmap)
       
    def onTemperatureChanged(self, value):
        if self.image is not None:
            onTemperatureChanged(self, value, self.pixmap)
 
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
        open(self)   
        
    def zoomIn(self):
        zoomIn(self)

    def zoomOut(self):
        zoomOut(self)
        
    def actionZoom(self):
        actionZoom(self)

    def resize(self):
        resize(self)
    
    def buttonClickToResize(self):
            buttonClickToResize(self)

    def save(self):
        save(self)

    def crop(self):
        crop(self)
    
    def buttonClicked(self):
        buttonClicked(self)
        
    def flipH(self):
        flipH(self)

    def flipV(self):
        flipV(self)

    def rotate(self):
        rotate(self)

    def rotateImage(self, angle):
        rotateImage(self, angle)

    def rotateImage90(self):
        rotateImage90(self)

    def rotateImage_90(self):
        rotateImage_90(self)

    def text(self):
        text(self)

    def buttonClickToSetText(self):
        buttonClickToSetText(self)

    def buttonClickToSetTextPixmap(self):
        buttonClickToSetTextPixmap(self)          

    def fontColorChanged(self):
        fontColorChanged(self)
        
    def highlight(self):
       highlight(self)
        
    def bold(self):
        bold(self)
    
    def italic(self):
        italic(self)

    def underline(self):
        underline(self)

    def strike(self):
        strike(self)
        
    def alignLeft(self):
        alignLeft(self)

    def alignRight(self):
        alignRight(self)

    def alignCenter(self):
        alignCenter(self)
    
    def alignJustify(self):
        alignJustify(self)


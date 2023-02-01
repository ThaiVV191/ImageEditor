from PyQt5.QtWidgets import *
from PyQt5.QtGui import *
from PyQt5.QtCore import *
import yaml
import torch
import numpy as np
import hydra
from basicsr.archs.rrdbnet_arch import RRDBNet
from omegaconf import OmegaConf
from lb.model.realesrgan.utils import RealESRGANer
from lb.model.realesrgan.srvggnet import SRVGGNetCompact
from lb.model.lama.saicinpainting.training.trainers import load_checkpoint
from customQGraphicsView import customQGraphicsView
from lb.backend.edittool import *
from lb.backend.filter import *
from lb.backend.aitools import *
from lb.backend.general import *

device = torch.device(f'cuda' if torch.cuda.is_available() else 'cpu')
checkpoint_path = '/home/thaivv/ImageEditor/lb/model/lama/weight/model/best.ckpt'
config = '/home/thaivv/ImageEditor/lb/model/lama/weight/config.yaml'

@hydra.main(config_path="/home/thaivv/ImageEditor/lb/model/lama/configs/prediction", config_name="default.yaml")
def main(predict_config: OmegaConf):
    with open(config, 'r') as f:
        train_config = OmegaConf.create(yaml.safe_load(f))
    train_config.training_model.predict_only = True
    model = load_checkpoint(train_config, checkpoint_path, strict=False, map_location='cpu')
    model.eval()
    model.to(device)
    return model


class ImageCropper(QMainWindow):
    def __init__(self):
        super().__init__()
        self.scale = 1
        self.image = None
        self.painting = False
        self.temperature = ()
        self.contrast = ()
        self.saturation = ()
        self.sharpness = ()
        self.highlights = ()
        self.shadows = ()
        self.brightness = ()
        self.initUI()
        self.initModelAi()
        self.toolFilter()
        self.toolEdit()    
        self.toolAI()   
        self.createToolBarV()
        self.initPaint()
        
    def initPaint(self):
        self.drawing = False
        self.brushSize = 9
        self.brushColor = Qt.black
        self.lastPoint = QPoint()


    def initModelAi(self):
        model = RRDBNet(num_in_ch=3, num_out_ch=3, num_feat=64, num_block=23, num_grow_ch=32, scale=2)
        netscale = 2
        # wdn_model_path = '/home/thaivv/ImageEditor/lb/model/realesrgan/weight/RealESRGAN_x4plus.pth'
        model_path = '/home/thaivv/ImageEditor/lb/model/realesrgan/weight/RealESRGAN_x2plus.pth'
        dni_weight = None
        tile = 0
        tile_pad = 10
        pre_pad = 0
        half = False
        gpu_id = 0
        self.outscale = 1
        self.upsampler = RealESRGANer(
            scale=netscale,
            model_path=model_path,
            dni_weight=dni_weight,
            model=model,
            tile=tile,
            tile_pad=tile_pad,
            pre_pad=pre_pad,
            half=half,
            gpu_id=gpu_id)
        self.modelLama = main(OmegaConf)

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
        self.dentaX = self.editToolBarV.width()
        self.dentaY = self.editToolBarH.height()
        # print(self.editToolBarH.height())
        self.showMaximized()

    def toolAI(self):       
        self.hboxToolAI = QVBoxLayout()
        self.resolution, _  = self.createtoolFilter('Super Resolution', self.superResolution, False)
        self.inpainting, _ = self.createtoolFilter('Inpainting', self.inpainting, False)
        self.hboxToolAI.addWidget(self.resolution)
        self.hboxToolAI.addWidget(self.inpainting)
        self.tabAI.setLayout(self.hboxToolAI)

    def toolFilter(self):       
        self.hboxTool = QVBoxLayout()
        self.blur, self.blurBin  = self.createtoolFilter('Box blur', self.boxBlur, True)
        self.blur1, self.gaus = self.createtoolFilter('Gaussian blur', self.gaussianBlur, True)
        self.blur2, self.med = self.createtoolFilter('Median blur', self.medianBlur, True)
        self.blur3, _ = self.createtoolFilter('Emboss', self.emboss, False)
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
        spinBoxW = QSpinBox()
        spinBoxW.setMinimum(1)
        spinBoxW.setSingleStep(2)
        spinBoxW.setValue(3)
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

    def superResolution(self):
        if self.image is not None:
            superResolution(self, self.pixmap)

    def inpainting(self):
        self.painting = True
        self.pixmapBlack = QPixmap(self.pixmap.size())
        self.pixmapBlack.fill(Qt.black)
        self.editToolBarH.clear()
        backColor = QAction(QIcon("icons/highlight.png"),"Change background color",self)
        backColor.triggered.connect(self.changeColor)
        px_7 = QAction('7px',self)
        px_7.triggered.connect(self.changeSize7px)
        px_9 = QAction('9px',self)
        px_9.triggered.connect(self.changeSize9px)
        px_13 = QAction('13px',self)
        px_13.triggered.connect(self.changeSize13px)
        px_17 = QAction('17px',self)
        px_17.triggered.connect(self.changeSize17px)
        px_21 = QAction('21px',self)
        px_21.triggered.connect(self.changeSize21px)
        finish = QAction('OK',self)
        finish.triggered.connect(self.lama)
        self.editToolBarH.addAction(backColor)
        self.editToolBarH.addAction(px_7)
        self.editToolBarH.addAction(px_9)
        self.editToolBarH.addAction(px_13)
        self.editToolBarH.addAction(px_17)
        self.editToolBarH.addAction(px_21)
        self.editToolBarH.addAction(finish)

    def lama(self):
        lama(self, self.pixmap, self.pixmapBlack)
    
    def changeSize7px(self):
        self.brushSize = 7

    def changeSize9px(self):
        self.brushSize = 9

    def changeSize13px(self):
        self.brushSize = 13

    def changeSize17px(self):
        self.brushSize = 17

    def changeSize21px(self):
        self.brushSize = 21


    def mousePressEvent(self, event):
        if self.painting and self.image is not None:
        # if left mouse button is pressed
            if event.button() == Qt.LeftButton:
                # make drawing flag true
                self.drawing = True
                # make last point to the point of cursor
                self.lastPoint = event.pos()

    def mouseMoveEvent(self, event):
        if self.painting and self.image is not None:
            # checking if left button is pressed and drawing flag is true
            if (event.buttons() & Qt.LeftButton) & self.drawing:
                # creating painter object
                painter = QPainter(self.pixmap)
                painterBlack = QPainter(self.pixmapBlack)
                
                # set the pen of the painter
                painter.setPen(QPen(self.brushColor, self.brushSize,
                                Qt.SolidLine, Qt.RoundCap, Qt.RoundJoin))
                painterBlack.setPen(QPen(Qt.white, self.brushSize,
                                Qt.SolidLine, Qt.RoundCap, Qt.RoundJoin))
                
                # draw line from the last point of cursor to the current point
                point1 = self.view.mapToScene(self.lastPoint)
                point2 = self.view.mapToScene(event.pos())
                point3 = QPointF(point1.x() - 1.5*self.dentaY , point1.y() - self.dentaX / 2 - 7)
                point4 = QPointF(point2.x() - 1.5*self.dentaY, point2.y() - self.dentaX / 2 - 7)
                painter.drawLine(point3 , point4)
                painterBlack.drawLine(point3 , point4)
                #self.view.mapToScene(event.pos())
                
                # change the last point
                self.lastPoint = event.pos()
                # update
                self.updateView()

    def mouseReleaseEvent(self, event):
        if self.painting and self.image is not None:
            if event.button() == Qt.LeftButton:
                # make drawing flag false
                self.drawing = False

    def paintEvent(self, event):
        if self.painting and self.image is not None:
        # create a canvas
            canvasPainter = QPainter(self)          
            # draw rectangle  on the canvas
            canvasPainter.drawPixmap(self.rect(), self.pixmap, self.pixmap.rect())

    def updateView(self):
        self.view.repaint()
        self.scene.clear()
        self.scene.addPixmap(self.pixmap)
        # self.pixmap = pixmap

    def changeColor(self):
        color = QColorDialog.getColor()
        self.brushColor = color

    def emboss(self):
        if self.image is not None:
            emboss(self, self.pixmap)

    def boxBlur(self):
        if self.image is not None:
            boxBlur(self, self.pixmap)

    def gaussianBlur(self):
        if self.image is not None:
            gaussianBlur(self, self.pixmap)

    def medianBlur(self):
        if self.image is not None:
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
        self.buttonOpen = self._createToolBar('icons/plus.png', self.openfile, "Ctrl+O")
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
        
    def openfile(self):
        openfile(self)   
        
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


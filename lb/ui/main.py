from PyQt5.QtWidgets import *
from PyQt5.QtGui import *
from PyQt5.QtCore import *
import sys
from actions import *
import cv2
# from PyQt5.QtGui import QMatrix
from customQGraphicsView import customQGraphicsView

class Main(QMainWindow):
    def __init__(self) -> None:
        super().__init__()
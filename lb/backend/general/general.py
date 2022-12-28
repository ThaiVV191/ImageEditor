from PyQt5.QtWidgets import *
from PyQt5.QtGui import *
from PyQt5.QtCore import *
from actions import *

def crop(self):
    if self.buttonCrop.isChecked and self.image is not None:
        self.editToolBarH.clear()
        self.view.activate = True
        button_action = QAction(QIcon("icons/check.png"), "OK", self)
        button_action.triggered.connect(self.buttonClicked)
        left_spacer = QWidget()
        left_spacer.setSizePolicy(QSizePolicy.Expanding, QSizePolicy.Expanding)
        right_spacer = QWidget()
        right_spacer.setSizePolicy(QSizePolicy.Expanding, QSizePolicy.Expanding)
        self.editToolBarH.addWidget(left_spacer)
        self.editToolBarH.addAction(button_action)
        self.editToolBarH.addWidget(right_spacer)
    return self
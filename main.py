from PyQt5.QtWidgets import *
from PyQt5.QtGui import *
from PyQt5.QtCore import *
import sys
from ui import ImageCropper

if __name__ == "__main__":
    app = QApplication(sys.argv)
    win = ImageCropper()
    win.show()
    sys.exit(app.exec_())
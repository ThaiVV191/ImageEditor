import sys
from PyQt5.QtWidgets import QApplication, QGraphicsView, QGraphicsScene, QTextEdit
from PyQt5.QtGui import QImage, QPixmap
from PyQt5.QtCore import Qt

class MouseTrackerView(QGraphicsView):
    def __init__(self, parent=None):
        super().__init__(parent)
        self.setMouseTracking(True)
        self.textedit = None

    def mouseMoveEvent(self, event):
        if self.textedit:
            self.textedit.move(event.pos())

    def mousePressEvent(self, event):
        if event.button() == Qt.LeftButton:
            self.textedit = QTextEdit()
            self.scene().addWidget(self.textedit)
            self.textedit.move(event.pos())
            self.textedit.show()

app = QApplication(sys.argv)

# Load the image
image = QImage("samoyed_puppy_dog_pictures.jpg")

# Create the QGraphicsScene and add the image to it
scene = QGraphicsScene()
scene.addPixmap(QPixmap.fromImage(image))

# Create the QGraphicsView and set the scene
view = MouseTrackerView()
view.setScene(scene)

view.show()

sys.exit(app.exec_())

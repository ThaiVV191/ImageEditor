from PyQt5.QtCore import Qt
from PyQt5.QtGui import QImage, QPixmap, QPainter
from PyQt5.QtWidgets import QGraphicsView, QGraphicsScene, QApplication, QMainWindow
import sys
app = QApplication(sys.argv)
# Load the image
image = QImage("samoyed_puppy_dog_pictures.jpg")

# Create a QGraphicsView widget and set the image as the background
view = QGraphicsView()
view.setScene(QGraphicsScene(view))
view.scene().addPixmap(QPixmap.fromImage(image))
view.setRenderHint(QPainter.SmoothPixmapTransform)
# Set the transformation anchor to the center of the view, so that the image is zoomed in from the center
view.setTransformationAnchor(QGraphicsView.AnchorUnderMouse)

# Set the zoom level to 2 (i.e., the image will be scaled up by a factor of 2)
view.scale(2, 2)

# Show the view
view.show()

# Run the QApplication event loop




# Run the QApplication event loop
sys.exit(app.exec_())

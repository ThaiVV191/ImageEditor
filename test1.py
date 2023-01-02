from PyQt5.QtWidgets import QWidget, QApplication

class MouseReleaseWidget(QWidget):
    def mouseReleaseEvent(self, event):
        # Your code here
        print("Mouse released at position:", event.pos())

def on_mouse_release():
    print("Mouse was released!")

app = QApplication([])
widget = MouseReleaseWidget()
widget.mouseReleaseEvent.connect(on_mouse_release)
widget.show()
app.exec_()

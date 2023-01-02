from PyQt5.QtGui import QPixmap, QPainter, QFont
from PyQt5.QtWidgets import QApplication, QLabel

app = QApplication([])

# Tạo đối tượng QPixmap để lưu trữ hình ảnh
pixmap = QPixmap("samoyed_puppy_dog_pictures.jpg")

# Tạo đối tượng QPainter và gọi hàm begin() trên đối tượng QPixmap
painter = QPainter(pixmap)
painter.begin(pixmap)

# Chèn chữ lên hình ảnh bằng cách gọi hàm drawText() trên đối tượng QPainter
font = QFont("Arial", 16)
painter.setFont(font)
painter.drawText(10, 50, "Hello \n World!")

# Gọi hàm end() để kết thúc quá trình vẽ
painter.end()

# Hiển thị hình ảnh với chữ đã được chèn vào
label = QLabel()
label.setPixmap(pixmap)
label.show()

app.exec_()

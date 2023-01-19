from PyQt5.QtMultimedia import QMediaPlayer, QMediaContent
from PyQt5.QtMultimediaWidgets import QVideoWidget
from PyQt5.QtWidgets import QApplication, QMainWindow
from PyQt5.QtCore import QUrl


app = QApplication([])

player = QMediaPlayer()
player.setMedia(QMediaContent(QUrl.fromLocalFile("SnapSave.io-Telfast Video 10s (Man).mp4")))

video_widget = QVideoWidget()
player.setVideoOutput(video_widget)

video_widget.show()

player.play()
app.exec_()

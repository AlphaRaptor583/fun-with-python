import sys
from PyQt6.QtWidgets import QApplication, QMainWindow, QPushButton, QVBoxLayout, QWidget, QFileDialog
from PyQt6.QtMultimedia import QMediaPlayer, QAudioOutput
from PyQt6.QtMultimediaWidgets import QVideoWidget
from PyQt6.QtCore import QUrl

class MainWindow(QMainWindow):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("PyQt6 Video Player")
        self.setGeometry(100, 100, 800, 600)

        self.mediaPlayer = QMediaPlayer()
        self.videoWidget = QVideoWidget()

        self.openButton = QPushButton("Open Video")
        self.openButton.clicked.connect(self.open_file)

        self.playButton = QPushButton("Play")
        self.playButton.clicked.connect(self.mediaPlayer.play)

        self.pauseButton = QPushButton("Pause")
        self.pauseButton.clicked.connect(self.mediaPlayer.pause)

        self.stopButton = QPushButton("Stop")
        self.stopButton.clicked.connect(self.mediaPlayer.stop)

        layout = QVBoxLayout()
        layout.addWidget(self.videoWidget)
        layout.addWidget(self.openButton)
        layout.addWidget(self.playButton)
        layout.addWidget(self.pauseButton)
        layout.addWidget(self.stopButton)

        container = QWidget()
        container.setLayout(layout)
        self.setCentralWidget(container)

        self.mediaPlayer.setVideoOutput(self.videoWidget)
        self.audioOutput = QAudioOutput()
        self.mediaPlayer.setAudioOutput(self.audioOutput)

    def open_file(self):
        fileName, _ = QFileDialog.getOpenFileName(self, "Open Video")
        if fileName != '':
            self.mediaPlayer.setSource(QUrl.fromLocalFile(fileName))

def main():
    app = QApplication(sys.argv)
    window = MainWindow()
    window.show()
    sys.exit(app.exec())

# Execute the code
main()

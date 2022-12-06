from PyQt5.QtGui import *
from PyQt5.QtWidgets import *
from PyQt5.QtCore import *
from PyQt5.QtMultimedia import *
from PyQt5.QtMultimediaWidgets import *

import os
import sys


class MainWindow(QMainWindow):

    def __init__(self, *args, **kwargs):
        super(MainWindow, self).__init__(*args, **kwargs)

        self.online_webcams = QCameraInfo.availableCameras()
        self.available_webcams = QCamera.availableDevices()
        self.list_available_cameras()
        self.list_online_webcams()
        if not self.online_webcams:
            pass # quit
        self.exist = QCameraViewfinder()
        self.exist.show()
        self.setCentralWidget(self.exist)

        # set the default webcam.
        self.get_webcam(1)
        self.setWindowTitle("WebCam")
        self.show()

    def list_available_cameras(self):
        print("QCamera")
        for camera in self.available_webcams:
            print(QCamera.deviceDescription(camera))

    def list_online_webcams(self):
        print("QCameraInfo")
        for camera in self.online_webcams:
            print(camera.description())

    def get_webcam(self, i):
        self.my_webcam = QCamera(self.online_webcams[i])
        self.recorder = QMediaRecorder(self.my_webcam)
        self.my_webcam.setViewfinder(self.exist)
        self.my_webcam.setCaptureMode(QCamera.CaptureVideo)
        self.my_webcam.error.connect(lambda: self.alert(self.my_webcam.errorString()))
        self.my_webcam.start()

        path = QUrl("")
        self.recorder.setOutputLocation(path)
        self.recorder.record()
        print(self.recorder.actualLocation())

    def alert(self, s):
        """
 This handle errors and displaying alerts.
 """
        err = QErrorMessage(self)
        err.showMessage(s)


if __name__ == '__main__':
    app = QApplication(sys.argv)
    app.setApplicationName("WebCam")

    window = MainWindow()
    app.exec_()
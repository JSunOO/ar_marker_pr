import sys
from PyQt5.QtWidgets import *
from PyQt5 import uic   # ui 파일을 사용하기 위한 모듈 import
from PyQt5.QtMultimedia import *
from PyQt5.QtMultimediaWidgets import *
import os
import sys
import time
import cv2

#UI파일 연결 코드
UI_class = uic.loadUiType("firstwindow.ui")[0]


class MyWindow(QMainWindow, UI_class) :
    def __init__(self) :
        super().__init__()
        self.setupUi(self)
        #self.image = None
        self.size = None
        #self.height_resolution.textChanged.connect(self.change_resolution(self.size))
        #self.width_resolution.textChanged.connect(self.change_resolution(self, self.size))
        #self.resolutionButton.clicked.connect(self.change_resolution)

    def MyVideoCapture(self):
        # Open the video source
        self.webcam = cv2.VideoCapture(0)
        if not self.webcam.isOpened():
            raise ValueError("Unable to open video source")

        # Get video source width and height
        self.width = self.webcam.get(cv2.CAP_PROP_FRAME_WIDTH, 640)
        self.height = self.webcam.get(cv2.CAP_PROP_FRAME_HEIGHT, 480)

        if self.webcam.isOpened():
            ret, frame = self.webcam.read()
            if ret:
                # Return a boolean success flag and the current frame converted to BGR
                return (ret, cv2.cvtColor(frame, cv2.COLOR_BGR2RGB))
            else:
                return (ret, None)
        else:
            return (ret, None)

    # Release the video source when the object is destroyed
    def __del__(self):
        if self.webcam.isOpened():
            self.webcam.release()    
            
    def change_resolution(self, size):
        pass
    
    def open_marker(self):
        pass
    
    def find_marker_in_video(self):
        pass


if __name__ == '__main__':
    app = QApplication(sys.argv) 
    
    Window = MyWindow() 

    Window.show()

    app.exec_()
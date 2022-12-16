from PyQt5.QtWidgets import *
from PyQt5 import uic, QtCore, QtGui, QtWidgets   # ui 파일을 사용하기 위한 모듈 import
from PyQt5.QtMultimedia import *
from PyQt5.QtMultimediaWidgets import *
from PyQt5.QtCore import *  # QTimer
from PyQt5.QtGui import QPixmap, QImage
import os
import sys
import time
import cv2

#UI파일 연결 코드
UI_class = uic.loadUiType("firstwindow.ui")[0]

class MyWindow(QMainWindow, UI_class) :
    #timeout = pyqtSignal()
    def __init__(self) :
        super().__init__()
        self.setupUi(self)
        # QLabel, 비디오 사이즈
        self.size = QSize(800, 600)
        self.resolutionButton.clicked.connect(self.rescale_frame)
        self.set_cam()


    def show_warning(self, title, msg):
        QMessageBox.warning(self, title, msg)         

    def set_cam(self):
        """
            카메라, QLable 사이즈 변경 
            타이머 등록 -> 카메라 읽어서 QLabel에 출력
        """
        # Open the video source
        self.webcam = cv2.VideoCapture(0)
        
        self.vidLabel.setFixedSize(self.size)
        self.webcam.set(cv2.CAP_PROP_FRAME_WIDTH, self.size.width())
        self.webcam.set(cv2.CAP_PROP_FRAME_HEIGHT, self.size.height())
        
        self.timer = QTimer(self)
        self.timer.timeout.connect(self.display_video_stream)
        self.timer.start(30)        


    def display_video_stream(self):
        """
            카메라 열리면 읽어오기 드옭
        """
        ret, frame = self.webcam.read()
        if ret is False:            
            self.timer.stop()
            self.show_warning("카메라", "카메라 장비 없음")            
        else:   
            frame = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
            frame = cv2.flip(frame, 1)
            image = QImage(frame, frame.shape[1], frame.shape[0], 
                frame.strides[0], QImage.Format_RGB888)        
            self.vidLabel.setPixmap(QPixmap.fromImage(image).scaled(self.size, Qt.KeepAspectRatioByExpanding,
                                                              Qt.SmoothTransformation))    

    
    def __del__(self):
        # Release the video source when the object is destroyed
        pass

    # 프레임의 너비와 높이를 재수정
    def rescale_frame(self):
        self.timer.stop()
        
        size_h = int(self.height_resolution.text())
        size_w = int(self.width_resolution.text())
        
        self.size = QSize(size_h, size_w)
        self.set_cam()  

    def open_marker(self):
        pass
    
    def find_marker_in_video(self):
        pass


if __name__ == '__main__':
    app = QApplication(sys.argv) 
    
    Window = MyWindow() 

    Window.show()

    app.exec_()
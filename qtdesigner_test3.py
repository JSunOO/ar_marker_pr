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
        #self.image = None
        self.size = (800, 600)
        #윈도우 크기 재설정
        self.resize(self.size[0], self.size[1])
        #경고창 설정
        btn_warning = QPushButton('Warning')
        btn_warning.clicked.connect(self.warning)
        #해상도 변경 QPushButoon인 resolutionButton에 기능 연결
        self.resolutionButton.clicked.connect(self.rescale_frame)
 


    def warning(self):
        QMessageBox.warning(
            self,
            'Warning',
            'This is a warning message.'
        )         

    def myVideoCapture(self):
        # Open the video source
        self.webcam = cv2.VideoCapture(0)
        ret, frame = self.webcam.read()
        while(self.webcam.isOpened()):
            ret, frame = self.webcam.read()
    
            # check for successfulness of cap.read()
            if ret:

                rescaled_frame=self.rescale_frame(self, frame)
                self.timer = QTimer(self)
                self.timer.timeout.connect(self.display_video_stream)
                self.start(30)

            else:
                break            
    
            cv2.imshow('frame',rescaled_frame)
            if cv2.waitKey(1) & 0xFF == ord('q'):
                break
    
        self.webcam.release()
        #cv2.destroyAllWindows()

    def display_video_stream(self):
    #Read frame from camera and repaint QLabel widget.
        _, frame = self.webcam.read()
        frame = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
        frame = cv2.flip(frame, 1)
        image = QImage(frame, frame.shape[1], frame.shape[0], 
            frame.strides[0], QImage.Format_RGB888)        
        self.vidLabel.setPixmap(QPixmap.fromImage(image))    


    # Release the video source when the object is destroyed
    def __del__(self):
        if self.webcam.isOpened():
            self.webcam.release()    

    # 프레임의 너비와 높이를 재수정
    def rescale_frame(self, frame):
        size_h = (self.height_resolution.text())
        size_w = (self.width_resoluiton.text())
        height = int(frame.shape[0]*0 + size_h)
        width = int(frame.shape[1]*0 + size_w)
        dim = (width, height)
        return cv2.resize(frame, dim, interpolation =cv2.INTER_AREA)

    def open_marker(self):
        pass
    
    def find_marker_in_video(self):
        pass


if __name__ == '__main__':
    app = QApplication(sys.argv) 
    
    Window = MyWindow() 

    Window.show()

    app.exec_()
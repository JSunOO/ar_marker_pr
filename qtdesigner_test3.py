import sys
from PyQt5.QtWidgets import *
from PyQt5 import uic, QtCore, QtGui, QtWidgets   # ui 파일을 사용하기 위한 모듈 import
from PyQt5.QtMultimedia import *
from PyQt5.QtMultimediaWidgets import *
from PyQt5.QtGui import QPixmap, QImage
import os
import sys
import time
import cv2
import threading


#UI파일 연결 코드
UI_class = uic.loadUiType("firstwindow.ui")[0]


class MyWindow(QMainWindow, UI_class) :
    def __init__(self) :
        super().__init__()
        self.setupUi(self)
        #self.image = None
        #self.size = None

    def Video_to_frame(self):

        cap = cv2.VideoCapture(0) #저장된 영상 가져오기 프레임별로 계속 가져오는 듯

        ###cap으로 영상의 프레임을 가지고와서 전처리 후 화면에 띄움###
        while True:
            self.ret, self.frame = cap.read() #영상의 정보 저장
            if self.ret:
                self.rgbImage = cv2.cvtColor(self.frame, cv2.COLOR_BGR2RGB) #프레임에 색입히기
                self.convertToQtFormat = QImage(self.rgbImage.data, self.rgbImage.shape[1], self.rgbImage.shape[0],
                                                QImage.Format_RGB888)

                self.pixmap = QPixmap(self.convertToQtFormat)
                self.p = self.pixmap.scaled(400, 300, QtCore.Qt.IgnoreAspectRatio) #프레임 크기 조정

                self.video_viewer_label.setPixmap(self.p)
                self.video_viewer_label.update() #프레임 띄우기

                sleep(0.01)  # 영상 1프레임당 0.01초로 이걸로 영상 재생속도 조절하면됨 0.02로하면 0.5배속인거임

            else:
                break

        cap.release()
        cv2.destroyAllWindows()

    # video_to_frame을 쓰레드로 사용
    #이게 영상 재생 쓰레드 돌리는거 얘를 조작하거나 함수를 생성해서 연속재생 관리해야할듯
    def video_thread(self):
        thread = threading.Thread(target=self.Video_to_frame, args=(self,))
        thread.daemon = True  # 프로그램 종료시 프로세스도 함께 종료 (백그라운드 재생 X)
        thread.start()


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
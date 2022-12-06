from PyQt5 import QtWidgets, QtGui
from PyQt5.QtGui import QImage, QPixmap
from PyQt5.QtCore import Qt, QThread, pyqtSignal,QCoreApplication, pyqtSlot
#from PyQt5.QtWidgets import QComboBox
import cv2
import sys

#1
class VideoWorker(QThread):
#1-1    
    send_qimage = pyqtSignal(QImage) #QImage 영상을 전달할 객체
#1-2    
    def __init__(self, parent, source=0):
        super(VideoWorker, self).__init__(parent)
        self.parent = parent
        self.source = source
        self.cap = cv2.VideoCapture(self.source)
        fw = cv2.CAP_PROP_FRAME_WIDTH
        fh = cv2.CAP_PROP_FRAME_HEIGHT
        self.width = self.cap.get(fw)
        self.height = self.cap.get(fh)
#1-3 ret=True일때 프레임을 QIMage영상인 qmig로 변환 -> self.send_qimage.emit(qimg)로 영상 전달
    def run(self):
        ret, frame = self.cap.read()
        if ret:
            self.stopped = False
        else:
            self.stopped = True

        H, W, C = frame.shape # 각각 frame의 높이, 너비, 채널(색상)을 의미
        bytesPerLine = W*C
        while not self.stopped:
            ret, frame =self.cap.read()
            if ret:
                frame = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
                qimg = QImage(frame.data.tobytes(), W, H, bytesPerLine, QtGui.QImage.Format_RGB888)
                self.send_qimage.emit(qimg)
            else:
                self.stopped = True
        self.cap.release()

    def make_320p(self):
        self.cap.set(3, 320)
        self.cap.set(4, 240)
        #return self.webcam      

    def make_480p(self):
        self.cap.set(3, 480) 
        self.cap.set(4, 320)
        #return self.webcam

    def make_640p(self):
        self.cap.set(3, 640)
        self.cap.set(4, 480)
        #return self.webcam

    def make_960p(self):
        self.cap.set(3, 960)
        self.cap.set(4, 640)
        #return self.webcam
        self.cap.set(cv2.CAP_PROP_FRAME_WIDTH, (int(self.width)))
        self.cap.set( cv2.CAP_PROP_FRAME_HEIGHT, (int(self.height)))
       

#2
class VideoWindow(QtWidgets.QWidget):
#2-1 
    def __init__(self, source=0): #웹캠을 이용하기 위해 1로 설정한다. 단, 출력하는데 시간이 조금 걸린다.
        super().__init__()
        self.title = 'OpenCV VideoCam'
        self.mode = 'RGB'
        self.source = source
        self.initUI() # UI를 생성하고 초기화
#2-2
    @pyqtSlot(QImage) # 이 데코레이터는 displatImage메서드가 #1-1의 send_qimage신호를 받을 메서드임을 표시
    def displatImage(self, image):
        if self.mode == 'GRAY':
            image = image.convertToFormat(QImage.Format_Grayscale8)
        
        self.image = image
        self.label.setPixmap(QPixmap.fromImage(image))

#해상도 조절
#    def switchframe():

#2-3
    def initUI(self):
        self.setWindowTitle(self.title)
        self.resize(800, 600)
        
        self.vid = VideoWorker(self)

        self.label = QtWidgets.QLabel()
        self.label.resize(640, 480)
        self.label.setScaledContents(True)

        self.btn1 = QtWidgets.QPushButton('RGB')
        self.btn2 = QtWidgets.QPushButton('GRAY')
        self.btn3 = QtWidgets.QPushButton('Quit')
        self.cb = QtWidgets.QComboBox(self)
        self.cb.addItem('320p')
        self.cb.addItem('480p')
        self.cb.addItem('640p')
        self.cb.addItem('960p')
        self.btn2.setEnabled(False)

        layout = QtWidgets.QVBoxLayout()

        layout.addWidget(self.label)
        layout.addWidget(self.btn1)
        layout.addWidget(self.btn2)
        layout.addWidget(self.btn3)
        layout.addWidget(self.cb)
        self.setLayout(layout)

        self.btn1.clicked.connect(self.toRGB)
        self.btn2.clicked.connect(self.toGray)
        self.btn3.clicked.connect(QCoreApplication.instance().quit)
        #self.cb.activated['320p'].connect(self.vid.make_320p)

        self.thread = VideoWorker(self, self.source)
        self.thread .send_qimage.connect(self.displatImage) # 1-3에서 self.send_qimage.emit(qimg)로 보낸 신호를 받을 스레드를 설정
        self.thread .start() # 1-3의 스레드 run() 메서드가 실행

#2-4
    def toGray(self):
        self.mode = 'GRAY'
        self.btn1.setEnabled(True)
        self.btn2.setEnabled(False)

    def toRGB(self):
        self.mode = 'RGB'
        self.btn1.setEnabled(False)
        self.btn2.setEnabled(True)

    def closeEvent(self, event): #윈도우 종료 이벤트 재정의 -> 메세지박스로 종료 여부를 다시 확인
        close = QtWidgets.QMessageBox.question(self, 'MSG', 'Are you sure?', 
                          QtWidgets.QMessageBox.Yes | \
                          QtWidgets.QMessageBox.No)
        if close == QtWidgets.QMessageBox.Yes:
            event.accept()
        else:
            event.ignore()

    def keyPressEvent(self, event):
        if event.key() ==Qt.Key_Escape:
            self.stopped = True
            self.close()

#3
if __name__=='__main__':
    app = QtWidgets.QApplication([])
    window = VideoWindow()
    window.show()
    sys.exit(app.exec_())
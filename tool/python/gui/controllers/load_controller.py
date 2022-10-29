from PyQt5 import QtWidgets, uic, QtCore, QtGui
from PyQt5.QtGui import *
from util.utils import join


UI_Window, UI_BASE = uic.loadUiType(join("gui","views","loading.ui", uplevel=2))
class LoadScreen(QtWidgets.QMainWindow, UI_Window):
    finished = QtCore.pyqtSignal()
    def __init__(self):
        QtWidgets.QMainWindow.__init__(self)
        self.setupUi(self)
        self.load_img = QtGui.QPixmap(join("gui","images","loading.png", uplevel=2))
        self.finished.connect(self.on_finish)
        self.rectF = QtCore.QRectF(0, 0, 100, 100)
        self.rotation()
        
           
    def rotation(self):
        self.animation = QtCore.QVariantAnimation(self)
        self.animation.setStartValue(QtCore.QVariant(360))
        self.animation.setEndValue(QtCore.QVariant(0))
        self.animation.setDuration(5000)
        self.animation.finished.connect(self.rotation)
        self.animation.start(QtCore.QAbstractAnimation.DeleteWhenStopped)
        self.animation.valueChanged.connect(self.rot)
    
      
    def on_finish(self):
        self.animation.stop()
        self.hide()       
        
        
    def rot(self, angle: QtCore.QVariant):
        pix = QPixmap(102, 102)
        painter = QPainter(pix)
        painter.translate(self.rectF.center())
        painter.rotate(angle)
        painter.translate(-self.rectF.center())
        painter.drawPixmap(0, 0, self.load_img)
        painter.end()
        self.load_wheel.setPixmap(pix)
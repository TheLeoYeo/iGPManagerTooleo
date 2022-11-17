from PyQt5.QtCore import *
from PyQt5.QtGui import *
from PyQt5.QtWidgets import *


class ConfirmButton(QPushButton):
    def __init__(self, *args, **kwargs):
        QPushButton.__init__(self, *args, **kwargs)
        self.setCursor(QCursor(Qt.PointingHandCursor))
        self.setMaximumSize(100, 30)


class RejectButton(QPushButton):
    def __init__(self, *args, **kwargs):
        QPushButton.__init__(self, *args, **kwargs)
        self.setCursor(QCursor(Qt.PointingHandCursor))
        self.setMaximumSize(100, 30)
        
class DefaultButton(QPushButton):
    pass
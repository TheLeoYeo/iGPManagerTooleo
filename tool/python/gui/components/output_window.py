from PyQt5.QtCore import *
from PyQt5.QtGui import *
from PyQt5.QtWidgets import *

from igp.util.tools import Output


class OutputWindow(QFrame):   
    def __init__(self, parent:QFrame=None):
        QFrame.__init__(self, parent, objectName="output_window")
        self.setupUi()
        Output.add_listener(self)
        self.hide()
    
    
    def setupUi(self):
        self.setCursor(QCursor(Qt.PointingHandCursor))
        layout = QHBoxLayout()
        layout.setAlignment(Qt.AlignRight)
        layout.addStretch(1)
             
        self.output = QLabel()
        self.output.setWordWrap(False)
        self.output.setObjectName("output")
        self.output.setAlignment(Qt.AlignCenter)
        layout.addWidget(self.output)
        self.setLayout(layout)
    
    
    def handle(self, message:str):
        self.output.setText(message)
        self.setToolTip(message)
        self.adjustSize()
        self.show()

  
    def mousePressEvent(self, e) -> None:
        self.hide()
    
    
    def enterEvent(self, e) -> None:
        self.setStyleSheet("#output{background-color:rgba(35, 35, 35, 0.4);}")


    def leaveEvent(self, e) -> None:
        self.setStyleSheet("#output {background-color:rgb(50, 50, 50);}")

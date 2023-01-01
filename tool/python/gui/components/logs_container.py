from PyQt5.QtCore import *
from PyQt5.QtGui import *
from PyQt5.QtWidgets import *

from gui.components.container import Container


class LogsContainer(Container):
    sequence:list = []
    
    def __init__(self, *args, **kwargs):
        Container.__init__(self, *args, **kwargs)
        self.text = QLabel()
        self.text.setStyleSheet("padding:0px 6px; background-color:rgb(35, 35, 35)")
        self.text.setWordWrap(True)
        self.cont.layout().addWidget(self.text)
             
        
    def set_text(self, text:str):
        self.text.setText(text)
        self.text.adjustSize()
        self.adjustSize()
        
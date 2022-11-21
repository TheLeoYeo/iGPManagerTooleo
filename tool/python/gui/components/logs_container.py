from PyQt5.QtCore import *
from PyQt5.QtGui import *
from PyQt5.QtWidgets import *

from gui.components.container import Container
from gui.components.row import BaseRow, RowDropDown, parent
from gui.components.modifier_window import ModifierWidget
from igp.util.tools import log_dir


class LogsContainer(Container):
    sequence:list = []
    
    def __init__(self, *args, **kwargs):
        Container.__init__(self, *args, **kwargs)
        self.text = QLabel()
        self.text.setStyleSheet("padding:6px")
        self.text.setWordWrap(True)
        self.cont.layout().addWidget(self.text)
             
        
    def set_text(self, text:str):
        self.text.setText(text)
        
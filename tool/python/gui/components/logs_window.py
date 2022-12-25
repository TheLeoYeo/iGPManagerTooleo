from PyQt5.QtCore import *
from PyQt5.QtGui import *
from PyQt5.QtWidgets import *

from gui.components.buttons import *
from gui.components.logs_container import LogsContainer
from igp.util.tools import LOGDIR



class LogsWindow(QFrame):
    def __init__(self, parent:QFrame=None):
        QFrame.__init__(self, parent, objectName=f"logs_window")
        self.setupUi()
        self.update_text()
        self.hide()
        
    '''
    def mousePressEvent(self, e) -> None:
        self.hide()
    
    
    def enterEvent(self, e) -> None:
        self.setStyleSheet("LogsWindow{background-color:rgb(35, 35, 35);}")


    def leaveEvent(self, e) -> None:
        self.setStyleSheet("LogsWindow{background-color:rgb(50, 50, 50);}")'''
    
    
    def setupUi(self):
        layout = QVBoxLayout()
        
        self.setGeometry(QRect(180, 20, 400, 400))

        self.setMaximumWidth(400)
        self.setMaximumHeight(300)
        
        self.close_button = RejectButton()
        self.close_button.setText("X")
        self.close_button.pressed.connect(self.hide)
        layout.addWidget(self.close_button, alignment=Qt.AlignRight)
        
        self.container = LogsContainer()
        layout.addWidget(self.container)
        
        self.confirm_window = ConfirmWindow(self.parent(), self.clear_logs, "Are you sure you want to clear the logs?")
        self.clear_button = RejectButton()
        self.clear_button.setText("Clear")
        self.clear_button.pressed.connect(self.confirm_window.show)
        layout.addWidget(self.clear_button, alignment=Qt.AlignHCenter)
             
        self.setLayout(layout)
        
        
    def show(self):
        super().show()
        self.update_text()
        self.setStyleSheet("LogsWindow{background-color:rgb(50, 50, 50);}")
    
    
    def update_text(self):
        message = ""
        with open(LOGDIR, "r") as log_file:
            lines = log_file.readlines()
            lines.reverse()
            for line in lines:
                message += line
        
        self.container.set_text(message)
        
        
    def clear_logs(self):
        open(LOGDIR, "w").close()
        self.confirm_window.hide()
        self.update_text()
        

class ConfirmWindow(QFrame):
    def __init__(self, parent:QFrame=None, func=None, message="Are you sure?"):
        QFrame.__init__(self, parent, objectName=f"confirm_window")
        self.message = message
        self.func = func
        self.setupUi()
        self.hide()
        
    def setupUi(self):
        self.setGeometry(QRect(300, 170, 200, 150))
        layout = QVBoxLayout()
        self.text = QLabel(self.message)
        self.text.setWordWrap(True)
        self.text.setAlignment(Qt.AlignHCenter)
        layout.addWidget(self.text, alignment=Qt.AlignHCenter)
        
        self.confirm = ConfirmButton()
        self.confirm.setText("Yes")
        self.confirm.pressed.connect(self.func)
        layout.addWidget(self.confirm, alignment=Qt.AlignHCenter)
        
        self.close = RejectButton()
        self.close.setText("No")
        self.close.pressed.connect(self.hide)
        layout.addWidget(self.close, alignment=Qt.AlignHCenter)
        
        self.setLayout(layout)
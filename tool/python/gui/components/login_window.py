from PyQt5.QtCore import *
from PyQt5.QtGui import *
from PyQt5.QtWidgets import *

from gui.components.buttons import *
from igp.service.accounts import AccountIterator
from igp.service.igpaccount import IGPaccount
from igp.util.exceptions import LoginDetailsError
from igp.util.tools import output


class LoginWindow(QFrame):
    def __init__(self, parent:QFrame=None):
        QFrame.__init__(self, parent, objectName=f"login_window")
        self.setupUi()
        self.hide()
        
        
    def mouseMoveEvent(self, e) -> None:
        if e.buttons() == Qt.LeftButton:
            drag = QDrag(self)
            mime = QMimeData()
            drag.setMimeData(mime)
            drag.exec_(Qt.MoveAction)
    
    
    def setupUi(self):
        layout = QVBoxLayout()
        
        self.setGeometry(QRect(200, 80, 220, 300))
        sizePolicy = QSizePolicy(QSizePolicy.Expanding, QSizePolicy.Expanding)

        self.setMaximumHeight(220)
        sizePolicy.setHeightForWidth(self.sizePolicy().hasHeightForWidth())
        self.setSizePolicy(sizePolicy)
        
        formlayout = QFormLayout()
        formlayout.setAlignment(Qt.AlignTop)
        formlayout.setObjectName("formLayout")
        formlayout.setContentsMargins(10, 10, 10, 10)
        
        self.username = QLabel(self)
        self.username.setText("Email: ")
        self.username.setObjectName("username")
        self.username.setAlignment(Qt.AlignCenter)

        formlayout.setWidget(0, QFormLayout.LabelRole, self.username)

        self.username_inp = QLineEdit(self)
        self.username_inp.setObjectName("textEdit")
        self.username_inp.setStyleSheet("background-color:white;")

        formlayout.setWidget(0, QFormLayout.FieldRole, self.username_inp)

        self.password_inp = QLineEdit(self)
        self.password_inp.setObjectName("textEdit_2")
        self.password_inp.setStyleSheet("background-color:white;")

        formlayout.setWidget(1, QFormLayout.FieldRole, self.password_inp)

        self.password = QLabel(self)
        self.password.setText("Password: ")
        self.password.setAlignment(Qt.AlignCenter)
        self.password.setObjectName("password")

        formlayout.setWidget(1, QFormLayout.LabelRole, self.password)
        layout.addLayout(formlayout)
        
        self.add_account = ConfirmButton()
        self.add_account.setText("add")
        self.add_account.pressed.connect(self.add_account_func)
        layout.addWidget(self.add_account, alignment=Qt.AlignHCenter)
        
        self.close = RejectButton()
        self.close.setText("close")
        self.close.pressed.connect(self.hide)
        layout.addWidget(self.close, alignment=Qt.AlignHCenter)
        
        self.setLayout(layout)
        
        
    def add_account_func(self):
        instance = AccountIterator.get_instance()
        try:
            account = IGPaccount(self.username_inp.text(), self.password_inp.text())
            instance.add_account(account)
        except LoginDetailsError:
            output("DETAILS EMPTY OR INCLUDE ; OR \\")

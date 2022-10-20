from PyQt5 import QtWidgets, uic
from PyQt5.QtCore import *
from PyQt5.QtGui import *
from PyQt5.QtWidgets import *

from igp.service.base_igp_account import BaseIGPaccount
from util.utils import join

class ConfirmButton(QtWidgets.QPushButton):
    pass

class RejectButton(QtWidgets.QPushButton):
    pass

class DefaultButton(QtWidgets.QPushButton):
    pass
        
class Heading(QtWidgets.QLabel):
    pass

class Text(QtWidgets.QCheckBox):
    pass


BaseLine, UI_BASE = uic.loadUiType(join("gui","views","rowSep.ui", uplevel=2))
class RowSep(QtWidgets.QFrame, BaseLine):
    def __init__(self, parent):
        QtWidgets.QFrame.__init__(self, parent)
        BaseLine.__init__(self)
        self.setupUi(self)
        self.line.setStyleSheet("""
                                background-color:rgb(70, 70, 70);
                                margin: 0px 5px;""")
        
    def aline(parent):
        return RowSep(parent).line


class DetailRow(QtWidgets.QFrame):
    selected = False
    account:BaseIGPaccount = None
    count = 0
    
    def __init__(self, account:BaseIGPaccount=None, parent:QtWidgets.QFrame=None):
        QtWidgets.QFrame.__init__(self, parent, objectName=f"detailrow{DetailRow.count}")
        self.setupUi()
        
        if account:
            self.account = account
            self.rowName.setText(account.username)
        self.show()
    
    def paintEvent(self, a0: QPaintEvent) -> None:
        if self.selected:
            self.setStyleSheet("background-color:rgb(100, 100, 255);")
        return super().paintEvent(a0)

    def setupUi(self):
        DetailRow.count += 1
        self.setGeometry(QRect(50, 210, 141, 41))
        sizePolicy = QSizePolicy(QSizePolicy.Expanding, QSizePolicy.Preferred)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.sizePolicy().hasHeightForWidth())
        self.setSizePolicy(sizePolicy)
        
        layout = QHBoxLayout()
        layout.setSpacing(0)
        layout.setObjectName(u"horizontalLayout")
        layout.setSizeConstraint(QLayout.SetMaximumSize)
        layout.setContentsMargins(0, 0, 0, 0)
        
        self.rowName = QLabel()
        self.rowName.setObjectName(u"rowName")
        sizePolicy1 = QSizePolicy(QSizePolicy.Expanding, QSizePolicy.Minimum)
        sizePolicy1.setHorizontalStretch(0)
        sizePolicy1.setVerticalStretch(0)
        sizePolicy1.setHeightForWidth(self.rowName.sizePolicy().hasHeightForWidth())
        self.rowName.setSizePolicy(sizePolicy1)
        self.rowName.setMaximumSize(QSize(16777215, 200))
        self.rowName.setAlignment(Qt.AlignLeading|Qt.AlignLeft|Qt.AlignVCenter)

        layout.addWidget(self.rowName)

        self.row_dropdown = QLabel()
        self.row_dropdown.setObjectName(u"row_dropdown")
        self.row_dropdown.setMaximumSize(QSize(20, 20))
        self.row_dropdown.setPixmap(QPixmap(join("gui","images","dropdown.png", uplevel=2)))
        self.row_dropdown.setScaledContents(True)

        layout.addWidget(self.row_dropdown)
        layout.setStretch(0, 1)
        self.setLayout(layout)
        
    def mousePressEvent(self, e) -> None:
        self.selected = not self.selected
        if self.selected:
            self.setStyleSheet("background-color:rgb(100, 100, 255);")
        else:
            self.setStyleSheet("background-color:none;")
        



class Container(QtWidgets.QFrame):
    rows = []
    noRows:bool = True
    def add_rows(self, accounts:list[BaseIGPaccount]=None):  
        if accounts:
            for account in accounts:
                self.add_row(account)
        
        
    def add_row(self, account:BaseIGPaccount):       
        row = DetailRow(account, self)
            
        if not self.noRows:
            self.layout().addWidget(RowSep.aline(self))
        
        self.layout().addWidget(row)      
        self.noRows = False
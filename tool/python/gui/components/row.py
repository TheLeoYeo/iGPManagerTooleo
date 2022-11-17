from PyQt5 import uic
from PyQt5.QtCore import *
from PyQt5.QtGui import *
from PyQt5.QtWidgets import *

from util.utils import join


BaseLine, UI_BASE = uic.loadUiType(join("gui","views","rowSep.ui", uplevel=2))
class RowSep(QFrame, BaseLine):
    def __init__(self, parent):
        QFrame.__init__(self, parent)
        BaseLine.__init__(self)
        self.setupUi(self)
        self.line.setStyleSheet("""
                                background-color:rgb(70, 70, 70);
                                margin: 0px 5px;""")
        
    def aline(parent):
        return RowSep(parent).line
    

def parent(object, levels = 1):
    if levels == 0:
        return object
    return parent(object.parent(), levels-1)


class RowDropDown(QLabel):
    inside = False
    DEF_STYLES = "RowDropDown{padding: 6px;"
    END = "}"
    
    def __init__(self, *args, **kwargs):
        QLabel.__init__(self, *args, **kwargs)
        self.setStyleSheet(f"{self.DEF_STYLES}{self.END}")
        self.object = None
    
    
    def mousePressEvent(self, e) -> None:
        self.setStyleSheet(f"{self.DEF_STYLES}background-color:rgba(200, 200, 200, 0.3);{self.END}")
        self.select_event()
    
    
    def select_event(self):
        pass
    
            
    def mouseReleaseEvent(self, e) -> None:
        self.setStyleSheet(f"{self.DEF_STYLES}background-color:none;{self.END}")
        if self.inside:
            self.enterEvent(e)
    
    
    def enterEvent(self, e) -> None:
        self.inside = True
        self.setStyleSheet(f"{self.DEF_STYLES}background-color:rgba(20,20,20,0.5);{self.END}")
        
        
    def leaveEvent(self, e) -> None:
        self.inside = False
        self.setStyleSheet(f"{self.DEF_STYLES}background-color:none;{self.END}")
        
        
class BaseRow(QFrame):
    selected = False
    inside = False
    object = None
    count = 0
    
    def __init__(self, object=None, parent:QFrame=None):
        QFrame.__init__(self, parent, objectName=f"baserow{BaseRow.count}")
        BaseRow.count += 1
        self.setupUi()
        
        if object:
            self.object = object
            self.select_if_it_was_selected(object)
            self.row_name.setText(object.__str__())
            self.row_name.setWordWrap(False)
            self.row_name.setStyleSheet("padding-left: 6px")
            self.set_second_column(object)
            self.setToolTip(object.help())
        

    def setupUi(self):
        self.setCursor(QCursor(Qt.PointingHandCursor))
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
        
        self.row_name = QLabel()
        self.row_name.setObjectName(u"rowName")
        sizePolicy1 = QSizePolicy(QSizePolicy.Expanding, QSizePolicy.Minimum)
        sizePolicy1.setHorizontalStretch(0)
        sizePolicy1.setVerticalStretch(0)
        sizePolicy1.setHeightForWidth(self.row_name.sizePolicy().hasHeightForWidth())
        self.row_name.setSizePolicy(sizePolicy1)
        self.row_name.setMaximumSize(QSize(16777215, 200))
        self.row_name.setAlignment(Qt.AlignLeading|Qt.AlignLeft|Qt.AlignVCenter)
        layout.addWidget(self.row_name)

        self.create_second_column(layout)         
        
        layout.setStretch(0, 1)
        self.setLayout(layout)
        
        
    def create_second_column(self, layout:QHBoxLayout):
        self.row_dropdown = self.new_drop_down()
        self.row_dropdown.setObjectName(u"row_dropdown")
        self.row_dropdown.setMaximumSize(QSize(30, 30))
        self.row_dropdown.setPixmap(QPixmap(join("gui","images","dropdown.png", uplevel=2)))
        self.row_dropdown.setScaledContents(True)
        layout.addWidget(self.row_dropdown)
    
    
    def new_drop_down(self) -> RowDropDown:
         return RowDropDown(self)
        
        
    def set_second_column(self, object):
        pass
   
        
    def load_updates(self):
        self.row_name.setText(self.object.__str__())
        self.setToolTip(self.object.help())
        
    
    def mousePressEvent(self, e) -> None:
        self.selected = not self.selected
        self.selected_event()
        if self.selected:
            self.setStyleSheet("BaseRow{background-color:rgb(100, 100, 255);}")
        else:
            self.setStyleSheet("BaseRow{background-color:none;}")
    
    
    def enterEvent(self, e) -> None:
        self.inside = True
        if not self.selected:
            self.setStyleSheet("BaseRow{background-color:rgba(35,35,35,0.5);}")


    def leaveEvent(self, e) -> None:
        self.inside = False
        if not self.selected:
            self.setStyleSheet("BaseRow{background-color:none;}")
    
    def selected_event(self):
        pass
    
    def select_if_it_was_selected(self, object):
        pass

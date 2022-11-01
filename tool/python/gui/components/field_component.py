from PyQt5.QtWidgets import *
from PyQt5.QtGui import *
from PyQt5.QtCore import *

from igp.service.modifier.modifier import *
from util.utils import join


def field_to_component(parent, field:Field):
    if isinstance(field, IntegerField):
        return IntegerComponent(parent, field)
    
    elif isinstance(field, OptionField):
        return OptionComponent(parent, field)


class FieldComponent():
    def __init__(self, field):
        self.field:Field = field
        self.setMaximumHeight(30)


class IntegerComponent(FieldComponent, QLineEdit):
    def __init__(self, parent, field):
        QLineEdit.__init__(self, parent)
        FieldComponent.__init__(self, field)
        self.setMaximumWidth(80)
        self.update_text()
        self.editingFinished.connect(self.update_value)
        
        
    def update_text(self):
        self.setText(self.field.value.__str__())
        
        
    def update_value(self):
        self.field.value=self.text()


class OptionComponent(FieldComponent, QFrame):
    def __init__(self, parent, field:OptionField):
        QFrame.__init__(self, parent)
        FieldComponent.__init__(self, field)
        layout = QHBoxLayout(self)
        layout.setContentsMargins(0,0,0,0)
        self.setMaximumHeight(30)
        self.setLayout(layout)
        
        left = self.add_button(ButtonType.LEFT)
        left.on_click = self.decrement
        
        self.option = QLabel(self)
        self.update_value()
        layout.addWidget(self.option)
        
        right = self.add_button(ButtonType.RIGHT)
        right.on_click = self.increment
        
    
    def update_value(self):
        self.option.setText(self.field.value_of().name.lower())
        
        
    def add_button(self, type):
        button = FieldButton(self.parent(), type)
        self.layout().addWidget(button)
        return button
    
    
    def decrement(self):
        self.field.decrement()
        self.update_value()
    
    
    def increment(self):
        self.field.increment()
        self.update_value()


class ButtonType(Enum):
    LEFT = 0
    RIGHT = 1


class FieldButton(QLabel):
    inside = False
    DEF_STYLES = "FieldButton{padding:6px;"
    END = "}"
    
    def __init__(self, parent, type:ButtonType):
        QLabel.__init__(self, parent)
        self.setCursor(QCursor(Qt.PointingHandCursor))
        self.setStyleSheet(f"{self.DEF_STYLES}{self.END}")
        self.setObjectName(u"button")
        self.setMaximumSize(QSize(30, 30))
        self.setPixmap(QPixmap(join("gui","images",f"{type.name.lower()}.png", uplevel=2)))
        self.setScaledContents(True)
        
        
    def on_click():
        pass
    
    
    def mousePressEvent(self, e) -> None:
        self.setStyleSheet(f"{self.DEF_STYLES}background-color:rgba(200, 200, 200, 0.3);{self.END}")
        self.on_click()
            
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
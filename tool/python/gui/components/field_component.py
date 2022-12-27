from PyQt5.QtWidgets import *
from PyQt5.QtGui import *
from PyQt5.QtCore import *

from igp.service.modifier.modifier import *
from util.utils import join


def field_to_component(parent, field:Field):
    if isinstance(field, IntegerField) or isinstance(field, TextField):
        return TextComponent(parent, field)
    
    elif isinstance(field, NumberOfStintsField):
        return NumberOfStintsComponent(parent, field)
    
    elif isinstance(field, OptionField):
        return OptionComponent(parent, field)
    
    elif isinstance(field, TyresField):
        return TyresComponent(parent, field)
    
    elif isinstance(field, StintsField):
        return StintsComponent(parent, field)


class FieldComponent():
    def __init__(self, field):
        self.field:Field = field
        self.setMaximumHeight(30)


class TextComponent(FieldComponent, QLineEdit):
    def __init__(self, parent, field):
        QLineEdit.__init__(self, parent)
        FieldComponent.__init__(self, field)
        if isinstance(field, TextField):
            self.setMaximumWidth(120)
        else:    
            self.setMaximumWidth(80)
        self.setMinimumWidth(20)
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
    
    def __init__(self, parent, type:ButtonType=None):
        QLabel.__init__(self, parent)
        self.setCursor(QCursor(Qt.PointingHandCursor))
        self.setStyleSheet(f"{self.DEF_STYLES}{self.END}")
        self.setObjectName(u"button")
        self.setMaximumSize(QSize(30, 30))
        if not type:
            type = ButtonType.LEFT
            
        self.setPixmap(QPixmap(join("gui","images",f"{type.name.lower()}.png", uplevel=2)))
        self.setScaledContents(True)
        
    def reset_pixmap(self, type:ButtonType):
        self.setPixmap(QPixmap(join("gui","images",f"{type.name.lower()}.png", uplevel=2)))
        
        
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
        
        
class TyreButton(FieldButton):
    field:TyresField = None
    
    def __init__(self, parent, field:TyresField, index, type:Tyres=Tyres.SUPERSOFT):
        if not type:
            type = Tyres.SUPERSOFT
        FieldButton.__init__(self, parent, type)
        self.field = field
        self.index = index
    
    def on_click(self):
        self.field.increment(self.index)
        self.reset_pixmap(self.field.value_of_index(self.index))


class TyresComponent(FieldComponent, QFrame):
    field:TyresField = None
       
    def __init__(self, parent, field:TyresField):
        QFrame.__init__(self, parent)
        FieldComponent.__init__(self, field)
        layout = QHBoxLayout(self)
        layout.setContentsMargins(0,0,0,0)
        self.setMaximumHeight(30)
        self.setLayout(layout)
        
        self.tyres:list[FieldButton] = []
        NumberOfStintsComponent.lastcomponent.tyre_component = self
                   
        for index, type in enumerate(self.field.value_of()):
            self.add_button(index, type)
            
            
    def add_button(self, index, type=None):
        button = TyreButton(self.parent(), self.field, index, type)
        self.layout().addWidget(button)
        self.tyres.append(button)
        return button

        
    def update_value(self):
        for index, type in enumerate(self.field.value_of()):
            self.tyres[index].reset_pixmap(type)
        
        
    def add_stint(self):
        self.add_button(len(self.tyres))
        self.update_value()
       
        
    def remove_stint(self):
        last = self.tyres[-1]
        self.layout().removeWidget(last)
        self.tyres.pop()
        

class StintsComponent(FieldComponent, QFrame):
    field:StintsField = None
    
    def __init__(self, parent, field:StintsField):
        QFrame.__init__(self, parent)
        FieldComponent.__init__(self, field)
        layout = QHBoxLayout(self)
        layout.setContentsMargins(0,0,0,0)
        self.setMaximumHeight(30)
        self.setLayout(layout)
        
        self.stints:list[TextComponent] = []
        NumberOfStintsComponent.lastcomponent.stints_component = self
        
               
        for field in self.field.value:
            self.add_component(field)
    
    
    def add_component(self, field):
        stint = TextComponent(self, field)
        self.layout().addWidget(stint)
        self.stints.append(stint)
    
    
    def update_value(self):
        for stint in self.stints:
            stint.update_value()
         
            
    def add_stint(self):
        self.add_component(self.field.value[-1])
        self.update_value()
       
        
    def remove_stint(self):
        last = self.stints[-1]
        self.layout().removeWidget(last)
        self.stints.pop()

        
class NumberOfStintsComponent(OptionComponent):
    lastcomponent = None
    field:NumberOfStintsField = None
    tyre_component:TyresComponent = None
    stints_component:StintsComponent = None
    
    def __init__(self, parent, field:NumberOfStintsField):
        OptionComponent.__init__(self, parent, field)
        NumberOfStintsComponent.lastcomponent = self
    
    
    def decrement(self):
        if not self.field.decrement():
            return
        
        self.update_value()
        self.tyre_component.remove_stint()
        if self.stints_component:
            self.stints_component.remove_stint()
        
    
    def increment(self):
        if not self.field.increment():
            return
        
        self.update_value()
        self.tyre_component.add_stint()
        if self.stints_component:
            self.stints_component.add_stint()

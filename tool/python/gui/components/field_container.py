from PyQt5.QtCore import *
from PyQt5.QtGui import *
from PyQt5.QtWidgets import *

from gui.components.container import Container
from gui.components.field_component import field_to_component
from gui.components.row import BaseRow
from igp.service.modifier.modifier import BaseModifier, Field
from igp.util.tools import output


class FieldContainer(Container):
    modifier:BaseModifier = None
    sequence:list = []
    selected:list[Field] = []
    
    def row(self, field, parent):
        return FieldRow(field, parent)
    
    def partial_refresh(self):
        if not self.modifier:
            return
        
        self.replace_rows(self.modifier.fields)
        
    def is_valid(self):
        if not self.modifier:
            return True
        
        message = ""
        for field in self.modifier.fields:
            if not field.is_valid():
                message += f"{field.help()}, "

        if message:
            output(message[:-2])
            return False
        
        return True


class FieldRow(BaseRow):
    def __init__(self, *args, **kwargs):
        BaseRow.__init__(self, *args, **kwargs)
        self.setCursor(QCursor(Qt.ArrowCursor))
        
    def create_second_column(self, layout:QHBoxLayout):
        pass
        
      
    def set_second_column(self, field:Field):
        component = field_to_component(self, field)
        self.field_edit = component
        self.layout().addWidget(self.field_edit)
            
    
    def mousePressEvent(self, e) -> None:
        pass
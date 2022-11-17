from PyQt5.QtCore import *
from PyQt5.QtGui import *
from PyQt5.QtWidgets import *

from gui.components.container import Container
from gui.components.row import BaseRow, RowDropDown, parent
from igp.service.base_igp_account import BaseIGPaccount
from igp.util.decorators import Command
from gui.components.modifier_window import ModifierWidget


class TasksContainer(Container):
    sequence:list = []
    selected:list[Command] = []
    instance = None
    
    def __init__(self, *args, **kwargs):
        Container.__init__(self, *args, **kwargs)
        TasksContainer.instance = self
        
        
    def row(self, task, parent):
        return TaskRow(task, parent)

   
    def partial_refresh(self):
        self.replace_rows(BaseIGPaccount.commands)


class TaskDropDown(RowDropDown):
    def __init__(self, *args, **kwargs):
        RowDropDown.__init__(self, *args, **kwargs)
        self.modwidget = ModifierWidget(parent(self, 7))
        
        
    def set_object(self, object):
        self.modwidget.set_object(object)
    
    
    def select_event(self):
        self.modwidget.update()
        self.modwidget.show()
        
        
class TaskRow(BaseRow):
    row_dropdown:TaskDropDown = None
    
    def new_drop_down(self) -> TaskDropDown:
         return TaskDropDown(self)
    
    def set_second_column(self, object):
        self.row_dropdown.set_object(object)
        
        
    def selected_event(self):
        if self.selected:
            TasksContainer.instance.selected.append(self.object)
        else:
            TasksContainer.instance.selected.remove(self.object)      

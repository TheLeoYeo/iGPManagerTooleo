from PyQt5.QtCore import *
from PyQt5.QtGui import *
from PyQt5.QtWidgets import *

from gui.components.container import Container
from gui.components.modifier_window import ModifierWidget
from gui.components.row import BaseRow, RowDropDown, parent
from igp.service.base_igp_account import BaseIGPaccount
from igp.service.commands.tasks import Categories, Category
from igp.util.decorators import Command



class TasksContainer(Container):
    sequence:list = []
    selected:list[Command] = []
    instance = None
    category_index = 0
    
    def __init__(self, *args, **kwargs):
        Container.__init__(self, *args, **kwargs)
        TasksContainer.instance = self
        
        
    def row(self, task, parent):
        return TaskRow(task, parent)

   
    def partial_refresh(self):
        commands = filter(self.matches_category, BaseIGPaccount.commands)
        self.replace_rows(commands)


    def category(self) -> Category:
        return Categories.ALL[self.category_index]
    
    
    def matches_category(self, command:Command):
        return command.category == self.category()
    
    
    def inc_category(self):
        self.category_index = (self.category_index + 1) % len(Categories.ALL)
        self.refresh()
    
    
    def dec_category(self):
        self.category_index = (self.category_index - 1) % len(Categories.ALL)
        self.refresh()


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

from PyQt5 import QtWidgets, uic, QtCore
from PyQt5.QtCore import Qt

from igp.service.accounts import AccountIterator
from igp.service.base_igp_account import BaseIGPaccount
from igp.service.jobs import AllJobs, Job
from util.utils import join
from gui.components.custom_widgets import LoginWindow

UI_Window, UI_BASE = uic.loadUiType(join("gui","views","home.ui", uplevel=2))


class TodoModel(QtCore.QAbstractListModel):
    def __init__(self, *args, todos=None, **kwargs):
        super(TodoModel, self).__init__(*args, **kwargs)
        self.todos: list[BaseIGPaccount] = todos or []


    def data(self, index, role):
        if role == Qt.DisplayRole:
            text = self.todos[index.row()].username
            return text

    def rowCount(self, index):
        return len(self.todos)


class Main(QtWidgets.QMainWindow, UI_Window):
    def __init__(self):
        QtWidgets.QMainWindow.__init__(self)
        UI_Window.__init__(self)
        self.setupUi(self)
        self.setAcceptDrops(True)
        self.addlogin = LoginWindow(self) 
        
        self.refreshButton.pressed.connect(self.refresh)
        self.add_account.pressed.connect(self.create_login)
        self.remove_account.pressed.connect(self.remove_acc)
        self.add_jobs_butt.pressed.connect(self.add_jobs)
        self.perform_butt.pressed.connect(self.perform)
    
      
    def refresh(self):
        self.tasksCont.refresh()
        self.accountsCont.refresh()
        self.jobsCont.refresh()
    
    
    def create_login(self):
        self.addlogin.show()
        
        
    def remove_acc(self):
        instance = AccountIterator.get_instance()
        accounts = self.accountsCont.selected.copy()
        instance.remove_accounts(accounts)


    def perform(self):
        self.jobsCont.perform()
        
    
        
    def add_jobs(self):
        Job(self.accountsCont.selected.copy(), self.tasksCont.selected.copy())
        
        
    def dragEnterEvent(self, e):
        e.accept()
    
    
    def dropEvent(self, e):
        pos = e.pos()
        widget:QtWidgets.QFrame = e.source()
        size = widget.size()
        widget.setGeometry(pos.x(), pos.y(), size.width(), size.height())
        

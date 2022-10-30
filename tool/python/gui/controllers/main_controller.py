from PyQt5 import QtWidgets, uic

from igp.service.accounts import AccountIterator
from igp.service.jobs import AllJobs, Job
from igp.util.events import AllContainersReadyEvent, Event
from util.utils import join
from gui.components.custom_widgets import LoginWindow, OutputWindow, ReadyContainers

UI_Window, UI_BASE = uic.loadUiType(join("gui","views","home.ui", uplevel=2))


class Main(QtWidgets.QMainWindow, UI_Window):
    def __init__(self, load):
        QtWidgets.QMainWindow.__init__(self)
        UI_Window.__init__(self) 
        self.setupUi(self)
        self.setAcceptDrops(True)
        self.addlogin = LoginWindow(self)
        self.output = OutputWindow(self)
        
        self.load = load
        ReadyContainers.get_instance().add_listener(self)
        self.accountsCont.set_ready_instance(ReadyContainers.get_instance())
        self.accountsCont.collect()
        self.refreshButton.pressed.connect(self.refresh)
        self.add_account.pressed.connect(self.create_login)
        self.remove_account.pressed.connect(self.remove_acc)
        self.add_jobs_butt.pressed.connect(self.add_jobs)
        self.remove_jobs_butt.pressed.connect(self.remove_jobs)
        self.perform_butt.pressed.connect(self.perform)
    
      
    def refresh(self):
        self.tasksCont.refresh()
        self.accountsCont.refresh()
        self.jobsCont.refresh()
        self.output.hide()
    
    
    def create_login(self):
        self.addlogin.show()
        
        
    def handle(self, event:Event):
        if isinstance(event, AllContainersReadyEvent):
            self.load.finished.emit()
            self.show()
            self.refreshButton.click()
        
        
    def remove_acc(self):
        instance = AccountIterator.get_instance()
        accounts = self.accountsCont.selected.copy()
        instance.remove_accounts(accounts)


    def perform(self):
        self.add_jobs_butt.setEnabled(False)
        self.remove_jobs_butt.setEnabled(False)
        self.jobsCont.perform([self.add_jobs_butt, self.remove_jobs_butt])
        
           
    def add_jobs(self):
        Job(self.accountsCont.selected.copy(), self.tasksCont.selected.copy())
       
        
    def remove_jobs(self):
        for job in self.jobsCont.selected.copy():
            AllJobs.remove(job)
        
        
    def dragEnterEvent(self, e):
        e.accept()
    
    
    def dropEvent(self, e):
        pos = e.pos()
        widget:QtWidgets.QFrame = e.source()
        size = widget.size()
        widget.setGeometry(pos.x(), pos.y(), size.width(), size.height())
        

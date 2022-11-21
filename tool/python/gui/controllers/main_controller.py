from PyQt5 import QtWidgets, uic

from gui.components.output_window import OutputWindow
from gui.components.login_window import LoginWindow
from gui.components.logs_window import LogsWindow
from gui.gui_util.ready_containers import ReadyContainers
from igp.service.accounts import AccountIterator
from igp.service.jobs import AllJobs, Job
from igp.util.events import AllContainersReadyEvent, Event
from igp.util.tools import output
from util.utils import join


UI_Window, UI_BASE = uic.loadUiType(join("gui","views","home.ui", uplevel=2))
class Main(QtWidgets.QMainWindow, UI_Window):
    def __init__(self, load):
        QtWidgets.QMainWindow.__init__(self)
        UI_Window.__init__(self) 
        self.setupUi(self)
        self.setAcceptDrops(True)
        self.addlogin = LoginWindow(self)
        self.logswindow = LogsWindow(self)
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
        self.turboModeButton.pressed.connect(self.toggle_turbo)
        self.logsButton.pressed.connect(self.show_logs)
        self.perform_butt.pressed.connect(self.perform)
    
      
    def refresh(self):
        self.tasksCont.refresh()
        self.accountsCont.refresh()
        self.jobsCont.refresh()
    
    
    def create_login(self):
        self.addlogin.show()
        
    
    def show_logs(self):
        self.logswindow.show()
        
        
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
        self.perform_butt.setEnabled(False)
        self.jobsCont.perform([self.add_jobs_butt, self.remove_jobs_butt, self.perform_butt])
        
        
    def toggle_turbo(self):
        self.jobsCont.toggle_turbo()
        tm = ("OFF", "ON")[self.jobsCont.turbo_enabled()]
        self.turboModeButton.setText(f"Turbo: {tm}")
    
    
    def add_jobs(self):
        Job(self.accountsCont.selected.copy(), self.tasksCont.selected.copy())
       
        
    def remove_jobs(self):
        if len(self.jobsCont.selected) == 0:
            output("Select a job first",screen_only=True)
            
        for job in self.jobsCont.selected.copy():
            AllJobs.remove(job)
        
        
    def dragEnterEvent(self, e):
        e.accept()
    
    
    def dropEvent(self, e):
        pos = e.pos()
        widget:QtWidgets.QFrame = e.source()
        size = widget.size()
        widget.setGeometry(pos.x(), pos.y(), size.width(), size.height())
        

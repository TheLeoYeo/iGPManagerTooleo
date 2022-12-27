from PyQt5 import QtWidgets, uic

from gui.components.output_window import OutputWindow
from gui.components.login_window import LoginWindow
from gui.components.logs_window import LogsWindow
from gui.components.modifier_window import ModifierWidget
from gui.gui_util.ready_containers import ReadyContainers
from gui.gui_util.window_size import read_size, update_size as US
from igp.service.accounts import AccountIterator
from igp.service.commands.tasks import Category
from igp.service.jobs import AllJobs, Job
from igp.util.events import AllContainersReadyEvent, Event
from igp.util.tools import output
from igp.util.turbomode import TurboMode
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
        self.task_left_butt.on_click = self.left
        self.task_right_butt.on_click = self.right
        self.fix_size()
        self.update_task_header()


    def closeEvent(self, *args, **kwargs):
        self.update_size()
        super().closeEvent(*args, **kwargs)
        
    
    def update_size(self):
        size = self.size()
        width, height = size.width(), size.height()
        US(height, width)
        
    
    def fix_size(self):
        try:
            dim = read_size()
            self.resize(dim["width"], dim["height"])
        except ValueError:
            output("Something is wrong with the win_size.ini file. Please fix", log_only=True)
        

    def refresh(self):
        self.tasksCont.refresh()
        self.accountsCont.refresh()
        self.jobsCont.refresh()
    
    
    def left(self):
        self.tasksCont.dec_category()
        self.update_task_header()
        
    
    def right(self):
        self.tasksCont.inc_category()
        self.update_task_header()
    
    
    def create_login(self):
        self.addlogin.show()
        
    
    def update_task_header(self):
        ModifierWidget.hide_class()
        category:Category = self.tasksCont.category()
        self.task_header.setText(category.name)
        
    
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
        TurboMode.toggle_turbo()
        tm = ("OFF", "ON")[TurboMode.turbo]
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

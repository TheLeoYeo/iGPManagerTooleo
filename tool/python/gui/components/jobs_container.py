import time

from PyQt5.QtCore import *
from PyQt5.QtGui import *
from PyQt5.QtWidgets import *

from gui.components.container import Container
from gui.components.row import BaseRow
from igp.service.base_igp_account import BaseIGPaccount
from igp.service.jobs import AllJobs, Job
from igp.util.events import *
from igp.util.tools import output


class JobsContainer(Container):
    sequence:list = []
    selected:list[Job] = []
    instance = None
    turbo_mode = False
    
    def __init__(self, *args, **kwargs):
        Container.__init__(self, *args, **kwargs)
        AllJobs.add_to_listeners(self)
        BaseIGPaccount.add_to_listeners(self)
        JobsContainer.instance = self
    
        
    def row(self, account, parent):
        return JobRow(account, parent)
        
        
    def partial_refresh(self):
        self.replace_rows(AllJobs.jobs.copy())
        
  
    def perform(self, buttons):
        self.inner_thread = QThread()
        self.worker = PerformWorker()
        self.worker.moveToThread(self.inner_thread)
        self.inner_thread.started.connect(self.worker.run)
        self.worker.finished.connect(self.inner_thread.quit)
        self.worker.finished.connect(self.worker.deleteLater)
        self.inner_thread.finished.connect(self.inner_thread.deleteLater)
        self.inner_thread.finished.connect(lambda: self.reenable_buttons(buttons))
        self.inner_thread.start()
        
        
    def reenable_buttons(self, buttons:list[QPushButton]):
        for button in buttons:
            button.setEnabled(True)
        
                     
    def handle(self, event:Event):
        if isinstance(event, JobAddedEvent):
            self.add_row(event.value)
            
        elif isinstance(event, JobRemovedEvent): 
            self.remove_row(event.value)
        
        elif isinstance(event, AccountNameUpdatedEvent):
            for child in self.sequence:
                if isinstance(child, BaseRow) and event.value in child.object.accounts:
                    self.update_row(child.object)
                         
        elif isinstance(event, ConfirmedLogInEvent):
            for child in self.sequence:
                if isinstance(child, BaseRow) and event.value in child.object.accounts:
                    self.update_row(child.object)
                
                    
    def toggle_turbo(self):
        JobsContainer.turbo_mode = not JobsContainer.turbo_mode
    
    def turbo_enabled(self):
        return JobsContainer.turbo_mode
    
    
class PerformWorker(QObject):
    progressed = pyqtSignal()
    finished = pyqtSignal()  
      
    def run(self):
        jobs = AllJobs.jobs.copy()
        for job in jobs:
            if not JobsContainer.turbo_mode:
                output("Waiting")
                time.sleep(5)
                output("Go!!!")
                
            job.perform()
            AllJobs.remove(job)
        
        self.finished.emit()
    
        
class JobRow(BaseRow):
    def selected_event(self):
        if self.selected:
            JobsContainer.instance.selected.append(self.object)
        else:
            JobsContainer.instance.selected.remove(self.object)
    
    
    def select_if_it_was_selected(self, object):
        if object in JobsContainer.instance.selected:
            self.mousePressEvent(None)

from PyQt5.QtCore import *
from PyQt5.QtGui import *
from PyQt5.QtWidgets import *

from gui.components.container import Container
from gui.components.row import BaseRow
from gui.components.modifier_window import ModifierWidget
from gui.gui_util.ready_containers import ReadyContainers
from igp.service.accounts import AccountIterator
from igp.service.base_igp_account import BaseIGPaccount
from igp.service.igpaccount import IGPaccount
from igp.service.main_browser import MainBrowser
from igp.util.events import *
from igp.util.tools import output


class DetailsContainer(Container):
    sequence:list = []
    selected:list[IGPaccount] = []
    instance = None
    ready_instance:ReadyContainers = None
                
    def __init__(self, *args, **kwargs):
        Container.__init__(self, *args, **kwargs)
        AccountIterator.get_instance().add_to_listeners(self)
        BaseIGPaccount.add_to_listeners(self)
        DetailsContainer.instance = self
        
        
    def set_ready_instance(self, instance):
        self.ready_instance = instance
        
        
    def row(self, account:BaseIGPaccount, parent):
        return DetailRow(account, parent)


    def handle(self, event: Event):
        if not self.ready_instance.ready:
            return
            
        if isinstance(event, AccountAddedEvent): 
            self.add_row(event.value)
            
        elif isinstance(event, AccountRemovedEvent):
            self.remove_row(event.value)
        
        elif isinstance(event, ConfirmedLogInEvent):
            output(f"{event.value.username} has valid details ")
            self.update_row(event.value)
            
        elif isinstance(event, AccountNameUpdatedEvent):
            output(f"{event.value.username} has changed details ")
            self.update_row(event.value)
            
            
    def partial_refresh(self):
        self.replace_rows(AccountIterator.get_instance().accounts)
        
 
    def add_ready(self):
        self.ready_instance.add_ready(self)

       
    def collect(self):
        self.inner_thread = QThread()
        self.worker = CollectWorker()
        self.worker.moveToThread(self.inner_thread)
        self.inner_thread.started.connect(self.worker.run)
        self.worker.finished.connect(self.add_ready)
        self.worker.finished.connect(self.inner_thread.quit)
        self.worker.finished.connect(self.worker.deleteLater)
        self.inner_thread.finished.connect(self.inner_thread.deleteLater)
        self.inner_thread.start()


class CollectWorker(QObject):
    finished = pyqtSignal()    
    def run(self):
        MainBrowser.get_instance(minimised=True)
        AccountIterator.get_instance().collect_accounts()
        self.finished.emit()


class DetailRow(BaseRow):
    def selected_event(self):
        if self.selected:
            DetailsContainer.instance.selected.append(self.object)
        else:
            DetailsContainer.instance.selected.remove(self.object)
           
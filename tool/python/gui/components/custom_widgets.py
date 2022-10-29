from datetime import datetime, timedelta

from PyQt5 import QtWidgets, uic, QtCore
from PyQt5.QtCore import *
from PyQt5.QtGui import *
from PyQt5.QtWidgets import *

from igp.service.accounts import AccountIterator
from igp.service.base_igp_account import BaseIGPaccount
from igp.service.igpaccount import IGPaccount
from igp.service.jobs import AllJobs, Job
from igp.util.decorators import Command
from igp.util.events import AccountAddedEvent, AccountNameUpdatedEvent, AccountRemovedEvent, AllContainersReadyEvent, Event, JobAddedEvent, JobRemovedEvent
from igp.util.exceptions import LoginDetailsError
from igp.util.tools import Output
from igp.service.main_browser import MainBrowser
from util.utils import join


class ConfirmButton(QtWidgets.QPushButton):
    def __init__(self, *args, **kwargs):
        QtWidgets.QPushButton.__init__(self, *args, **kwargs)
        self.setCursor(QCursor(Qt.PointingHandCursor))
        self.setMaximumSize(100, 30)


class RejectButton(QtWidgets.QPushButton):
    def __init__(self, *args, **kwargs):
        QtWidgets.QPushButton.__init__(self, *args, **kwargs)
        self.setCursor(QCursor(Qt.PointingHandCursor))
        self.setMaximumSize(100, 30)


class DefaultButton(QtWidgets.QPushButton):
    pass
        
class Heading(QtWidgets.QLabel):
    pass

class Text(QtWidgets.QCheckBox):
    pass


BaseLine, UI_BASE = uic.loadUiType(join("gui","views","rowSep.ui", uplevel=2))
class RowSep(QtWidgets.QFrame, BaseLine):
    def __init__(self, parent):
        QtWidgets.QFrame.__init__(self, parent)
        BaseLine.__init__(self)
        self.setupUi(self)
        self.line.setStyleSheet("""
                                background-color:rgb(70, 70, 70);
                                margin: 0px 5px;""")
        
    def aline(parent):
        return RowSep(parent).line


class RowDropDown(QLabel):
    inside = False
    DEF_STYLES = "padding: 6px;"
    
    def __init__(self, *args, **kwargs):
        QLabel.__init__(self, *args, **kwargs)
        self.setStyleSheet(f"{self.DEF_STYLES}")
    
    def mousePressEvent(self, e) -> None:
        self.setStyleSheet(f"{self.DEF_STYLES}background-color:rgba(200, 200, 200, 0.3);")
            
    def mouseReleaseEvent(self, e) -> None:
        self.setStyleSheet(f"{self.DEF_STYLES}background-color:none;")
        if self.inside:
            self.enterEvent(e)
    
    def enterEvent(self, e) -> None:
        self.inside = True
        self.setStyleSheet(f"{self.DEF_STYLES}background-color:rgba(20,20,20,0.5);")
        
    def leaveEvent(self, e) -> None:
        self.inside = False
        self.setStyleSheet(f"{self.DEF_STYLES}background-color:none;")
        

class BaseRow(QtWidgets.QFrame):
    selected = False
    inside = False
    object = None
    count = 0
    
    def __init__(self, object=None, parent:QtWidgets.QFrame=None):
        QtWidgets.QFrame.__init__(self, parent, objectName=f"detailrow{BaseRow.count}")
        BaseRow.count += 1
        self.setupUi()
        
        if object:
            self.object = object
            self.select_if_it_was_selected(object)
            self.row_name.setText(object.__str__())
            self.row_name.setWordWrap(False)
            self.row_name.setStyleSheet("padding-left: 6px")
            self.setToolTip(object.help())
        self.show()
        

    def setupUi(self):
        self.setCursor(QCursor(Qt.PointingHandCursor))
        self.setGeometry(QRect(50, 210, 141, 41))
        sizePolicy = QSizePolicy(QSizePolicy.Expanding, QSizePolicy.Preferred)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.sizePolicy().hasHeightForWidth())
        self.setSizePolicy(sizePolicy)
        
        layout = QHBoxLayout()
        layout.setSpacing(0)
        layout.setObjectName(u"horizontalLayout")
        layout.setSizeConstraint(QLayout.SetMaximumSize)
        layout.setContentsMargins(0, 0, 0, 0)
        
        self.row_name = QLabel()
        self.row_name.setObjectName(u"rowName")
        sizePolicy1 = QSizePolicy(QSizePolicy.Expanding, QSizePolicy.Minimum)
        sizePolicy1.setHorizontalStretch(0)
        sizePolicy1.setVerticalStretch(0)
        sizePolicy1.setHeightForWidth(self.row_name.sizePolicy().hasHeightForWidth())
        self.row_name.setSizePolicy(sizePolicy1)
        self.row_name.setMaximumSize(QSize(16777215, 200))
        self.row_name.setAlignment(Qt.AlignLeading|Qt.AlignLeft|Qt.AlignVCenter)
        layout.addWidget(self.row_name)

        self.row_dropdown = RowDropDown()
        self.row_dropdown.setObjectName(u"row_dropdown")
        self.row_dropdown.setMaximumSize(QSize(30, 30))
        self.row_dropdown.setPixmap(QPixmap(join("gui","images","dropdown.png", uplevel=2)))
        self.row_dropdown.setScaledContents(True)
        layout.addWidget(self.row_dropdown)
        
        layout.setStretch(0, 1)
        self.setLayout(layout)
        
    def load_updates(self):
        self.row_name.setText(self.object.__str__())
        self.setToolTip(self.object.help())
        
    
    def mousePressEvent(self, e) -> None:
        self.selected = not self.selected
        self.selected_event()
        if self.selected:
            self.setStyleSheet("BaseRow{background-color:rgb(100, 100, 255);}")
        else:
            self.setStyleSheet("BaseRow{background-color:none;}")
    
    
    def enterEvent(self, e) -> None:
        self.inside = True
        if not self.selected:
            self.setStyleSheet("BaseRow{background-color:rgba(35,35,35,0.5);}")


    def leaveEvent(self, e) -> None:
        self.inside = False
        if not self.selected:
            self.setStyleSheet("BaseRow{background-color:none;}")
    
    def selected_event(self):
        pass
    
    def select_if_it_was_selected(self, object):
        pass


class DetailRow(BaseRow):
    def selected_event(self):
        if self.selected:
            DetailsContainer.instance.selected.append(self.object)
        else:
            DetailsContainer.instance.selected.remove(self.object)
            

class TaskRow(BaseRow):
    def selected_event(self):
        if self.selected:
            TasksContainer.instance.selected.append(self.object)
        else:
            TasksContainer.instance.selected.remove(self.object)

      
class JobRow(BaseRow):
    def selected_event(self):
        if self.selected:
            JobsContainer.instance.selected.append(self.object)
        else:
            JobsContainer.instance.selected.remove(self.object)
    
    
    def select_if_it_was_selected(self, object):
        if object in JobsContainer.instance.selected:
            self.mousePressEvent(None)


class ContainerFrame(QFrame):
    pass


class ReadyContainers():
    ready = False
    containers = []
    listeners = []
    instance = None
    
    def get_instance():
        if ReadyContainers.instance:
            return ReadyContainers.instance
        
        ReadyContainers.instance = ReadyContainers()
        return ReadyContainers.instance
    
    
    def add_ready(self, container):
        self.containers.append(container)
        if len(self.containers) == 1:
            self.ready = True
            for listener in self.listeners:
                listener.handle(AllContainersReadyEvent())


    def add_listener(self, object):
        self.listeners.append(object)
    

class Container(QScrollArea):
    noRows:bool = True
    sequence:list[QWidget] = []
    
    def __init__(self, *args, **kwargs):
        QScrollArea.__init__(self, *args, **kwargs)
        self.setupUi()
        self.show()


    def setupUi(self):
        self.setObjectName("accountsCont")
        
        self.setVerticalScrollBarPolicy(Qt.ScrollBarAsNeeded)
        self.setWidgetResizable(True)
        
        self.setAlignment(Qt.AlignHCenter|Qt.AlignTop)
        self.scrollAreaWidgetContents = QWidget()
        self.scrollAreaWidgetContents.setObjectName(u"scrollAreaWidgetContents")
        
        self.scrollAreaWidgetContents.setGeometry(QRect(0, 0, 171, 16))
        sizePolicy1 = QSizePolicy(QSizePolicy.Preferred, QSizePolicy.Fixed)
        sizePolicy1.setHorizontalStretch(0)
        sizePolicy1.setVerticalStretch(0)
        sizePolicy1.setHeightForWidth(self.scrollAreaWidgetContents.sizePolicy().hasHeightForWidth())
        self.scrollAreaWidgetContents.setSizePolicy(sizePolicy1)
        
        self.horzlayout = QHBoxLayout(self.scrollAreaWidgetContents)
        self.horzlayout.setObjectName(u"horzlayout")
        self.horzlayout.setContentsMargins(0, 0, 0, 0)
        self.cont = ContainerFrame()
        self.cont.setFrameShape(QFrame.Box)
        self.cont.setFrameShadow(QFrame.Sunken)
        self.cont.setObjectName(u"cont")
        sizePolicy2 = QSizePolicy(QSizePolicy.Preferred, QSizePolicy.Maximum)
        sizePolicy2.setHorizontalStretch(0)
        sizePolicy2.setVerticalStretch(0)
        sizePolicy2.setHeightForWidth(self.cont.sizePolicy().hasHeightForWidth())
        self.cont.setSizePolicy(sizePolicy2)
        self.cont.setFrameShape(QFrame.NoFrame)
        self.cont.setFrameShadow(QFrame.Sunken)
        self.vertLayout = QVBoxLayout(self.cont)
        self.vertLayout.setSpacing(0)
        self.vertLayout.setObjectName(u"vertLayout")
        self.vertLayout.setSizeConstraint(QLayout.SetMaximumSize)
        self.vertLayout.setContentsMargins(0, 0, 0, 0)
        self.horzlayout.addWidget(self.cont)

        self.setWidget(self.scrollAreaWidgetContents)
    
    
    def add_rows(self, objects:list=None):  
        if objects:
            for object in objects:
                self.add_row(object)
        
        
    def add_row(self, object):       
        row = self.row(object, self.cont)
            
        if not self.noRows:
            rowsep = RowSep.aline(self)
            self.cont.layout().addWidget(rowsep)
            self.sequence.append(rowsep)
        
        self.cont.layout().addWidget(row) 
        self.sequence.append(row)     
        self.noRows = False
        
    
    def remove_row(self, object):
        for index, child in enumerate(self.sequence):
            if isinstance(child, BaseRow) and child.object == object:
                self.cont.layout().removeWidget(child)
                self.sequence.remove(child)
                
                # remove a seperator if needed
                if index > 0:
                    rowsep = self.sequence[index - 1]
                    self.cont.layout().removeWidget(rowsep)
                    self.sequence.remove(rowsep)

    def update_row(self, object):
        for child in self.sequence:
            if isinstance(child, BaseRow) and child.object == object:
                child.load_updates()

       
    def replace_rows(self, objects:list=None):      
        for child in self.cont.children():
            if not isinstance(child, QVBoxLayout):
                self.cont.layout().removeWidget(child)
                      
        self.noRows = True
        self.add_rows(objects)
    
    
    def row(self, object, parent):
        return BaseRow(object, parent)

  
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
        
        elif isinstance(event, AccountNameUpdatedEvent):
            self.update_row(event.value)
            
            
    def refresh(self):
        self.selected = []
        self.sequence = []
        self.partial_refresh()
   
        
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
    

class TasksContainer(Container):
    sequence:list = []
    selected:list[Command] = []
    instance = None
    
    def __init__(self, *args, **kwargs):
        Container.__init__(self, *args, **kwargs)
        TasksContainer.instance = self
        
        
    def row(self, task, parent):
        return TaskRow(task, parent)

   
    def refresh(self):
        self.selected = []
        self.sequence = []
        self.replace_rows(BaseIGPaccount.commands)
    
       
class JobsContainer(Container):
    sequence:list = []
    selected:list[Job] = []
    instance = None
    
    def __init__(self, *args, **kwargs):
        Container.__init__(self, *args, **kwargs)
        AllJobs.add_to_listeners(self)
        BaseIGPaccount.add_to_listeners(self)
        JobsContainer.instance = self
    
        
    def row(self, account, parent):
        return JobRow(account, parent)
    
    
    def refresh(self):
        self.selected = []
        self.sequence = []
        self.partial_refresh()
        
        
    def partial_refresh(self):
        self.replace_rows(AllJobs.jobs.copy())

        
    def perform(self, button):
        self.inner_thread = QThread()
        self.worker = PerformWorker()
        self.worker.moveToThread(self.inner_thread)
        self.inner_thread.started.connect(self.worker.run)
        self.worker.finished.connect(self.inner_thread.quit)
        self.worker.finished.connect(self.worker.deleteLater)
        self.inner_thread.finished.connect(self.inner_thread.deleteLater)
        # self.inner_thread.finished.connect(lambda: button.setEnabled(True))
        self.inner_thread.start()
        
                     
    def handle(self, event:Event):
        if isinstance(event, JobAddedEvent):
            self.add_row(event.value)
            
        elif isinstance(event, JobRemovedEvent): 
            self.remove_row(event.value)
        
        elif isinstance(event, AccountNameUpdatedEvent):
            for child in self.sequence:
                if isinstance(child, BaseRow) and event.value in child.object.accounts:
                    self.update_row(child.object)
    
    
class PerformWorker(QObject):
    progressed = pyqtSignal()
    finished = pyqtSignal()    
    def run(self):
        jobs = AllJobs.jobs.copy()
        for job in jobs:
            job.perform()
            AllJobs.remove(job)
        
        self.finished.emit()
    
    
class LoginWindow(QFrame):
    def __init__(self, parent:QtWidgets.QFrame=None):
        QtWidgets.QFrame.__init__(self, parent, objectName=f"login_window")
        self.setupUi()
        self.hide()
        
        
    def mouseMoveEvent(self, e) -> None:
        if e.buttons() == Qt.LeftButton:
            drag = QDrag(self)
            mime = QMimeData()
            drag.setMimeData(mime)
            drag.exec_(Qt.MoveAction)
    
    
    def setupUi(self):
        layout = QVBoxLayout()
        self.setGeometry(QRect(200, 80, 261, 300))
        sizePolicy = QSizePolicy(QSizePolicy.Expanding, QSizePolicy.Expanding)

        self.setMaximumHeight(220)
        sizePolicy.setHeightForWidth(self.sizePolicy().hasHeightForWidth())
        self.setSizePolicy(sizePolicy)
        
        formlayout = QFormLayout()
        formlayout.setObjectName("formLayout")
        formlayout.setContentsMargins(10, 10, 10, 10)
        
        self.username = QLabel(self)
        self.username.setText("Email: ")
        self.username.setObjectName("username")
        self.username.setAlignment(Qt.AlignCenter)

        formlayout.setWidget(0, QFormLayout.LabelRole, self.username)

        self.username_inp = QTextEdit(self)
        self.username_inp.setObjectName("textEdit")
        self.username_inp.setStyleSheet("background-color:white;")

        formlayout.setWidget(0, QFormLayout.FieldRole, self.username_inp)

        self.password_inp = QTextEdit(self)
        self.password_inp.setObjectName("textEdit_2")
        self.password_inp.setStyleSheet("background-color:white;")

        formlayout.setWidget(1, QFormLayout.FieldRole, self.password_inp)

        self.password = QLabel(self)
        self.password.setText("Password: ")
        self.password.setAlignment(Qt.AlignCenter)
        self.password.setObjectName("password")

        formlayout.setWidget(1, QFormLayout.LabelRole, self.password)
        
        self.warning = QLabel()
        self.warning.setObjectName("warning")
        self.warning.setWordWrap(True)
        self.warning.setAlignment(Qt.AlignCenter)
                       
        layout.addLayout(formlayout)
        
        self.add_account = ConfirmButton()
        self.add_account.setText("add")
        self.add_account.pressed.connect(self.add_account_func)
        layout.addWidget(self.add_account, alignment=Qt.AlignHCenter)
        
        self.close = RejectButton()
        self.close.setText("close")
        self.close.pressed.connect(self.hide)
        layout.addWidget(self.close, alignment=Qt.AlignHCenter)
        
        layout.addWidget(self.warning)
        self.setLayout(layout)
        
        
    def add_account_func(self):
        instance = AccountIterator.get_instance()
        try:
            account = IGPaccount(self.username_inp.toPlainText(), self.password_inp.toPlainText())
            self.warning.setText("")
            instance.add_account(account)
        except LoginDetailsError:
            self.warning.setText("DETAILS EMPTY OR INCLUDE\n ; OR \\")            


class MessageWorker(QObject):
    finished = pyqtSignal()
    DELTA = 3
    already_in_loop = False 
    
    def run(self):
        self.reset()
                  
        end = self.end
        while datetime.now() < end:
            end = self.end
        
        self.finished.emit()
    
      
    def reset(self):
        now = datetime.now()
        self.end = now + timedelta(seconds=self.DELTA)


class OutputWindow(QFrame):   
    def __init__(self, parent:QtWidgets.QFrame=None):
        QtWidgets.QFrame.__init__(self, parent, objectName="output_window")
        self.setupUi()
        Output.add_listener(self)
        self.hide()
        self.inner_thread = QtCore.QThread()
    
    
    def setupUi(self):
        self.setCursor(QCursor(Qt.PointingHandCursor))
        layout = QHBoxLayout()
        layout.setAlignment(Qt.AlignRight)
        layout.addStretch(1)
             
        self.output = QLabel()
        self.output.setWordWrap(False)
        self.output.setObjectName("output")
        self.output.setAlignment(Qt.AlignCenter)
        layout.addWidget(self.output)
        self.setLayout(layout)
    
    
    def handle(self, message:str):
        self.output.setText(message)
        self.adjustSize()
        # self.setMinimumWidth(self.parent().width())
        self.show()
        
        try:
            if self.inner_thread.isRunning():
                self.worker.reset()
                return
        except RuntimeError:
            pass
        
        self.inner_thread = QtCore.QThread()
        self.worker = MessageWorker()
        
        self.worker.moveToThread(self.inner_thread)
        
        self.inner_thread.started.connect(self.worker.run)
        self.worker.finished.connect(self.inner_thread.quit)
        self.worker.finished.connect(self.worker.deleteLater)
        self.inner_thread.finished.connect(lambda: self.hide())
        self.inner_thread.finished.connect(self.inner_thread.deleteLater)
        self.inner_thread.start()

  
    def mousePressEvent(self, e) -> None:
        self.hide()
    
    
    def enterEvent(self, e) -> None:
        self.setStyleSheet("#output{background-color:rgb(35,35,35);}")


    def leaveEvent(self, e) -> None:
        self.setStyleSheet("#output {background-color:rgb(50, 50, 50);}")

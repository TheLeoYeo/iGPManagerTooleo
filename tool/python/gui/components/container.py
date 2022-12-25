from PyQt5.QtCore import *
from PyQt5.QtGui import *
from PyQt5.QtWidgets import *

from gui.components.row import RowSep, BaseRow
from igp.util.events import Event


class ContainerFrame(QFrame):
    pass


class RefreshEvent(Event):
    pass


class Container(QScrollArea):
    noRows:bool = True
    sequence:list[QWidget] = []
    listeners = []
    count = 0
    
    def __init__(self, *args, **kwargs):
        QScrollArea.__init__(self, *args, **kwargs)
        self.setupUi()
        self.show()


    def setupUi(self):
        self.setObjectName(f"container{Container.count}")
        Container.count += 1
        
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
                if object in self.selected:
                    self.selected.remove(object)
                
                # remove above separator if needed
                # check if we didn't remove the first row
                if index > 0:
                    # remove the rowseparator above our row other than the first                    
                    rowsep = self.sequence[index - 1]
                    self.cont.layout().removeWidget(rowsep)
                    self.sequence.remove(rowsep)
                
                # We just removed the first row, check if there are still some rows after this
                elif len(self.sequence) > 0:
                    rowsep = self.sequence[0]
                    self.cont.layout().removeWidget(rowsep)
                    self.sequence.remove(rowsep)
                
                # check if there are now no rows at all
                if len(self.sequence) == 0:
                    self.noRows = True


    def update_row(self, object):
        for child in self.sequence:
            if isinstance(child, BaseRow) and child.object == object:
                child.load_updates()
         
                
    def update_all(self):
        for child in self.sequence:
            if isinstance(child, BaseRow):
                child.load_updates()
       
       
    def replace_rows(self, objects:list=None):      
        for child in self.cont.children():
            if not isinstance(child, QVBoxLayout):
                self.cont.layout().removeWidget(child)
                      
        self.noRows = True
        self.add_rows(objects)

  
    def refresh(self):
        self.selected = []
        self.sequence = []
        for listener in Container.listeners:
            listener.handle(RefreshEvent())
            
        self.partial_refresh()
    
    
    def partial_refresh(self):
        pass
    
    
    def row(self, object, parent):
        return BaseRow(object, parent)
    
    
    def add_to_listeners(object):
        Container.listeners.append(object)
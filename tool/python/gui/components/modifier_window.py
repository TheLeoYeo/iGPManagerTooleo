from PyQt5.QtCore import *
from PyQt5.QtGui import *
from PyQt5.QtWidgets import *

from gui.components.buttons import ConfirmButton
from gui.components.container import Container, RefreshEvent
from gui.components.field_container import FieldContainer
from igp.service.modifier.modifier import BaseModifier, TextField
from igp.util.events import Event


class ModifierWidget(QFrame):
    shown_modifier = None
    count = 0
    modifier:BaseModifier = None
    object = None
     
    def __init__(self, parent=None):
        QFrame.__init__(self, parent, objectName=f"mod_window{ModifierWidget.count}")
        ModifierWidget.count += 1
        self.setupUi()
        self.show()
        
        
    def set_modifier(self, modifier:BaseModifier):
        self.modifier = modifier
        self.container.modifier = modifier
        self.container.partial_refresh()
        
    def set_object(self, object):
        self.object = object
        self.name.setText(self.object.__str__())
        self.set_modifier(object.modifier)
        
        
    def update(self):
        if not self.object:
            return
        self.name.setText(self.object.__str__())

     
    def setupUi(self):
        self.setGeometry(QRect(50, 50, 261, 200))
        
        sizePolicy = QSizePolicy(QSizePolicy.Expanding, QSizePolicy.Expanding)
        sizePolicy.setHeightForWidth(self.sizePolicy().hasHeightForWidth())
        self.setSizePolicy(sizePolicy)
        layout = QVBoxLayout()
        layout.setStretch(0,0)
        layout.setStretch(1,0)
        layout.setStretch(2,1)
        
        self.name = QLabel(self)
        self.name.setText(self.object.__str__())
        layout.addWidget(self.name)
        
        self.container = FieldContainer(self)
        self.container.setWidgetResizable(True)
        layout.addWidget(self.container)
        
        self.set = ConfirmButton()
        self.set.setText("set")
        self.set.pressed.connect(self.hide)
        self.set.setCursor(QCursor(Qt.PointingHandCursor))
        layout.addWidget(self.set, alignment=Qt.AlignHCenter)
        
        self.random = ConfirmButton()
        self.random.setText("randomize")
        self.random.setToolTip("Only randomizes text fields")
        self.random.pressed.connect(self.randomize)
        self.random.setCursor(QCursor(Qt.PointingHandCursor))
        layout.addWidget(self.random, alignment=Qt.AlignHCenter)
        
        self.setLayout(layout)
        
     
    def show(self):
        if ModifierWidget.shown_modifier:
            ModifierWidget.shown_modifier.hide()
        ModifierWidget.shown_modifier = self
        super().show()
    
    
    def hide(self):
        if not self.container.is_valid():
            return
        ModifierWidget.shown_modifier = None
        super().hide()
    
       
    def hide_class():
        if ModifierWidget.shown_modifier:
            ModifierWidget.shown_modifier.hide()
    
    
    def randomize(self):
        for field in self.modifier.fields:
            if isinstance(field, TextField):
                field.randomize()
        self.container.partial_refresh()
    
        
    def handle(event:Event):
        if isinstance(event, RefreshEvent):
            if ModifierWidget.shown_modifier:
                ModifierWidget.shown_modifier.hide()


Container.add_to_listeners(ModifierWidget)
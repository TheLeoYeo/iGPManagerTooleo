from PyQt5.QtWidgets import QLabel, QCheckBox
from PyQt5.QtCore import QSize

from python.gui.components.field_component import ButtonType, FieldButton


class Heading(QLabel):
    pass

class Text(QCheckBox):
    pass


class LeftButton(FieldButton):
    DEF_STYLES = "FieldButton{padding:1px;"
    
    def __init__(self, parent):
        FieldButton.__init__(self, parent, type=ButtonType.LEFT)
        self.setMaximumSize(QSize(20, 20))


class RightButton(FieldButton):
    DEF_STYLES = "FieldButton{padding:1px;"
    
    def __init__(self, parent):
        FieldButton.__init__(self, parent, type=ButtonType.RIGHT)
        self.setMaximumSize(QSize(20, 20))
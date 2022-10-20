from PyQt5 import QtWidgets, uic, QtCore
from PyQt5.QtCore import Qt

from igp.service.base_igp_account import BaseIGPaccount
from igp.service.accounts import AccountIterator
from util.utils import join

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
        
        
        self.confButton.pressed.connect(self.add)
        
    def add(self):
        self.accountsCont.add_rows(AccountIterator.get_instance().accounts)

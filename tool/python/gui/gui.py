from threading import Thread
from util.utils import join
import sys
sys.path.append(join("gui","components",uplevel=2))

import gui.controllers.main_controller as MC
from gui.controllers.main_controller import Main as MainWindow
from PyQt5 import QtWidgets, QtGui

from gui.styles import appStyles
from igp.service.accounts import AccountIterator

class Main():
    def main(self):
        # Create app object
        self.app = QtWidgets.QApplication(sys.argv)
        self.app.setStyleSheet(appStyles)

        window = MainWindow() 
        window.show()
        
        self.collector = Thread(args=[window],target=self.collection)
        self.collector.start()
        # Start the event loop of the app
        sys.exit(self.app.exec())


    def running(self):
        pass


    def collection(self, window):
        AccountIterator.get_instance(minimised=True)
        window.refreshButton.click()
        
    
if __name__ == "main":
    Main().main()
        
        

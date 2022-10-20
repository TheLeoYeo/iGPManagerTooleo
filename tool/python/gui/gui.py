from threading import Thread
from util.utils import join
import sys
sys.path.append(join("gui","components",uplevel=2))

import gui.controllers.main_controller as MC
from gui.controllers.main_controller import Main
from PyQt5 import QtWidgets

from gui.styles import appStyles
from igp.service.accounts import AccountIterator

def main():
    # Create app object
    app = QtWidgets.QApplication(sys.argv)
    app.setStyleSheet(appStyles)

    window = Main() 
    window.show()
    
    Thread(args=[window],target=collection).start()
    # Start the event loop of the app
    sys.exit(app.exec())

def collection(window):
    AccountIterator.get_instance(minimised=True)
    window.confButton.click()   
    
if __name__ == "main":
    main()
        
        

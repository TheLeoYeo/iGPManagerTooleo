from threading import Thread

from util.utils import join
import sys
sys.path.append(join("gui","components",uplevel=2))


from PyQt5 import QtWidgets

from gui.controllers.main_controller import Main as MainWindow
from gui.styles import appStyles
from igp.service.accounts import AccountIterator
from igp.util.tools import output


class Main():
    def main(self):
        output("Started application", log_only=True)
        # Create app object
        self.app = QtWidgets.QApplication(sys.argv)
        self.app.setStyleSheet(appStyles)

        window = MainWindow() 
        window.show()
        
        self.collector = Thread(args=[window],target=self.collection)
        self.collector.start()
        # Start the event loop of the app
        sys.exit(self.final())


    def collection(self, window):
        AccountIterator.get_instance(minimised=True)
        window.refreshButton.click()
        
        
    def final(self):
        self.app.exec()
        output("Exited application\n", log_only=True)
        
    
if __name__ == "main":
    Main().main()
        
        

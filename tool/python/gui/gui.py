from util.utils import join
import sys
sys.path.append(join("gui","components",uplevel=2))

from PyQt5 import QtWidgets, QtCore

from gui.controllers.load_controller import LoadScreen
from gui.controllers.main_controller import Main as MainWindow
from gui.styles import appStyles
from igp.util.tools import output


class Main():
    def main(self):
        output("Started application", log_only=True)
        # Create app object
        if hasattr(QtCore.Qt, 'AA_EnableHighDpiScaling'):
            QtWidgets.QApplication.setAttribute(QtCore.Qt.AA_EnableHighDpiScaling, True)
        if hasattr(QtCore.Qt, 'AA_UseHighDpiPixmaps'):
            QtWidgets.QApplication.setAttribute(QtCore.Qt.AA_UseHighDpiPixmaps, True)
        
        self.app = QtWidgets.QApplication(sys.argv)
        self.app.setStyleSheet(appStyles)
        
        self.load = LoadScreen()
        self.load.show()   
        
        self.window = MainWindow(self.load)
           
        sys.exit(self.final())
        
        
    def final(self):
        # Start the event loop of the app
        self.app.exec()
        
        # app stopped executing, exit the app
        output("Exited application\n", log_only=True)
        
    
if __name__ == "main":
    Main().main()      

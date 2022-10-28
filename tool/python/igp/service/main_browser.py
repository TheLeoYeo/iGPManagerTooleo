import atexit

from selenium import webdriver
from selenium.webdriver.firefox.options import Options
from selenium.webdriver.firefox.service import Service as FirefoxService
from selenium.webdriver.support import expected_conditions as ec
from selenium.webdriver.support.ui import WebDriverWait
from webdriver_manager.firefox import GeckoDriverManager

from igp.util.tools import output


class BrowserWindow():
    handle: str = None

    def __init__(self, handle: str):
        self.handle = handle
        

class MainBrowser(webdriver.Firefox):
    winstance = None
    option: Options = None
    driver: webdriver.Firefox = None
    stay_minimised = False

    @staticmethod
    def get_instance(minimised:bool=False):
        if not MainBrowser.winstance:
            MainBrowser.winstance = MainBrowser(minimised)
        
        return MainBrowser.winstance
    

    def __init__(self, minimised:bool=False):
        self.stay_minimised = minimised
        self.option = Options()
        self.try_maximise()
        webdriver.Firefox.__init__(self, options=self.option, service=FirefoxService(GeckoDriverManager().install()))

 
    def open_window(self, url: str) -> BrowserWindow:

        all_handles = self.window_handles
        num_windows = len(all_handles)

        self.execute_script(f"window.open('{url}')")
        WebDriverWait(self, 10).until(ec.number_of_windows_to_be(num_windows+1))
        all_handles = self.window_handles

        new_handle = all_handles[num_windows]
        new_window = BrowserWindow(new_handle)
        self.to_window(new_window)
        return new_window


    def to_window(self, window: BrowserWindow) -> bool:
        self.switch_to.window(window.handle)
        
    """
    def close_current_window(self):
        try:
            num_windows = len(self.window_handles)
            self.close()
            self.switch_to.window(self.window_handles[0])
        except Exception:
            output("Tried to close a tab when they were all already closed", log_only=True)"""


    def close_specific_window(self, window: BrowserWindow):
        if window:
            try:
                self.to_window(window)
                self.close()
                output(f"Specific tab has been closed", log_only=True)
                self.switch_to.window(self.window_handles[0])
            except Exception:
                output("Tried to close a tab which did not exist")


    def try_maximise(self):
        if self.stay_minimised:
            self.option.add_argument("--headless")
            return


def exit_handler():
    MainBrowser.get_instance().quit()

atexit.register(exit_handler)

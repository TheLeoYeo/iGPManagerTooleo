from datetime import datetime
import time

from selenium.common.exceptions import ElementClickInterceptedException
from selenium.webdriver.remote.webelement import WebElement
from util.utils import join


def replace_if_gone(file_dir:str, default:str=""):
    # create file if not present   
    open(file_dir, "a").close()
    
    # collect number of lines
    lines = 0
    with open(file_dir, "r") as file:
        lines = file.readlines()
    
    # add default line if empty
    with open(file_dir, "a") as file:
        if len(lines) == 0:
            file.write(default)
    

def output(message:str, log_only=False, screen_only=False):
    message = message.__str__()
    if not screen_only:
        replace_if_gone(log_dir())
        with open(log_dir(), "a") as log_file:
            log_file.write(f"[{datetime.now()}] {message}\n")
    
    if not log_only:
        Output.output(message)  


LOGDIR = ("igp","results","log.txt")
def log_dir():
    return join(*LOGDIR, uplevel=2)
    

class Listener():
    def handle(self):
        pass  

    
class Output():
    listeners:list[Listener] = []
    def output(message:str):
        for listener in Output.listeners:
            listener.handle(message)
    
    def add_listener(object:Listener):
        Output.listeners.append(object)
        
        
def click(button:WebElement, tries = 10):
    # try to click a maximum of 10 times
    if tries > 10:
        tries = 10
        
    # try to click button
    try:
        button.click()
    # specifically catch error where stupid curtain appears in front of button
    except ElementClickInterceptedException:
        # decrement tries
        tries -= 1
        # no more tries, raise the error as there might be a bigger problem here
        if tries == 0:
            raise ElementClickInterceptedException
        
        # wait an amount of time, try again. Wait longer the more tries we have done
        time.sleep(0.5 * (11 - tries))
        click(button, tries)

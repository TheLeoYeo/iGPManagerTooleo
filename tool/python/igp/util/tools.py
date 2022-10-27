from datetime import datetime

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
    

def output(message:str, log_only=False):
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

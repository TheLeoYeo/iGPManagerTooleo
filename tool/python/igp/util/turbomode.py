import time

from igp.util.tools import output


class TurboMode():
    '''A class for controlling whether turbo-mode is on or not
    Turbo mode allows commands to be performed ASAP if on, 
    turbowaits can be used to wait an arbitrary amount of time if turbo mode is off'''
    
    # determines whether program is in turbo-mode or not
    turbo = False
    
    def toggle_turbo():
        TurboMode.turbo = not TurboMode.turbo
        return TurboMode.turbo
    

def turbo_wait(seconds:int=5):
    '''Wait an arbitrary amount of time before continuing if turbo mode is off.
    It's a good idea to put these right after a loading of a page or something major'''
    
    if not TurboMode.turbo:
        time.sleep(seconds)
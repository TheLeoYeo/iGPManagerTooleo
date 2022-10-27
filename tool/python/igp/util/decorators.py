import functools
import inspect
from typing import Callable

from igp.service.base_igp_account import BaseIGPaccount
from igp.util.tools import output


class Command():
    def __init__(self, alias:str, function:Callable, param_names:dict):
        self.alias = alias
        self.function = function
        self.params:dict = param_names
       
        
    def perform(self, account:BaseIGPaccount):
        self.function(account, **self.params)

   
    def __str__(self):
        return self.alias
    
    
    def help(self):
        return self.__str__()


def igpcommand(_func:Callable=None, *, page:str=None, alias:str=None):
    def decorator_command(func:Callable):
        _alias = alias
        if not _alias:
            _alias = func.__name__
            
            
        @functools.wraps(func)
        def wrapper(self:BaseIGPaccount, *args, **kwargs):
            output(f"Trying to do task '{_alias}'")
            
            if not self.driver:
                output("Could not perform task because the webdriver was not properly initialised.")
                return

            if not self.logged_in():
                self.login()
            
            if not self.logged_in():
                output("Could not perform task because log in failed")
                return
            
            if page and self.driver.current_url != page:
                self.driver.get(page)
            
            func(self, *args, **kwargs)
            output(f"Finished doing task '{_alias}'")
        
        
        argspec = inspect.getfullargspec(func)
        param_names = dict.fromkeys(argspec[0][1:])
        values = argspec[3]
        for index, param in enumerate(param_names.keys()):
            param_names[param] = values[index]
        
        BaseIGPaccount.commands.append(Command(_alias, wrapper, param_names))
        return wrapper
    
    if not _func:
        return decorator_command
    
    else:
        return decorator_command(_func)

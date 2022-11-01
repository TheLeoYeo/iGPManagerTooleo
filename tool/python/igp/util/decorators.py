import functools
import inspect
from typing import Callable

from igp.service.base_igp_account import BaseIGPaccount
from igp.util.tools import output
from igp.service.modifier.modifier import BaseModifier
from igp.util.exceptions import BadModifierException


class Command():
    def __init__(self, alias:str, function:Callable, help:str=None, modifier:BaseModifier=None):
        self.alias = alias
        self.function = function
        self.help_text = alias
        if help:
            self.help_text = help
            
        if modifier:
            self.modifier = modifier
        else:
            self.modifier = BaseModifier()
       
        
    def perform(self, account:BaseIGPaccount):
        params = self.modifier.params()
        self.function(account, **params)

   
    def __str__(self):
        return self.alias
    
    
    def help(self):
        return self.help_text


def igpcommand(_func:Callable=None, *, page:str=None, alias:str=None, help:str=None, modifier:BaseModifier=None):
    def decorator_command(func:Callable):
        _alias = alias
        if not _alias:
            _alias = func.__name__
        
        _help = help
        if not _help:
            _help = func.__doc__
            
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
            output(f"Finished doing task '{_alias}'", log_only=True)
        
        
        if modifier:
            argspec = inspect.getfullargspec(func)
            # make sure modifier includes all parameters
            req_params = argspec[0][1:]
            mod_params = modifier.params()
            if len(req_params) != len(mod_params):
                raise BadModifierException(f"Wrong number of parameters found in modifier ")
            
            for req_param in req_params:
                if req_param not in mod_params:
                    raise BadModifierException(f"Parameter '{req_param}' was not found in modifier")
        
        BaseIGPaccount.commands.append(Command(_alias, wrapper, _help, modifier))
        return wrapper
    
    if not _func:
        return decorator_command
    
    else:
        return decorator_command(_func)

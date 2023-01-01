from enum import Enum
import functools
import inspect
from typing import Callable

from igp.service.base_igp_account import BaseIGPaccount
from igp.service.commands.tasks import Categories, Category
from igp.service.modifier.modifier import BaseModifier
from igp.util.tools import output
from igp.util.exceptions import BadModifierException
from igp.util.turbomode import turbo_wait


class CommandType(Enum):
    DEFAULT = 0
    ACCOUNTLESS = 1


class Command():
    def __init__(self, alias:str, function:Callable, help:str=None, modifier:BaseModifier=None, category:Category=None, type:CommandType=None):
        self.alias = alias
        self.function = function
        self.help_text = alias
        
        if help:
            self.help_text = help
            
        if modifier:
            self.modifier = modifier
        else:
            self.modifier = BaseModifier()
            
        if category:
            self.category = category
        else:
            self.category = Categories.MISC
        
        self.type = CommandType.DEFAULT
        if type == CommandType.ACCOUNTLESS:
            self.type = type
            self.alias = "_" + self.alias
            self.help_text = f"Accountless task\n{self.help_text}"
            
            
        
    def perform(self, account:BaseIGPaccount):
        params = self.modifier.params()
        self.function(account, **params)

   
    def __str__(self):
        return self.alias
    
    
    def help(self):
        return self.help_text
    
    
    
class CommandDecorator():
    def outer_wrapper(obj, func:Callable, _alias:str, page:str):
        @functools.wraps(func)
        def wrapper(self:BaseIGPaccount, *args, **kwargs):
            output(f"Trying to do task '{_alias}'")
            
            if not self.driver:
                output("Could not perform task because the webdriver was not properly initialised.")
                return
            
            self.tuto_skip()
            
            if not self.logged_in():
                self.login()
            
            if not self.logged_in():
                output("Could not perform task because log in failed")
                return
            
            if page and self.driver.current_url != page:
                self.driver.get(page)
                turbo_wait()
            
            self.tuto_skip()
            
            func(self, *args, **kwargs)
            output(f"Finished doing task '{_alias}'", log_only=True)
        return wrapper
    
    
    def command(self, _func:Callable=None, *, page:str=None, alias:str=None, help:str=None, 
                modifier:BaseModifier=None, category:Category=None, type:CommandType=None):
        
        def decorator_command(func:Callable):
            _alias = alias
            if not _alias:
                _alias = func.__name__
            
            _help = help
            if not _help:
                _help = func.__doc__
        
            if modifier:
                # make sure modifier includes all parameters
                argspec = inspect.getfullargspec(func)
                req_params = argspec[0][1:]
                mod_params = modifier.params()
                if len(req_params) != len(mod_params):
                    raise BadModifierException(f"Wrong number of parameters found in modifier ")
                
                for req_param in req_params:
                    if req_param not in mod_params:
                        raise BadModifierException(f"Parameter '{req_param}' was not found in modifier")
                               
            wrapper:Callable = self.outer_wrapper(func, _alias, page)
            
            BaseIGPaccount.commands.append(Command(_alias, wrapper, _help, modifier, category, type))
            return wrapper
        
        if not _func:
            return decorator_command     
        else:
            return decorator_command(_func)
        
        
class SimpleCommandDecorator(CommandDecorator):
    '''Similar to a normal command decorator except the created function will start completely logged out'''
    
    def outer_wrapper(obj, func, _alias, page):
        @functools.wraps(func)
        def wrapper(self:BaseIGPaccount, *args, **kwargs):
            output(f"Trying to do task '{_alias}'")
            
            if not self.driver:
                output("Could not perform task because the webdriver was not properly initialised.")
                return
            
            if page and self.driver.current_url != page:
                self.driver.get(page)
                turbo_wait()
                     
            if self.logged_in():
                self.log_out()
                
            
            func(self, *args, **kwargs)
            output(f"Finished doing task '{_alias}'", log_only=True)
        return wrapper


def igpcommand(_func:Callable=None, *, page:str=None, alias:str=None, help:str=None, 
                modifier:BaseModifier=None, category:Category=None, type:CommandType=None):
    
    return CommandDecorator().command(_func=_func, page=page, alias=alias, help=help, 
                            modifier=modifier, category=category, type=type)


def simpleigpcommand(_func:Callable=None, *, page:str=None, alias:str=None, help:str=None, 
                modifier:BaseModifier=None, category:Category=None, type:CommandType=None):
    
    return SimpleCommandDecorator().command(_func=_func, page=page, alias=alias, help=help, 
                                  modifier=modifier, category=category, type=type)

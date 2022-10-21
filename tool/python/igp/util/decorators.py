import functools

from igp.service.base_igp_account import BaseIGPaccount

class Command():
    def __init__(self, alias, function):
        self.alias = alias
        self.function = function
    
    def __str__(self):
        return self.alias

def igpcommand(_func=None, *args, **kwargs):
    def decorator_command(func, alias=None, page=None):  
        if not alias:
            alias = func.__name__
            
        @functools.wraps(func)
        def wrapper(self:BaseIGPaccount, *args, **kwargs):
            if not self.logged_in():
                self.login()
            
            if not self.logged_in():
                print("Could not log in to perform command")
                return
            
            if page and self.driver.current_url != page:
                self.driver.get(page)
                
            return func(self, *args, **kwargs)
        
        BaseIGPaccount.commands.append(Command(alias, wrapper))
        return wrapper
    

    if not _func:
        return decorator_command
    
    else:
        return decorator_command(_func, args, kwargs)

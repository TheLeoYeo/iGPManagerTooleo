from enum import Enum


class Field():
    def __init__(self, param_name, value=None):
        self.param_name = param_name
        self.value = value
    
    
    def is_valid(self) -> bool:
        return True
    
    def __str__(self):
        return self.param_name
    
    def help(self):
        return f"edit {self.param_name}"
    
    def value_of(self):
        return self.value


class IntegerField(Field):
    def __init__(self, param_name, lb=0, ub=1000, number:int=None):
        if not number:
            number = lb
            
        Field.__init__(self, param_name, number)
        self.lower = lb
        self.upper = ub
        
        
    def is_valid(self) -> bool:
        try: 
            self.value = int(self.value)
        except:
            return False
        
        return self.value >= self.lower and self.value <= self.upper


    def help(self):
        return f"{self.param_name} must be between {self.lower} and {self.upper}"
          
        
class OptionField(Field):
    def __init__(self, param_name, options:list[Enum], index:int=0):
        Field.__init__(self, param_name, index)
        self.options = options
        
        
    def is_valid(self) -> bool:        
        return self.value >= 0 and self.value < len(self.options)
    
    def value_of(self):
        return self.options[self.value]
    
    def decrement(self):
        self.value = (self.value - 1) % len(self.options)
    
    def increment(self):
        self.value = (self.value + 1) % len(self.options)


class BaseModifier():
    def __init__(self, *fields):
        self.fields:list[Field] = list(fields)
        
        
    def params(self):
        params = {}
        for field in self.fields:
            params[field.param_name] = field.value_of()
            
        return params
        
        
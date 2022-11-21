from enum import Enum

from util.utils import ALL_STINT_NUMBERS, ALL_TYRE_TYPES, DEFAULT_LENGTH, StintNumbers, Tyres


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
        
    def help(self):
        return f"click on the left/right arrow to change {self.param_name}"
    

class TyresField(Field):
    value:list[int] = None
    
    def __init__(self, param_name):
        Field.__init__(self, param_name, [])
        for i in range(DEFAULT_LENGTH):
            self.add_stint()
    
    
    def increment(self, index):
        self.value[index] = (self.value[index] + 1) % len(ALL_TYRE_TYPES)
    
    
    def remove_last_stint(self):
        self.value.pop()
    
    
    def value_of(self):
        return list(map(self.converter, self.value))
    
    
    def value_of_index(self, index):
        return self.converter(self.value[index])
    
    
    def converter(self, index:int)-> Tyres:
        return ALL_TYRE_TYPES[index]
    
    
    def add_stint(self):
        self.value.append(0)


    def is_valid(self) -> bool:
        for tyre_val in self.value: 
            if not (tyre_val >= 0 and tyre_val < len(ALL_TYRE_TYPES)):
                return False
        return True
        
        
    def help(self):
        return "Tyre must be SS, S, M, H, I or W"


class StintsField(Field):
    value:list[IntegerField] = None
    
    def __init__(self, param_name, lb=1, ub=150):
        Field.__init__(self, param_name, [])
        self.lower = lb
        self.upper = ub
        
        for i in range(DEFAULT_LENGTH):
            self.add_stint()
        
    
    def add_stint(self):
        self.value.append(IntegerField(self.param_name, self.lower, self.upper, 20))


    def set_length(self, index, value):
        self.value[index].value = value
        
        
    def remove_last_stint(self):
        self.value.pop()
    
    
    def value_of(self):
        return list(map(self.converter, self.value))
    
    
    def value_of_index(self, index):
        return self.converter(self.value[index])
    
    
    def converter(self, field:IntegerField)-> int:
        return field.value
    
    
    def is_valid(self) -> bool:
        for stint_field in self.value: 
            if not stint_field.is_valid():
                return False
        return True
    
    
    def help(self):
        return f"each stint length must be between {self.lower} and {self.upper}"


class NumberOfStintsField(OptionField):
    value:int
    options:list[StintNumbers]
    def __init__(self, param_name, tyre_field:TyresField, stint_field:StintsField):
        OptionField.__init__(self, param_name, ALL_STINT_NUMBERS, 1)
        self.tyre_field = tyre_field
        self.stint_field = stint_field
    
    
    def is_valid(self) -> bool:
        if not super().is_valid():
            return False
        
        if not self.tyre_field.is_valid():
            return False
        
        return self.stint_field.is_valid()

 
    def decrement(self) -> bool:
        if self.value > 0:
            self.value -= 1
            self.tyre_field.remove_last_stint()
            self.stint_field.remove_last_stint()
            return True
        return False


    def increment(self) -> bool:
        if self.value < len(self.options) - 1:
            self.value += 1
            self.tyre_field.add_stint()
            self.stint_field.add_stint()
            return True
        return False
    
    
class BaseModifier():
    def __init__(self, *fields):
        self.fields:list[Field] = list(fields)
        
        
    def params(self):
        params = {}
        for field in self.fields:
            params[field.param_name] = field.value_of()
            
        return params
        
        
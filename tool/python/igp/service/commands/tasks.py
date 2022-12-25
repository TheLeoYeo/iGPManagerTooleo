

class Category():
    def __init__(self, name):
        self.name = name
        

class Categories():
    MISC = Category("Misc. Tasks")
    TRAINING = Category("Training Tasks")
    CAR = Category("Car Repair Tasks")
    SETUP = Category("Setup Tasks")
    ALL = [TRAINING, CAR, SETUP, MISC]

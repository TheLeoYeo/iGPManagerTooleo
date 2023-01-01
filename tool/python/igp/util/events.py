class Event():
    def __init__(self, source=None, value=None):
        self.source = source
        self.value = value
        
class AccountsUpdatedEvent(Event):
    pass

class JobsUpdatedEvent(Event):
    pass

class JobAddedEvent(Event):
    pass

class JobRemovedEvent(Event):
    pass

class AccountNameUpdatedEvent(Event):
    pass

class ConfirmedLogInEvent(Event):
    pass

class AccountRemovedEvent(Event):
    pass

class AccountAddedEvent(Event):
    pass

class AccountCreatedEvent(Event):
    pass

class AllContainersReadyEvent(Event):
    pass
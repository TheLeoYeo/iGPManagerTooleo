from igp.service.igpaccount import IGPaccount
from igp.util.decorators import Command
from igp.util.events import Event


class Job():
    accounts:list[IGPaccount] = []
    commands:list[Command] = []
    
    def __init__(self, accounts:list[IGPaccount], commands:list[Command]):
        self.accounts = accounts
        self.commands = commands
        self.number = len(AllJobs.jobs)
        AllJobs.append(self)
        
        
    def perform(self):
        for account in self.accounts:
            for command in self.commands:
                command.function(account)


    def cancel(self):
        AllJobs.jobs.remove(self)
        
              
    def __str__(self):
        return f"{self.number}: {', '.join([account.__str__() for account in self.accounts])}"


class AllJobs():
    jobs:list[Job] = []
    listeners = []
    
    def append(job:Job):
        AllJobs.jobs.append(job)
        AllJobs.changed()

  
    def add_to_listeners(object):
        AllJobs.listeners.append(object)
        
        
    def changed():
        for listener in AllJobs.listeners:
            listener.handle(Event.JOBS_UPDATED)
            
    def perform():
        for job in AllJobs.jobs:
            job.perform()
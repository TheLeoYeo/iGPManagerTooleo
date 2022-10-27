from igp.service.igpaccount import IGPaccount
from igp.util.decorators import Command
from igp.util.events import Event
from igp.util.tools import output


class Job():
    def __init__(self, accounts:list[IGPaccount], commands:list[Command]):
        self.accounts = accounts
        self.commands = commands
        self.number = len(AllJobs.jobs)
        AllJobs.append(self)
        
        
    def perform(self):
        for account in self.accounts:
            for command in self.commands:
                command.perform(account)
        self.cancel()


    def cancel(self):
        AllJobs.remove(self)
        
              
    def __str__(self):
        return f"{', '.join([account.__str__() for account in self.accounts])}"
    
    
    def help(self):
        return f"Doing {', '.join([command.__str__() for command in self.commands])}"


class AllJobs():
    jobs:list[Job] = []
    listeners = []
    
    
    def append(job:Job):
        output("Added job")
        AllJobs.jobs.append(job)
        AllJobs.changed()
        
        
    def remove(job:Job):
        AllJobs.jobs.remove(job)
        AllJobs.changed()

  
    def add_to_listeners(object):
        AllJobs.listeners.append(object)
        
        
    def changed():
        for listener in AllJobs.listeners:
            listener.handle(Event.JOBS_UPDATED)

    
    def perform():
        jobs = AllJobs.jobs.copy()
        for job in jobs:
            print(job.help())
            job.perform()
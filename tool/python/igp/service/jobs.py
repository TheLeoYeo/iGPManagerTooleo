from igp.service.igpaccount import IGPaccount
from igp.util.decorators import Command
from igp.util.events import Event, JobAddedEvent, JobRemovedEvent
from igp.util.tools import output


class Job():
    def __init__(self, accounts:list[IGPaccount], commands:list[Command]):
        if len(accounts) == 0:
            output("Select at least one account")
            return
        
        if len(commands) == 0:
            output("Select at least one task")
            return
        
        self.accounts = accounts
        self.commands = commands
        self.number = len(AllJobs.jobs)
        AllJobs.append(self)
        
        
    def perform(self):
        for account in self.accounts:
            for command in self.commands:
                command.perform(account)
        
              
    def __str__(self):
        return f"{', '.join([account.__str__() for account in self.accounts])}"
    
    
    def help(self):
        return f"Doing {', '.join([command.__str__() for command in self.commands])}"
    
    def command_string(self):
        return f"{', '.join([command.__str__() for command in self.commands])}"


class AllJobs():
    jobs:list[Job] = []
    listeners = []
    
    
    def append(job:Job):
        output(f"Added job {job.command_string()}")
        output(f"Job is doing this on {job.__str__()}", log_only=True)
        AllJobs.jobs.append(job)
        AllJobs.changed(JobAddedEvent(AllJobs, job))
        
        
    def remove(job:Job):
        output(f"Removed job {job.command_string()}", log_only=True)
        AllJobs.jobs.remove(job)
        AllJobs.changed(JobRemovedEvent(AllJobs, job))

  
    def add_to_listeners(object):
        AllJobs.listeners.append(object)
        
        
    def changed(event:Event):
        for listener in AllJobs.listeners:
            listener.handle(event)
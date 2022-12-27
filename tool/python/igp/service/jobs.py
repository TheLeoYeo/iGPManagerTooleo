from igp.service.igpaccount import MONITOR_ACCOUNT, IGPaccount
from igp.util.decorators import Command, CommandType
from igp.util.events import Event, JobAddedEvent, JobRemovedEvent
from igp.util.tools import output


class Job():
    modifier = None
    def __init__(self, accounts:list[IGPaccount], commands:list[Command]):
        if len(commands) == 0:
            output("Select at least one task")
            return
              
        # check all commands are of the same type
        prev_type = None
        for command in commands:
            if prev_type and prev_type != command.type:
                output("All selected commands must be of the same type: Default/Accountless")
                return
            prev_type = command.type
        
        # if commands are all accountless, make sure no accounts have been selected
        if prev_type == CommandType.ACCOUNTLESS:
            if len(accounts) > 0:
                output("Deselect all accounts when using Accountless commands")
                return
            else:
                accounts = [MONITOR_ACCOUNT]
            
        # commands are all default, check if we have selected accounts
        elif len(accounts) == 0:
            output("Select at least one account")
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
from threading import Thread
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


    def cancel(self):
        AllJobs.remove(self)
        
              
    def __str__(self):
        return f"{', '.join([account.__str__() for account in self.accounts])}"
    
    
    def help(self):
        return f"Doing {', '.join([command.__str__() for command in self.commands])}"
    
    def command_string(self):
        return f"{', '.join([command.__str__() for command in self.commands])}"


class AllJobs():
    jobs:list[Job] = []
    listeners = []
    performing = False
    loop:Thread = None
    
    
    def append(job:Job):
        output(f"Added job {job.command_string()}")
        output(f"Job is doing this on {job.__str__()}", log_only=True)
        AllJobs.jobs.append(job)
        AllJobs.changed(Event.JOBS_UPDATED)
        
        
    def remove(job:Job):
        output(f"Removed job")
        output(f"Removed job {job.command_string()}", log_only=True)
        AllJobs.jobs.remove(job)

  
    def add_to_listeners(object):
        AllJobs.listeners.append(object)
        
        
    def changed(event:Event):
        for listener in AllJobs.listeners:
            listener.handle(event)

    """
    def perform():
        # toggle pause/unpause 
        AllJobs.performing = not AllJobs.performing
        
        # start new performing thread as we aren't currently doing anything
        if not (AllJobs.loop and AllJobs.loop.is_alive()):
            AllJobs.loop = Thread(target=AllJobs.perform_loop)
            AllJobs.loop.start()"""
        
    
    def perform_loop():
        jobs = AllJobs.jobs.copy()
        for job in jobs:
            job.perform()
        
        print("outed")
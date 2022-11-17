from igp.util.events import AllContainersReadyEvent


"""A class which stores a list of containers that have finished loading
    once the number of containers reaches a threshold, an event will be sent
    out to all listeners indicating that enough containers are ready!
    
    Uses singleton pattern so only one instance of this class can exist at a time
"""
class ReadyContainers():
    ready = False
    containers = []
    listeners = []
    instance = None
    ready_threshold = 1
    
    def get_instance():
        if ReadyContainers.instance:
            return ReadyContainers.instance
        
        ReadyContainers.instance = ReadyContainers()
        return ReadyContainers.instance
    
    
    def add_ready(self, container):
        self.containers.append(container)
        if len(self.containers) == self.ready_threshold:
            self.ready = True
            for listener in self.listeners:
                listener.handle(AllContainersReadyEvent())


    def add_listener(self, object):
        self.listeners.append(object)

#=======================================================================================================================
# EventSource
#=======================================================================================================================
class EventSource(object):
    
    BOX_CREATED = 1
    BOX_MODIFIED = 2
    BOX_DELETED = 4
    ENTRY_CREATED = 8
    ENTRY_MODIFIED = 16
    ENTRY_DELETED = 32
    CREATION = BOX_CREATED + ENTRY_CREATED
    MODIFICATION = BOX_MODIFIED + ENTRY_MODIFIED
    DELETION = BOX_DELETED + ENTRY_DELETED
    ALL = CREATION + DELETION + MODIFICATION
    BOX_EVENTS = BOX_CREATED + BOX_MODIFIED + BOX_DELETED
    ENTRY_EVENTS = ENTRY_CREATED + ENTRY_MODIFIED + ENTRY_DELETED
    
    __methods = { BOX_CREATED: "onBoxCreated",
                 BOX_MODIFIED: "onBoxModified",
                 BOX_DELETED: "onBoxDeleted",
                 ENTRY_CREATED: "onEntryCreated",
                 ENTRY_MODIFIED: "onEntryModified",
                 ENTRY_DELETED: "onEntryDeleted" }
    
    __eventListeners = None
    
    def isListenable(self, target, type_):
        """Returns whether a given type_ of event can be listened on this object or not. 
        The default implementation always returns true, and can be subclassed. """
        return True
    
    def getListenedEvents(self, listener, target):
        return listener.__tkzes__listening_to_events[self][target]
    
    def setListenedEvents(self, listener, target, events):
        if not hasattr(listener, "__tkzes__listening_to_events"):
            listener.__tkzes__listening_to_events = {}
        if not self in listener.__tkzes__listening_to_events.keys():
            listener.__tkzes__listening_to_events[self] = {}
            
        listener.__tkzes__listening_to_events[self][target] = events
    
    def listen(self, listener, target=None, eventTypes=ALL):
        if not self.__eventListeners: self.__eventListeners = {}
        if not self.isListenable(target, type):
            print("This event source can't be listened for this target/type.")
            return
        
        if not (eventTypes & EventSource.ALL):
            print("This listener can't listen to anything. Not added.")
            return
        
        if not target:
            target = self
        
        if not target in self.__eventListeners.keys():
            self.__eventListeners[target] = set()
        
        if not listener in self.__eventListeners[target]:
            self.__eventListeners[target].add(listener)
            
        self.setListenedEvents(listener, target, eventTypes)
        
        return True
        
    def unlisten(self, listener, target=None, eventTypes=ALL):
        if target:
            targets = [ target ]
        else:
            targets = self.__eventListeners.keys()
            
        for t in targets:
            if listener in self.__eventListeners[t]:
                remains = self.getListenedEvents(listener, t) - eventTypes
                if not (remains):
                    # print ("All removed. Was listening {0} and removed {1}".format(self.getListenedEvents(listener, t), eventTypes))
                    self.__eventListeners[t].remove(listener)
                else:
                    self.setListenedEvents(listener, t, remains)
                    # print("Remains: {0}".format(remains))
                    
    def getListeners(self, target=None, eventTypes=ALL):
        ret = set()
        if target:
            targets = [ target ]
        else:
            targets = self.__eventListeners.keys()
            
        for t in targets:
            if t in self.__eventListeners.keys():
                for l in self.__eventListeners[t]:
                    if self.getListenedEvents(l, t) & eventTypes:
                        ret.add(l)
        return ret
                    
    def trigger(self, source, object_, type_, exclude=[]):
        
        if not type_ in self.__methods.keys(): 
            raise Exception("Illegal event type_ {0}".format(type_))
        
        method = self.__methods[type_]
        
        listeners = self.getListeners(source, type_)
        # Add listeners who listen to the repository if the event was triggered on a repository item.
        if hasattr(object_, "repository"):
            listeners.union(self.getListeners(object_.repository, type_))
        
        try:
            listeners.difference_update(exclude)
        except TypeError:
            listeners.remove(exclude)
        
        for l in listeners:
            getattr(l, method)(source, object_)
      
#=======================================================================================================================
# DelegatedEventSource
#=======================================================================================================================
class DelegatedEventSource(object):
    
    __eventDelegate = None
    
    def __init__(self, eventDelegate):
        self.__eventDelegate = eventDelegate
    
    def listen(self, listener, eventTypes=EventSource.ALL, target=None):
        self.__eventDelegate.listen(listener, target, eventTypes)
    
    def unlisten(self, listener, eventTypes=EventSource.ALL, target=None):
        self.__eventDelegate.listen(listener, target, eventTypes)

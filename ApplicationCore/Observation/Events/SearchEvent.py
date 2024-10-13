from enum import Enum

class SearchEvent:
    class EventType(Enum):
        STARTED = 1
        FINISHED = 2

    def __init__(self, event_type):
        self.event_type = event_type
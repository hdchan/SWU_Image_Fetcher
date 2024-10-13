import weakref


class ObservationTower:

    def __init__(self):
         self.subscribers = {}

    def notify(self, event):
        # filter dead subscribers
        # self.subscribers[event.__class__][0]() is None
        filtered_subscribers = filter(lambda x: x() is not None, self.subscribers[event.__class__])
        self.subscribers[event.__class__] = list(filtered_subscribers)
        if event.__class__ in self.subscribers:
            for s in self.subscribers[event.__class__]:
                 s().handle_observation_tower_event(event)

    def subscribe(self, subscriber, event):
        if event not in self.subscribers:
            self.subscribers[event] = []
        self.subscribers[event].append(weakref.ref(subscriber))
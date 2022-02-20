

class CompositeView:
    def __init__(self):
        self.views = [];

    def add(self, view):
        self.views.append(view)

    def receiveMessages(self, messages):
        for v in self.views:
            v.receiveMessages(messages)

    def receiveMessageToMe(self, messages):
        for v in self.views:
            v.receiveMessageToMe(messages)
    
    def receiveAccToMe(self, message):
        for v in self.views:
            v.receiveAccToMe(message)
    
    def receivedRouteMessage(self, message):
        for v in self.views:
            v.receivedRouteMessage(message)

    def receivedNoRouteMessage(self, message):
        for v in self.views:
            v.receivedNoRouteMessage(message)

    def sendMessage(self, message):
        for v in self.views:
            v.sendMessage(message)
    
    def update(self, pymeshAdapter):
        for v in self.views:
            v.update(pymeshAdapter)
    
    def receivedFindMessage(self, message):
        for v in self.views:
            v.receivedFindMessage(message)
    def suggestRoute(self, message):
        for v in self.views:
            v.suggestRoute(message)
    def passOnFindMessage(self, message):
        for v in self.views:
            v.passOnFindMessage(message)
    def receiveAccToOther(self, message):
        for v in self.views:
            v.receiveAccToOther(message)

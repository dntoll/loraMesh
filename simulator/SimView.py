

class SimView:
    
    def __init__(self, nodeName):
        self.nodeName = nodeName
    
    def receiveMessages(self, messages):
        if len(messages) > 0:
            print(self.nodeName + "receiveMessages", flush=True)

    def receiveMessageToMe(self, messages):
        print(self.nodeName + "receiveMessageToMe", flush=True)
    
    def receiveAccToMe(self, message):
        print(self.nodeName + "receiveAccToMe", flush=True)
    
    def receivedRouteMessage(self, message):
        print(self.nodeName + "receivedRouteMessage", flush=True)

    def receivedNoRouteMessage(self, message):
        print(self.nodeName + "receivedNoRouteMessage", flush=True)

    def sendMessage(self, message):
        print(self.nodeName + "sendMessage", flush=True)
    
    def showIps(self, ips):
        print(self.nodeName + "showIps", flush=True)
    
    def update(self, pymeshAdapter):
        print(self.nodeName + "update", flush=True)

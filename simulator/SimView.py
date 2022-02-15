from lib.ANSIEscape import ANSIEscape

class SimView:
    
    def __init__(self, nodeName):
        self.nodeName = str(nodeName) + ": "
        self.nodeID = nodeName
    
    def receiveMessages(self, messages):
        #if len(messages) > 0:
        #    print(self.nodeName + "receiveMessages", flush=True)
        return

    def receiveMessageToMe(self, message):
        self.printMessage("receiveMessageToMe", message)
    
    def receiveAccToMe(self, message):
        self.printMessage("receiveAccToMe", message)
    
    def receivedRouteMessage(self, message):
        self.printMessage("receivedRouteMessage", message)

    def receivedNoRouteMessage(self, message):
        self.printMessage("receivedNoRouteMessage", message)

    def sendMessage(self, message):
        self.printMessage("sendMessage", message)
    
    def showIps(self, ips):
        print(self.nodeName + "showIps", flush=True)
    
    def update(self, pymeshAdapter):
        print(self.nodeName + "update", flush=True)
    
    def receivedFindMessage(self, message):
        self.printMessage("receivedFindMessage", message)
    def suggestRoute(self, message):
        self.printMessage("suggestRoute", message)
    def passOnFindMessage(self, message):
        self.printMessage("passOnFindMessage", message)
    def receiveAccToOther(self, message):
        self.printMessage("receiveAccToOther", message)

        

    def printMessage(self, title, message):
        r = message.getRoute()
        t = message.messageType
        s = message.senderMac
        if message.isAcc():
            t = "acc"
        elif message.isFind():
            t = "find"
        
        
        print(self.nodeName + title + "(" + str(s) + ")" + self._routeToStr(r) + " " + str(t), flush=True)

    
    def _routeToStr(self, route):
        routeStr = "";
        for b in route.getBytes():
            if b is self.nodeID:
                routeStr += ANSIEscape.getTextColor("Green") + "[" + str(b) + "]"+ ANSIEscape.getResetCode() 
            else:
                routeStr += "[" + str(b) + "]"
        return routeStr
from lib.ANSIEscape import ANSIEscape


class SimTestView:
    
    def __init__(self, nodeName):
        self.nodeName = str(nodeName) + ": "
        self.nodeID = nodeName
        self.buffer = []
    
    def receiveMessages(self, messages):
        #if len(messages) > 0:
        #    print(self.nodeName + "receiveMessages", flush=True)
        return

    def receiveMessageToMe(self, message):
        self.processMessage("receiveMessageToMe", message)
    
    def receiveAccToMe(self, message):
        self.processMessage("receiveAccToMe", message)
    
    def receivedRouteMessage(self, message):
        self.processMessage("receivedRouteMessage", message)

    def receivedNoRouteMessage(self, message):
        self.processMessage("receivedNoRouteMessage", message)
        return

    def sendMessage(self, message):
        self.processMessage("sendMessage", message)
       
    def update(self, pymeshAdapter):
        #print(self.nodeName + "update", flush=True)
        return
    
    def receivedFindMessage(self, message):
        self.processMessage("receivedFindMessage", message)
    def suggestRoute(self, message):
        self.processMessage("suggestRoute", message)
    def passOnFindMessage(self, message):
        self.processMessage("passOnFindMessage", message)
    def receiveAccToOther(self, message):
        self.processMessage("receiveAccToOther", message)

        

    def processMessage(self, title, message):
        self.buffer.append(message)
        self._printMessage(title, message)

    def hasMessage(self, messageType):
        for message in self.buffer:
            if message.messageType == messageType:
                return True
        return False

    def hasMessageFrom(self, sender, messageType):
        for message in self.buffer:
            if message.messageType == messageType and message.getRoute().getOrigin() == sender:
                return True
        return False

    def clearMessages(self):
        self.buffer = []


    def _printMessage(self, title, message):
        r = message.getRoute()
        t = message.messageType
        s = message.senderMac
        if message.isAcc():
            t = "acc"
        elif message.isFind():
            t = "fin"
        else:
            t = "mes"
        
        
        print(self.nodeName + title + "(" + str(s) + ")" + self._routeToStr(r) + " " + str(t))

    #TODO: copy paste
    def _routeToStr(self, route):
        routeStr = "";
        for b in route.getBytes():
            if b is self.nodeID:
                routeStr += ANSIEscape.getTextColor("Green") + "[" + str(b) + "]"+ ANSIEscape.getResetCode() 
            else:
                routeStr += "[" + str(b) + "]"
        return routeStr
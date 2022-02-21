from mesh.Message import Message
from mesh.Router import Router
from mesh.Route import Route
from mesh.SendQue import SendQue
from mesh.MessageChecksum import MessageChecksum

#this class implements the mesh network protocol
class MeshController:

    def __init__(self, view, myMac, pycomInterface):
        self.sendQue = SendQue(pycomInterface)
        self.router = Router(pycomInterface, myMac)
        self.myMac = myMac
        self.view = view

    def onReceive(self, message, loraStats):
        
        self.router.deriveRouterData(message, loraStats)

        route = message.getRoute()
        if route.getTarget() is self.myMac:
            self._reachedFinalTarget(message)
        else:
            self._receivedMessageMeantForOther(message)
    
    def getSendQue(self):
        return self.sendQue
        

    def _reachedFinalTarget(self, message):
        if not message.isAcc() or message.isFind():
            self.view.receiveMessageToMe(message)    

            route = message.getRoute()
            newRoute = route.getShortenedRoute(message.senderMac, self.myMac)

            accRoute = newRoute.getBackRoute()
            checksum = MessageChecksum.fromMessage(message)

            self.addToQue(Message(self.myMac, accRoute, Message.TYPE_ACC, checksum.toBytes()))
        elif message.isAcc():
            if self.sendQue.receiveAcc(message):
                self.view.receiveAccToMe(message)

    def _receivedMessageMeantForOther(self, message):    

        route = message.getRoute()

        messageFinalTarget = route.getTarget()
        
        if route.bothInRouteAndOrdered(message.senderMac, self.myMac):
            newRoute = route.getShortenedRoute(message.senderMac, self.myMac)
            relayedMessage = Message(self.myMac, newRoute, message.messageType, bytes(message.contentBytes))
            self.view.receivedRouteMessage(relayedMessage)
            self.addToQue(relayedMessage)
        elif message.isFind() and route.notInRoute(self.myMac):
            self.view.receivedFindMessage(message)
            if self.router.hasRoute(self.myMac, messageFinalTarget):
                fromMeToTarget = self.router.getRoute(self.myMac, messageFinalTarget)
                newRoute = route.expandTail(fromMeToTarget) #prevRoute, prevTarget => prevRoute + fromMetoTarget
                relayedMessage = Message(self.myMac, newRoute, Message.TYPE_MESSAGE, bytes(message.contentBytes))
                self.view.suggestRoute(relayedMessage)
                self.addToQue(relayedMessage)
            else:
                fromMeToTarget = Route(bytes([self.myMac, messageFinalTarget]))
                newRoute = route.expandTail(fromMeToTarget)
                searchMessage = Message(self.myMac, newRoute, Message.TYPE_FIND, bytes(message.contentBytes))
                self.view.passOnFindMessage(searchMessage)
                self.addToQue(searchMessage)
        else:
            self.view.receivedNoRouteMessage(message)

        if message.isAcc():
            if self.sendQue.receiveAcc(message):
                self.view.receiveAccToOther(message)
                relayedMessage = Message(self.myMac, message.getRoute(), Message.TYPE_ACC, bytes(message.contentBytes))
                self.addToQue(relayedMessage)

    def getKnownNeighbors(self):
        return self.neighbors

    def addToQue(self, message):
        self.sendQue.addToQue(message)

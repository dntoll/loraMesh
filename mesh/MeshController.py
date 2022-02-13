from mesh.Message import Message
from mesh.Router import Router
from mesh.SendQue import SendQue
from mesh.MessageChecksum import MessageChecksum

#this class implements the mesh network protocol
class MeshController:

    def __init__(self, view, myMac, pycomInterface):
        self.sendQue = SendQue(pycomInterface)
        self.router = Router(pycomInterface)
        
        self.view = view
        self.myMac = myMac

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
        if message.messageType is Message.TYPE_MESSAGE:
            self.view.receiveMessageToMe(message)    

            route = message.getRoute()
            newRoute = route.getSubRoute(message.senderMac, self.myMac)

            accRoute = newRoute.getBackRoute()
            checksum = MessageChecksum.fromMessage(message)

            self.addToQue(Message(self.myMac, accRoute, Message.TYPE_ACC, checksum.toBytes()))
        elif message.isAcc():
            self.sendQue.receiveAcc(message)
            self.view.receiveAccToMe(message)

    def _receivedMessageMeantForOther(self, message):    

        route = message.getRoute()

        messageFinalTarget = route.getTarget()
        print("Target was " + str(messageFinalTarget))
        if route.IShouldRoute(message.senderMac, self.myMac):
            
            newRoute = route.getSubRoute(message.senderMac, self.myMac)

            relayedMessage = Message(self.myMac, newRoute, message.messageType, bytes(message.contentBytes))
            self.view.receivedRouteMessage(relayedMessage)
            self.addToQue(relayedMessage)            
        else:
            self.view.receivedNoRouteMessage(message)
            #I need not to send it again if I received it from someone downstream from me
        
        if message.isAcc():
            self.sendQue.receiveAcc(message)
            self.view.receiveAccToMe(message)


    def getKnownNeighbors(self):
        return self.neighbors

    def addToQue(self, message):
        self.sendQue.addToQue(message)

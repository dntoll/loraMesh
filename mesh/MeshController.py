from mesh.Message import Message
from mesh.Router import Router

#this class implements the mesh network protocol
class MeshController:

    def __init__(self, view, myMac):
        self.sendQue = []
        self.router = Router()
        
        self.view = view
        self.myMac = myMac

    def onReceive(self, message, loraStats):
        self.router.deriveRouterData(message, loraStats)

        messageFinalTarget = message.getTarget()
        if messageFinalTarget is self.myMac:
            self._reachedFinalTarget(message)
        else:
            self._receivedMessageMeantForOther(message)
    
    def getMessagesInSendQue(self):
        return self.sendQue
        

    def _reachedFinalTarget(self, message):
        if message.messageType is Message.TYPE_MESSAGE:
            self.view.receiveMessageToMe(message)    
            route = self.router.getRoute(self.myMac, message.getOrigin())
            self.append(Message(self.myMac, route, Message.TYPE_ACC, bytes()))
        elif message.messageType is Message.TYPE_ACC:
            self.view.receiveAccToMe(message)

    def _receivedMessageMeantForOther(self, message):    
        messageFinalTarget = message.getTarget()
        print("Target was " + str(messageFinalTarget))

        if message.IShouldRoute(self.myMac):
            nextInRouteMac = message.getNextInRoute(self.myMac)
            self.append(Message(self.myMac, message.route, message.messageType, message.contentBytes))

    def getMessage(self):
        if len(self.sendQue) > 0:
            return self.sendQue.pop()
        return None


    def getKnownNeighbors(self):
        return self.neighbors

    def append(self, message):
        self.sendQue.append(message)

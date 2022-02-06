from mesh.Message import Message
from mesh.Router import Router
from mesh.SendQue import SendQue
from mesh.MessageChecksum import MessageChecksum

#this class implements the mesh network protocol
class MeshController:

    def __init__(self, view, myMac):
        self.sendQue = SendQue()
        self.router = Router()
        
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

            route = message.getRoute()

            self.view.receiveMessageToMe(message)    
            route = self.router.getRoute(self.myMac, route.getOrigin())

            checksum = MessageChecksum.fromMessage(message)
            
            self.addToQue(Message(self.myMac, route, Message.TYPE_ACC, checksum.toBytes()))
        elif message.isAcc():
            self.sendQue.receiveAcc(message)
            self.view.receiveAccToMe(message)

    def _receivedMessageMeantForOther(self, message):    

        route = message.getRoute()

        messageFinalTarget = route.getTarget()
        print("Target was " + str(messageFinalTarget))
        if route.IShouldRoute(message.senderMac, self.myMac):
            print("I should route...")
            self.addToQue(Message(self.myMac, route, message.messageType, message.contentBytes))
        else:
            print("I should not route...")
            self.sendQue.perhapsPartialAcc(message) 
            #I need not to send it again if I received it from someone downstream from me
            


    def getKnownNeighbors(self):
        return self.neighbors

    def addToQue(self, message):
        self.sendQue.addToQue(message)

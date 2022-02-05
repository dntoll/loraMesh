from mesh.Message import Message
from mesh.Router import Router

#this class implements the mesh network protocol
class MeshController:

    def __init__(self, messageCallback, myMac):
        self.sendQue = []
        self.router = Router()
        
        self.messageCallback = messageCallback
        self.myMac = myMac

    def onReceive(self, message, loraStats):
        self.router.deriveRouterData(message, loraStats)
        

        messageFinalTarget = message.getTarget()
        print("Target was " + str(messageFinalTarget))

        if messageFinalTarget is self.myMac:
            self.messageCallback(message.senderMac, message.contentBytes)

            if message.messageType is Message.TYPE_MESSAGE:
                print("acc")
                route = self.router.getRoute(message.senderMac)
                self.append(Message(self.myMac, route, Message.TYPE_ACC, bytes()))
            elif message.messageType is Message.TYPE_ACC:
                print("message was acced")
        

        

    def getMessage(self):
        if len(self.sendQue) > 0:
            return self.sendQue.pop()
        return None


    def getKnownNeighbors(self):
        return self.neighbors

    def append(self, message):
        self.sendQue.append(message)

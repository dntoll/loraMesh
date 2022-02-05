from mesh.Message import Message


#this class implements the mesh network protocol
class MeshController:

    def __init__(self, messageCallback, myMac):
        self.sendQue = []
        self.neighbors = set()
        self.messageCallback = messageCallback
        self.myMac = myMac

    def onReceive(self, message):
        self.neighbors.add(message.senderMac)

        messageFinalTarget = message.getTarget()
        print("Target was " + str(messageFinalTarget))

        if messageFinalTarget is self.myMac:
            self.messageCallback(message.senderMac, message.contentBytes)
            if message.messageType is Message.TYPE_MESSAGE:
                print("acc")
                route = bytearray(1)
                route[0] = message.senderMac
                self.append(Message(self.myMac, route, Message.TYPE_ACC, bytes()))
            elif message.messageType is Message.TYPE_ACC:
                print("message was acced")

        print(message)

    def getMessage(self):
        if len(self.sendQue) > 0:
            return self.sendQue.pop()
        return None


    def getKnownNeighbors(self):
        return self.neighbors

    def append(self, message):
        self.sendQue.append(message)

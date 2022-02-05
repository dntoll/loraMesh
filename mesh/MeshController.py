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

        if message.receiverMac is self.myMac:
            self.messageCallback(message.senderMac, message.contentBytes)
            if message.messageType is Message.TYPE_MESSAGE:
                print("acc")
                self.append(Message(self.myMac, message.senderMac, Message.TYPE_ACC, bytes()))
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

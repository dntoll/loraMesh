

#this class implements the mesh network protocol
class MeshController:

    def __init__(self, messageCallback, myMac):
        self.sendQue = []
        self.neighbors = {}
        self.messageCallback = messageCallback
        self.myMac = myMac

    def onReceive(self, message):
        self.neighbors.add(message.senderMac)

        if message.receiverMac is self.myMac:
            self.messageCallback(message.senderMac, message.contentBytes)
            if message.messageType is Message.TYPE_PING:
                #return a pong
                self.append(Message(self.mymac, message.senderMac, Message.TYPE_PONG, 0, bytes()))

        print(message)

    def getMessage(self):
        if len(self.sendQue) > 0:
            return self.sendQue.pop()
        return None


    def getKnownNeighbors(self):
        return self.neighbors

    def append(self, message):
        self.sendQue.append(message)

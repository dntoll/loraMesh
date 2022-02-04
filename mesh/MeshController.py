

#this class implements the mesh network protocol
class MeshController:

    def __init__(self, messageCallback):
        self.sendQue = []
        self.neighbors = {}
        self.messageCallback = messageCallback

    def onReceive(self, message):
        self.neighbors.add(message.senderMac)
        print(message)

    def getMessage(self):
        if len(self.sendQue) > 0:
            return self.sendQue.pop()
        return None
    

    def getKnownNeighbors(self):
        return self.neighbors

    def append(self, message):
        self.sendQue.append(message)
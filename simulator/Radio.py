class Radio:
    def __init__(self):
        self.nodes = []
        self.sends = 0
    

    def add(self, node):
        self.nodes.append(node)

    def process(self):
        for ss in self.nodes:
            #check outgoing
            if len(ss.sendBuffer):
                self.sends += 1
                self.sendToAllButMe(ss, ss.sendBuffer)
                ss.clearSendBuffer()
    
    def sendToAllButMe(self, sender, buffer):
        bytesArray = bytes(buffer)

        for ss in self.nodes:
            if ss is not sender:
                if (ss.inRange(sender)):
                    ss.fillReceiveBuffer(buffer)
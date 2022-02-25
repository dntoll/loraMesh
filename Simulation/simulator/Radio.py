from time import sleep

class Radio:
    def __init__(self):
        self.nodes = {}
        self.sends = 0
    

    def add(self, nodeIndex, node):
        self.nodes[nodeIndex] = node

    def disableRadio(self, nodeId):
        self.nodes[nodeId].disableRadio()


    def processUntilSilent(self, secondsOfSilence):
        sleepTime = 0.01

        timeSilent = 0
        while timeSilent < secondsOfSilence:
            sleep(sleepTime)
            timeSilent += sleepTime
            if self.process():
                timeSilent = 0.0



    def process(self):

        handledMessage = False
        for ix in self.nodes:
            ss = self.nodes[ix]
            #check outgoing
            if len(ss.sendBuffer):
                self.sends += 1
                self.sendToAllButMe(ss, ss.sendBuffer)
                ss.clearSendBuffer()
                handledMessage = True
        
        return handledMessage
    
    def sendToAllButMe(self, sender, buffer):
        bytesArray = bytes(buffer)

        for ix in self.nodes:
            ss = self.nodes[ix]
            if ss is not sender:
                if (ss.inRange(sender)):
                    ss.fillReceiveBuffer(buffer)
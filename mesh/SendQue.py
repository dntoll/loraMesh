
from mesh.MessageChecksum import MessageChecksum

class QueItem:

    WAIT_UNTIL_RESEND_MS = 10000
    MAX_SEND_TIMES = 10

    def __init__(self, message, sendEarliestAt):
        self.acced = False
        self.sentCount = 0
        self.sentTime = sendEarliestAt
        self.message = message
        self.sendEarliestAt = sendEarliestAt
        self.furthestDownStreamMac = self.message.senderMac

    def shouldBeSent(self, now):
        if self.acced == False:
            jumps = self.message.route.getNumberOfJumps()

            #delay find-messages
            if (self.sentCount == 0 and self.sendEarliestAt < now ) or (self.sentCount > 0 and now - self.sentTime > jumps * self.WAIT_UNTIL_RESEND_MS):
                return True

            
        return False
    
    def doSend(self, now):
        self.sentCount += 1
        self.sentTime = now

        #Acces are only sent a few times
        if self.message.isAcc():
            self.acced = True
        
        if self.sentCount > QueItem.MAX_SEND_TIMES:
            self.acced = True


    def tryAcc(self, accMessage):
        if accMessage.isAccOf(self.message):
            if self.acced is False:
                self.acced = True
                return True
        return False

class SendQue:
    MIN_WAIT_FOR_FIND = 20
    MAX_WAIT_FOR_FIND = 100

    def __init__(self, pycomInterface):
        self.sendQue = []
        self.pycomInterface = pycomInterface
    
    def getSendQue(self):
        return self.sendQue

    def receiveAcc(self, message):
        didAcc = False
        for queItem in self.sendQue:
            if queItem.tryAcc(message):
                didAcc = True
        return didAcc
    
    def getMessageToSend(self):
        now = self.pycomInterface.ticks_ms()

        couldBeSent = []
        for queItem in self.sendQue:
            if queItem.shouldBeSent(now):
                couldBeSent.append(queItem)
        
        if len(couldBeSent) > 0:

            sendIndex = self.pycomInterface.rng() % len(couldBeSent)
            queItem = couldBeSent[sendIndex]
            queItem.doSend(now)
            return queItem.message

        return None

    def InQue(self, message):
        messageChecksum = MessageChecksum.fromMessage(message)
        for queItem in self.sendQue:
            #things that are acced are no longer in que and can be re-sent
            #if queItem.acced:
            #    continue
            if MessageChecksum.fromMessage(queItem.message).isSame(messageChecksum):
                return True

        return False
    
    def getQueItemByMessage(self, message):
        messageChecksum = MessageChecksum.fromMessage(message)
        for queItem in self.sendQue:
            #things that are acced are no longer in que and can be re-sent
            #if queItem.acced:
            #    continue
            if MessageChecksum.fromMessage(queItem.message).isSame(messageChecksum):
                return queItem

        raise Exception("We should not ask for a message not in que")
    
    

    def addToQue(self, message):
        
        if not self.InQue(message):
            sendAtTime = self.pycomInterface.ticks_ms()

            #delay finds
            if message.isFind():
                sendAtTime += SendQue.MIN_WAIT_FOR_FIND + self.pycomInterface.rng() % SendQue.MAX_WAIT_FOR_FIND 

            self.sendQue.append(QueItem(message, sendAtTime))
        else:
            if message.isFind():
                originalMessageQueItem = self.getQueItemByMessage(message)
                originalMessageQueItem.sendEarliestAt += SendQue.MIN_WAIT_FOR_FIND + self.pycomInterface.rng() % SendQue.MAX_WAIT_FOR_FIND 
                #print("Delayed find in que")
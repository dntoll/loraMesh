
from mesh.MessageChecksum import MessageChecksum

class QueItem:

    WAIT_UNTIL_RESEND_MS = 10000
    MAX_SEND_TIMES = 10

    def __init__(self, message):
        self.acced = False
        self.sentCount = 0
        self.message = message
        self.furthestDownStreamMac = self.message.senderMac

    def shouldBeSent(self, now):
        if self.acced == False:
            jumps = self.message.route.getNumberOfJumps()
            if self.sentCount == 0 or now - self.sentTime > jumps * self.WAIT_UNTIL_RESEND_MS:
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
            self.acced = True

class SendQue:
    def __init__(self, pycomInterface):
        self.sendQue = []
        self.pycomInterface = pycomInterface
    
    def getSendQue(self):
        return self.sendQue

    def receiveAcc(self, message):
        for queItem in self.sendQue:
            queItem.tryAcc(message)

    
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
            if queItem.acced:
                continue
            if MessageChecksum.fromMessage(queItem.message).isSame(messageChecksum):
                return True

        return False

    def addToQue(self, message):
        if not self.InQue(message):
            self.sendQue.append(QueItem(message))
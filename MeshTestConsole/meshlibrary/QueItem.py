class QueItem:

    WAIT_UNTIL_RESEND_MS = 10000
    WAIT_UNTIL_REMOVE_ACCED = 6000
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
    
    def shouldBeRemoved(self, now):
        if self.acced == False:
            return False
        
        if now - self.sentTime > self.WAIT_UNTIL_REMOVE_ACCED:
            return True
        return False

    
    def doSend(self, now):

        if self.sentCount > 0:
            self.message.transformIntoFindDueToSecondSend()

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
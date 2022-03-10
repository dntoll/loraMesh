
from meshlibrary.MessageChecksum import MessageChecksum
from meshlibrary.QueItem import QueItem
from meshlibrary.timers import *


class SendQue:


    def __init__(self, pycomInterface):
        self.sendQue = []
        self.pycomInterface = pycomInterface
    
    def getSendQue(self):
        return self.sendQue

    def tryToAccMessagesInQue(self, message):
        didAcc = False
        for queItem in self.sendQue:
            if queItem.tryAcc(message):
                didAcc = True
        return didAcc

    def removeOld(self):
        now = self.pycomInterface.ticks_ms()
        for queItem in self.sendQue:
            if queItem.shouldBeRemoved(now):
                self.sendQue.remove(queItem)

    
    def getQueItemToSend(self):
        now = self.pycomInterface.ticks_ms()

        couldBeSent = []
        for queItem in self.sendQue:
            if queItem.shouldBeSent(now):
                couldBeSent.append(queItem)
        
        if len(couldBeSent) > 0:

            sendIndex = self.pycomInterface.rng() % len(couldBeSent)
            queItem = couldBeSent[sendIndex]


            queItem.doSend(now)
            return queItem

        return None

    def InQue(self, message):
        messageChecksum = MessageChecksum.fromMessage(message)
        for queItem in self.sendQue:
            #things that are acced are no longer in que and can be re-sent
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
                sendAtTime += MIN_WAIT_FOR_FIND + self.pycomInterface.rng() % MAX_WAIT_FOR_FIND 
            

            self.sendQue.append(QueItem(message, sendAtTime))
        else:
            if message.isFind():
                originalMessageQueItem = self.getQueItemByMessage(message)
                originalMessageQueItem.sendEarliestAt += MIN_WAIT_FOR_FIND + self.pycomInterface.rng() % MAX_WAIT_FOR_FIND 
                #print("Delayed find in que")
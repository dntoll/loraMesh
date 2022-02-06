from lib.Console import Console
from lib.ANSIEscape import ANSIEscape


class SerialConsoleView:
    def __init__(self):
        self.console = Console(6)
         
        return


    def sendMessage(self, message):
        #print('Sending %d bytes to %s: %s' %
        #    (len(message.contentBytes), message.getRoute().getTarget(), message.contentBytes))
        return

    def receiveMessageToMe(self, message):
        #print("to mee!")
        return
    
    def receiveAccToMe(self, message):
        #print("acced")
        return

    def receiveMessages(self, messages):
        #for m in messages:
        #    print('Incoming %d bytes from %s: %s' %
        #        (len(m.contentBytes), m.senderMac, m.contentBytes))
        return
   
    def showIps(self, ips):
        for ip in ips:
            print("Network node: %s" % 
                (ip))
    
    def update(self, pymeshAdapter):
        
        consolePosition = 100
        self.console.frame(consolePosition,0, 55, 6)
        self.console.printAt("mac : " + str(pymeshAdapter.getMyAddress()), consolePosition+2, 0)

        y= 1

        self.console.printAt("Target\tCount\tIsAcc\tAcced\tContent", consolePosition+2, 2)
        for queItem in pymeshAdapter.getMessagesInSendQue():
            target = queItem.message.route.getTarget()
            contentBytes = queItem.message.contentBytes
            isAcc = queItem.message.isAcc()
            sentCount = queItem.sentCount
            acced = queItem.acced
            furthestDownStreamMac = queItem.furthestDownStreamMac

            if acced:
                color = ANSIEscape.getTextColor("Red")
            else:
                if isAcc:
                    color = ANSIEscape.getTextColor("Blue")
                else:
                    color = ANSIEscape.getTextColor("Green")
            self.console.printAt(color + str(target) + "\t"+str(furthestDownStreamMac)+"\t" + str(sentCount) + "\t" + str(isAcc) + "\t" + str(acced) + "\t" + str(contentBytes), consolePosition+2, 2+y)
            y += 1
        
        self.console.buffer += ANSIEscape.getResetCode()

        for route in pymeshAdapter.getKnownRoutes():
            self.console.printAt(str(route), consolePosition+2, 2+y)


        
        
        self.console.show()
        return
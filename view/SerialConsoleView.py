from lib.Console import Console

class SerialConsoleView:
    def __init__(self):
        self.console = Console(6)
         
        return


    def sendMessage(self, message):
        print('Sending %d bytes to %s: %s' %
            (len(message.contentBytes), message.getRoute().getTarget(), message.contentBytes))
        

    def receiveMessageToMe(self, message):
        print("to mee!")
    
    def receiveAccToMe(self, message):
        print("acced")

    def receiveMessages(self, messages):
        for m in messages:
            print('Incoming %d bytes from %s: %s' %
                (len(m.contentBytes), m.senderMac, m.contentBytes.decode('utf-8')))
   
    def showIps(self, ips):
        for ip in ips:
            print("Network node: %s" % 
                (ip))
    
    def update(self, pymeshAdapter):
        
        consolePosition = 100
        self.console.frame(consolePosition,0, 30, 6)
        self.console.printAt("mac : " + str(pymeshAdapter.getMyAddress()), consolePosition+2, 0)

        y= 0
        for message in pymeshAdapter.getMessagesInSendQue():
            target = message.route.getTarget()
            contentBytes = message.contentBytes
            self.console.printAt(" : " + str(target) + "\t" + str(contentBytes), consolePosition+2, 2+y)
            y += 1
        

        self.console.show()
        return
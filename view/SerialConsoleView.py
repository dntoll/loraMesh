from lib.Console import Console

class SerialConsoleView:
    def __init__(self):
        self.console = Console(6)
         
        return


    def sendMessage(self, message):
        print('Sending %d bytes to %s: %s' %
            (len(message.contentBytes), message.getTarget(), message.contentBytes))
        

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
        
        self.console.frame(30,0, 30, 6)
        self.console.printAt("I am : " + str(pymeshAdapter.getMyAddress()), 30, 0)

        for i in pymeshAdapter.getMessagesInSendQue():
            self.console.printAt("I am : " + str(i), 30, 2)


        self.console.show()
        return
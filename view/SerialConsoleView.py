

class SerialConsoleView:
    def __init__(self):
        return


    def sendMessage(self, ip, message):

        print('Sending %d bytes to %s: %s' %
            (len(message), ip, message))
        

    def receiveMessage(self, ip, message):
        print('Incoming %d bytes from %s: %s' %
            (len(message), ip, message.decode('utf-8')))

    def donePymeshInit(self, mac):
        print("Mesh MAC: %s" %
            (mac))
    
    def notConnected(self, message):
        print("Still not connected: %s" %
            (message))
    
    def isConnected(self, myAddress, otherNodesInNetwork):
        print("Connected MACshort: %s, Other Nodes In Network: %s" %
            (myAddress, str(otherNodesInNetwork)))
    
    def showIps(self, ips):
        for ip in ips:
            print("Network node: %s" % 
                (ip))
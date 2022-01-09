

class pybytesView:
    def __init__(self, pybytes):
        self.pybytes = pybytes
    
    def donePymeshInit(self, mac):
        self.pybytes.send_signal(1, str(mac))

    def receiveMessage(self, ip, message):
        return

    def sendMessage(self, ip, message):
        return

    def notConnected(self, message):
        return
    
    def showIps(self, ips):
        return

    def isConnected(self, myAddress, otherNodesInNetwork):
        return

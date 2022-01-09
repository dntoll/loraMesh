

class CompositeView:
    def __init__(self):
        self.views = [];

    def add(self, view):
        self.views.append(view)

    def donePymeshInit(self, mac):
        for v in self.views:
            v.donePymeshInit(mac)

    def receiveMessage(self, ip, message):
        for v in self.views:
            v.receiveMessage(ip, message)

    def sendMessage(self, ip, message):
        for v in self.views:
            v.sendMessage(ip, message)
    
    def notConnected(self, message):
        for v in self.views:
            v.notConnected(message)
    
    def isConnected(self, myAddress, otherNodesInNetwork):
        for v in self.views:
            v.isConnected(myAddress, otherNodesInNetwork)
    
    

    def showIps(self, ips):
        for v in self.views:
            v.showIps(ips)

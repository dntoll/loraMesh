#from tabnanny import check
from ansiconsole.Console import Console
from ansiconsole.ANSIEscape import ANSIEscape
from meshlibrary.Message import Message
from meshlibrary.MessageChecksum import MessageChecksum


class SerialConsoleView:
    def __init__(self):
        self.console = Console(6)
        self.console.clearScreen()
        return


    def sendMessage(self, message):
        self._printMessage("Sent ", message)
        return

    def receiveMessageToMe(self, message):
        self._printMessage("Recv ", message)
        return
    
    def receiveAccToMe(self, message):
        self._printMessage("Accd ", message)
        return
    
    def receivedRouteMessage(self, message):
        self._printMessage("Rout ", message)

    def receivedNoRouteMessage(self, message):
        self._printMessage("Igno ", message)
    
    def receivedFindMessage(self, message):
        self._printMessage("receivedFindMessage ", message)
    def suggestRoute(self, message):
        self._printMessage("suggestRoute ", message)
    def passOnFindMessage(self, message):
        self._printMessage("passOnFindMessage ", message)
    def receiveAccToOther(self, message):
        self._printMessage("receiveAccToOther ", message)

    def _printMessage(self, title, message):
        strMessage = title + " "
        strMessage += str(message.senderMac) + " "
        strMessage += self._typeToStr(message.messageType) + " "
        strMessage += self._routeToStr(message.getRoute()) + " "
        strMessage += " CS[" + self._checksumToStr(MessageChecksum.fromMessage(message))  + "] "
        strMessage += " CO[" + self._contentToStr(message.contentBytes) +"]"

        print(strMessage)
        

    def receiveMessages(self, messages):
        #for m in messages:
        #    print('Incoming %d bytes from %s: %s' %
        #        (len(m.contentBytes), m.senderMac, m.contentBytes))
        return


    def _contentToStr(self, content):
        return str(content)
    
    def _checksumToStr(self, checksum):
        return str(checksum.toBytes())

    def _routeToStr(self, route):
        routeStr = "";
        for b in route.getBytes():
            routeStr += "[" + str(b) + "]"
        return routeStr

    def _neighborToStr(self, neigh):
        return str(neigh.mac) + " RSSI: " + str(neigh.rssi) + " T: " + str(neigh.time)

    def _typeToStr(self, type):
        if type == Message.TYPE_ACC:
            return "acc"
        if type == Message.TYPE_FIND:
            return "fin"
        
        return "mes"


    def update(self, pymeshAdapter):
        consolePosition = 75
        self.console.frame(consolePosition,0, 55, 6)
        self.console.printAt("mac : " + str(pymeshAdapter.getMyAddress()), consolePosition+2, 0)

        y= 1

        self.console.printAt("Target\tCount\tIsAcc\tAcced\tContent", consolePosition+2, 2)
        for queItem in pymeshAdapter.getMessagesInSendQue():
            target = queItem.message.route.getTarget()
            contentBytes = queItem.message.contentBytes
            isAcc = self._typeToStr(queItem.message.messageType)
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
            self.console.printAt(color + str(target) + "\t\t" + str(sentCount) + "\t" + str(isAcc) + "\t" + str(acced) + "\t" + str(contentBytes), consolePosition+2, 2+y)
            y += 1
        
        self.console.buffer += ANSIEscape.getResetCode()

        y += 2
        neighbors = pymeshAdapter.getNeighbors()
        for x in neighbors:
            routeStr = self._neighborToStr(neighbors[x])
            self.console.printAt(routeStr, consolePosition+2, 2+y)
            y += 1
        
        y += 2
        routes = pymeshAdapter.getRoutes()
        for x in routes:
            routeStr = self._routeToStr(routes[x])
            self.console.printAt(routeStr, consolePosition+2, 2+y)
            y += 1


        
        
        self.console.show()

        
        return
import cairo
import math


class PlotView:
    def __init__(self, x, y, index):
        self.x = x
        self.y = y
        self.messages = []
        return

    def draw(self, context, views):
        context.set_line_width(0.04)
        context.arc(self.x, self.y, 0.1, 0, 2*math.pi)
        context.stroke()
        for m in self.messages:

            context.new_path()
            context.move_to(self.x, self.y)
            ox, oy = self._getPos(m, views)
            context.line_to(ox, oy)
            context.stroke()
            print(str(m.messageType) + " : " + str(self.x) + " " + str(self.y) + " to " + str(ox) + " " + str(oy))
            
        return

    def _getPos(self, message, views):
        return views[message.senderMac].x, views[message.senderMac].y

    def receiveMessages(self, messages):
        return

    def receiveMessageToMe(self, message):
        self.messages.append(message)
        return
    
    def receiveAccToMe(self, message):
        self.messages.append(message)
        return
    
    def receivedRouteMessage(self, message):
        #self.messages.append(message)
        return

    def receivedNoRouteMessage(self, message):
        #self.messages.append(message)
        return
    def receivedFindMessage(self, message):
        self.messages.append(message)
        return
    def sendMessage(self, message):
        return
    
    def update(self, pymeshAdapter):
        return 
    
    def suggestRoute(self, message):
        return
    def passOnFindMessage(self, message):
        return
    def receiveAccToOther(self, message):
        return



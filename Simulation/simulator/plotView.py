import cairo
import math


class PlotView:
    def __init__(self, x, y, index):
        self.x = x
        self.y = y
        self.messages = []
        self.index = index
        return

    
    def drawNumbers(self, context, views):
        context.set_source_rgb(0,0,0)
        context.arc(self.x+0.1, self.y+0.1, 0.1, 0, 2*math.pi)
        context.stroke()

        
        
        context.select_font_face("Purisa", cairo.FONT_SLANT_NORMAL, 
            cairo.FONT_WEIGHT_NORMAL)
        context.set_font_size(0.3)

        context.move_to(self.x, self.y)
        context.show_text(str(self.index))
        context.stroke()

    def clear(self):
        self.messages = []

    def draw(self, context, views):
        for m in self.messages:
            context.new_path()
            if m.isAcc():
                context.set_source_rgb(1,0,0)
            elif m.isFind():
                context.set_source_rgb(0,1,0)
            else:
                context.set_source_rgb(0,0,1)

            ox, oy = self._getPos(m, views)
            self._drawArrow(context, ox+m.messageType*0.1, oy+m.messageType*0.1, self.x+m.messageType*0.1, self.y+m.messageType*0.1)

    def _drawArrow(self, context, x, y, ox, oy):
        arrow_length = math.sqrt((x-ox)*(x-ox)+(y-oy)*(y-oy))
        arrow_angle = math.atan2(-(y-oy) , -(x-ox))
        
        arrowhead_angle = math.pi/6
        arrowhead_length = 0.3

        context.move_to(x, y) # move to center of canvas

        context.rel_line_to(arrow_length * math.cos(arrow_angle), arrow_length * math.sin(arrow_angle))
        context.rel_move_to(-arrowhead_length * math.cos(arrow_angle - arrowhead_angle), -arrowhead_length * math.sin(arrow_angle - arrowhead_angle))
        context.rel_line_to(arrowhead_length * math.cos(arrow_angle - arrowhead_angle), arrowhead_length * math.sin(arrow_angle - arrowhead_angle))
        context.rel_line_to(-arrowhead_length * math.cos(arrow_angle + arrowhead_angle), -arrowhead_length * math.sin(arrow_angle + arrowhead_angle))
        context.stroke()

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
        self.messages.append(message)
        return

    def receivedNoRouteMessage(self, message):
        self.messages.append(message)
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
        self.messages.append(message)
        return



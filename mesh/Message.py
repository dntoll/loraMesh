from mesh.Route import Route

class ToShortMessageException(Exception):
    def __init__(self, text):
        super().__init__(text)

class Message:

    TYPE_MESSAGE = 0
    TYPE_ACC = 1

    
    HEADER_BEGIN_CHAR = ord('#')
    HEADER_END_CHAR = ord('>')
    MESSAGE_END_CHAR = ord('<')

    #"#"
    #Sender
    #Message type
    #Route len
    #Content len
    #'>'
    #content
    #'<'
    HEADER_BEGIN = 0
    SENDER_MAC = 1 
    MESSAGE_TYPE = SENDER_MAC +1 
    ROUTE_LENGTH = MESSAGE_TYPE +1
    CONTENT_LENGTH = ROUTE_LENGTH +1 
    HEADER_END = CONTENT_LENGTH +1
    HEADER_SIZE = HEADER_END +1

    def __init__(self, senderMac, route, messageType, contentBytes):
        self.senderMac = senderMac
        self.route = route
        self.messageType = messageType
        self.contentBytes = contentBytes
        return

    
    def getRoute(self):
        return self.route
 

    def getBytes(self):

        routeBytes = self.route.getBytes()
        routeLength = len(routeBytes);
        completeMessageSizeBytes = Message.HEADER_SIZE + len(self.contentBytes) + routeLength+1

        ret = bytearray(completeMessageSizeBytes)
        ret[Message.HEADER_BEGIN : Message.HEADER_SIZE] = bytes((Message.HEADER_BEGIN_CHAR, self.senderMac, self.messageType, routeLength, len(self.contentBytes), Message.HEADER_END_CHAR))
        ret[Message.HEADER_SIZE : Message.HEADER_SIZE + routeLength] = routeBytes
        ret[Message.HEADER_SIZE + routeLength: Message.HEADER_SIZE+routeLength + len(self.contentBytes)] = self.contentBytes

        
        ret[completeMessageSizeBytes-1] = Message.MESSAGE_END_CHAR

        return bytes(ret)

    def fromBytes(bytes):
        if len(bytes) < Message.HEADER_SIZE:
            raise Exception("to small to be a message")

        headerBegin = bytes[Message.HEADER_BEGIN]
        if headerBegin != Message.HEADER_BEGIN_CHAR:
            raise Exception("headers should begin with " + chr(Message.HEADER_BEGIN_CHAR))
        
        if bytes[Message.HEADER_END] != Message.HEADER_END_CHAR:
            raise Exception("headers should end with " + chr(Message.HEADER_END_CHAR) + " was " + str(bytes[Message.HEADER_END]))

        senderMac = bytes[Message.SENDER_MAC]
        messageType = bytes[Message.MESSAGE_TYPE]
        contentLength = bytes[Message.CONTENT_LENGTH]
        routeLength = bytes[Message.ROUTE_LENGTH]
        completeMessageSizeBytes = Message.HEADER_SIZE + contentLength + routeLength + 1

        if len(bytes) < completeMessageSizeBytes :
            raise ToShortMessageException("not enough data in Buffer, perhaps not full message received")
        
        if bytes[completeMessageSizeBytes-1] != Message.MESSAGE_END_CHAR:
            raise Exception("Messages should end with " + chr(Message.MESSAGE_END_CHAR))

        route =        bytes[Message.HEADER_SIZE              : Message.HEADER_SIZE + routeLength]
        contentBytes = bytes[Message.HEADER_SIZE + routeLength: Message.HEADER_SIZE + routeLength + contentLength]

        return (completeMessageSizeBytes, Message(senderMac, Route.fromBytes(route), messageType, contentBytes))

    def test():
        contentBytes = bytes((4,5,6))
        route = bytes((2,3))
        m = Message(1, Route.fromBytes(route), Message.TYPE_MESSAGE, contentBytes)

        byteMessage = m.getBytes()

        cl, r = Message.fromBytes(byteMessage)

        assert(cl == Message.HEADER_SIZE + 3 + 2 + 1)
        assert(r.senderMac == m.senderMac)
        assert(r.route.getTarget() == m.route.getTarget() and r.route.getOrigin() == m.route.getOrigin())
        assert(r.messageType == m.messageType)
        assert(r.contentBytes[0] == m.contentBytes[0] and r.contentBytes[1] == m.contentBytes[1] and r.contentBytes[2] == m.contentBytes[2]) #<- ? comparison?

        toSMall = bytearray(Message.HEADER_SIZE-1)
        try:
            Message.getBytes(toSMall)
            assert(False)
        except Exception:
            print("Pass")

        notCorrectStart = bytearray(Message.HEADER_SIZE)
        try:
            Message.fromBytes(notCorrectStart)
            assert(False)
        except Exception:
            print("Pass")

        notEnoughContent = bytearray(Message.HEADER_SIZE)
        notEnoughContent[Message.HEADER_BEGIN] = Message.HEADER_BEGIN_CHAR
        notEnoughContent[Message.HEADER_END] = Message.HEADER_END_CHAR
        notEnoughContent[Message.CONTENT_LENGTH] = 1
        try:
            Message.fromBytes(notEnoughContent)
            assert(False)
        except ToShortMessageException:
            print("Pass")

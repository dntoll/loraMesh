class ToShortMessageException(Exception):
    def __init__(self, text):
        super().__init__(text)

class Message:

    TYPE_MESSAGE = 0
    TYPE_ACC = 1


    HEADER_BEGIN_CHAR = ord('\t')
    HEADER_BEGIN = 0
    SENDER_MAC = 1 ##byte index
    MESSAGE_TYPE = SENDER_MAC +1 #byte index
    ROUTE_LENGTH = MESSAGE_TYPE +1
    CONTENT_LENGTH = ROUTE_LENGTH +1 #byte index
    HEADER_SIZE = CONTENT_LENGTH +1

    def __init__(self, senderMac, route, messageType, contentBytes):
        self.senderMac = senderMac
        self.route = route
        self.messageType = messageType
        self.contentBytes = contentBytes
        return

    def getTarget(self):
        return self.route[len(self.route)-1]

    def getBytes(self):
        completeMessageSizeBytes = Message.HEADER_SIZE + len(self.contentBytes) + len(self.route)

        ret = bytearray(completeMessageSizeBytes)
        ret[Message.HEADER_BEGIN:Message.HEADER_SIZE] = bytes((Message.HEADER_BEGIN_CHAR, self.senderMac, self.messageType, len(self.route), len(self.contentBytes)))
        ret[Message.HEADER_SIZE:] = self.route
        ret[Message.HEADER_SIZE + len(self.route):] = self.contentBytes
        return bytes(ret)

    def fromBytes(bytes):
        if len(bytes) < Message.HEADER_SIZE:
            raise Exception("to small to be a message")

        headerBegin = bytes[Message.HEADER_BEGIN]
        if headerBegin != Message.HEADER_BEGIN_CHAR:
            raise Exception("messages should begin with " + chr(Message.HEADER_BEGIN_CHAR))

        senderMac = bytes[Message.SENDER_MAC]
        messageType = bytes[Message.MESSAGE_TYPE]
        contentLength = bytes[Message.CONTENT_LENGTH]
        routeLength = bytes[Message.ROUTE_LENGTH]

        

        completeMessageSizeBytes = Message.HEADER_SIZE + contentLength + routeLength

        if len(bytes) < completeMessageSizeBytes :
            raise ToShortMessageException("not enough data in Buffer, perhaps not full message received")


        route =        bytes[Message.HEADER_SIZE              : Message.HEADER_SIZE + routeLength]
        contentBytes = bytes[Message.HEADER_SIZE + routeLength: Message.HEADER_SIZE + routeLength + contentLength]

        return (completeMessageSizeBytes, Message(senderMac, route, messageType, contentBytes))

    def test():
        contentBytes = bytes((4,5,6))
        route = bytes((2,3))
        m = Message(1,route,3,contentBytes)

        byteMessage = m.getBytes()

        cl, r = Message.fromBytes(byteMessage)

        assert(cl == Message.HEADER_SIZE + 3 + 2)
        assert(r.senderMac == m.senderMac)
        assert(r.route[0] == m.route[0] and r.route[1] == m.route[1])
        assert(r.messageType == m.messageType)
        assert(r.contentBytes[0] == m.contentBytes[0] and r.contentBytes[1] == m.contentBytes[1] and r.contentBytes[2] == m.contentBytes[2]) #<- ? comparison?

        toSMall = bytearray(Message.HEADER_SIZE-1)
        try:
            Message.fromBytes(toSMall)
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
        notEnoughContent[Message.CONTENT_LENGTH] = 1
        try:
            Message.fromBytes(notEnoughContent)
            assert(False)
        except ToShortMessageException:
            print("Pass")

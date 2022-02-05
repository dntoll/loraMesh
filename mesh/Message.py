class ToShortMessageException(Exception):
    def __init__(self, text):
        super().__init__(text)

class Message:

    TYPE_MESSAGE = 0
    TYPE_ACC = 1


    HEADER_BEGIN_CHAR = ord('\t')
    HEADER_BEGIN = 0
    SENDER_MAC = 1 ##byte index
    RECEIVER_MAC = SENDER_MAC + 1 #byte index
    MESSAGE_TYPE = RECEIVER_MAC +1 #byte index
    CONTENT_LENGTH = MESSAGE_TYPE +1 #byte index
    HEADER_SIZE = CONTENT_LENGTH +1

    def __init__(self, senderMac, receiverMac, messageType, contentBytes):
        self.senderMac = senderMac
        self.receiverMac = receiverMac
        self.messageType = messageType
        self.contentBytes = contentBytes
        return

    def getBytes(self):
        ret = bytearray(Message.HEADER_SIZE+len(self.contentBytes))
        ret[Message.HEADER_BEGIN:Message.HEADER_SIZE] = bytes((Message.HEADER_BEGIN_CHAR, self.senderMac, self.receiverMac, self.messageType, len(self.contentBytes)))
        ret[Message.HEADER_SIZE:] = self.contentBytes
        return bytes(ret)

    def fromBytes(bytes):
        if len(bytes) < Message.HEADER_SIZE:
            raise Exception("to small to be a message")

        headerBegin = bytes[Message.HEADER_BEGIN]
        if headerBegin != Message.HEADER_BEGIN_CHAR:
            raise Exception("messages should begin with " + chr(Message.HEADER_BEGIN_CHAR))

        senderMac = bytes[Message.SENDER_MAC]
        receiverMac = bytes[Message.RECEIVER_MAC]
        messageType = bytes[Message.MESSAGE_TYPE]
        contentLength = bytes[Message.CONTENT_LENGTH]

        if len(bytes) < Message.HEADER_SIZE + contentLength:
            raise ToShortMessageException("not enough data in Buffer, perhaps not full message received")


        contentBytes = bytes[Message.HEADER_SIZE: Message.HEADER_SIZE + contentLength]

        return (Message.HEADER_SIZE+contentLength, Message(senderMac, receiverMac, messageType, contentBytes))

    def test():
        contentBytes = bytes((4,5,6))
        m = Message(1,2,3,contentBytes)

        byteMessage = m.getBytes()

        cl, r = Message.fromBytes(byteMessage)

        assert(cl == Message.HEADER_SIZE + 3)
        assert(r.senderMac == m.senderMac)
        assert(r.receiverMac == m.receiverMac)
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
